# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:07:49 2020

@author: Mika Sipilä
"""

import simpy
import random
import numpy
import settings
import statistics
from Hospital import Hospital
import json
import regression


def get_data(hospital):
    patients = hospital.patients
    patients_finished = list(filter(lambda p: p.finished, patients))
    n_finished = len(patients_finished)
    mean_blocking_time = hospital.time_operation_theatre_blocked / n_finished
    mean_queue_at_entrance = numpy.mean(hospital.queues_at_entrance)
    utilization_rate_of_operation_theatre = hospital.total_time_operating / settings.SIM_TIME

    total_throughput_time = sum([p.end_time - p.start_time for p in patients_finished])
    
    # Display the autocorrelation plot of entrance queue
    
    
    #patients_json = list(map(lambda x: x.to_dict(), patients))

    #"patients": patients_json,
    return {
        "mean_blocking_time": mean_blocking_time,
        "mean_queue_at_entrance": mean_queue_at_entrance,
        "utilization_rate_of_operation_theatre": utilization_rate_of_operation_theatre,
        "total_throughput_time": total_throughput_time,
        "entrance_queue_timeseries": hospital.queues_at_entrance
    }

def run_experiment(config, n_samples, independence, random_seeds):
    """
    Run clinic simulation with one configuration n_samples times
    each with their own random_seed if not independence  
    Returns:
        [dict()] data gathered from each of the samples
    """
    samples = []
    for sample_i in range(n_samples):
        if not independence:
            random.seed(random_seeds[sample_i])
        env = simpy.Environment()

        n_prep = config["n_preparation_rooms"]
        n_rec = config["n_recovery_rooms"]
        prep_s = config["preparation_time_random_stream"]
        rec_s = config["recovery_time_random_stream"]
        inter_s = config["interarrival_time_random_stream"]
        cancelling_prob = config["cancelling_prob"]
        
        hospital = Hospital(env, n_prep, n_rec, prep_s, rec_s, inter_s, cancelling_prob)

        env.run(until=settings.WARM_UP_TIME + settings.SIM_TIME)
        sample_data = get_data(hospital)
        samples.append(sample_data)

    return samples

def run_simulation(independence):
    #list(list(dict()))
    data = []
    if independence:
        random.seed(42)

    for config in settings.CONFIGURATIONS:
        samples = run_experiment(config, settings.N_SAMPLES, independence, random_seeds)
        data.append(samples)
    statistics.calculate_and_print_statistics(data)

    twist_test_data = []

    # Test twisted version againt original version
    print("RESULTS FOR TESTING TWIST")
    print("-" * 20)
    for config in settings.CONFIGURATIONS_FOR_TESTING_TWIST:
        samples = run_experiment(config, settings.N_SAMPLES, independence, random_seeds)
        twist_test_data.append(samples)
    statistics.calculate_and_print_statistics(twist_test_data)

    #save to file
    #with open("data.json", mode="w", encoding="utf-8") as f:
    #    json.dump(data, f, indent=4)


if __name__ == "__main__":
    #random.seed(settings.RANDOM_SEED)
    random_seeds = [*range(settings.N_SAMPLES)]

    print("AUTOCORRELATION ANALYSIS")
    samples = run_experiment(settings.CONFIGURATIONS[0], 10, True, None)
    statistics.acf_plots(samples)

    print("SIMULATION FOR INDEPENDENT SAMPLES")
    print("-"*40)
    run_simulation(True)
    print("SIMULATION FOR DEPENDENT SAMPLES")
    print("-"*40)
    run_simulation(False)

    regression.experiment()