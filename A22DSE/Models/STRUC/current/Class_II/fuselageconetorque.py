# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:20:28 2019

@author: tomhu
"""

import math as m
import numpy as np

#import os
#from pathlib import Path
#os.chdir(Path(__file__).parents[5])
#
#from A22DSE.Parameters.Par_Class_Conventional import Conv
#


def GetJ(do,di):
    """Gets the torsional stiffness"""
    J = m.pi*(do**4-di**4)/32
    return J

def GetSigma(T,do,di):
    sigma = T*do/2/GetJ(do,di)
    return sigma

def GetStressShear(t,do,V,A):
    sigma = (2+ t / do*2)*V/A
    return sigma




def Get_t(Aircraft, do):
    """ INPUT: do which is the outer diameter"""
#    anfp = Aircraft.ParAnFP
#    struc = Aircraft.ParStruc
#    prop = Aircraft.ParProp
    layout = Aircraft.ParLayoutConfig
    t  = np.linspace(0.1,50) * 10**-3
    di = do - 2*t
    T = layout.bv*2/3 * 0.5 * 1.225 * 150**2 * 1.2 * layout.Svt  #Nm
    V = 0.5 * 1.225 * 150**2 * 1.2 * layout.Svt  #N
    A = m.pi * (do/2)**2
    sigma = GetSigma(T,do,di) + GetStressShear(t,do,V,A)
    sigmay = 207 * 10**6 #for al 7075 t6
    return(min(t[np.where(sigma<sigmay)]))
