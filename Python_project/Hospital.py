# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:32:41 2020

@author: Mika Sipilä
"""

import random;
import settings
from Patient import Patient;
import simpy
import helpers

class Hospital:
    """
    Params:
        env: simpy.Environment object
        n_prep: number of preparation room slots
        n_rec: number of recovery room slots
        prep_s: function to generate random preparation times
        rec_s: function to generate random recovery times
        inter_s: function to generate random interarrival times
        cancelling_prop: probability that operation gets cancelled during preparation
    """
    def __init__(self, env, n_prep, n_rec, prep_s, rec_s, inter_s, cancelling_prob):
        self.env = env
        self.patients = []
        #self.patients_finished = []
        #self.preparation = simpy.Resource(env, N_PREPARATION_ROOMS)
        self.preparation = simpy.Resource(env, n_prep)
        self.operation_room = simpy.Resource(env, 1)
        #self.recovery = simpy.Resource(env, N_RECOVERY_ROOMS)
        self.recovery = simpy.Resource(env, n_rec)
        self.time_operation_theatre_blocked = 0
        self.queues_at_entrance = []
        self.total_time_operating = 0
        self.cancelling_prob = cancelling_prob

        #constant here
        self.operation_time_stream = helpers.exp(20)

        self.preparation_time_stream = prep_s
        self.recovery_time_stream = rec_s
        self.interarrivaltime_stream = inter_s

        self.process = self.env.process(self.run())
        env.process(self.entrance_queue_ac())
    
    def run(self):
        while True:
            #next_patient_time = random.expovariate(settings.NEW_PATIENT_LAMBDA)
            next_patient_time = self.interarrivaltime_stream()
            yield self.env.timeout(next_patient_time)
            self.generate_patient()
            
    def generate_patient(self):
        preparation_time = self.preparation_time_stream()
        operation_time = self.operation_time_stream()
        recovery_time = self.recovery_time_stream()
        patient = Patient(self.env, self, preparation_time, operation_time, recovery_time)
        self.patients.append(patient)

    def entrance_queue_ac(self):
        while True:
            self.queues_at_entrance.append(len(self.preparation.queue))
            yield self.env.timeout(10)
        