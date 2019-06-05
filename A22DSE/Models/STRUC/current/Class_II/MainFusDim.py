# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:33:19 2019

@author: hksam
"""

import sys
sys.path.append('../../../../../')
import numpy as np
#from FuselageLength import GetTotalLength
from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (
        GetFuselageLength, GetCabinLength)

def GetTotalFuselageLength(Aircraft, fineness_f, fineness_n,
                           fineness_t, L_freq, SF0, dSF):
#fineness_f = 12
#fineness_n = 1.25
#fineness_t = 2.0
#l_freq     = 24.

    SFi = SF0
    
    L_fi = np.sum(GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                                fineness_t, SFi, L_freq))
    dSFi = dSF

    while L_fi < L_freq:
        SFi += dSFi
        L_fi = np.sum(GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                                fineness_t, SFi, L_freq))
        
    L_req = GetFuselageLength(Aircraft, fineness_f, fineness_n,
                                     fineness_t, SFi, L_freq)
    D_eq, dim_cabin = GetCabinLength(Aircraft, fineness_f, SFi)[1:]
    
    return L_req, D_eq, dim_cabin

a = GetTotalFuselageLength(Conv, 8, 2, 2, 24, 1, 0.1)

    