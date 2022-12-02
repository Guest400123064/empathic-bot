# -*- coding: utf-8 -*-
# =============================================================================
# Author: Yuxuan Wang
# Date: 12-03-2022
# =============================================================================
"""
The main client script for chatting and chat-history collection.
"""

from pathlib import Path
FILE_DIR = Path(__file__).parent
CHAT_DIR = FILE_DIR / "chat_history"
LOGS_DIR = FILE_DIR / "logs"

import argparse
import json

import websocket
from http.server import BaseHTTPRequestHandler, HTTPServer

from frontend import WEB_HTML, STYLE_SHEET, FONT_AWESOME

KEEP_RUNNING = True
USER_NAME = None
SHARED    = {}
CHAT_HIST = []


class ChatHandler(BaseHTTPRequestHandler):
    """The handler for the HTTP server that displays the frontend."""

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self._interactive_running(body)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            model_response = {'id': 'Model', 'episode_done': False}
            model_response.update(json.loads(SHARED['ws'].recv()))
            json_str = json.dumps(model_response)
            self.wfile.write(bytes(json_str, 'utf-8'))
        elif self.path == '/reset':
            self._interactive_running(b"[RESET]")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("{}", 'utf-8'))
        else:
            return self._respond({'status': 500})

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})
            
    def _interactive_running(self, reply_text):
        
        global KEEP_RUNNING
        
        data = {
            "user": USER_NAME,
            "text": reply_text.decode("utf-8")
        }

        CHAT_HIST.append(data)
        json_data = json.dumps(data)
        SHARED['ws'].send(json_data)

        if data["text"] == "[DONE]":
            KEEP_RUNNING = False

    def _handle_http(self, status_code, path, text=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def run_browser():
    """Starts the HTTP server that displays the frontend."""
    
    host = "localhost"
    port = 8080
    
    SHARED['wb'] = httpd = HTTPServer((host, port), ChatHandler)
    print(f"Please connect to the link: http://{host}:{port}/")
    
    while KEEP_RUNNING:
        httpd.handle_request()

        
def get_parser():
    """Helper function to parse command line arguments, 
        mainly for getting the host and port number of the 
        remote chatbot server and where to display the frontend."""
    
    parser = argparse.ArgumentParser(description="Chat with a remote chatbot.")

    parser.add_argument("-n", "--name", type=str, 
                        help="Your name/school ID; Better without any space.")
    parser.add_argument("--host-bot", type=str, default="localhost",
                        help="The host of the remote chatbot (GCP) server.")
    parser.add_argument("--port-bot", type=int, default=35496,
                        help="The port of the remote chatbot (GCP) server.")
    return parser

        
if __name__ == "__main__":
    
    parser = get_parser()
    opt = parser.parse_args()
    
    print(f"Connecting to {opt.host_bot}:{opt.port_bot}")    
    SHARED["ws"] = websocket.WebSocket()
    SHARED["ws"].connect(f"ws://{opt.host_bot}:{opt.port_bot}/websocket")

    run_browser()
