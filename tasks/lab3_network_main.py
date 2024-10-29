import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'

with open(file_input) as file:
    data = json.load(file)

nodes = {}

for label, attributes in data.items():
    nodes[label] = {
        'connected_nodes': attributes['connected_nodes'],
        'position': attributes['position']
    }

for node, info in nodes.items():
    print(f"Node: {node}")
    print(f"   Connected node: {info['connected_nodes']}")
    print(f"   Positions: {info['position']}")
# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
