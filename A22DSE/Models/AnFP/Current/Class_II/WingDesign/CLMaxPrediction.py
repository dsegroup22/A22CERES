# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:15:25 2019

@author: tomhu
"""

"""CRITICAL SECTION METHOD"""
"""
INPUTS: Re, Mach, span
OUTPUTS: CLMAX, AOA@CLMAX
Method: give the clmax(airfoil) at every section (here it's the same 
everywhere), compute for a range of AOA the CL distribution, check if they
are within a margin prior specified. Here the VLM used will be XFLR5 and data 
from NASA SC(2)-0712
"""





"""Philips and Halley Method"""
def PhilipsCLMAX(Aircraft):
    clmax = 1.2
    kLsweep = 1 + kL1*Lam-kL2 * Lam**0.5
    kLomega = (1-CL/clmax/())
    kLs = 1+ (0.0042*AR-0.068)*(1+2.3*CLA)*Omega/clmax
    CLMAX = CLunsw/clmax * kLs*kLsweep * (clmax-kLomega*CLA*Omega)