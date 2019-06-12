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

#from A22DSE.Parameters.Par_Class_Conventional import Conv

#anfp = Conv.ParAnFP
#struc = Conv.ParStruc
#prop = Conv.ParProp

def GetJ(do,di):
    J = m.pi*(do**4-di**4)/32
    return J

def GetSigma(T,do,di):
    sigma = T*do/2/GetJ(do,di)
    return sigma

def GetStressShear(t,do,V,A):
    sigma = (2+ t / do*2)*V/A
    return sigma



do = 750 * 10**-3 #m
t  = np.linspace(0.1,20) * 10**-3
di = do - 2*t
T = 5 * 0.5 * 1.225 * 150**2 * 1.2 * 30  #Nm
V = 0.5 * 1.225 * 150**2 * 1.2 * 30  #N
A = m.pi * (do/2)**2
sigma = GetSigma(T,do,di) + GetStressShear(t,do,V,A)
sigmay = 331 * 10**6
print(min(t[np.where(sigma<sigmay)]))
