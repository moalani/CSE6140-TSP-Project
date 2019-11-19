import argparse
import datetime as dt
import random
import numpy as np
import sys

# Custom utilities
from tracer import Tracer
from utilities import load_data, early_stop_checker

# Optimization
import BnB
import genetic_algorithm

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
                        default=sys.maxsize,
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

    score, solution = None, None

    if args.alg == 'LS1':
        score, solution = genetic_algorithm.solve(data=city_data,
                                                  timer=early_stop_checker(seconds=args.time),
                                                  tracer=tracer)
    elif args.alg == 'BnB':
        score, solution = BnB.solve(data=city_data,
                                    timer=early_stop_checker(seconds=args.time),
                                    tracer=tracer)

    save_solution_file(score,
                       solution,
                       method=args.alg,
                       instance=instance_name,
                       seed=args.seed,
                       cutoff=args.time)
    tracer.write_to('./')
