import argparse
from typing import Any, Callable, Union

import genetic_algorithm
import numpy as np
import datetime as dt
import random
import os


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


class Tracer:
    def __init__(self, method, instance, seed, cutoff):
        self.cutoff = cutoff
        self.seed = seed
        self.instance = instance
        self.method = method
        self._event_log = []
        self._current_best = float('inf')

    def next_result(self, value):
        if value < self._current_best:
            self._event_log.append((dt.datetime.now(), value))


    def write_to(self, file_path):
        first_time = self._event_log[0][0]
        full_path = os.path.join(file_path, f'{self.instance}_{self.method}_{self.cutoff}_{self.seed}.trace')
        with open(full_path, 'w') as f:
            for time, value in self._event_log:
                seconds_elapsed = round((time - first_time).total_seconds(), 2)
                f.write(f'{seconds_elapsed}, {value}\n')

def save_solution_file(cost_value, solution, method, instance, seed, cutoff):
    with open(f'{instance}_{method}_{cutoff}_{seed}.sol', 'w') as solution_file:
        solution_file.write(str(cost_value) + '\n')
        solution_file.write(str(solution)[1:-1] + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run TSP on a given location file.')
    parser.add_argument('-inst',
                        type=str,
                        help='The full file path to the TSP data to solve.')
    parser.add_argument('-alg',
                        type=str,
                        help='The TSP algorithm to use. Currently supports LS1 only')
    parser.add_argument('-time',
                        type=int,
                        help='Time limit for TSP to solve in.')
    parser.add_argument('-seed',
                        type=int,
                        default=np.random.randint(999999),
                        help='Random seed for solver to use to ensure repeatable results.')
    args = parser.parse_args()

    print(
        f'''Running algorithm {args.alg} on file {args.inst} with a time limit of {args.time} seconds and a random seed of {args.seed}''')

    np.random.seed(args.seed)
    random.seed(np.random.randint(999999))
    start_time = dt.datetime.now()
    instance_name, city_data = load_data(args.inst)
    tracer = Tracer(method=args.alg, instance=instance_name, seed=args.seed, cutoff=args.time)

    def timer():
        return (dt.datetime.now() - start_time).total_seconds() < args.time


    if args.alg == 'LS1':
        score, solution = genetic_algorithm.solve(data=city_data,
                                                  timer=timer,
                                                  tracer=tracer)

    save_solution_file(score, solution, method=args.alg, instance=instance_name, seed=args.seed, cutoff=args.time)
    tracer.write_to('./')

# Roanoke Best So Far
#1313450.1104071145
#[159, 151, 192, 9, 194, 83, 56, 118, 199, 190, 177, 156, 48, 117, 6, 228, 62, 31, 162, 82, 106, 160, 129, 101, 39, 168, 80, 77, 49, 93, 34, 150, 54, 111, 154, 132, 86, 214, 100, 26, 61, 27, 33, 88, 182, 209, 19, 146, 73, 134, 206, 38, 139, 66, 42, 198, 30, 126, 70, 71, 161, 35, 0, 116, 4, 219, 180, 10, 213, 46, 224, 16, 196, 124, 153, 43, 155, 144, 90, 95, 21, 178, 165, 204, 36, 115, 74, 191, 183, 107, 210, 5, 223, 102, 186, 103, 229, 203, 220, 1, 81, 120, 76, 179, 23, 140, 127, 105, 221, 40, 65, 189, 98, 52, 215, 53, 99, 201, 91, 174, 17, 55, 104, 218, 157, 148, 114, 32, 128, 145, 87, 108, 216, 20, 3, 227, 152, 169, 141, 149, 185, 170, 89, 11, 37, 202, 211, 44, 171, 51, 138, 142, 13, 163, 197, 24, 112, 41, 125, 121, 176, 225, 97, 2, 137, 50, 68, 22, 158, 14, 119, 96, 207, 184, 15, 188, 136, 63, 47, 18, 29, 45, 110, 226, 222, 67, 8, 195, 25, 143, 59, 200, 173, 164, 7, 109, 135, 205, 84, 123, 130, 131, 79, 181, 193, 175, 12, 133, 64, 78, 75, 28, 166, 94, 58, 212, 92, 57, 167, 172, 122, 187, 60, 147, 113, 85, 69, 72, 217, 208]
