# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:16:07 2019

@author: kamph
"""

import numpy as np
from math import *


## Functions ##
#Relief factors

def R_wg(Aircraft):
    #Determines wing relief factor due to structure, can be more precies by
    #using exact y locations of wing group and CoP
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    MTOW = struc.MTOW
    W_w = struc.Wing_weight #Dummy change functions in diff_configs
    #y_wg
    #y_cp  
    return W_w/MTOW

def R_en(Aircraft):
    #Determines engine relief factor 
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    x_eng = config.x_engine
    x_cp = config.x_CoP
    MTOW = struc.MTOW
    W_eng = config.m_engine
    return 3 * (x_eng**2 / x_cp) * (W_eng / MTOW)

def R_f(Aircraft):
    #Determines fuel relief factor, for layout it is necessary that inner
    #bulkhead coincides with wing root
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    b_f = config.b_fueltank
    b = anfp.b
    taper = anfp.taper
    MTOW = struc.MTOW
    MZF = MTOW - struc.FW
    return 0.5 * (b_f/b) * (1 + (3 * taper**2)/(1 + 2*taper)) * (1 - MZF/MTOW)
    