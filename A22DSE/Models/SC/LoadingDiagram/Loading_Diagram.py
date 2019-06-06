# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:56:34 2019

@author: atiqah
"""
import numpy as np
import matplotlib.pyplot as plt

def loadingdiag(Aircraft):
    MAC = Aircraft.ParAnFP.MAC
    
    y_mac = Aircraft.ParAnFP.y_MAC
    
    l_fuselage = Aircraft.ParLayoutConfig.l_fuselage
    xf = 0.42 * l_fuselage
    #xpayload = np.array([0.8,0.7,0.6,0.5,0.4,0.3,0.2]*l_fuselage)
    xcg_totalpayload_empty = Aircraft.ParPayload.xcg_totalpayload_empty
    
    fuel_mass = Aircraft.ParStruc.FW
    payload_mass = 13500 #append value [kg]
    
    x_lemac = Aircraft.ParLayoutConfig.x_lemac
    
    xcg_wing = 0.25*MAC
    xcg_w_global = xcg_wing + x_lemac
    
    oew = 45000
    
    top = 20*oew #append real value
    bottom = oew #kg append real value
    payload_mlist = np.ones(payload_mass)
    
    cg_in = x_lemac + 0.24*MAC
    
    cg_range = [cg_in]
    wrange = [oew]
    
    #xf must be changed to the loading of the sulphur
    #loading for payload
    for i in range(payload_mass):
        cg = ((top + xf*payload_mlist[i]))/(bottom + payload_mlist[i])
        top = (top + xf*payload_mlist[i])
        bottom = bottom + payload_mlist[i]
        cg_range.append(cg)
        wrange.append(bottom)
 
    #loading for fuel
#    for i in range(fuel_mass):
    
    xfuel = xcg_wing
    fuel_mlist = np.ones(int(fuel_mass))
    
    for i in range(int(fuel_mass)):
        cg = ((top + xfuel*fuel_mlist[i]))/(bottom + fuel_mlist[i])
        top = (top + xfuel*fuel_mlist[i])
        bottom = bottom + fuel_mlist[i]
        cg_range.append(cg)
        wrange.append(bottom)
        
    
#    plt.plot((cg_range-x_lemac)/MAC,wrange)
#    plt.plot(cg_range,wrange)
#    plt.show()
#        
    
    
    #return  fuel_mass
        
        
        
        
#    
#f = 50
#
#payload = np.arange(50)
#
##for i in range(f):
# #   print payload[i]
    
    
    
    