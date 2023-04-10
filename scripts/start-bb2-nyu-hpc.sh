#!/bin/bash

# Activate environment
cd $SCRATCH
singularity exec --nv --overlay overlay-50GB-10M.ext3:ro \
    /scratch/work/public/singularity/cuda11.6.124-cudnn8.4.0.27-devel-ubuntu20.04.4.sif \
    /bin/bash

source /ext3/env.sh
conda activate parlai

cd projects

# Start search engine for blenderbot2
#   - assuming the <parlai> environment is installed
#   - will serve at <localhost:5000>
# python ./packages/SearchEngine/main.py serve \
#     --host localhost:5000 \
#     --search_engine="CustomDoc" &

# Start BlenderBot2 in background
python ./apps/terminal_server/main.py \
    --config-path ./apps/terminal_server/config/config_echo.yml &