# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:56:34 2019

@author: atiqah
"""
import numpy as np
import matplotlib.pyplot as plt

def loadingdiag(Aircraft):
    """DESCRIPTION: loading diagram based on SAED lecture
       INPUT: OEW, x_lemac, 
    """
    rangecg = np.array([1,1.15,0.85])#,1.15,0.85])
    Layout = Aircraft.ParLayoutConfig
    x_lemac = Aircraft.ParLayoutConfig.x_lemac
    xcg_fwd = []
    xcg_aft = []
    y = []
    
    for i in range(len(rangecg)):
        MAC = Aircraft.ParAnFP.MAC
          
        #xpayload = np.array([0.8,0.7,0.6,0.5,0.4,0.3,0.2]*l_fuselage)
        xcg_totalpayload_empty = 18 #Aircraft.ParPayload.xcg_totalpayload_empty
        
        fuel_mass = Aircraft.ParStruc.FW
        payload_mass = Aircraft.ParPayload.m_payload #13500 #append value [kg]
        
        x_lemac = Aircraft.ParLayoutConfig.x_lemac*rangecg[i]
        
        oew = Aircraft.ParStruc.OEW
        x_oew = Aircraft.ParLayoutConfig.x_oe*rangecg[i]*MAC + x_lemac
        
        top = x_oew*oew #append real value
        bottom = oew #kg append real value
        payload_mlist = np.ones(int(payload_mass))
        
        cg_range = [x_oew]
        wrange = [oew]
        
        xfuel = 0.5*MAC+x_lemac #assumptions
        
        fuel_mlist = np.ones(int(fuel_mass))
        
        for i in range(int(fuel_mass)):
            cg = (top + xfuel*fuel_mlist[i])/(bottom + fuel_mlist[i])
            top = (top + xfuel*fuel_mlist[i])
            bottom = bottom + fuel_mlist[i]
            cg_range.append(cg)
            wrange.append(bottom)
            
        fuelindex = len(cg_range)
        
        #xf must be changed to the loading of the sulphur
        #loading for payload
        for i in range(int(payload_mass)):
            cg = ((top + xcg_totalpayload_empty*payload_mlist[i]))/(bottom + payload_mlist[i])
            top = (top + xcg_totalpayload_empty*payload_mlist[i])
            bottom = bottom + payload_mlist[i]
            cg_range.append(cg)
            wrange.append(bottom)
     
        #loading for fuel
    #    for i in range(fuel_mass):
            
        cg_range_mac = (cg_range-x_lemac)/MAC
        x_oew_mac = Aircraft.ParLayoutConfig.x_oe / MAC
        
        xcg_fwd.append(min(cg_range_mac))
        xcg_aft.append(max(cg_range_mac))
        
        l_fuselage = Aircraft.ParLayoutConfig.l_fuselage
        y.append(x_lemac/l_fuselage)
        
        
        #plt.plot((cg_range-x_lemac)/MAC,wrange)
#        plt.plot(cg_range_mac[0:fuelindex+1],np.array(wrange[0:fuelindex+1]),color='palevioletred',label='Fuel')
#        plt.plot(cg_range_mac[fuelindex:],np.array(wrange[fuelindex:]),color='plum', label='Payload')
#        plt.legend(loc=1)
#        plt.axvline(x=max(cg_range_mac), color='gray', linestyle='--')
#        plt.axvline(x=min(cg_range_mac), color='gray', linestyle='--')
#        plt.axvline(x=max(cg_range_mac)+0.02, color='indianred', linestyle='--')
#        plt.axvline(x=min(cg_range_mac)-0.02, color='indianred', linestyle='--')
#        plt.annotate('OEW',(x_oew_mac,oew))
#        plt.show()
    #x_lemac = Layout.x_lemac
#    plt.plot(xcg_fwd,y)
#    plt.plot(xcg_aft,y)
#    plt.xlim(0,1)
#    plt.show()
    
    
    xcg_fwd_global = xcg_fwd[0]*MAC+x_lemac
    xcg_aft_global = xcg_aft[0]*MAC+x_lemac
    return xcg_fwd_global, xcg_aft_global
