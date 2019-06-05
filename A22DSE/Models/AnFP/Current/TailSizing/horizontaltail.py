# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:33:10 2019

@author: Atiqah Tarmizi
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../../../../../')
from math import sqrt, atan, tan, pi, cos, radians

def htail(Aircraft):
    AnFP = Aircraft.ParAnFP
#    taper_main = AnFP.taper
    MAC = AnFP.MAC
    sweep_main = AnFP.Sweep_LE
    AR_main = AnFP.A
    b_main = AnFP.b
    Sw = AnFP.S
    
    #initial sizing
    h_tail = Aircraft.ParLayoutConfig
    h_S1 = h_tail.Sht
    h_A = h_tail.Aht
    h_taper = h_tail.trht
    h_sweep25 = h_tail.Sweep25ht*pi/180
    h_hta = h_tail.xht #tail arm
    
    V_cruise = AnFP.V_cruise
    Vd = 1.4*V_cruise
    kh = 1.1
    h_sweep50 = atan(tan(h_sweep25)-(4/h_A)*(0.5-0.25)*((1-h_taper)/(1+h_taper)))
    
    Vh = 1.0 #based on military transport
    h_S = Vh*Sw*MAC/h_hta
    
    mh = kh*h_S*(62*(h_S**0.2*Vd)/(1000*sqrt(cos(h_sweep50)))-2.5)
    
    #using the scissor plot can find the Sh required
    
#    ShS = 0.3
#    Sh = 0.3*Sw #new horizotal tail surface area
#    tail_diff = (Sh - h_S)/h_S
#    
#    if tail_diff > 0.1:
#        h_S = Sh
#        mh = kh*h_S*(62*(h_S**0.2*Vd)/(1000*sqrt(cos(h_sweep50)))-2.5)
#        
#    if tail_diff < 0.03:
#        h_S = Sh
    
     
    return (h_S, h_hta)

def convtail(Aircraft,ISA):
    Vh = 1 #based on military transport
    AnFP = Aircraft.ParAnFP
    taper_main = AnFP.taper
    MAC = AnFP.MAC
    sweep_main = AnFP.Sweep_LE
    AR_main = AnFP.A
    b_main = AnFP.b
    Sw = AnFP.S
    V_cruise = AnFP.V_cruise
    h_cruise = np.array([20000]) #m 

    lay = Aircraft.ParLayoutConfig
    Df = lay.d_fuselage #using diameter of cabin
    #Df = lay.dim_cabin[0] #using width of cabin
    
    l_arm_opt = 1.4*sqrt((4*MAC*Sw*Vh)/(pi*Df))
    #mac3c = l_arm_opt/MAC
    
    Sh = Vh*MAC*Sw/l_arm_opt
    etha = 0.95 
    
    #taper ratio, sweep angle, dihedral angle, airfoil selection
    h = 0.2 #(Xcg/MAC)
    h0 = (.2 + .25)/2 #(Xac_wf/MAC)
    #g0 = ISA.g0
    
    Wavg = .5 * (19000+8000)*ISA.g0 #change Wi and Wf
    #------airfoil NACA0012
    #Cmaf = (0.0061--0.0061)/(4--4)
    #------airfoil NACA0010 ; based on horizontal tail has to be 10% less thickness than wing airfoil
    Cmaf = (0.0041--0.0041)/(3--3) 
    rho = ISA.ISAFunc(h_cruise)[2]
    
    CL= (2*Wavg)/(rho*V_cruise**2*Sw)
    
    
    CLh = (Cmaf*(AR_main*(cos(sweep_main))**2)/(AR_main+2*cos(sweep_main)) + (CL*(h-h0)) )/ (etha*Vh)
     
    #must be iterated with the right cg, Wavg, h etc.
    #no incidence angle as it is not a fixed tail 
    AR_h = 2/3 * AR_main
    tr_h = 0.348
    sweep_h = sweep_main+5*pi/180
    #Gamma = sweep_h #dihedral angle
    
    ch_root = 3/2*Vh*((1+tr_h)/(1+tr_h+tr_h**2))
    ch_tip = ch_root*tr_h
    bh = Sh/Vh
    
    iw = 0 #wing incidence
    ht = l_arm_opt*tan(radians(12.5)-iw-radians(3)) #tail height from relative to the wing ac
    
    Vd = 1.4*V_cruise
    kh = 1.1
    
    sweep_h50 = atan(tan(sweep_h)-(4/AR_h)*(0.5-0)*((1-tr_h)/(1+tr_h)))
    
    mh = kh*Sh*(62*(Sh**0.2*Vd)/(1000*sqrt(cos(sweep_h50)))-2.5)
    
    #using scissor plot and update values of Sh
    
    #---------------- elevator design procedure 
    bebh = 1 #elevator span = h tail span
    cech = 0.3 #
    tau_e = 0.525
    SeSh = 0.3
    cech = 0.3
    
    #---------------- iterative process 
    Vmc = 45 #m/s
    Vr = 1.05*Vmc
    
    T = 325000 #N 
    CL_to = AnFP.C_L_max_slow #1.5 #subject to change
    CD_to = 0.07
    Cm_ac_wf = -0.5
    mu = 0.03
    
    Lwf = 0.5*ISA.rho0*Vr**2*CL_to*Sw
    Dto = 0.5*ISA.rho0*Vr**2*CD_to*Sw
    Macwf = 0.5*ISA.rho0*Vr**2*Cm_ac_wf*Sw*MAC
    MTOW = Aircraft.ParStruc.MTOW
    
    a = (T-Dto-mu*(MTOW*ISA.g0-(Lwf+0.5*ISA.rho0*Vr**2*CLh*Sh)))/MTOW
    
    betah = sqrt(1-AnFP.M_cruise**2)
    CLalphah = 2*pi*AR_h/(2.+ sqrt(4.+(AR_h*betah/etha)**2*(1.+((tan(radians(AnFP.Sweep_50)))**2/betah**2)))) #/rad

    Cm_deltae = - CLalphah*etha*Vh*bebh*tau_e #rate of change of aircraft pitching moment coefficient wrt elevator deflection
    CL_deltae = CLalphah*etha*(Sh/Sw)*bebh*tau_e #rate of change of aircraft lift coefficient wrt to elevator deflection
    CL_h_deltae = CLalphah*tau_e #rate of change of tail lift coefficient wrt elevator deflection
    
    #for large transport
    rot_t = 4 #[s] rotation time
    theta_dd = 5 #[deg/s] take-off pitch angular acceleration
    
    
    
    alpha_onset = 0
    ih = 0
   
    alpha_h = alpha_onset + ih - (2*CL_to)/(pi*AR_main)
    #de_max_up = (CLh/CLalphah - alpha_h) /tau_e
    
    #finish once we have all parameters
    
#    return (l_arm_opt,Sh,CL,CLh,mh,CL_to)
    return (ch_root, ch_tip,bh,sweep_h,tr_h,AR_h,mh,Sh)
#def rudder(Aircraft):
    
    
    