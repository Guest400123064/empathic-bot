#!/bin/bash

# Activate environment
source /ext3/env.sh
conda activate parlai

# Start search engine for blenderbot2
#   - assuming the <parlai> environment is installed
#   - will serve at <localhost:5000>
# python ./packages/SearchEngine/main.py serve \
#     --host localhost:5000 \
#     --search_engine="CustomDoc" &

# Start BlenderBot2 in background
python ./apps/terminal_server/main.py \
    --config-path ./apps/terminal_server/config/config_echo.yml &

# Start ngrok
/scratch/js11531/labshare/ngrok tcp 35496
