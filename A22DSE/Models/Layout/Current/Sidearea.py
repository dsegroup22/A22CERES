# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:54:24 2019

@author: menno
"""
import numpy as np


def Area(Aircraft):

    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    
    l_nose=config.l_nose
    l_cabin=config.l_cabin
    l_tail=config.l_tail
    
    h_fuselage=config.h_fuselage
    d_cockpit=config.d_cockpit
    
    h_APU=config.h_APU
    
    Svt=config.Svt
    
    A_nose=np.pi*d_cockpit/4*l_nose #elliptical nose cone
    A_cabin=l_cabin*h_fuselage
    A_tail=(h_fuselage+h_APU)/2*l_tail
    
    return sum([Svt,A_nose,A_cabin,A_tail])
    
    