# CSE6140-TSP-Project

Project Report Folder
https://drive.google.com/drive/folders/1C3KlKVYS37SJlamtDxwUDJeaTvf16mvx

Comprehensive Report Results
https://docs.google.com/spreadsheets/d/1s1JZGs5PHlm51C7ku-QRZw8UeWOzn6Ny4yUw4hdiBkM/edit?usp=sharing


# Summary of how to run the code

The various algorithms can be ran by running the following command from the project root:
python main.py -inst [PROJECT ROOT PATH]/DATA/NYC.tsp -alg BnB -time 10

Where "[PROJECT ROOT PATH]" is the path to the root of the project (the path to the inside of the project folder) on your computer.

-alg specifies the algorithm to use. Currently BnB and LS1 are implemented. LS1 is a genetic algorithm.

-time specifies a run time in seconds. If it is not specified it will default to sys.maxsize which is really really long and you'll never hit the limit.1C3KlKVYS37SJlamtDxwUDJeaTvf16mvx

You can also specify -seed and provide a seed for the random number generators. If you do not provide a seed, a random see will be specified and used. You will find this on the solution and trace files that are created.


# How to Add an Algorithm

Algorithms need to have the following signature to enable reporting on the necessary metrics:

    solve(data: list, timer=lambda x: True, tracer=None) -> tuple:

The module must have a method called "solve" that takes in the following arguments:
1. data- a list of coordinate tuples
1. timer- a lambda that returns True as long as the algorithm should continue running. A very robust one can be created using the early_stop_checker function in the utilities module. This allows limits to be set on time and solution quality. By default the timer is unbounded; it uses infinity seconds and a solution cost of 0 to achieve that.
1. tracer- the tracer is what collects the log of updates from your algorithm. Simply instantiate a tracer and then call "next_result" while passing the current solution quality on every iteration. It will handle the logic of when the solution has improved and make the minimal number of log entries.




