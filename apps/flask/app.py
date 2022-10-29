from parlai.core.agents import create_agent, create_agent_from_shared

from flask import Flask

from pprint import pprint


OPT = {
    "model": "_custom/echo"
}

SHARED     = create_agent(OPT).share()
pprint(SHARED)
AGENT_POOL = {}


def create_app():
    
    app = Flask(__name__)
    
    @app.route("/response", methods=("GET", "POST"))
    def chatbot_response():
        
        global AGENT_POOL
        global SHARED
        
        from flask import request
        
        data = request.json
        text = data.get("text")
        uid  = data.get("uid")
        
        agent = AGENT_POOL.get("uid")
        if agent is None:
            agent = AGENT_POOL[uid] = create_agent_from_shared(SHARED)
            
        pprint(AGENT_POOL)
            
        agent.observe({"text": text, "episode_done": False})
        response = agent.act()
        return {"response": response["text"]}

    return app


if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True)
