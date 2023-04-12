#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate
conda activate parlai

# Save current directory
export PARLAI_EMPATHIC_BOT_DIR=$(pwd)

# Start search engine for blenderbot2
#   - assuming the <parlai> environment is installed
#   - will serve at <localhost:5000>
cd ./packages/SearchEngine/
python main.py serve \
    --host localhost:5000 \
    --search_engine="CustomDoc" &
cd $PARLAI_EMPATHIC_BOT_DIR

# Start BlenderBot2 in background
cd ./apps/terminal_server/
python main.py \
    --config-path ./apps/terminal_server/config/config_bb2.yml &
cd $PARLAI_EMPATHIC_BOT_DIR
