import glob
from Algorithms import BnB
import datetime as dt
import utilities
import json
from tracer import NullTracer


if __name__ == '__main__':
    runs_per_instance = 15
    results = {}
    for city_file in glob.glob('DATA/*.tsp'):
        print(city_file)
        for i in range(runs_per_instance):
            print(i)
            instance_name, city_data = utilities.load_data(city_file)
            start_time = dt.datetime.now()
            score, solution = BnB.solve(data=city_data,
                                        timer=utilities.early_stop_checker(600),
                                        tracer=NullTracer())
            end_time = dt.datetime.now()
            instance_results = results.get(instance_name, {'costs': [], 'times': []})
            instance_results['costs'].append(int(score))
            instance_results['times'].append((end_time - start_time).total_seconds())
            results[instance_name] = instance_results
    json.dump(obj=results, fp=open('comprehensive_report_bnb.json', 'w'))
