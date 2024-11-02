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
SIGNAL_POWER_W = 1e-3  # Signal power in mW for SNR calculations

# TODO: 2) Define a Pandas dataframe with the following columns: path, total accumulated latency, total accumulated noise
#  and the SNR obtained with the propagation through the paths of spectral information with a signal power of 1 mW

network = Network(file_input)

network.connect()

# # Print all nodes
# for node_label, node in network.nodes.items():
#     print(node)
#
# # Print all lines
# for line_label, line in network.lines.items():
#     print(line)

column_names = ['Node couple', 'Path', 'Accumulated latency', 'Accumulated noise', 'SNR for P_tx = 0 dBm']
df = pd.DataFrame(columns=column_names)
possible_node_comb = [lines.label for lines in network.lines.values()]
possible_paths = {}
for node_comb in possible_node_comb:
    possible_paths = network.find_paths(node_comb[0], node_comb[1])
    for path in possible_paths

    list_of_string = ["->".join(path) for path in network.find_paths(node_comb[0], node_comb[1])]
    possible_paths[node_comb] = list_of_string

# for label, paths in possible_paths.items():
#     new_row = {
#         'Node couple': label,
#         'Path':
#     }
#     print(f"Possible paths that connect nodes \"{label[0]}\" and \"{label[1]}\"")
#     for path in paths:
#         print(f"   {path}")
# print(f"\"{node_comb[0]}\" -> \"{node_comb[1]}\": {found_paths}")
# possible_paths.append(found_paths)




