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
        self.preparation_time = random.gammavariate(PREPARATION_ALPHA, PREPARATION_BETA)
        self.severe = bool_with_probability(SEVERE_PATIENT_PROBABILITY)
        self.operation_time = random.gammavariate(OPERATION_ALPHA, OPERATION_BETA)
        self.recovery_time = random.gammavariate(RECOVERY_ALPHA, RECOVERY_BETA)
        self.start_time = self.env.now
        self.time_operation_done = None
        self.time_recovery_start = None
        self.end_time = None
        self.process = env.process(self.preparation())
        
    def preparation(self):
        with self.hospital.preparation.request() as preparation_turn:
            yield preparation_turn
            yield self.env.timeout(self.preparation_time)
            self.process = self.env.process(self.operation())
    
    def operation(self):
        with self.hospital.operation_room.request() as operation_turn:
            yield operation_turn
            yield self.env.timeout(self.operation_time)
            self.process = self.env.process(self.recovery())
        
    def recovery(self):
        with self.hospital.recovery.request() as recovery_turn:
            yield recovery_turn
            yield self.env.timeout(self.recovery_time)
        self.end_time = self.env.now
        self.hospital.patients_finished.append(self)
        print("Time spent in process: %6.3f" % (self.end_time - self.start_time))
        
        
        
        
            
        
