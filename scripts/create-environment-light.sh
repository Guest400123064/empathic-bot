#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate

# Create conda ParlAI & Mephisto env 
#   - will create a conda env called <parlai>
conda create --force -n parlai-light python=3.9
conda activate parlai-light

# Install torch
pip install pytorch==1.12.1

# Install openai (for gpt3 prompting)
pip install openai

# Install transformers
pip install transformers

# Install ParlAI and Mephisto from source
cd packages

# Install Search Engine dependencies
cd SearchEngine
pip install -r ./requirements.txt
cd ..

# Install ParlAI
#   - will have package conflict with Mephisto on,
#       + pytest<6.0,>=5.0 (but you have pytest 6.2.0)
#   - however, the code seems to be running at this point
cd ParlAI
pip install -e .
cd ..

# Install Fairseq last to minimize version conflict
#   - fairseq will have version conflict due to the following packages:
#       + hydra-core<1.1,>=1.0.7 (but you have hydra-core 1.2.0)
#       + omegaconf<2.1 (but you have omegaconf 2.2.3)
#   - however, the code seems to be running at this point
# cd Fairseq
# pip install -e .
# cd ..

# Wrap-up
cd ..
conda deactivate
