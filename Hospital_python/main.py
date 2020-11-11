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
