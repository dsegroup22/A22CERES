# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np
import scipy.integrate as integrate

def WingWeight(Aircraft):
    anfp=Aircraft.ParAnFP
    layout=Aircraft.ParLayoutConfig
    
    sweep_EA=anfp.Sweep_50
    