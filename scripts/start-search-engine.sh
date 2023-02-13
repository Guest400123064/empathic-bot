#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate

# Start search engine for blenderbot2
#   - assuming the <parlai> environment is installed
#   - will serve at <localhost:5000>
conda activate parlai
cd ./packages/SearchEngine
python ./main.py serve --host localhost:5000 --search_engine="CustomDoc" &
