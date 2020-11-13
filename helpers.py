# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:38:32 2020

@author: Mika Sipilä
"""

import random

def bool_with_probability(probability):
    random_prob = random.uniform(0,1)
    if random_prob >= probability:
        return True
    return False        