# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:26:38 2019

@author: Nikki Kamphuis
"""

import numpy as np
from math import pi, sqrt, exp,atan, tan, cos
import sys
sys.path.append('../')

                    
 #Still undefined variables                   
V_lf = 120.         #Landing speed, flap configuration in m/s
spoiler_brakes = 0  #Speed brakes or spoiler on (1) or off (0)
#HLD list
S_f = 20            #Projected flap area in m^2
d_f = 0.5           #Flap deflection in radians
b_fs = 10.          #Flap span in meters
sweep_f = 0.6       #Flap sweep in radians
flap_type = 1       #Flap type: 1 = single slotted/double slotted fixed hinge
                    #           2 = double slotted/ moving 4-bar/single slotted 
                    #               Fowler
                    #           3 = double slotted Fowler
                    #           4 = triple slotted Fowler
W_lef = 100         #Read from a plot in appendix C Torenbeek in kg
tc_f = 0.14         #Flap thickness to chord ratio
HLD = [S_f, d_f, b_fs, sweep_f, flap_type, W_lef, tc_f]


                    #####Functions#####

def Wing_Geo(Aircraft):
    #INPUT: Quarter chord sweep, aspect ratio, surface area
    #OUTPUT: geometry of the wing: sweep at different places in radians,
    #span, taper ratio, root chord, tip chord, MAC
    anfp = Aircraft.ParAnFP
    Sweep_50 = anfp.Sweep50
    AR = anfp.A
    S = anfp.S
    
    Sweep_50 = Sweep_50 * pi / 180.
    Taper = 0.45 * exp( -0.0375 * Sweep_50) 
    Sweep_25_rad = atan( tan(Sweep_50) + (4 / AR) * 0.25 \
                    * (1 - Taper) / (1 + Taper))
    Sweep_LE = atan( tan(Sweep_25_rad) - (4 / AR) * -0.25 \
                    * (1 - Taper) / ( 1 + Taper))
#    print(AR, S)
    b = sqrt(AR * S)
    c_r = (2 * S ) / (b * (1 + Taper) )
    c_t = Taper * c_r
    c_mac = (2./3.) * c_r * (1. + Taper + Taper**2.)/(1. + Taper)
    y_mac=b/6*((1+2*Taper)/(1+Taper))
    
    return [Sweep_25_rad, Sweep_LE, Sweep_50, b, Taper, c_r, c_t, c_mac, y_mac]



def Wing_Geo_Additional(Aircraft):
    """
    This function calculates additional geometric properties of the wing
    """
    layout = Aircraft.ParLayoutConfig
    afnp = Aircraft.ParAnFP
    
    #get parameters
    y_mac = afnp.y_MAC
    Sweep_LE = afnp.Sweep_LE
    #calculate new things
    x_LE_root = layout.x_lemac - y_mac*np.tan(Sweep_LE)
    
    return(x_LE_root)



def Basic_Wing(Aircraft): #geometry, wing_specs, FP
    #INPUT: General wing planform geometry, other specifications such 
    #as statistical weight and t/c, flight profile parameters
    #OUTPUT: Estimation of clean configuration wing weight in kg
    
    wing_fr = 0.3641                    #fraction of the wing weight 8,65%
    n_ult = 2.5                         #ultimate load factor
    
    geometry = Wing_Geo(Aircraft)       #Import wing geometry
    
    anfp = Aircraft.ParAnFP             #Short Cut
    struc = Aircraft.ParStruc           #Short Cut
    
    n_engines = struc.N_engines          #Amount of Wing Mounted Engines    
    wm_un = anfp.wm_un                  #Undercarriage in Fuselage or Wing
    MZF = struc.MTOW - struc.FW         #Zero Fuel Weight   
    tc_r = anfp.tc #
    w_w = wing_fr * struc.MTOW
    V_d= 1.4 * anfp.V_cruise
    
    #determine constants necessary for class II estimation
    b_s = geometry[3] / cos(geometry[2]) 
    k_no = 1 + sqrt(1.905 / b_s)
    k_taper = ( 1 + geometry[4] ) ** (0.4)
        
    #Account for engine relief
    if n_engines == 0:
        k_e = 1.
    elif n_engines == 2:
        k_e = 0.95
    else:
        k_e = 0.9
        
    #Account for undercarriage    
    if wm_un == 1:
        k_uc = 1.
    else:
        k_uc = 0.95
        
    #Account for flutter at high speeds    
    if n_engines == 4:
        k_st = 1.
    else:
        k_st = 1 + 9.06e-4 \
        * ( ((geometry[3] * cos(geometry[1]))**3.) / MZF) \
        * ((0.01 * V_d / tc_r)**2. ) \
        *cos(geometry[2])
        
    k_b = 1. #cantilevered wing
        
    W_basic = 4.58e-3 * k_no * k_taper * k_e * k_uc * k_st \
    * ((k_b * n_ult * (MZF - 0.8 * w_w )) ** (0.55)) \
    * (geometry[3] ** (1.675)) \
    * (tc_r ** (-0.45)) \
    * (cos(geometry[2]) ** (-1.325))
    return(W_basic)    
    #return W_basic

#def HLD_weight(HLD, FP):
##INPUT is list containing High lift devices specification and flight profile
##OUTPUT is weight of the high lift devices
#    
#    #determine constant
#    if HLD[4] == 1:
#        k_f = 1.
#    elif HLD[4] == 2:
#        k_f = 1.15
#    elif HLD[4] == 3:
#        k_f = 1.30
#    else:
#        k_f = 1.45
#    
#    #calculate TE flap weight
#    W_tef = HLD[0] * 2.706 * k_f * (HLD[0]*HLD[2]) ** (3./16.) \
#    * ((0.01*FP[2])**2. * sin(HLD[1]) * cos(HLD[3]) / HLD[6])**(3./4.)
#    
#    #Sum TE flap + LE flap weight        
#    W_hld = W_tef + HLD[5]
#    
#    return 0#W_hld
#    
#    
#
#def ClassII_Wing(Sweep_25, AR, S, wing_specs, FP, HLD):
#    
#    geometry = Wing_Geo(Sweep_25, AR, S) #import wing geometry
#    W_basic = Basic_Wing(geometry, wing_specs, FP)
#    W_hld = HLD_weight(HLD, FP)
#    
#    if wing_specs[5] == 1:
#        W_sp = 0.015 * wing_specs[4]
#    else:
#        W_sp = 0.
#    
#    Wing_group = W_basic + 1.2*(W_hld + W_sp)
#    
#    return Wing_group


    
    
    
    
    
        
    
    
    
        
        
        
        
    
    
    