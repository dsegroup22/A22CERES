# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:49:03 2019

@author: rickv
"""
import numpy as np

def wing_sweep(Aircraft):
    M_crit=0.935
    M_dd=Aircraft.ParAnFP.Mdd
    tc=Aircraft.ParAnFP.tc
    cossweep=3/8*M_crit/M_dd*(1+np.sqrt(1-32*tc*M_dd/9/M_crit/M_crit))
    sweep=np.arccos(cossweep)
    
    return sweep
