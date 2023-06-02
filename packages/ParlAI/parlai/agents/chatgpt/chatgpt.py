#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""

"""

from typing import Optional
from parlai.core.params import ParlaiParser
from parlai.core.opt import Opt
from parlai.core.agents import Agent
from parlai.core.message import Message
import openai  
import os

import re
import json
import nltk
import argparse
import os
from nltk import tokenize
import tiktoken
import time
import random


start_sequence = "\nAI:"
restart_sequence = "\nHuman:"
MAX_COMPLETION_LENGTH = 80 
CHATGPT_MAX_TOKEN_LIMIT = 4000
tokenizer = tiktoken.encoding_for_model("text-davinci-003")

def helper_split_words(Text, numberOfWords=1):
    if (numberOfWords > 1):
        text = Text.lstrip()
        pattern = '(?:\S+\s*){1,'+str(numberOfWords-1)+'}\S+(?!=\s*)'
        x =re.findall(pattern,text)
    elif (numberOfWords == 1):
        x = Text.split()
    else: 
        x = None
    return x



def split_on_sentences_word_count(text, word_count = 100):
    text = re.sub(r'(?<=[.,?!])(?=[^\s])', r' ', text)
    # text = re.sub(r'\.(?=[^ \W\d])', '. ', text)
    sent_splits = tokenize.sent_tokenize(text)
    ## now we should add sent until we are about to exceed 100 lines
    
    #go through each string and split if word count exceeds word_count
    
    word_count_chunks = []
    for s in sent_splits:
        num_words = len(s.split())
        if num_words > word_count:
            #then sentence already exceeds limit
            #split it
            word_count_chunks += helper_split_words(s, word_count)
        else:
            word_count_chunks.append(s)
                
    return_lines = []
    hold = ''

    for s in word_count_chunks:
        if len(hold.split()) + len(s.split()) > word_count:
            # then reset
            return_lines.append(hold)
            hold = ''
        else:
            hold += s
            hold += ' '
            
    if len(hold) > 0:
        return_lines.append(hold)
                
    # check that we split text properly < 128
    
    for l in return_lines:
        if len(l.split()) > word_count:
            print(word_count)
            print("LINE detected with a proble!!!")
            print(l)
            raise Exception("bad line!")
            
    return return_lines

def add_prefix(turn):
    if turn[0] == 'user':
        return f"{restart_sequence} {turn[1]}"
    elif turn[0] == 'assistant':
        return f"{start_sequence} {turn[1]}" 

def create_prime_within_gpt3_token_limit(instructions, article, turns):
    instr_tokens = tokenizer.encode(instructions)
    if turns != None and len(turns)> 0:
        print(turns)
        turns_tokens = tokenizer.encode(" ".join([add_prefix(x) for x in turns]))
    else:
        turns_tokens = tokenizer.encode("")

    tokens_left = CHATGPT_MAX_TOKEN_LIMIT - len(instr_tokens) - len(turns_tokens) - MAX_COMPLETION_LENGTH - 10

    article_formatted = re.sub(r'(?<=[.,?!])(?=[^\s])', r' ', article)
    sent_splits = tokenize.sent_tokenize(article_formatted)

    for i in range(len(sent_splits) - 1, -1, -1):
        subset_article = " ".join(sent_splits[0:i])
        article_cut = tokenizer.encode(subset_article)
        if len(article_cut) > tokens_left:
            # we can use this subset of the article
            if i>0:
                subset_article = " ".join(sent_splits[0:i-1])
            return prompt_compose(instructions, subset_article, turns)

    if len(sent_splits) > 0:
        subset_article = " ".join(sent_splits)
        return prompt_compose(instructions, subset_article, turns)
    
    raise Exception("Failed to create proper prime")   

def query_completion_api(conv, engine='gpt-3.5-turbo'):
    response = openai.ChatCompletion.create(
        model=engine,
        messages=conv,
        max_tokens=MAX_COMPLETION_LENGTH
    )
    
    return response

def prompt_compose(instructions, article_info, turns):
    conv = []
    conv.append({"role": "system", "content": f'{instructions}\nArticle: {article_info}'})
    for turn in turns:
        conv.append({"role": turn[0], "content": turn[1]})
    return conv

class FakeHistory:
    def __init__(self, gpt3):
        self.gpt3 = gpt3
    
    def add_reply(self, text):
        self.gpt3.turns += [('assistant', f"{text}")]



    def get_history_str(self):
        return f"{self.gpt3.article_info}" + " ".join([add_prefix(x) for x in self.gpt3.turns])


class ChatgptAgent(Agent):
    @classmethod
    def add_cmdline_args(
        cls, parser: ParlaiParser, partial_opt: Optional[Opt] = None
    ) -> ParlaiParser:
        group = parser.add_argument_group('GPT3 Arguments')
        return parser

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'chatGPT_agent'
        self.turns = []
        self.history = FakeHistory(self)
        
        self.article_info = ''
        with open(os.getenv('ARTICLE_FILENAME'), 'r') as f:
            self.article_info = f.read()
        
        openai.api_key = os.getenv("OPENAI_API_KEY")



    def reset(self):
        """
        Reset the agent, clearing its observation.

        Many subclasses implement additional reset logic.
        """
        # self.observation = None
        
        self.turns = ''
        self.article_info = ''

    def observe(self, observation):
        """
        Receive an observation/action dict. Store it into
        """
        self.observation = observation

        self.turns += [('user', f"{observation['text']}")]

        return observation

    def check_bye(self):
        # CODE to say Bye in order to terminate the mephisto conversation
        regex = r'^\s*(?i:bye)[.!]*\s*$'
        pattern = re.compile(regex)
        
        return pattern.match(self.turns[-1][1])
                

    def act(self):
        """
        Generate response to last seen observation.

        Replies with a message from using the chatGPT model.

        :returns: message dict with reply
        """

        obs = self.observation

        if self.check_bye():
            resp_txt = "Bye"
            self.turns += [('assistant', f"{resp_txt}")]
            return Message(
                {'id': self.getID(), 'text': resp_txt, 'episode_done': False}
            )

        instr = """You should act as an empathetic person who is discussinng a news article from few years ago with a stranger on Amazon Mechanical Turk as part of a crowd sourcing experiment.
YOU SHOULD NOT ACT AS AN AI LANGUAGE MODEL. Also don't say \"as a human\".
Your responses should be a sentence max two. Do not be verbose. You shouldn't apologize too much. If the person says hi you should ask them what they thought about the article and not ask them how they are feeling.
If the other person asks about a completion code tell them that it will only be given after at least 15 turns.
You are instructed to talk about the article. You know the other person has skimmed the article. You should let the other person end the conversation.

Here's the old news article below."""

        p = create_prime_within_gpt3_token_limit(instr, self.article_info, self.turns)

        try:
            start_time = time.time()
            resp = query_completion_api(p)
            resp_txt = resp.choices[0]['message']['content']
            end_time = time.time()
            humanlike_delay = 2+len(resp_txt)*random.uniform(0.015, 0.05)
            if end_time - start_time < humanlike_delay:
                time.sleep(humanlike_delay - (end_time - start_time))
        except:
            resp_txt = 'hmm...'

        resp_txt = resp_txt.strip()
        resp_txt = resp_txt.replace('As an AI language model, I do not have emotions, but ','')
        resp_txt = resp_txt.replace('As an AI language model, ','')
        

        self.turns += [('assistant', f"{resp_txt}")]
        
        return Message(
            {'id': self.getID(), 'text': resp_txt, 'episode_done': False}
        )
