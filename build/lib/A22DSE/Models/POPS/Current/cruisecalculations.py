# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:57:33 2019

@author: rickv
"""
import sys
#sys.path.append('../../../../')

#from A22DSE.Parameters.Par_Class_All import ParPayloadLst
#from A22DSE.Parameters.Par_Class_Conv1 import conv


def CruiseRange(Aircraft):
    payl = Aircraft.ParPayload
    m_sulphur = payl.m_sulphur
    dispersionrate = payl.dispersionrate
    #function that calculates the cruise range
        
    return m_sulphur/dispersionrate #cruise range [m]

def CruiseTime(Aircraft, ISA_model):
    import numpy as np
    #function that calculates the cruise time
    h = Aircraft.ParAnFP.h_cruise
    a = np.sqrt(ISA_model.gamma*ISA_model.R* \
                ISA_model.ISAFunc([h])[0])
    return Aircraft.ParAnFP.s_cruise/(Aircraft.ParAnFP.M_cruise*a)

