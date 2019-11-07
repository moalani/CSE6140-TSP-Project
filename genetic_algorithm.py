import numpy as np


def distance(node_a: tuple, node_b: tuple) -> float:
    return np.sqrt((node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2)


def tour_cost(path: list) -> float:
    cost = 0
    for previous_index, current_node in enumerate(path[1:]):
        previous_node = path[previous_index]
        cost += distance(previous_node, current_node)
    return cost


def load_data(file_name):
    with open(file_name, 'r') as input_file:
        # Read all the data from the 5th index until before the last index
        # Parse the line into index numbers and coordinates
        # Convert coordinates to float
        data = [list(map(float, text.strip().split(' ')[1:3])) for text in input_file.readlines()[5:-1]]
    return data


def breed_to_right(left, right_input):
    right = list(right_input)
    start_index = np.random.randint(len(left))
    selection_length = np.random.randint(1, len(left))
    actual_selection_length = min(len(left) - start_index, selection_length)
    end_index = start_index + actual_selection_length - 1
    left_chromosome = left[start_index : end_index + 1]
    right_insertion_index = np.random.randint(0, len(right) - actual_selection_length)
    for index, left_insertion in enumerate(left_chromosome):
        right_removed = right[right_insertion_index: right_insertion_index + actual_selection_length]
        if left_insertion not in right_removed:
            swap_index = right.index(left_insertion)
            right[swap_index] = right[right_insertion_index + index]
        else:
            swap_index = right_removed.index(left_insertion)
            right[right_insertion_index + swap_index] = right_removed[index]
        right[right_insertion_index + index] = left_insertion
    return right

import random

def optimize_tsp(locations):
    current_low = float('inf')
    time_spent = 0
    epochs = 0

    population_size = 400
    population = [locations.copy() for _ in range(population_size)]
    list(map(random.shuffle, population))
    costs = list(map(tour_cost, population))
    ranked_costs, ranked_population = list(zip(*sorted(zip(costs, population), key=lambda x: x[0])))

    while time_spent <= 200 and epochs <= 10000:
        pairings = list(zip(ranked_population[::2], ranked_population[1::2]))[:10]
        offspring = []
        offspring += ranked_population[:40] # save top 10 just like they are
        for _ in range(15):
            offspring += list(map(lambda x: breed_to_right(x[0], x[1]) if np.random.random() > 0.5 else breed_to_right(x[1], x[0]), pairings))
        costs = list(map(tour_cost, list(offspring)))
        rankings = list(zip(*sorted(zip(costs, offspring), key=lambda x: x[0])))

        # Maintain a constant population
        ranked_costs, ranked_population = rankings[:population_size]
        if ranked_costs[0] < current_low:
            current_low = ranked_costs[0]
            time_spent = 0
        elif ranked_costs[0] == current_low:
            time_spent += 1
        epochs += 1
        print(f'Lowest cost: {ranked_costs[0]}')
    return ranked_costs[0], ranked_population[0]


if __name__ == '__main__':
    tsp_data = load_data('DATA/Atlanta.tsp')
    print(tsp_data)
    print(tour_cost(tsp_data))
    print(optimize_tsp(tsp_data))
    #breed_to_right([6,1,4,9,3,2,5,8,7,0], [0,1,2,3,4,5,6,7,8,9])

    # TODO: Doesn't support random mutations yet.
