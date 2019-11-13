import glob
import genetic_algorithm
import datetime as dt
from utilities import load_data
import json
from tracer import NullTracer


if __name__ == '__main__':
    runs_per_instance = 15
    results = {}
    for city_file in glob.glob('DATA/*.tsp'): #['DATA/UKansasState.tsp', 'DATA/Atlanta.tsp']:#
        print(city_file)
        for i in range(runs_per_instance):
            print(i)
            instance_name, city_data = load_data(city_file)
            start_time = dt.datetime.now()
            score, solution = genetic_algorithm.solve(data=city_data,
                                                      timer=lambda: (dt.datetime.now() - start_time).total_seconds() < 600,
                                                      tracer=NullTracer())
            end_time = dt.datetime.now()
            instance_results = results.get(instance_name, {'costs': [], 'times': []})
            instance_results['costs'].append(score)
            instance_results['times'].append((end_time - start_time).total_seconds())
            results[instance_name] = instance_results
    json.dump(obj=results, fp=open('comprehensive_report.json', 'w'))
