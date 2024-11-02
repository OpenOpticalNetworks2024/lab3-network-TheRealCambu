import json
import matplotlib.pyplot as plt
import numpy as np


class Signal_information(object):
    # This constructor initializes the signal power to a given value, the noise
    # power and the latency to zero and the path as a given list of letters
    # that represents the labels of the nodes the signal has to travel through.
    def __init__(self, signal_power: float, path: list[str]):
        self._signal_power = signal_power  # Signal power. Type: float
        self._noise_power = 0.0  # Noise power. Type: float
        self._latency = 0.0  # Latency. Type: float
        self._path = path  # List of node labels the signal must traverse. Type: list[string]

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self, increment: float):
        self._signal_power += increment

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, value: float):
        self._noise_power = value

    def update_noise_power(self, increment: float):
        self._noise_power += increment

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, value: float):
        self._latency = value

    def update_latency(self, increment: float):
        self._latency += increment

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: list[str]):
        self._path = value

    def update_path(self, node: str):
        # Append the node label to the path history
        self._path.append(node)


class Node(object):
    def __init__(self, input_dict: dict):
        self._label = input_dict['label']  # Unique identifier for the line. Type: list[string]
        self._position = tuple(input_dict['position'])  # Tuple of position. Type: tuple(float, float)
        self._connected_nodes = input_dict['connected_nodes']  # List of connected node labels. Type: list[string]
        self._successive = {}  # Dictionary to hold Line objects for each connected node. Type: dict

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, connections: dict):
        # Sets a connection in successive to a Line object
        self._successive = connections

    def propagate(self, signal_info: Signal_information):
        # Update the signal path and mark this node as visited
        signal_info.update_path(self._label)

        # Call the successive element propagate method, according to the specified path
        if signal_info.path:
            next_node_label = signal_info.path.pop(0)
            if next_node_label in self._successive:
                # Call propagate on the connecting line object
                self._successive[next_node_label].propagate(signal_info)


class Line(object):
    def __init__(self, label: str, length: float):
        self._label = label  # Unique identifier for the line. Type: string
        self._length = length  # Length of the line. Type: float
        self._successive = {}  # Successive node after the line. Type: dict

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, connections: dict):
        self._successive = connections

    def latency_generation(self) -> float:
        # Compute the latency as the fiber length divided by the speed of light in fiber
        return self._length / 2e8

    def noise_generation(self, signal_power: float) -> float:
        # Compute the noise
        return 1e-9 * signal_power * self._length

    def propagate(self, signal_info: Signal_information):
        # Update the signal noise power
        noise = self.noise_generation(signal_info.signal_power)
        signal_info.update_noise_power(noise)

        # Update the signal latency
        latency = self.latency_generation()
        signal_info.update_latency(latency)

        # Call the successive element propagate method, according to the specified path
        if signal_info.path:
            next_node_label = signal_info.path.pop(0)
            if next_node_label in self._successive:
                self._successive[next_node_label].propagate(signal_info)


class Network(object):
    def __init__(self, json_file: str):
        with open(json_file) as file:
            data = json.load(file)

        # Initialize the dictionaries as empty
        self._nodes = {}
        self._lines = {}

        # Initialize nodes
        for label, attributes in data.items():
            node = Node({
                'label': label,
                'connected_nodes': attributes['connected_nodes'],
                'position': tuple(attributes['position'])
            })
            self._nodes[label] = node

        # Initialize lines with forward and backward connections
        for node_label, node in self._nodes.items():
            for connected_node_label in node.connected_nodes:
                # Produce the line label
                line_label = f"{node_label}{connected_node_label}"

                # Compute the length of the line
                node_position = np.array(node.position)
                connected_node_position = np.array(self._nodes[connected_node_label].position)
                length = np.linalg.norm(node_position - connected_node_position)

                # Add lines to the lines dictionary (for both directions)
                self._lines[node_label] = Line(line_label, length)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        for node_label, node in self._nodes.items():
            x, y = node.position
            plt.plot(x, y, 'bo')
            plt.text(x, y, node_label, color='red', fontsize=12, ha='right')

        for line in self._lines.values():
            start_node_label, end_node_label = line.label[0], line.label[1]
            start_pos, end_pos = self._nodes[start_node_label].position, self._nodes[end_node_label].position
            plt.plot([start_pos[0], start_pos[1]], [end_pos[0], end_pos[1]], 'g-')

        plt.title("Optical Network")
        plt.show()

    # Find_paths: given two node labels, returns all paths that connect the 2 nodes as a list of node labels.
    # Admissible path only if cross any node at most once
    def find_paths(self, label1: str, label2: str):
        all_paths = []
        visited = set()

        def dfs(current_node, target_node, path):
            if current_node == target_node:
                all_paths.append(path.copy())
                return
            visited.add(current_node)
            for neighbor in self._nodes[current_node].connected_nodes:
                if neighbor not in visited:
                    path.append(neighbor)
                    dfs(neighbor, target_node, path)
                    path.pop()
            visited.remove(current_node)

        dfs(label1, label2, [label1])
        return all_paths

    # Connect function set the successive attributes of all NEs as dicts each node must have dict of lines and viceversa
    def connect(self):
        # Fill the "_successive" dictionary of each node with all the information about the lines
        for node_label, node in self._nodes.items():
            for connected_node_label in node.connected_nodes:
                # Get the line that connects this node to the connected node
                line_label = f"{node_label}{connected_node_label}"
                line = self._lines[line_label]

                # Update the node's successive attribute
                node.successive[line_label] = line

                # Update the line's successive attribute (pointing to the connected node)
                line.successive[connected_node_label] = self._nodes[connected_node_label]

    # Propagate signal_information through path specified in it and returns the modified spectral information
    def propagate(self, signal_information):
        start_node_label = signal_information.path.pop(0)
        self._nodes[start_node_label].propagate(signal_information)
        return signal_information
