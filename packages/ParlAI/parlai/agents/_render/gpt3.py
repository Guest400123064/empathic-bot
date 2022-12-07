from typing import Callable, Dict

import json
import logging

from parlai.core.agents import Agent, create_agent, create_agent_from_shared


class GPT3RenderWrapper(Agent):
    """A wrapper for GPT3-based style transfer. On initialization, it will instantiate 
        a base generator agent and a renderer function. The renderer function will 
        use GPT3 API call to perform style transfer."""

    gpt3_config_key      = "gpt3"
    generator_config_key = "generator"
    generator_shared_key = "generator"

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        
        logging.debug("CONFIG:\n" + json.dumps(opt, indent=True))

        self.id = __class__.__name__
        self.renderer = self.create_renderer(opt[GPT3RenderWrapper.gpt3_config_key])
        
        # Create generator from config file (first-time instantiation)
        if shared is None:
            logging.debug("CREATED FROM PROTOTYPE")
            
            key = GPT3RenderWrapper.generator_config_key
            self.generator = create_agent(opt[key])
        
        # Create generator from shared state
        else:
            logging.debug("CREATED FROM COPY")
            
            key = GPT3RenderWrapper.generator_shared_key
            self.generator = create_agent_from_shared(shared[key])

    def share(self) -> Dict:
        """Copy response function <self.resp_fn>"""

        logging.debug("MODEL COPIED")

        shared = super().share()
        shared[GPT3RenderWrapper.generator_shared_key] = self.generator.share()
        return shared

    def act(self) -> Dict:
        """Forward the observation to the wrapped generator, then call the 
            GPT-3 renderer to perform style transfer."""

        observation = self.observation
        if observation is None:
            return {"text": "Nothing to reply to yet"}

        # Call the wrapped generator
        self.generator.observe(observation)
        base_response = self.generator.act().get("text")
        
        # Call the renderer to perform style transfer
        response, prompt = self.renderer(base_response)
        return {"id":            self.getID(),
                "base_response": base_response,
                "gpt3_prompt":   prompt,
                "text":          response}

    def reset(self):
        """Reset the agent, clearing its observation."""

        self.observation = None
        self.generator.reset()

    def create_renderer(self, opt: Dict) -> Callable[[str], str]:
        """Create a GPT-3 renderer function based on the options passed in."""

        import openai

        def gpt_completion(s: str) -> str:
            """GPT-3 completion function. Takes a raw bot response and returns a new response.
                TODO: Should allow prompt to be passed in as well, or read from a config file."""

            prompt_table = {
                "empathetic": (
                    "Here is an empathetic sentence: {I thought it was terribly depressing what these children had to go through.}"
                    "Here is another empathetic sentence: {I feel so sad for everyone especially the old and sickly seems as they are in the worst position.}"
                    "Here is another empathetic sentence: {You always want better for your kid and I think giving them up to someone else would be the best option even though it hurts. So sad. My heart just breaks for these woman.}"
                    "Here is some text: {" + s + ".} Here is a rewrite of the text, which is more empathetic: {"
                ),
                "self-disclosure": (
                    "Here is a sentence of high self-disclosure: {I was always scared as a catholic to go to church as a kid and would always talk my mom out of going which probably turned out to save me in the long run.}"
                    "Here is another sentence of high self-disclosure: {I love that, personally my father went outside to smoke and never smoked with us in the car but my friends parents did and I would feel so sick after being in there car no child should suffer through it.}"
                    "Here is another sentence of high self-disclosure: {My father was in the Navy and I have two sisters in the Army.}"
                    "Here is some text: {" + s + ".} Here is a rewrite of the text, which is of higher self-disclosure: {"
                )
            }
            prompt = prompt_table.get([opt["style"]])
            if prompt is None:
                raise ValueError(f"Style {opt['style']} not supported. Choose from {list(prompt_table.keys())}")

            openai.api_key = opt["token"]
            completion = openai.Completion.create(prompt=prompt, **opt["generation_config"])
            return completion["choices"][0]["text"].rstrip("}").strip(), prompt

        return gpt_completion
