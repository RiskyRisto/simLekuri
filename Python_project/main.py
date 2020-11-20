# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:07:49 2020

@author: Mika Sipilä
"""

import simpy;
import random;
from settings import *;
from Hospital import Hospital;

if __name__ == "__main__":
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    hospital = Hospital(env)
    env.run(until=SIM_TIME)

    patients = hospital.patients

    patients_finished = list(filter(lambda p: p.finished, patients))
    n_finished = len(patients_finished)
    n_patients = len(patients)
    mean_blocking_time = hospital.time_operation_theatre_blocked / n_finished
    mean_queue_at_entrance = hospital.total_queue_at_entrance / n_patients
    utilization_rate_of_operation_theatre = hospital.total_time_operating / SIM_TIME

    print("Patients came: ", n_patients)
    print("Patients got treated: ", n_finished)
    print("Average time operation theatre was blocked: %.3f" % mean_blocking_time)
    print("Average queue at entrance: %.3f" % mean_queue_at_entrance)
    print("Utilization rate of operation theatre: %.3f" % utilization_rate_of_operation_theatre)

    total_throughput_time = sum([p.end_time - p.start_time for p in patients_finished])
    print("Total throughput time %.3f" % (total_throughput_time))
    print("Average throughput time %.3f" % (total_throughput_time / n_patients))