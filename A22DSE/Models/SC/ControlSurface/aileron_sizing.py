# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:16:32 2019

@author: lujingyi
"""
from math import pi
#y_aileron

def aileron(Aircraft):
    b = Aircraft.ParAnFP.b
    b1 = b/2*0.65
    b2 = b/2*0.88
    cl_delta_a = 3 #per rad !!!!!!!
    c_r = Aircraft.ParAnFP.c_r
    S = Aircraft.ParAnFP.S
    tr = Aircraft.ParAnFP.taper
    chord_ratio = 0.2
    tau = 0.41
    Cl_delta_a = 2*tau*cl_delta_a*c_r/(S*b)*((b2**2-b1**2)+2*(tr-1)/(3*b)*(b2**3-b1**3))
    cl_a = Aircraft.ParAnFP.cl_alpha*180/pi
    cd0 = Aircraft.ParAnFP.Cd0
    Cl_p = -(cl_a+cd0)*c_r*b*(1+3*tr)/24/S
    delta = 15
    roll = -Cl_delta_a/Cl_p*delta*pi/180
    
    Aircraft.ParLayoutConfig.y_aileron = b1
    Aircraft.ParLayoutConfig.y_aileron_end = b2
    