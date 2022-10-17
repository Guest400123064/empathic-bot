#!/bin/zsh

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate

# Create conda ParlAI & Mephisto env 
#   - will create a conda env called <parlai>
conda create --force -n parlai python=3.9
conda activate parlai

# Install a ParlAI dependency that is not documented
#   If the following command fails, please run:
#       `sudo apt install libxml2-dev`
conda install -c conda-forge cudatoolkit-dev

# For vscode notebook env
pip install ipykernel ipywidgets

# Install openai (for gpt3 prompting)
pip install openai

# Install torch
conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge

# Install ParlAI and Mephisto from source
cd packages

# Install Mephisto
cd Mephisto
pip install -e .
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
cd Fairseq
pip install -e .
cd ..

# Install Search Engine dependencies
cd SearchEngine
pip install -r ./requirements.txt
cd ..

# Wrap-up
cd ..
conda deactivate
