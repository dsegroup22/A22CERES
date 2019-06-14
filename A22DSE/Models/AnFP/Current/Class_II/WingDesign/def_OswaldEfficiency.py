# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 13:44:57 2019

@author: Nout
"""
import numpy as np

def OswaldEfficiency(Conv):
    """
DESCRIPTION: This function calculates the Oswald efficiency factor, based on
the quarter cord sweep, aspect ratio, dihedral , fuselage interference, zero
lift drag, and mach number. All information is taken from 
https://www.fzt.haw-hamburg.de/pers/Scholz/OPerA/OPerA_PUB_DLRK_12-09-10.pdf
pg. 9-12.
There are 2 methods, method 1 is more accurate accordingt to the paper, this is
the one that i use.

INPUTS: Conv aircraft, all parameters mentioned above are used.
OUTPUTS: float e Oswald efficiency is added to the Conv object
    """
    #get shortcuts
    Layout = Conv.ParLayoutConfig
    anfp = Conv.ParAnFP

    
    #get relevant parameters from Conv
    taper = anfp.taper
    sweep_25 = anfp.Sweep_25
    A = anfp.A
    d_fus = Layout.d_fuselage
    b = anfp.b
    M_cruise = anfp.M_cruise
    CD0 = anfp.CD0
    dihedral = anfp.dhwing
    
    #determine coefficients specific for this code
    a_e = -0.001521 #from statistics, see p10
    b_e = 10.82 # same as above
    M_comp = 0.3 #[-] mach number above which compressibility happens
    K = 0.38 #coefficient for induced drag penalty method 1, based on Kroo, p9
    kwl = 2.13 #[-] coefficient for dihedral from Kroo, TAB4 p11
    
    #functions
    delta_taper = -0.357+0.45*np.exp(0.0375*sweep_25)
    taper = taper-delta_taper
    
    f = 0.0524*taper**4-0.15*taper**3+0.1659*taper**2-0.0706*taper+0.0119 #interpolated from paper mentioned p9
    
    #Theoretical Oswald efficiency
    e_theo = 1./(1.+f*A) #[-]
    
    #penalties:
    K_e_f = 1.-2.*(d_fus/b)**2. #[-]penalty for the fuselage
    K_e_M = a_e*(M_cruise/M_comp-1)**b_e + 1. #[-] penalty for machnumber
    K_e_D = 0.873 #penalty for induced drag, for method 2
    K_e_dihedral = ((1.+(1./kwl)*(1./np.cos(dihedral)-1.))**2) #gives value larger than 1

    # variables for final calculation of e for method 1
    Q = 1./(e_theo*K_e_f)
    P = K*CD0
    
    
    
    #final e
    #e = K_e_M/(Q+P*np.pi*A)*K_e_dihedral #[-] Method 1 Kroo
    e = e_theo*K_e_f*K_e_M*K_e_D*K_e_dihedral # [-] Method 2 Paper mentioned above
    
    return (e)



# =============================================================================
# #test function here
# test = True
# if test:
#     import os
#     from pathlib import Path
#     os.chdir(Path(__file__).parents[6])
#     from A22DSE.Parameters.Par_Class_Diff_Configs import Conv
# 
# =============================================================================
