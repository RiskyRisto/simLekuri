# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:07:49 2020

@author: Mika Sipilä
"""

import simpy;
import random;
from settings import *;
from Hospital import Hospital;

#random.seed(RANDOM_SEED)
env = simpy.Environment()
hospital = Hospital(env)
env.run(until=SIM_TIME)

print("Patients came: %7.0f" % (len(hospital.patients)))
print("Patients got treated: %7.0f" % (len(hospital.patients_finished)))
print("Average time operation theatre was blocked: %7.3f" % (hospital.time_operation_theatre_blocked / len(hospital.patients_finished)))
print("Average queue at entrance: %7.3f" % (hospital.total_queue_at_entrance / len(hospital.patients)))
print("Utilization rate of operation theatre: %7.3f" % (hospital.total_time_operating / SIM_TIME))