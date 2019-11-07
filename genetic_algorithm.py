import datetime as dt
import random
import numpy as np


def distance(node_a: list, node_b: list) -> float:
    return np.sqrt((node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2)


def tour_cost(path: list) -> float:
    cost = 0
    for previous_index, current_node in enumerate(path[1:]):
        previous_node = path[previous_index]
        cost += distance(previous_node, current_node)
    cost += distance(path[0], path[-1])
    return cost


def load_data(file_name):
    with open(file_name, 'r') as input_file:
        lines_read = input_file.readlines()
        # Read all the data from the 5th index until before the last index
        # Parse the line into index numbers and coordinates
        # Convert coordinates to float
    data = []
    for text in lines_read:
        if len(text) > 0 and text[0].isdigit():
            data.append(tuple(map(float, text.strip().split(' ')[1:3])))
    return data


def breed_to_right(left, right_input):
    right = list(right_input)
    start_index = np.random.randint(len(left))
    selection_length = np.random.randint(1, len(left))
    actual_selection_length = min(len(left) - start_index, selection_length)
    end_index = start_index + actual_selection_length - 1
    left_chromosome = left[start_index: end_index + 1]
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


def optimize_tsp(locations, timer, seed):
    current_low = float('inf')
    epochs = 0

    population_size = 400
    population = generate_new_population(locations, population_size)
    costs = list(map(tour_cost, population))
    ranked_costs, ranked_population = list(zip(*sorted(zip(costs, population), key=lambda x: x[0])))
    time_spent = 0
    while time_spent <= 200 and timer():
        ranked_population = ranked_population[:population_size // 4]
        ranked_population += tuple(generate_new_population(locations, 3 * population_size // 4))
        best_pairings = list(zip(random.choices(ranked_population[:5], k=population_size // 8),
                                 random.choices(ranked_population, k=population_size // 8)))
        random_pairings = list(zip(random.choices(ranked_population[5:], k=population_size // 8),
                                   random.choices(ranked_population[5:], k=population_size // 8)))

        pairings = best_pairings + random_pairings

        offspring = []
        offspring += ranked_population[:5]  # save top N just like they are
        offspring += list(
            map(lambda x: breed_to_right(x[0], x[1]) if np.random.random() > 0.5 else breed_to_right(x[1], x[0]),
                pairings))

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


def generate_new_population(locations, population_size):
    population = [locations.copy() for _ in range(population_size)]
    list(map(random.shuffle, population))
    return population


def load_and_solve(seed: int, file_path: str = 'DATA/Atlanta.tsp', timer=lambda: True) -> object:
    tsp_data = load_data(file_path)
    location_index_map = {location: i for i, location in enumerate(tsp_data)}
    score, path = optimize_tsp(tsp_data, timer=timer, seed=seed)
    return score, [location_index_map[location] for location in path]


if __name__ == '__main__':
    start_time = dt.datetime.now()


    def timer():
        return (dt.datetime.now() - start_time).total_seconds() < args.time


    score, solution = load_and_solve(
        file_path='''/Users/justin/SynologyDrive/Learning Materials/School/Grad School/CSE 6140 Algorithms/Project/CSE6140-TSP-Project/DATA/Berlin.tsp''',
        timer=timer,
        seed=0)
    print(score, solution)
