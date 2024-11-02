import sys
from pathlib import Path
import pandas as pd

# Add the path to the core directory (two levels up from tasks)
sys.path.append(str(Path(__file__).resolve().parent.parent / 'core'))
from elements import Network, Signal_information
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

for line in network.lines.values():
    start_node, end_node = line.label[0], line.label[1]
    possible_paths = network.find_paths(start_node, end_node)

    for path in possible_paths:
        # Path label
        node_couple = f"{start_node}-{end_node}"

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
            'Node couple': node_couple,
            'Path': path_str,
            'Accumulated latency': acc_latency,
            'Accumulated noise': acc_noise,
            'SNR (dB)': snr_db
        })

# Create DataFrame
df = pd.DataFrame(results)

print(df)
