# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:32:41 2020

@author: Mika Sipilä
"""

import random;
from settings import *;
from Patient import *;

def time_to_next_patient():
    return random.expovariate(NEW_PATIENT_LAMBDA)

class Hospital:
    
    def __init__(self, env):
        self.env = env
        self.patients = []
        self.patients_finished = []
        self.preparation = simpy.Resource(env, N_PREPARATION_ROOMS)
        self.operation_room = simpy.Resource(env, 1)
        self.recovery = simpy.Resource(env, N_RECOVERY_ROOMS)
        self.time_operation_theatre_blocked = 0
        self.total_queue_at_entrance = 0
        self.total_time_operating = 0
        self.process = self.env.process(self.run())
    
    def run(self):
        while True:
            next_patient_time = random.expovariate(NEW_PATIENT_LAMBDA)
            yield self.env.timeout(next_patient_time)
            self.generate_patient()
            
    def generate_patient(self):
        patient = Patient(self.env, self)
        self.patients.append(patient)
        
            
            
            