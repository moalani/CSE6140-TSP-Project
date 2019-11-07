import argparse
import genetic_algorithm
import numpy as np


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

    print(f'''Running algorithm {args.alg} on file {args.inst} with a time limit of {args.time} seconds and a random seed of {args.seed}''')

    if args.alg == 'LS1':
        score, solution = genetic_algorithm.load_and_solve(file_path=args.inst,
                                         time=args.time,
                                         seed=args.seed)
        print(score)
        print(solution)
