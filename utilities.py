import datetime as dt

import numpy as np


def load_data(file_name):
    with open(file_name, 'r') as input_file:
        lines_read = input_file.readlines()
        # Read all the data from the 5th index until before the last index
        # Parse the line into index numbers and coordinates
        # Convert coordinates to float
    name = ''
    data = []
    for text in lines_read:
        if len(text) > 0 and text[0].isdigit():
            data.append(tuple(map(float, text.strip().split(' ')[1:3])))
        elif 'NAME: ' in text:
            name = text[6:-1]
    return name, data


def early_stop_checker(seconds=float('inf'), target_cost=0):
    start_time = dt.datetime.now()
    def _lambda(q): 
        return ((dt.datetime.now() - start_time).total_seconds() < seconds) and q > target_cost
    return _lambda


def distance(node_a: list, node_b: list) -> float:
    return np.sqrt((node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2)


def tour_cost(path: list) -> float:
    cost = 0
    for previous_index, current_node in enumerate(path[1:]):
        previous_node = path[previous_index]
        cost += distance(previous_node, current_node)
    cost += distance(path[0], path[-1])
    return cost