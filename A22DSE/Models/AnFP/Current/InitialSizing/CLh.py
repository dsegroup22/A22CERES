# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:08:48 2019

@author: Atiqah Tarmizi
"""
from math import pi, sqrt, tan, cos
import numpy as np
import matplotlib.pyplot as plt

def CLh(Conv):
    layout = Conv.ParLayoutConfig
    anfp = Conv.ParAnFP
    AR_h = layout.Aht 
    M = anfp.M_cruise
    M = np.array([0.2,0.4,0.6,0.8])
    label = ['M=0.2','M=0.4','M=0.6','M=0.8']
    sweep50 = layout.sweep50ht
    sweep25 = layout.sweep25ht
    etha = 0.95
    
    alpha_xflr = np.array([1,1.5,2,2.5,3,3.5,4,4.5,5])
    CL_xflr = np.array([0.301035,0.3352779,0.3694953,0.4036846,0.4378431,\
                     0.4719682,0.5060575,0.5401082,0.5741177])
    fit = np.polyfit(alpha_xflr,CL_xflr,1)
    
    alphah = np.arange(-4,8,1)
    CLh = []
    for i in range(len(alphah)):
        y = fit[0]*alphah[i] + fit[1]
        CLh.append(y)
        
#    plt.plot(alphah,CLh)
#    #plt.plot(alpha_h,CL_h)
#    plt.axhline(y=0, color='k',linewidth=0.5)
#    plt.axvline(x=0,color='k',linewidth=0.5)
#    plt.ylabel('$CL_h$')
#    plt.xlabel(r'$\alpha_h$')
#    plt.title(r'$CL_h$ vs $\alpha_h$ curve')
#    plt.show()
#    
#    for i in range(len(M)):
#        beta = sqrt(1-M[i]**2)
#        CLalpha_h = ((2*pi*AR_h)/(2+sqrt(4+((AR_h**2*beta**2)/(etha**2))*(1+\
#                                 ((tan(sweep50))**2)/(beta**2))))) *pi/180
#        #print (CLalpha_h)
#        alpha_h = np.arange(-5,8,1)
#        CLh = CLalpha_h*alpha_h
#        CLhmax = 0.9*1.4*cos(sweep25)
#        alphamax = CLhmax/CLalpha_h
#        #print (CLh)
#        
#        plt.plot(alpha_h,CLh,label=label[i])
#        plt.scatter(alphamax,CLhmax)
#        plt.legend(loc=2)
#        plt.show()
    Clh_max = 0.9 * 1.5 * cos(sweep25)
    
#        
#def CL_h(Conv):
#    layout = Conv.ParLayoutConfig
#    anfp = Conv.ParAnFP
#    AR_h = layout.Aht 
#    M = anfp.M_cruise
#    etha = 0.95
#    sweep50 = layout.sweep50ht
#    beta = sqrt(1-M**2)
#    alphah_0 = -4*pi/180
#    CLalpha_h = ((2*pi*AR_h)/(2+sqrt(4+((AR_h**2*beta**2)/(etha**2))*(1+\
#                                 ((tan(sweep50))**2)/(beta**2))))) 
#    
#    C_L_to_C_l=0.83 
#    delta_C_L_max=-0.35
#    delta_alpha_C_L_max=2/180*pi
#    C_lh_max = 1.56
#    C_Lh_max=C_lh_max*C_L_to_C_l+delta_C_L_max
#    print (C_Lh_max)
#    
#    #alpha_stall=C_Lh_max/CLalpha_h+alphah_0+delta_alpha_C_L_max
#    alphah_linstall=C_Lh_max/CLalpha_h+alphah_0
#    print (alphah_linstall)    
#
#    plt.plot([alphah_0*180/pi,alphah_linstall*180/pi],[0,C_Lh_max])
#    plt.show()
    return Clh_max, fit[0]
    
    
        