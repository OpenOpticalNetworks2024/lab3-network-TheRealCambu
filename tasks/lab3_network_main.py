import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'

# Open the JSON file, read it and store the data
with open(file_input) as file:
    data = json.load(file)

# Initialize and empty dictionary
nodes = {}

# Fill the dictionary with the data of the JSON
for label, attributes in data.items():
    nodes[label] = {
        'connected_nodes': attributes['connected_nodes'],
        'position': attributes['position']
    }

for node, info in nodes.items():
    print(f"Connections for node {node}:")
    for connected_node in info['connected_nodes']:
        print(f"    {node}{connected_node}")
        print(f"    {connected_node}{node}")

# print(f"Node: {node}")
# print(f"   Connected node: {info['connected_nodes']}")
# print(f"   Positions: {info['position']}")

