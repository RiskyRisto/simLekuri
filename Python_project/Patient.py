# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:59:58 2020

@author: Mika Sipilä
"""

import random;
import simpy;
from settings import *;
from helpers import *;

class Patient():
    
    def __init__(self, env, hospital):
        self.hospital = hospital
        self.env = env
        self.preparation_time = random.expovariate(PREPARATION_LAMBDA) #random.gammavariate(PREPARATION_ALPHA, PREPARATION_BETA)
        self.severe = bool_with_probability(SEVERE_PATIENT_PROBABILITY)
        self.operation_time = random.expovariate(OPERATION_LAMBDA) #random.gammavariate(OPERATION_ALPHA, OPERATION_BETA)
        self.recovery_time = random.expovariate(RECOVERY_LAMBDA) #random.gammavariate(RECOVERY_ALPHA, RECOVERY_BETA)
        self.start_time = self.env.now
        self.time_operation_done = None
        self.time_recovery_start = None
        self.end_time = None
        self.process = env.process(self.preparation())
        
    def preparation(self):
        preparation_request = self.hospital.preparation.request()
        yield preparation_request
        self.hospital.total_queue_at_entrance += len(self.hospital.preparation.queue)
        yield self.env.timeout(self.preparation_time)
        self.process = self.env.process(self.operation(preparation_request))
    
    def operation(self, preparation_request):
        operation_request = self.hospital.operation_room.request()
        yield operation_request
        self.hospital.preparation.release(preparation_request)
        yield self.env.timeout(self.operation_time)
        self.hospital.total_time_operating += self.operation_time
        self.time_operation_done = self.env.now
        self.process = self.env.process(self.recovery(operation_request))
        
    def recovery(self, operation_request):
        with self.hospital.recovery.request() as recovery_request:
            yield recovery_request
            self.hospital.operation_room.release(operation_request)
            self.time_recovery_start = self.env.now
            yield self.env.timeout(self.recovery_time)
        self.end_time = self.env.now
        self.hospital.patients_finished.append(self)
        self.hospital.time_operation_theatre_blocked += (self.time_recovery_start - self.time_operation_done)
        print("Time spent in process: %6.3f" % (self.end_time - self.start_time))
        
        
        
        
            
        