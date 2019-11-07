import argparse
from typing import Any, Callable, Union

import genetic_algorithm
import numpy as np
import datetime as dt

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

    start_time = dt.datetime.now()


    def timer():
        return (dt.datetime.now() - start_time).total_seconds() < args.time


    if args.alg == 'LS1':
        score, solution = genetic_algorithm.load_and_solve(file_path=args.inst,
                                                           timer=timer,
                                                           seed=args.seed)
        print(score)
        print(solution)


# Roanoke Best So Far
# 3037024.2378277727
# [175, 143, 178, 82, 134, 161, 43, 219, 115, 168, 54, 88, 160, 183, 195, 191, 20, 3, 49, 116, 165, 129, 5, 196, 176, 197, 109, 67, 210, 137, 12, 119, 107, 26, 39, 61, 182, 117, 51, 200, 58, 113, 148, 171, 136, 7, 48, 101, 106, 74, 204, 31, 0, 6, 164, 199, 121, 163, 79, 187, 123, 69, 158, 73, 8, 184, 93, 36, 27, 80, 33, 132, 86, 111, 154, 209, 45, 226, 135, 30, 190, 198, 131, 229, 211, 128, 11, 185, 108, 169, 32, 227, 216, 214, 220, 19, 59, 2, 172, 62, 228, 34, 90, 202, 63, 18, 153, 225, 41, 207, 42, 139, 156, 71, 206, 68, 64, 78, 223, 124, 224, 4, 155, 144, 133, 84, 159, 9, 194, 192, 47, 72, 28, 60, 75, 151, 140, 174, 201, 180, 96, 222, 188, 110, 193, 208, 138, 83, 127, 189, 23, 177, 56, 203, 213, 97, 126, 77, 95, 100, 150, 10, 50, 181, 1, 24, 13, 146, 38, 162, 70, 66, 35, 118, 112, 46, 81, 114, 166, 22, 167, 14, 15, 130, 205, 173, 102, 120, 53, 85, 141, 149, 170, 87, 145, 186, 217, 212, 92, 122, 125, 147, 40, 98, 215, 17, 52, 99, 104, 65, 157, 142, 16, 25, 21, 29, 94, 103, 37, 152, 89, 179, 218, 221, 76, 105, 91, 55, 57, 44]