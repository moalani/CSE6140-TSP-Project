
import random

import utilities
from tracer import Tracer


def optimize(data, timer, tracer:Tracer):
    remaining_cities = list(data)
    first_city = random.choice(remaining_cities)
    greedy_path = [first_city]
    current_cost = utilities.tour_cost(remaining_cities)

    while len(remaining_cities) > 0 and timer(q=current_cost):
        best_city_index = None
        best_score = float('inf')
        for i, city in enumerate(remaining_cities):
            score = utilities.distance(greedy_path[-1], city)
            if score < best_score:
                best_city_index = i
                best_score = score
        greedy_path.append(remaining_cities.pop(best_city_index))
        current_cost = utilities.tour_cost(greedy_path + remaining_cities)
        tracer.next_result(current_cost)

    final_cost = utilities.tour_cost(greedy_path)
    return final_cost, greedy_path

def solve(data: list, timer=lambda x: True, tracer=None) -> object:
    location_index_map = {location: i for i, location in enumerate(data)}
    score, path = optimize(data, timer=timer, tracer=tracer)
    return score, [location_index_map[location] for location in path]