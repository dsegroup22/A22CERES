# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:02:37 2019

@author: kamph
"""

import os
import sys
import numpy as np

def LG_loads(Aircraft):
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    MTOW = struc.MTOW
    F = config.lg_x_main - config.lg_x_nose
    M = config.lg_x_main - config.x_cg[1]
    L = config.x_cg[0] - config.lg_x_nose
    N = config.x_cg[1] - config.lg_x_nose
    J = config.z_cg[0]
    
    max_static_main =  ((MTOW*(F-M))/(2*F)) * 2.20462
    max_static_nose = ((MTOW*(F-L))/F) * 2.20462
    min_static_nose = ((MTOW*(F-N))/F) * 2.20462
    max_braking_load = max_static_nose + ((10*J*MTOW*2.20462*0.3048**2)/(32.2*F*0.3048))*0,45359
    
    return max_static_main, max_static_nose, min_static_nose, max_braking_load

