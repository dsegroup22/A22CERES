# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:06:59 2019

@author: kamph
"""
import numpy as np
from math import *
import sys
sys.path.append('../')


#Determine CD0

def S_wet_wing(Aircraft):
    #INPUT: thickness to chord ratio of the wing, taper ratio, surface area and A
    #OUTPUT: wetted wing area
    
    anfp = Aircraft.ParAnFP
    tc_w = anfp.tc
    taper =  anfp.taper
    S_w = anfp.S
    A = anfp.A
    
    kq = 0.95
    Q_w = ( (kq * tc_w) / sqrt(1. + taper) ) * S_w * sqrt(S_w / A)
    S_wet = (2 + 0.5 * tc_w) * ((Q_w * sqrt(A + A* taper)) / (kq * tc_w) )**(2./3.)
    return S_wet

def S_wet_fuselage(Aircraft):
    #INPUT: length fuselage, mean! diameter fuselage
    #OUTPUT: Wetted area of the fuselage
    
    Config = Aircraft.ParLayoutConfig
    l_fus = Config.l_fuselage
    d_fus = Config.d_fuselage
    fineness = l_fus/d_fus
    
    S_fus_front = pi/4. * d_fus**2
    Q_fus = (pi/4.) * d_fus**2 * l_fus * ( 1. - 2./ fineness)
    S_fus_around = pi*d_fus*(l_fus - 1.3*d_fus)
    return S_fus_front + S_fus_around

def S_wet_tail(Aircraft):
    #INPUT: Horizontal and vertical tail area
    #OUTPUT: Wetted tail area
    Config = Aircraft.ParLayoutConfig
    S_h = Config.Sht
    S_v = Config.Svt
    
    return S_h + S_v

def S_wet_engine(Aircraft):
    anfp = Aircraft.ParAnFP
    N_eng = Aircraft.ParStruc.N_engines
    T_to = 139.4 #Check with Vomas
    S_ref = 25
    T_ref = 100
    B = 4.6 #Check with Vomas
    
    
    S_nac = 0.8*S_ref*N_eng*(1+B)**0.2*(T_to/T_ref + 0.25)
    return 1.2*S_nac #add 20% for pylons

def friction_coef(Aircraft):
    #INPUT: V_cruise, atmospheric conditions, span, wetted area
    #OUTPUT: friction coefficient
    anfp = Aircraft.ParAnFP
    V = anfp.V_cruise #Cruise speed
    b = anfp.b #Span
    
    mu = 1.43226e-5 #dynamic friction
    rho = 0.0880349 #density
    nu = mu / rho #kinematic friction
    
    S_wet = S_wet_wing(Aircraft) + S_wet_fuselage(Aircraft) + \
    S_wet_tail(Aircraft) + S_wet_engine(Aircraft)
    
    Re = (S_wet / b) * V / nu
    C_fe = 0.00258 + 0.00102*np.exp(-6.28e-9 * Re) + 0.00295*np.exp(-2.01e-8*\
                                   Re)
    return C_fe, S_wet

def CD0(Aircraft):
    #INPUT: 
    
    anfp = Aircraft.ParAnFP
    S = anfp.S
    C_fe = friction_coef(Aircraft)[0]
    S_wet = friction_coef(Aircraft)[1]
    CD0_ac = C_fe * (S_wet/S)
    CD0_wing = C_fe *(S_wet_wing(Aircraft)/S)
    return CD0_ac, CD0_wing
    