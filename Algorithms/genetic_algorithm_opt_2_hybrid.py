import random
import numpy as np

from tracer import NullTracer
from utilities import tour_cost
import Algorithms.two_opt as ato


def breed_to_right(left, right_input):
    right = list(right_input)
    start_index = np.random.randint(len(left))
    # This section should choose randomly from the feasible sequence
    # This was initially meant to allow for circular reference but that
    # hasn't happened yet.
    # actual_selection_length = (len(foo)-1) - start_index
    # Replace next two lines with this ^^
    #selection_length = np.random.randint(1, len(left))
    #actual_selection_length = min(len(left) - start_index, selection_length)
    actual_selection_length = (len(left) - 1) - start_index
    left_chromosome = left[start_index: start_index + actual_selection_length]
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


def mutate(offspring):
    mutation_occurs = np.random.uniform() < 0.1
    if mutation_occurs:
        mutation_count = np.random.randint(1, int(np.sqrt(len(offspring)) + 2))
        for _ in range(mutation_count):
            swap_left = swap_right = 0
            while swap_left == swap_right:
                swap_left = np.random.randint(0, len(offspring))
                swap_right = np.random.randint(0, len(offspring))
            offspring[swap_left], offspring[swap_right] = offspring[swap_right], offspring[swap_left]
    return offspring


def optimize_tsp(locations, timer, tracer):
    current_low = float('inf')

    population_size = 200
    print("Running two_opt initially")
    initial_solve = ato.run_two_opt(locations, timer=timer, tracer=NullTracer())[1]
    print("Done running two_opt initially")
    population = generate_new_population(locations, population_size)
    population.append(initial_solve)
    costs = list(map(tour_cost, population))
    ranked_costs, ranked_population = list(zip(*sorted(zip(costs, population), key=lambda x: x[0])))
    time_spent = 0
    while time_spent <= 100 and timer(ranked_costs[0]):
        ranked_population = ranked_population[:population_size // 8]
        ranked_population += tuple(generate_new_population(locations, 4 * population_size // 8))
        best_pairings = list(zip(random.choices(ranked_population[:5], k=population_size // 4),
                                 random.choices(ranked_population[:100], k=population_size // 4)))
        random_pairings = list(zip(random.choices(ranked_population[:100], k=population_size // 4),
                                   random.choices(ranked_population[100:], k=population_size // 4)))

        pairings = best_pairings + random_pairings

        offspring = []
        offspring += list(
            map(lambda x: breed_to_right(x[0], x[1]) if np.random.random() > 0.5 else breed_to_right(x[1], x[0]),
                pairings))

        offspring = list(map(mutate, offspring))
        offspring += ranked_population[1:10]  # save top N just like they are

        if time_spent % 20 == 0:
            print(f'Running Two-Opt {time_spent}')
            counter = 0
            def two_opt_timer(x):
                nonlocal counter
                counter += 1
                return counter % 1000 == 0
            offspring = list(map(lambda x: ato.run_two_opt(x, timer=two_opt_timer, tracer=tracer)[1], offspring))
            print('Done running Two-Opt')
            #print(offspring)

        costs = list(map(tour_cost, list(offspring)))
        rankings = list(zip(*sorted(zip(costs, offspring), key=lambda x: x[0])))

        # Maintain a constant population
        ranked_costs, ranked_population = rankings[:population_size]

        if ranked_costs[0] < current_low:
            current_low = ranked_costs[0]
            time_spent = 0
        elif ranked_costs[0] == current_low:
            time_spent += 1

        tracer.next_result(ranked_costs[0])
    return ranked_costs[0], ranked_population[0]


def generate_new_population(locations, population_size):
    population = [locations.copy() for _ in range(population_size)]
    list(map(random.shuffle, population))
    return population


def solve(data: list, timer=lambda x: True, tracer=None) -> object:
    tsp_data = data
    location_index_map = {location: i for i, location in enumerate(tsp_data)}
    score, path = optimize_tsp(tsp_data, timer=timer, tracer=tracer)
    return score, [location_index_map[location] for location in path]