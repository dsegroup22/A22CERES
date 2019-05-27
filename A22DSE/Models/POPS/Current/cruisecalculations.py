# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:57:33 2019

@author: rickv
"""

def CruiseRange(Aircraft):
    payl = Aircraft.ParPayload
    m_payload = payl.m_payload
    dispersionrate = payl.dispersionrate
    #function that calculates the cruise range
        
    return m_payload/dispersionrate #cruise range [m]

def CruiseTime(Aircraft, ISA_model):
    import numpy as np
    #function that calculates the cruise time
    h = Aircraft.ParAnFP.h_cruise
    a = np.sqrt(ISA_model.gamma*ISA_model.R* \
                ISA_model.ISAFunc([h])[0])
    return Aircraft.ParAnFP.s_cruise/(Aircraft.ParAnFP.M_cruise*a)

