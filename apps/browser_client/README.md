# __Simple Browser Chat__
This is a simple re-implementation of `ParlAI`'s browser chat client using mostly standard library for portability. It also has a simple functionality of collecting chat history. __Note: all instructions below assume that we are in the program folder, e.g., `browser_client`__ The structure of the folders should be,
```
PROGRAM_FOLDER
  |-- README.md
  |-- main.py
  |-- _gui.py
  |-- requirements.txt
  |-- example.png
  |-- chat
        |-- .gitkeep
        |-- chat_history.json
```
So, one should be in the `PROGRAM_FOLDER`. You can check your current working directory in command line/bash by typing `pwd`.

## __Installation__
Assuming `python` is already installed. I developed this client with `python 3.9`. But it should be compatible with most of the other versions.

Firstly, download (or clone from GitHub) the source files under this folder. In particular, make sure that `main.py` and `_gui.py` are present. If the `chat` folder (storing chat histories) is not created, the script will automatically create one for you.

Next, please manually install the dependencies in `requirements.txt` (which is essentially [`websocket-client`](https://websocket-client.readthedocs.io/en/latest/installation.html)) with,
```
pip install -r requirements.txt
```
One should be able to start the client from command line/bash.

## __Chatting__
__Get Started:__ Under `PROGRAM_FOLDER`, in command line, type,
```
python main.py < your_id > --host-bot < GCP_addr > --port-bot < GCP_port >
```
In the command, `your_id` is simply used to generate the filename for produced chat history `JSON` file. So, better without any white space. `GCP_addr` and `GCP_port` are used to indicate where is the chatbot hosted. By default, the client script assumes the bot running locally, with default parameter `localhost` and `35496` respectively. For example, suppose the user ID is `wangy49`, with the chatbot hosted at `34.136.228.74` (port `35496`), the corresponding command should be,
```
python main.py wangy49 --host-bot 34.136.228.74 --port-bot 35496
```
If the client starts successfully, you should see from command line,
```
Connected to chatbot at < ws://34.136.228.74:35496/websocket >.
Please access the chatting service at < http://localhost:8080/ >.
```
Now, in your browser (where you usually type `google.com`), enter `http://localhost:8080/` and hit enter. You should be able to see a simple chat GUI (see below). Hit enter to start the chat service. ![example-gui](example.png) 

__Stop Chatting:__ In the input block, type `[DONE]` and hit enter to stop the chat service and the chat history should be saved locally under `PROGRAM_FOLDER/chat/`.

## __Chat History__
Chat history is saved as `< your_id >-< date_time >.json` in a __list-of-dictionaries__ format. Each dictionary corresponds to a user/bot response. The `PROGRAM_FOLDER/chat/example-12-04-17-59.json` examples should be clear enough.
