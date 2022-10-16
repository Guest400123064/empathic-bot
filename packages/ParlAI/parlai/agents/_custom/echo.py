import json
import logging

from parlai.core.agents import Agent


class EchoAgent(Agent):
    """Dummy agent that simply echos everything it observed. On initialization,
        it also print out all options it receives."""

    def __init__(self, opt, shared=None):
        """Init agent and echo options"""

        super().__init__(opt)
        logging.info('CONFIG:\n' + json.dumps(opt, indent=True))

        self.id = 'EchoBot'
        if shared is None:
            logging.info('CREATED FROM PROTOTYPE')
            self.resp_fn = lambda x: x
        else:
            logging.info('CREATED FROM COPY')
            self.resp_fn = shared['resp_fn']

    def share(self) -> dict:
        """Copy response function <self.resp_fn>"""

        logging.info('MODEL COPIED')

        shared = super().share()
        shared['resp_fn'] = self.resp_fn
        return shared

    def act(self):
        """Simply copy the input messages"""

        obs = self.observation
        if obs is None:
            return {'text': 'Nothing to reply to yet'}

        ipt = obs.get('text', 'I don\'t know')
        raw_resp = self.resp_fn(ipt)
        return {
            'id': self.getID(),
            'text': f'[ echo ] :: {self.render(raw_resp)}'
        }

    def render(self, s: str) -> str:

        # GPT-3 API call
        return s
