import sys
from pathlib import Path

# Add the path to the core directory (two levels up from tasks)
sys.path.append(str(Path(__file__).resolve().parent.parent / 'core'))

import json
import numpy as np
import pandas as pd
from elements import Network, Signal_information  # Direct import after adjusting sys.path

# Define paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'  # Full path to the JSON file

# TODO: 2) Define a Pandas dataframe with the following columns: path, total accumulated latency, total accumulated noise
#  and the SNR obtained with the propagation through the paths of spectral information with a signal power of 1 mW

network = Network(file_input)

network.connect()

# TODO: 1) Find all the combinations of nodes in two places

# Print all nodes
for node_label, node in network.nodes.items():
    print(node)

# Print all lines
for line_label, line in network.lines.items():
    print(line)





