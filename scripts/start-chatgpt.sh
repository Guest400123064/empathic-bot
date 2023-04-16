#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate
conda activate parlai

# Save current directory
export PARLAI_EMPATHIC_BOT_DIR=$(pwd)

# Start ParlAI with chatgpt agent in background
cd ./apps/terminal_server/
python main.py \
    --config-path ./config/config_chatgpt.yml &
cd $PARLAI_EMPATHIC_BOT_DIR
