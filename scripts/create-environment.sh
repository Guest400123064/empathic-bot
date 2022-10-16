#!/bin/sh

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate

# Create conda ParlAI & Mephisto env 
#   - will create a conda env called <parlai>
conda create --force -n parlai python=3.8
conda activate parlai

# Install a ParlAI dependency that is not documented
#   If the following command fails, please run:
#       `sudo apt install libxml2-dev`
conda install -c conda-forge cudatoolkit-dev

# For vscode notebook env
pip install -U ipykernel ipywidgets

# Install torch
conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge

# Install ParlAI and Mephisto from source
cd packages

# Install Fairseq first to avoid version conflict
cd Fairseq
pip install -U -e .
cd ..

# Install Mephisto
cd Mephisto
pip install -U -e .
cd ..

# Install ParlAI
cd ParlAI
pip install -U -e .
cd ..

conda deactivate

# Install Search Engine dependencies
#   - will create a conda env called <search-engine>
conda env create --force -f ./SearchEngine/environment.yml
cd ..
