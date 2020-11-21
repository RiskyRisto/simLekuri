# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:02:36 2020

@author: Mika Sipilä
"""

RANDOM_SEED = 42
N_PREPARATION_ROOMS = 3
N_OPERATION_ROOMS = 1
N_RECOVERY_ROOMS = 3
#PREPARATION_ALPHA = 240.0
#PREPARATION_BETA = 1/6.0
PREPARATION_LAMBDA = 1 / 40.0
OPERATION_LAMBDA = 1 / 20.0
RECOVERY_LAMBDA = 1 / 40.0
#OPERATION_ALPHA = 120.0 
#OPERATION_BETA = 1/6.0
#RECOVERY_ALPHA = 480.0
#RECOVERY_BETA = 1/6.0
MEAN_NEW_PATIENT = 25.0
NEW_PATIENT_LAMBDA = 1 / MEAN_NEW_PATIENT  # Param. for expovariate distribution
#TODO: use this
SEVERE_PATIENT_PROBABILITY = 0.3
CANCELLING_PROBABILITY = 0.1
#WEEKS = 12             # Simulation time in weeks
#SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes
SIM_TIME = 1000
N_SAMPLES = 20

CONFIGURATIONS = [
    {
        "n_preparation_rooms": 3,
        "n_recovery_rooms": 4
    },
    {
        "n_preparation_rooms": 3,
        "n_recovery_rooms": 5
    },
    {
        "n_preparation_rooms": 4,
        "n_recovery_rooms": 5
    }
]
