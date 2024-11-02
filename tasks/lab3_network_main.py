import json
import numpy as np
import pandas as pd
from pathlib import Path
from core.elements import Node, Network

# Define paths
ROOT = Path(__file__).parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'

# TODO: 1) Find all the combinations of node in two places

# TODO: 2) Define a Pandas dataframe with the following columns: path, tot accumulated latency, tot accumulated noise
#  and the SNR obtained with the propagation through the paths of a spectral information with a signal power of 1 mW

network = Network(INPUT_FOLDER)


