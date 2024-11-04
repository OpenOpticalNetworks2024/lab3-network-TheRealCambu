import sys
from pathlib import Path
import pandas as pd
from itertools import permutations

# Add the path to the core directory (two levels up from tasks)
sys.path.append(str(Path(__file__).resolve().parent.parent / 'core'))
from elements import Network
from science_utils import calculate_snr

# Define paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'  # Full path to the JSON file
SIGNAL_POWER_W = 1e-3  # Signal power in watts (1 mW)

# Initialize the network from JSON file and connect it
network = Network(file_input)
network.connect()

# Initialize results list to store paths and their metrics
results = []

# Find all the possible combinations of nodes in the network
node_couples = permutations(network.nodes.keys(), 2)

# Iterate through each line in the network to find paths between node pairs
for node_couple in node_couples:
    start_node, end_node = node_couple[0], node_couple[1]
    possible_paths = network.find_paths(start_node, end_node)

    for path in possible_paths:
        # Generate a string containing all the nodes traversed by the signal
        path_str = "->".join(path)

        # Generate a list containing all the line labels between the start and end nodes
        line_labels = [f"{path[idx]}{path[idx + 1]}" for idx in range(len(path) - 1)]

        # Calculate cumulative latency and noise for the path
        acc_latency = sum(network.lines[line_label].latency_generation() for line_label in line_labels)
        acc_noise = sum(network.lines[line_label].noise_generation(SIGNAL_POWER_W) for line_label in line_labels)

        # Calculate SNR in dB
        snr_db = calculate_snr(SIGNAL_POWER_W, acc_noise)

        # Append the result
        results.append({
            'Node couple': f"{start_node}-{end_node}",
            'Path': path_str,
            'Accumulated latency (s)': acc_latency,
            'Accumulated noise (W)': acc_noise,
            'SNR (dB)': snr_db
        })

# Create DataFrame
df = pd.DataFrame(results)

# Display the DataFrame
print(df)

# Draw the network
network.draw()