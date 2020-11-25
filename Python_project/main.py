# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:07:49 2020

@author: Mika Sipilä
"""

import simpy
import random
import settings
import statistics
from Hospital import Hospital
import json

def printStatistics(hospital, sample_number, hospital_number):
    patients = hospital.patients

    patients_finished = list(filter(lambda p: p.finished, patients))
    n_finished = len(patients_finished)
    n_patients = len(patients)
    mean_blocking_time = hospital.time_operation_theatre_blocked / n_finished
    mean_queue_at_entrance = hospital.total_queue_at_entrance / n_patients
    utilization_rate_of_operation_theatre = hospital.total_time_operating / settings.SIM_TIME

    print("-" * 20)
    print("sample: ", sample_number)
    print("hospital: ", hospital_number)
    print("Patients came: ", n_patients)
    print("Patients got treated: ", n_finished)
    print("Average time operation theatre was blocked: %.3f" % mean_blocking_time)
    print("Average queue at entrance: %.3f" % mean_queue_at_entrance)
    print("Utilization rate of operation theatre: %.3f" % utilization_rate_of_operation_theatre)

    total_throughput_time = sum([p.end_time - p.start_time for p in patients_finished])
    print("Total throughput time %.3f" % (total_throughput_time))
    print("Average throughput time %.3f" % (total_throughput_time / n_patients))

    print("-" * 20)

def get_data(hospital):
    patients = hospital.patients

    patients_finished = list(filter(lambda p: p.finished, patients))
    n_finished = len(patients_finished)
    n_patients = len(patients)
    mean_blocking_time = hospital.time_operation_theatre_blocked / n_finished
    mean_queue_at_entrance = hospital.total_queue_at_entrance / n_patients
    utilization_rate_of_operation_theatre = hospital.total_time_operating / settings.SIM_TIME

    total_throughput_time = sum([p.end_time - p.start_time for p in patients_finished])

    #patients_json = list(map(lambda x: x.to_dict(), patients))

    #"patients": patients_json,
    return {
        "mean_blocking_time": mean_blocking_time,
        "mean_queue_at_entrance": mean_queue_at_entrance,
        "utilization_rate_of_operation_theatre": utilization_rate_of_operation_theatre,
        "total_throughput_time": total_throughput_time
    }

def run_simulation(independence):

    #3d matrix: hospital, sample, {}
    data = []
    if independence:
        random.seed(42)

    for config in settings.CONFIGURATIONS:
        samples = []
        for sample_i in range(settings.N_SAMPLES):
            if not independence:
                random.seed(random_seeds[sample_i])
            env = simpy.Environment()

            n_prep = config["n_preparation_rooms"]
            n_rec = config["n_recovery_rooms"]
            prep_s = config["preparation_time_random_stream"]
            rec_s = config["recovery_time_random_stream"]
            inter_s = config["interarrival_time_random_stream"]

            hospital = Hospital(env, n_prep, n_rec, prep_s, rec_s, inter_s, 0.1)

            env.run(until=settings.WARM_UP_TIME + settings.SIM_TIME)
            sample_data = get_data(hospital)
            samples.append(sample_data)
        data.append(samples)
    statistics.calculate_and_print_statistics(data)

    twist_test_data = []

    # Test twisted version againt original version
    print("RESULTS FOR TESTING TWIST")
    print("-" * 20)
    for config in settings.CONFIGURATIONS_FOR_TESTING_TWIST:
        samples = []
        for sample_i in range(settings.N_SAMPLES):
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
        twist_test_data.append(samples)
    statistics.calculate_and_print_statistics(twist_test_data)

    #save to file
    #with open("data.json", mode="w", encoding="utf-8") as f:
    #    json.dump(data, f, indent=4)


if __name__ == "__main__":
    #random.seed(settings.RANDOM_SEED)
    random_seeds = [*range(settings.N_SAMPLES)]

    print("SIMULATION FOR INDEPENDENT SAMPLES")
    print("-"*40)
    run_simulation(True)
    print("SIMULATION FOR DEPENDENT SAMPLES")
    print("-"*40)
    run_simulation(False)
