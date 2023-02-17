# -*- coding: utf-8 -*-
# =============================================================================
# Author: Yuxuan Wang
# Date: 12-04-2022
# =============================================================================
"""
The main client script for chatting and chat-history collection. This script
  starts a local http server for the frontend, and connects to the remote
  chatbot service. User should enter in their own browsers the link printed 
  in the terminal to start chatting. E.g., http://localhost:8080 is the default 
  endpoint for the frontend.
"""

import csv
import json

import websocket
from http.server import BaseHTTPRequestHandler, HTTPServer

from _gui import WEB_HTML, STYLE_SHEET, FONT_AWESOME, END_MESSAGE


class G:
    """Global variables and helper functions."""

    chat_end_tok = "[DONE]"
    chat_history = []

    keep_running = True
    websocket    = None
    httpd        = None
    
    @staticmethod
    def ws_send(text: str, keep_history: bool = True):
        """Serialize dictionary and send data to websocket server.
            Also, save the data to chat history."""

        err_msg = "Websocket server is not connected."
        
        if G.websocket is None:
            raise RuntimeError(err_msg)

        if G.websocket.connected:
            data = {"role": "User", "text": text}
            G.websocket.send(json.dumps(data))
            
            if keep_history:
                G.chat_history.append(data)

    @staticmethod
    def ws_recv(keep_history: bool = True) -> dict:
        """Receive data from websocket server and deserialize it. 
            Also, save the data to chat history."""
        
        err_msg = "Websocket server is not connected."
        
        if G.websocket is None:
            raise RuntimeError(err_msg)
        
        if G.websocket.connected:
            data = json.loads(G.websocket.recv())
            data.update({"role": "Bot"})

            if keep_history:
                G.chat_history.append(data)
            return data
        
    @staticmethod
    def start_ws(host: str, port: int):
        """Start websocket connection with chatbot."""
        
        addr = f"ws://{host}:{port}/websocket"
        G.websocket = websocket.WebSocket()

        try:
            G.websocket.connect(addr)
            print(f"Connected to chatbot at < {addr} >.")

            # This is a hack to skip the OverWorld and TaskWorld by 
            #   sending dummy messages. OverWorld accept any message
            #   and TaskWorld accept only "begin" as the identifier.
            G.ws_send("", keep_history=False)
            _ = G.ws_recv(keep_history=False)
            G.ws_send("begin", keep_history=False)
            _ = G.ws_recv(keep_history=False)

        except ConnectionRefusedError:
            print(f"Failed to connect to chatbot at < {addr} >. Maybe wrong host or port?")
            exit(1)

    @staticmethod
    def save_chat_history(user_name: str):
        """Save cached chat history to a file named with
            <user_name>-<datetime>.json"""

        import os
        from pathlib import Path
            
        import datetime

        file_dir = Path(__file__).parent
        chat_dir = file_dir / "chat"

        if not os.path.exists(chat_dir):
            os.makedirs(chat_dir)

        timestamp = str(datetime.datetime.now().isoformat())
        file_name_base = f"{user_name}-{datetime.datetime.now():%m_%d_%H_%M}"
        with open(chat_dir / f"{file_name_base}.json", "w") as f:
            data = {"id": user_name,
                    "timestamp": timestamp,
                    "chat_hist": G.chat_history}
            json.dump(data, f, indent=4)

        # Construct CSV file for annotating preferences 
        #   for base_response or rendered_response
        head = ["id", "timestamp", "user_input", "base_response", "rendered_response",
                "preference", "empathy", "likable", "sincere", "honest", "similar"]
        rows = []
        for i in range(len(G.chat_history) // 2):
            j = i * 2
            if G.chat_history[j]["text"] == G.chat_end_tok:
                break

            data_usr, data_bot = G.chat_history[j:j + 2]
            assert data_usr["role"] == "User", "User input should be sent first."
            assert data_bot["role"] == "Bot", "Consecutive messages sent from the user."

            row = [user_name, timestamp, 
                   data_usr["text"], 
                   data_bot["base_response"],
                   data_bot["text"]]
            rows.append(row + [""] * (len(head) - len(row)))

        with open(chat_dir / f"{file_name_base}.csv", "w") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(head)
            writer.writerows(rows)

    @staticmethod
    def stop_httpd():
        """Simply set the keep_running flag to False"""

        G.ws_send("exit", keep_history=False)
        _ = G.ws_recv(keep_history=False)

        G.keep_running = False

    @staticmethod
    def start_httpd(port: int = 8080):
        """Start a http server for the frontend."""
        
        G.httpd = HTTPServer(("localhost", port), ChatHandler)
        print(f"Please access the chatting service at < http://localhost:{port}/ >."
                " Refresh the page if you don't see the chat window in your browser.")
        
        while G.keep_running:
            G.httpd.handle_request()


class ChatHandler(BaseHTTPRequestHandler):
    """The handler for the HTTP server that displays the frontend."""

    def do_HEAD(self):
        """Handle HEAD requests."""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        """Handle POST request, especially replying to a chat message."""
        
        if self.path == "/interact":
            
            # Get user input and forward it to the bot via websocket
            content_length = int(self.headers["Content-Length"])
            human_response = self.rfile.read(content_length).decode("utf-8")
            G.ws_send(human_response)

            # Prepare bot response header for user
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # Get bot response from websocket and send it back to user
            model_response = {"id": "Model", "episode_done": False}
            
            # End of chat
            if human_response == G.chat_end_tok:
                model_response.update({"text": END_MESSAGE, "episode_done": True})
                self.wfile.write(bytes(json.dumps(model_response), "utf-8"))
                G.stop_httpd()
            
            # Normal interactive chat
            else:
                model_response.update(G.ws_recv())
                self.wfile.write(bytes(json.dumps(model_response), "utf-8"))

    def do_GET(self):
        """Respond to GET request, especially the initial load."""        

        status = {"/": 200,
                  "/favicon.ico": 202}  # For Chrome
    
        self.send_response(status.get(self.path, 500))
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)
        self.wfile.write(bytes(content, "utf-8")) 

        
def get_arguments():
    """Helper function to parse command line arguments, 
        mainly for getting the host and port number of the 
        remote chatbot server and where to display the frontend."""

    import argparse
    
    parser = argparse.ArgumentParser(description="Chat with a remote chatbot.")
    parser.add_argument("user_id", type=str, 
                        help="Your name/school ID; Better without any space.")
    parser.add_argument("--host-bot", type=str, default="localhost",
                        help="The host of the remote chatbot (GCP) server.")
    parser.add_argument("--port-bot", type=int, default=35496,
                        help="The port of the remote chatbot (GCP) server.")
    parser.add_argument("--port-browser", type=int, default=8080,
                        help="The port of the local browser server (default to 8080).")
    return parser.parse_args()

        
if __name__ == "__main__":

    opt = get_arguments()

    G.start_ws(opt.host_bot, opt.port_bot)
    G.start_httpd(opt.port_browser)
    G.save_chat_history(opt.user_id)
