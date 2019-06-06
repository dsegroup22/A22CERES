# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:49:11 2019

@author: menno
"""

import numpy as np


def sweep(knownsweep,knownstation,neededstation,aspectratio,taperratio):
    #input sweep in radians and stations in fractions
    #output sweep at wanted station in radians
    return(np.arctan(np.tan(knownsweep)-4/aspectratio*((neededstation-knownstation)\
                                      *(1-taperratio)/(1+taperratio))))


def C_L_CurveCruise(Aircraft):
    #raymer method from airfoil & planform data to wing lift curve during cruise
    #input configuration
    #output at cruise Mach number
    #output in radians where applicable
    anfp = Aircraft.ParAnFP
    layout = Aircraft.ParLayoutConfig
    
    eta=anfp.eta_airfoil
    C_l_max=anfp.cl_max
    alpha_0=anfp.alpha_0
    delta_alpha_C_L_max=anfp.delta_alpha_C_L_max
    C_L_to_C_l=anfp.C_L_to_C_l
    delta_C_L_max=anfp.delta_C_L_max_cruise
    M_cruise=anfp.M_cruise
    A=anfp.A
    taperratio=anfp.taper
    sweep25=anfp.Sweep_25
    S=anfp.S
    c_r=anfp.c_r
    d_fuselage=layout.d_fuselage
    b=anfp.b
    max_t_loc=anfp.max_t_loc
    
    S_exposed=S-d_fuselage*c_r
    sweep_max_t=sweep(sweep25,0.25,max_t_loc,A,taperratio)
    
    C_L_max=C_l_max*C_L_to_C_l+delta_C_L_max
    
    
    beta=np.sqrt(1-M_cruise**2)
    F=1.07*(1+d_fuselage/b)**2
    C_L_alpha=2*np.pi*A/(2+np.sqrt(4+(A*beta/eta)**2*(1+(np.tan(sweep_max_t)/beta)**2)))*(S_exposed/S)*F
    
    alpha_stall=C_L_max/C_L_alpha+alpha_0+delta_alpha_C_L_max
    return (alpha_0,C_L_alpha,C_L_max,alpha_stall)

def C_L_CurveLowSpeed(Aircraft):
    #raymer method from airfoil & planform data to wing lift curve @ Mach=0.2
    #input configuration
    #output @ Mach=0.2
    #output in radians where applicable
    anfp = Aircraft.ParAnFP
    layout = Aircraft.ParLayoutConfig
    
    eta=anfp.eta_airfoil
    C_l_max=anfp.cl_max
    alpha_0=anfp.alpha_0
    delta_alpha_C_L_max=anfp.delta_alpha_C_L_max
    C_L_to_C_l=anfp.C_L_to_C_l
    delta_C_L_max=anfp.delta_C_L_max_lowspeed
    M_cruise=0.2
    A=anfp.A
    taperratio=anfp.taper
    sweep25=anfp.Sweep_25
    S=anfp.S
    c_r=anfp.c_r
    d_fuselage=layout.d_fuselage
    b=anfp.b
    max_t_loc=anfp.max_t_loc
    
    S_exposed=S-d_fuselage*c_r
    sweep_max_t=sweep(sweep25,0.25,max_t_loc,A,taperratio)
    
    C_L_max=C_l_max*C_L_to_C_l+delta_C_L_max
    
    
    beta=np.sqrt(1-M_cruise**2)
    F=1.07*(1+d_fuselage/b)**2
    C_L_alpha=2*np.pi*A/(2+np.sqrt(4+(A*beta/eta)**2*(1+(np.tan(sweep_max_t)/beta)**2)))*(S_exposed/S)*F
    
    alpha_stall=C_L_max/C_L_alpha+alpha_0+delta_alpha_C_L_max
    return (alpha_0,C_L_alpha,C_L_max,alpha_stall)