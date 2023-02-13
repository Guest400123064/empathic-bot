#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate
conda activate parlai

# Setup mephisto data folder
mkdir -p ./data/mephisto-data/data

mephisto config core.main_data_directory ./data/mephisto-data/data
mephisto check

conda deactivate
