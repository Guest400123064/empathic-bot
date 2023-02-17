# **Empathic Conversation Study**
​
Thanks for the help! Please follow all of the steps below and this should be a seamless process. There are two main steps,
1. Start a conversation with a chatbot hosted on GCP server. You will be using a simple browser-based client to accomplish this.
2. The chat client will store your chat history with the bot locally, and please upload the history to Google Cloud.
<!-- 3. After chatting, you will be asked to complete a Qualtrics survey about your experiences with the chatbot. -->

Detailed instructions are as follows. ​

## __Step One: Chat with the Bot__
Follow the instructions [here](https://github.com/Guest400123064/empathic-bot/tree/main/apps/browser_client) to download the chat service client and interact with the chatbot. The instruction also mentions where is your chat history stored.

__Notes:__
1. __Please use some unique ID__ that you believe it is very unlikely to coincidentally match that of others. For instance, you can use your school ID or your cool, unique game ID.
2. At some point the client will ask you for an IP address of the chatbot to fill `--host-bot`. This may vary, and please refer to your instructor.
​
## __Step Two: Upload Chat History__
Please upload the conversational data (one `CSV` file, one `JSON` file) to the shared [google drive](https://drive.google.com/drive/folders/1UBtqF_PXoOwkOSvGZrjiBdy_6utJCSrm?usp=sharing). There is a `JSON` file keeping all of your chat history and a `CSV` file that you should annotate your preferences for the two responses. The annotation instruction is listed below.

In the csv file, each row is a single-turn conversation consisting of:
- `user_input`: what you said.
- `base_response`: what the chatbot would have said normally.
- `rendered_response`: what the chatbot said to you in an empathetic way.

__Assuming each row is independent of each other__, please rate the chatbot's responses for each row based on the following criteria:

1) In the "preference" column, please type 0 if you prefer 'base_response', 1 if you prefer 'rendered_response', 2 if you prefer both, and 3 if you prefer neither.
2) In the "empathy" column, please rate on a 1-5  scale how much empathy you felt from 'rendered_response'. 1 if no empathy at all; 5 if the highest empathy possible given what you said to it.
3) In the "likable" column, please rate on a 1-5 scale how much you would like to talk to the chatbot given 'rendered_response'. 1 if you do not want to talk to it ever again; 5 if you would love to talk to it more.
4) In the "sincere" column, please rate on a 1-5 scale how much you think the chatbot cares about what you said given 'rendered_response'. 1 if you think the chatbot does not care at all; 5 if you think the chatbot genuinely cares about your words.
5) In the "honest" column, please rate on a 1-5 scale how much you think the chatbot is honest with its 'rendered_response'. 1 if you think the chatbot is a hypocrite; 5 if you think the chatbot is truly honest with its words.
6) In the "similar" column, please rate on a 1-5 scale how similar you think 'base_response' and 'rendered_response' are in terms of content and meaning. 1 if you think they are completely different; 5 if you think they have identical content.

__Notes:__
1. Suppose your ID is `my_cool_id` and the client folder is `browser_client`. Your chat history should be located at `browser_client/chat/my_cool_id-12_07_18_12.json`, where `12_07_18_12` is the datetime when you carried out the conversation, which may vary.
​
<!-- ## __Step Three: A Survey about Chat Experience__
**After finishing the conversation**, please fill out the following questions on the [Qualtrics survey](https://nyu.qualtrics.com/jfe/form/SV_26jZ2beozdQrcHk).  -->

Thats it, thanks for your time and participation!
