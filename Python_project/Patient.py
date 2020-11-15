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
        self.operation_time = random.expovariate(OPERATION_LAMBDA) #random.gammavariate(OPERATION_ALPHA, OPERATION_BETA)
        self.recovery_time = random.expovariate(RECOVERY_LAMBDA) #random.gammavariate(RECOVERY_ALPHA, RECOVERY_BETA)
        self.severe = bool_with_probability(SEVERE_PATIENT_PROBABILITY)
        self.operation_cancelled = bool_with_probability(CANCELLING_PROBABILITY)
        self.operation_cancelled_time = random.uniform(0, self.preparation_time) #Random time of preparation when new information is found and operation is cancelled
        self.start_time = self.env.now
        self.time_operation_done = None
        self.time_recovery_start = None
        self.end_time = None
        self.process = env.process(self.preparation())
        
    def preparation(self):
        preparation_request = self.hospital.preparation.request() # start queing if there is no free preparation available
        yield preparation_request
        if self.operation_cancelled: # with probability of CANCELLING_PROBABILITY operation is cancelled during preparation
            yield self.env.timeout(self.operation_cancelled_time)
            self.hospital.preparation.release(preparation_request)
        else:
            self.hospital.total_queue_at_entrance += len(self.hospital.preparation.queue) # for calculating average queue at entrance
            yield self.env.timeout(self.preparation_time)
            self.process = self.env.process(self.operation(preparation_request)) # free the preparation room
    
    def operation(self, preparation_request):
        operation_request = self.hospital.operation_room.request() # start queing if the operation theatre is not free
        yield operation_request
        self.hospital.preparation.release(preparation_request) # free the preparation room
        yield self.env.timeout(self.operation_time)
        self.hospital.total_time_operating += self.operation_time # for calculation utilization rate
        self.time_operation_done = self.env.now
        self.process = self.env.process(self.recovery(operation_request)) # start queing if there is no space in recovery
        
    def recovery(self, operation_request):
        with self.hospital.recovery.request() as recovery_request:
            yield recovery_request
            self.hospital.operation_room.release(operation_request) # free the operation theatre
            self.time_recovery_start = self.env.now
            yield self.env.timeout(self.recovery_time)
        self.end_time = self.env.now
        self.hospital.patients_finished.append(self)
        self.hospital.time_operation_theatre_blocked += (self.time_recovery_start - self.time_operation_done) # for calculating average blocked time
        print("Time spent in process: %6.3f" % (self.end_time - self.start_time))
