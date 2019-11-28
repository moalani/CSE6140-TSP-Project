import random

import numpy as np

from Algorithms import genetic_algorithm, BnB, two_opt, genetic_algorithm_opt_2_hybrid, nearest_neighbor
from tracer import Tracer
from utilities import load_data, early_stop_checker


def save_solution_file(cost_value, solution, method, instance, seed, cutoff):
    file_name = f'output/{instance}_{method}_{cutoff}_{seed}.sol' if method != 'BnB' else f'output/{instance}_{method}_{cutoff}.sol'
    with open(file_name, 'w') as solution_file:
        solution_file.write(str(int(cost_value)) + '\n')
        solution_file.write(','.join(map(str, solution)) + '\n')


def solve_with_options(algorithm_to_run,
                       seed,
                       run_time,
                       inst):
    print(
        f'''Running algorithm {algorithm_to_run} on file {inst} with a time limit of {run_time} seconds and a random seed of {seed}''')
    np.random.seed(seed)
    random.seed(np.random.randint(999999))
    instance_name, city_data = load_data(inst)
    tracer = Tracer(method=algorithm_to_run, instance=instance_name, seed=seed, cutoff=run_time)
    score, solution = None, None
    if algorithm_to_run == 'LS1':
        score, solution = genetic_algorithm.solve(data=city_data,
                                                  timer=early_stop_checker(seconds=run_time),
                                                  tracer=tracer)
    elif algorithm_to_run == 'BnB':
        score, solution = BnB.solve(data=city_data,
                                    timer=early_stop_checker(seconds=run_time),
                                    tracer=tracer)
    elif algorithm_to_run == 'LS2':
        score, solution = two_opt.solve(data=city_data,
                                        timer=early_stop_checker(seconds=run_time),
                                        tracer=tracer)
    elif algorithm_to_run == 'LS3':
        score, solution = genetic_algorithm_opt_2_hybrid.solve(data=city_data,
                                                               timer=early_stop_checker(seconds=run_time),
                                                               tracer=tracer)
    elif algorithm_to_run == 'Approx':
        score, solution = nearest_neighbor.solve(data=city_data,
                                                 timer=early_stop_checker(seconds=run_time),
                                                 tracer=tracer)
    save_solution_file(score,
                       solution,
                       method=algorithm_to_run,
                       instance=instance_name,
                       seed=seed,
                       cutoff=run_time)
    tracer.write_to('output/')