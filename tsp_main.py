import argparse
import numpy as np
import sys

# Custom utilities
from solve_controller import solve_with_options

# Optimization


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
                        default=sys.maxsize,
                        help='Time limit for TSP to solve in.')
    parser.add_argument('-seed',
                        type=int,
                        default=np.random.randint(999999),
                        help='Random seed for solver to use to ensure repeatable results.')
    args = parser.parse_args()

    solve_with_options(algorithm_to_run = args.alg,
                       seed=args.seed,
                       run_time = args.time,
                       inst = args.inst)
