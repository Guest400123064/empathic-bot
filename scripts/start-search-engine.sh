source $CONDA_PREFIX/etc/profile.d/conda.sh

# Start search engine for blenderbot2
#   - assuming the search-engine environment is installed
#   - will serve at <localhost:8080>
conda activate search-engine
python ./packages/SearchEngine/main.py serve --host localhost:8080
