import uuid
import json
import websocket


def connect(ws, uid):
    
    while True:
        x = input("\033[44m Me: ")
        print("\033[0m")
        data = {}
        data['id'] = uid
        data['text'] = x
        
        # End of conversation
        if x == "[DONE]":
            ws.send(json.dumps(data))
            break

        ws.send(json.dumps(data))
        response = ws.recv()
        response = json.loads(response)

        print("Bot: " + response.get("text"))


if __name__ == "__main__":
    
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:35496/websocket")
    connect(ws, str(uuid.uuid4()))
