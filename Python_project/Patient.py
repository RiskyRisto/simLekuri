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
        #random.gammavariate(PREPARATION_ALPHA, PREPARATION_BETA)
        #random.gammavariate(OPERATION_ALPHA, OPERATION_BETA)
        #random.gammavariate(RECOVERY_ALPHA, RECOVERY_BETA)
        self.preparation_time = random.expovariate(PREPARATION_LAMBDA) 
        self.operation_time = random.expovariate(OPERATION_LAMBDA) 
        self.recovery_time = random.expovariate(RECOVERY_LAMBDA) 
        self.severe = bool_with_probability(SEVERE_PATIENT_PROBABILITY)
        self.operation_cancelled = bool_with_probability(CANCELLING_PROBABILITY)
        #Random time of preparation when new information is found and operation is cancelled
        self.operation_cancelled_time = random.uniform(0, self.preparation_time) 
        self.start_time = self.env.now
        self.time_operation_done = None
        self.time_recovery_start = None
        self.end_time = None
        self.process = env.process(self.preparation())

        self.finished = False
        
    def preparation(self):
        # start queing if there is no free preparation available
        preparation_request = self.hospital.preparation.request() 
        yield preparation_request
        # with probability of CANCELLING_PROBABILITY operation is cancelled during preparation
        if self.operation_cancelled: 
            yield self.env.timeout(self.operation_cancelled_time)
            self.hospital.preparation.release(preparation_request)
        else:
            # for calculating average queue at entrance
            self.hospital.total_queue_at_entrance += len(self.hospital.preparation.queue) 
            yield self.env.timeout(self.preparation_time)
            # free the preparation room
            self.process = self.env.process(self.operation(preparation_request)) 
    
    def operation(self, preparation_request):
        # start queing if the operation theatre is not free
        operation_request = self.hospital.operation_room.request() 
        yield operation_request
        # free the preparation room
        self.hospital.preparation.release(preparation_request) 
        yield self.env.timeout(self.operation_time)
        # for calculation utilization rate
        self.hospital.total_time_operating += self.operation_time 
        self.time_operation_done = self.env.now
        # start queing if there is no space in recovery
        self.process = self.env.process(self.recovery(operation_request)) 
        
    def recovery(self, operation_request):
        with self.hospital.recovery.request() as recovery_request:
            yield recovery_request
            # free the operation theatre
            self.hospital.operation_room.release(operation_request) 
            self.time_recovery_start = self.env.now
            yield self.env.timeout(self.recovery_time)
        self.end_time = self.env.now

        self.finished = True
        #self.hospital.patients_finished.append(self)
        # for calculating average blocked time
        self.hospital.time_operation_theatre_blocked += (self.time_recovery_start - self.time_operation_done) 
        #print("Time spent in process: %6.3f" % (self.end_time - self.start_time))
