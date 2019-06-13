# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:16:32 2019

@author: lujingyi
"""
from math import pi,sqrt,log
#y_aileron

def aileron(Aircraft):
    b = Aircraft.ParAnFP.b
    b1 = b/2*0.75
    b2 = b/2*0.9
    rho = 1.225
#    cl_delta_a = 5 #per rad !!!!!!!
    CL_w_a = Aircraft.ParAnFP.C_L_alpha_slow
    c_r = Aircraft.ParAnFP.c_r
    S = Aircraft.ParAnFP.S
    tr = Aircraft.ParAnFP.taper
    chord_ratio = 0.2
    tau = 0.41
    #Cl_delta_a = 2*tau*cl_delta_a*c_r/(S*b)*((b2**2-b1**2)+2*(tr-1)/(3*b)*(b2**3-b1**3))
    Cl_delta_a = 2*tau*CL_w_a*c_r/(S*b)*((b2**2-b1**2)+2*(tr-1)/(3*b)*(b2**3-b1**3))
    cl_a = Aircraft.ParAnFP.cl_alpha*180/pi
    cd0 = Aircraft.ParAnFP.Cd0
    Cl_p = -(cl_a+cd0)*c_r*b*(1+3*tr)/24/S
    delta = 15
    roll = -Cl_delta_a/Cl_p*delta*pi/180 #should be larger 0.07
    #stel 11    
    Cl = Cl_delta_a*delta*pi/180
    #step 12
    V_app = 1.3*Aircraft.ParAnFP.V_stall
    L_A = 0.5*rho*V_app**2*S*Cl*b
    #step 13
    Sht = Aircraft.ParLayoutConfig.Sht
    Svt = Aircraft.ParLayoutConfig.Svt
    CDr = 0.9
    y_D = 0.4*b/2
    P_ss = sqrt(2*L_A/(rho*(S+Sht+Svt)*CDr*(y_D**3)))
    #step 14
    I_xx = Aircraft.ParStruc.OEW*2.2046*((b*3.28)**2)/1870*1.35
    phi1 = I_xx*log(P_ss**2)/(rho*(S+Sht+Svt)*CDr*(y_D**3))
    #step 15
    Pdot = P_ss**2/2/phi1
    #step 16
    phi_req = 30
    t2 = sqrt(2*phi_req/Pdot*pi/180)
#=========================================================================
    Aircraft.ParLayoutConfig.y_aileron = b1
    Aircraft.ParLayoutConfig.y_aileron_end = b2
#=========================================================================
    #return I_xx
    #return roll,t2