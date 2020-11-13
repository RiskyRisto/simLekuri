# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:02:36 2020

@author: Mika Sipilä
"""

RANDOM_SEED = 42
N_PREPARATION_ROOMS = 3
N_OPERATION_ROOMS = 1
N_RECOVERY_ROOMS = 3
PREPARATION_ALPHA = 240.0
PREPARATION_BETA = 1/6.0
OPERATION_ALPHA = 120 
OPERATION_BETA = 1/6.0
RECOVERY_ALPHA = 240.0 
RECOVERY_BETA = 1/6.0
MEAN_NEW_PATIENT = 45.0
NEW_PATIENT_LAMBDA = 1 / MEAN_NEW_PATIENT  # Param. for expovariate distribution
SEVERE_PATIENT_PROBABILITY = 0.3
WEEKS = 12             # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes