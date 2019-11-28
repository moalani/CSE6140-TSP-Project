import glob

import solve_controller

for file_name in glob.glob('DATA/*.tsp'):
    for algorithm in ['Approx', 'BnB', 'LS1', 'LS2']:
        if algorithm == 'LS2':
            solve_controller.solve_with_options(algorithm,
                                                42,
                                                600,
                                                file_name)
