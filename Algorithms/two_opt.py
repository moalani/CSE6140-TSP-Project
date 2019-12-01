import random

from tracer import NullTracer
from utilities import distance, tour_cost


def optimize(tsp_data, timer, tracer=NullTracer()):
    return run_two_opt(tsp_data, timer, tracer)


def two_opt_swap(sequence, i, k):
    return sequence[:i] + sequence[i:k+1][::-1] + sequence[k+1:]


def run_two_opt(tsp_data, timer, tracer):
    updated_cost = tour_cost(tsp_data)
    sequence = list(tsp_data)
    # Keep searching for 2-opt swaps until there are no further improvements.
    while True:
        iteration_cost = updated_cost
        for i in range(0, len(sequence)-1):
            for k in range(i+1, len(sequence)):
                if not timer(updated_cost):
                    return updated_cost, sequence
                new_route = two_opt_swap(sequence, i, k)
                new_cost = tour_cost(new_route)
                tracer.next_result(new_cost)
                if new_cost < updated_cost:
                    sequence = new_route
                    updated_cost = new_cost
                    break
        if updated_cost >= iteration_cost:
            return updated_cost, sequence


def solve(data: list, timer=lambda x: True, tracer=None) -> object:
    random.shuffle(data)
    location_index_map = {location: i for i, location in enumerate(data)}
    score, path = optimize(data, timer=timer, tracer=tracer)
    return score, [location_index_map[location] for location in path]
