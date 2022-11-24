#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh
conda deactivate

conda activate parlai

# Setup mephisto data folder
mephisto config core.main_data_directory ./data/mephisto-data
mephisto check