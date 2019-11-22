from tracer import NullTracer
from utilities import distance, tour_cost


def optimize(tsp_data, timer, tracer=NullTracer()):
    return run_two_opt(tsp_data, timer, tracer)


def run_two_opt(tsp_data, timer, tracer):
    original_cost = tour_cost(tsp_data)
    updated_cost = original_cost
    sequence = list(tsp_data)
    # For each edge-pair evaluate if there is a cross-over
    # For each city compare against every non-neighboring city
    for i, A in enumerate(sequence):
        for k, B in enumerate(sequence[:i - 1]):
            sequence[i], sequence[k] = sequence[k], sequence[i]
            updated_cost = tour_cost(sequence)
            if updated_cost < original_cost:
                original_cost = updated_cost
            else:
                sequence[i], sequence[k] = sequence[k], sequence[i]
            tracer.next_result(updated_cost)
            if not timer(updated_cost):
                break
        for k_, B in enumerate(sequence[i + 2:]):
            k = k_ + i + 2
            sequence[i], sequence[k] = sequence[k], sequence[i]
            updated_cost = tour_cost(sequence)
            if updated_cost < original_cost:
                original_cost = updated_cost
            else:
                sequence[i], sequence[k] = sequence[k], sequence[i]
            tracer.next_result(updated_cost)
            if not timer(updated_cost):
                break
        if not timer(updated_cost):
            break
    return updated_cost, sequence


def solve(data: list, timer=lambda x: True, tracer=None) -> object:
    location_index_map = {location: i for i, location in enumerate(data)}
    score, path = optimize(data, timer=timer, tracer=tracer)
    return score, [location_index_map[location] for location in path]


# A B C D A -> A C B D A

# A B C D E A -> A C B D E A

# (x1, y1) -> (x2, y2) -> (x3, y3) -> (x4, y4) -> (x1, y1)