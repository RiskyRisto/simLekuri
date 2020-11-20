# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:07:49 2020

@author: Mika Sipilä
"""

import simpy
import random;
import settings
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

    patients_json = list(map(lambda x: x.to_dict(), patients))

    #"patients": patients_json,
    return {
        "mean_blocking_time": mean_blocking_time,
        "mean_queue_at_entrance": mean_queue_at_entrance,
        "utilization_rate_of_operation_theatre": utilization_rate_of_operation_theatre,
        "total_throughput_time": total_throughput_time
    }



if __name__ == "__main__":
    random.seed(settings.RANDOM_SEED)

    #3d matrix: hospital, sample, {}
    data = []

    for config in settings.CONFIGURATIONS:
        samples = []
        for sample_i in range(settings.N_SAMPLES):
            env = simpy.Environment()

            hospital = Hospital(env, config["n_preparation_rooms"], config["n_recovery_rooms"])

            env.run(until=settings.SIM_TIME)

            sample_data = get_data(hospital)

            samples.append(sample_data)
        
        data.append(samples)

    #save to file
    with open("data.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
