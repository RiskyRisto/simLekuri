# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:38:32 2020

@author: Mika Sipilä
"""

import random

def bool_with_probability(probability):
    random_prob = random.uniform(0,1)
    if random_prob <= probability:
        return True
    return False        

def exp(mean):
    """
    Returns a function that generates exponentially distributed values with given mean
    """
    a = 1.0 / mean
    def exp_f():
        return random.expovariate(a)

    return exp_f

def unif(a,b):
    """
    Returns a function that generates uniformly distributed values with between a and b
    """
    def uniff():
        return random.uniform(a,b)

    return uniff
