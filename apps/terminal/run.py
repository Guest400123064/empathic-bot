#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Terminal Chat Runner. Used to run the terminal chat server.
"""

import os
import logging

if not os.path.exists('./log'):
    os.makedirs('./log')

file_handler = logging.FileHandler('log/run.log', 'w')
formatter    = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
for handler in logger.handlers[:]:
    logger.removeHandler(handler)
logger.addHandler(file_handler)

import parlai.chat_service.utils.config as config_utils
from parlai.core.params import ParlaiParser

from src.terminal_manager import TerminalManager


SERVICE_NAME = 'terminal'


def setup_args():
    """
    Set up args.

    :return: A parser that takes in command line arguments for chat services (debug, config-path, password), and a port.
    """

    parser = ParlaiParser(False, False)
    parser.add_parlai_data_path()
    parser.add_chatservice_args()
    parser_grp = parser.add_argument_group('Terminal Chat')
    parser_grp.add_argument(
        '--port', default=35496, type=int, help='Port to run the terminal chat server'
    )
    return parser.parse_args()


def run(opt):
    """
    Run TerminalManager.
    """
    opt['service'] = SERVICE_NAME
    manager = TerminalManager(opt)
    try:
        manager.start_task()
    finally:
        manager.shutdown()


if __name__ == '__main__':

    opt = setup_args()
    config_path = opt.get('config_path')
    config = config_utils.parse_configuration_file(config_path)
    opt.update(config['world_opt'])
    opt['config'] = config
    run(opt)
