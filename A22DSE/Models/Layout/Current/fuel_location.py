# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:32:18 2019

@author: AtiqahTarmizi
"""
import numpy as np
from math import sqrt

def fuel_loc(Conv):
    
    rho_fuel = 804 #[kg/m3] #fuel density at 15degCelcius - must change to density of actual fuel
    fuel_mass = Conv.ParStruc.FW
    fuel_vol = fuel_mass / rho_fuel
    #fuel_vol = fuel_l * 0.00378541 / 3.785
    
    #assumption that front spar = 0.25 c
    #assumption that rear spar = 0.75 c
    Sw = Conv.ParAnFP.S
    Cr = Conv.ParAnFP.c_r
    Ct = Conv.ParAnFP.c_t
    half_span = Conv.ParAnFP.b / 2
    MAC = Conv.ParAnFP.MAC
    tc = 0.12 * MAC
    taper = Conv.ParAnFP.taper
    
#    l_s1 = 0.75*Cr - 0.25*Cr
#    l_s2 = 0.75*MAC - 0.25*MAC
#    l = Conv.ParAnFP.y_MAC
    
    #alpha = l/4 * (l_s1+3*l_s2+2*sqrt(l_s1*l_s2))/(l_s1+l_s2+sqrt(l_s1*l_s2))
    
    #cg_loc_fuel = alpha*Conv.ParAnFP.y_MAC
    
    #y = np.arange(0,int(half_span),0.5)
    #cy = 2*Sw/((1+taper)*half_span) *(1-((1-taper)/half_span)*y)
    
    wing_vol = 0.8*(Cr+Ct)*half_span*tc
    
    wing_1 = fuel_vol / 2
    #can have main tanks extends to half of half-span
    
    
    return half_span, Ct, taper, Cr, half_span


    
