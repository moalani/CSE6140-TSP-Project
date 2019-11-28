from tracer import NullTracer
from utilities import distance, tour_cost


def optimize(tsp_data, timer, tracer=NullTracer()):
    return run_two_opt(tsp_data, timer, tracer)

def two_opt_swap(sequence, i, k):
    return sequence[:i] + sequence[i:k+1][::-1] + sequence[k+1:]

def run_two_opt(tsp_data, timer, tracer):
    original_cost = tour_cost(tsp_data)
    updated_cost = original_cost
    sequence = list(tsp_data)
    # For each edge-pair evaluate if there is a cross-over
    # For each city compare against every non-neighboring city
    while True:
        new_sequence_found = False
        for i in range(0, len(sequence)-1):
            for k in range(i+1, len(sequence)):
                if not timer(updated_cost):
                    return updated_cost, sequence
                new_route = two_opt_swap(sequence, i, k)
                new_cost = tour_cost(new_route)
                tracer.next_result(new_cost)
                if new_cost < updated_cost:
                    sequence = new_route
                    new_sequence_found = True
                    updated_cost = new_cost
                    break
            if new_sequence_found:
                break
        if not new_sequence_found:
            return updated_cost, sequence


def solve(data: list, timer=lambda x: True, tracer=None) -> object:
    location_index_map = {location: i for i, location in enumerate(data)}
    score, path = optimize(data, timer=timer, tracer=tracer)
    return score, [location_index_map[location] for location in path]


# A B C D A -> A C B D A

# A B C D E A -> A C B D E A

# (x1, y1) -> (x2, y2) -> (x3, y3) -> (x4, y4) -> (x1, y1)