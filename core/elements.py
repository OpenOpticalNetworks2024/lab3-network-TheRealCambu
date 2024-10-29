import json


class Signal_information(object):
    # This constructor initializes the signal power to a given value, the noise
    # power and the latency to zero and the path as a given list of letters
    # that represents the labels of the nodes the signal has to travel through.
    def __init__(self, signal_power: float, path: list[str]):
        self._signal_power = signal_power  # float
        self._noise_power = 0.0  # float
        self._latency = 0.0  # float
        self._path = path  # list[string]

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
        # # Remove the current node to reflect the progression in the path
        # if self._path:
        #     self._path.pop(0)  # Move to the next node
        self._path.append(node)  # Append the node label to the path history


class Node(object):
    # This constructor initializes these values from a Python dictionary input.
    # The successive attribute must be initialized in an empty dictionary.
    def __init__(self, input_dict: dict):
        self._label = input_dict['label']  # String
        self._position = input_dict['position']  # Tuple of floats
        self._connected_nodes = input_dict['connected_nodes']  # List of strings
        self._successive = {}  # Dictionary to hold Line objects for each connected node

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
        # Modify the path attribute of the Signal Information
        # object by adding the current node's label
        signal_info.update_path(self._label)

        # Call the successive element propagate method, according to the specified path
        if signal_info.path:
            next_node_label = signal_info.path[0]
            if next_node_label in self._successive:
                self._successive[next_node_label].propagate(signal_info)
            else:
                print(f"Node {self._label}: No successive node found for {next_node_label}.")


class Line(object):
    def __init__(self, label: str, length: float):
        self._label = label  # string
        self._length = length  # float
        self._successive = {}

    @property
    def label(self):
        return self._length

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, connections: dict):
        self._successive = connections

    def latency_generation(self, signal: Signal_information) -> float:
        # Speed of light in fiber (2/3 of the speed of light in vacuum)
        speed_of_light_fiber = (2 / 3) * 3 * 10 ** 8

        # Compute the latency (s) = length (m) / c (m/s)
        latency = self._length / speed_of_light_fiber

        # Update the signal latency and return the new latency value
        signal.update_latency(latency)
        return signal.latency

    def noise_generation(self):
        pass

    def propagate(self):
        pass


class Network(object):
    def __init__(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def lines(self):
        pass

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
