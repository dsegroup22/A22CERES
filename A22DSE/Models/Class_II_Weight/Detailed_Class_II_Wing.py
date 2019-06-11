# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno & nikki
"""
import numpy as np
import scipy.integrate as integrate
import os
from pathlib import Path
os.chdir(Path(__file__).parents[3])

from math import *

#torenbeek method, exports in Newtons
# Chapter 11 2013

def SharedParams(Aircraft):
    #Function created for overlapping parameters used in the different functions 
    #below
    anfp = Aircraft.ParAnFP
    b=anfp.b                        #[m]
    Sweep_EA=anfp.Sweep_50          #[rad]
    S=anfp.S                        #[m^2]
    sigma_t=480*10**6/1.5           #[n/m^2]
    sigma_c=0.4*sigma_t             #[n/m^2] http://home.iitk.ac.in/~mohite/axial_compressive.pdf

    
    w_ic=0.25                       #[m] manhole width
    b_st=b/np.cos(Sweep_EA)         #[m]

    R_ic = 1+2*w_ic*b_st/S          #[-]
    sigma_r=(0.5*(R_ic/sigma_t+1.25/sigma_c))**-1 #N/m2
    return b,Sweep_EA,S,sigma_t,sigma_c,w_ic,b_st,R_ic,sigma_r

def R_wg(Aircraft):
    #Determines wing relief factor due to structure, can be more precise by
    #using exact y locations of wing group and CoP
    struc = Aircraft.ParStruc

    MTOM = struc.MTOW                   #[kg]
    M_w = struc.Mw_Mtow * struc.MTOW    #[kg]
    #y_wg
    #y_cp  
    return M_w/MTOM                     #[-]

def R_en(Aircraft):
    #Determines engine relief factor 
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    prop = Aircraft.ParProp
    taper = anfp.taper                  #[-]
    n_ult = anfp.n_ult                         #[-]
    Sweep_25 =anfp.Sweep_25             #[rad]


    x_eng = 0.25     	    #[-] dimensionless config.x_engine
    x_cp = 1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper)) \
    +0.02*np.sin(Sweep_25)              #[-] dimensionless p330
    MTOM = struc.MTOW                   #kg
    M_eng =  prop.Engine_weight         #kg
    
    return 3 * (x_eng**2 / x_cp) * (M_eng / MTOM)

def R_f(Aircraft):
    #Determines fuel relief factor, for layout it is necessary that inner
    #bulkhead coincides with wing root
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    b_f = 0.8            #[m] config.b_fueltank
    b = anfp.b                          #[m]
    taper = anfp.taper                  #[-]
    MTOW = struc.MTOW                   #kg
    MZF = MTOW - struc.FW               #kg
    return 0.5 * (b_f/b) * (1 + (3 * taper**2)/(1 + 2*taper)) * (1 - MZF/MTOW)
   
def W_nid(Aircraft):
    #Calculate weight penalties for several components
    #Tapered skin, fail safety margins, engine mouting, connection to the
    #fuselage, aerolasticity weight. For now tapered skin and an aerolasticity
    #penalty have been neglected, since too little is known about the wing box
    struc = Aircraft.ParStruc
    anfp = Aircraft.ParAnFP
    
    g = 9.80665                         #m/s2
    
    rho = 1600                          #Specific weight wing box [kg/m3]
    W_pp = 5000 * g                     #powerplant weight DUMMY [N]
    
    MTOW = struc.MTOW * g               #[N]
    Sweep_50 = anfp.Sweep_50            #[rad]
    W_G = MTOW - ((0.5*struc.FW+0.5*Aircraft.ParPayload.m_payload)*g) #Gross weight approx ZFW [N]
    b = anfp.b                          #[m]
    taper = anfp.taper                  #[-]
    Sweep_25 = anfp.Sweep_25            #[rad]
    
    n_ult = anfp.n_ult                         #[-]
    x_cp = 1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper)) \
    +0.02*np.sin(Sweep_25)              #[-] = eta_cp
    n_eng = struc.N_engines             
    b_st=b/np.cos(Sweep_50)             #[m]
    stress_av = SharedParams(Aircraft)[8] #[N/m2]

    #Penalties
    fail_safety = 0.18 * n_ult * W_G * x_cp * b_st * (rho*g/stress_av) #[N]
    engine = 0.015*(1 + 0.2*n_eng)*W_pp                                #[N] 
    fus_connection = 0.0003 * n_ult * MTOW                             #[N]
    
    #Addittional Penalties
    #aerolasticity = W_ref * (q_D/q_ref) * (b*cos(sweep_LE)/b_ref)**3 * \
    #(tc_ref)**(-2) * (1 - sin(sweep_50)) * (1 - (M_D * cos (sweep_50)))**(-0.5)
    #Weight penalty for torsional stiffness of an aluminium wing box 
    #(we have composites)
    #skin_taper = incr * rho * g * S_box // communicate whether we add taper
    
    return fail_safety + engine + fus_connection  

def LE_TE_Weight(Aircraft):
    #Determines weight of fixed LE and TE based on emperical relations
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    
    g = 9.80665     #m/s2
    Omega_ref = 56  #[N/m2]
    k_fle = 1       #1.3 with slats
    b_ref = 50      #[m]
    W_ref = 10**6   #[N]
    q_ref = 30e3    #[N/m2] All reference values are taken from Torenbeek
    
    b = anfp.b      #[m]
    MAC = anfp.MAC  #[m]
    Sweep_50 = anfp.Sweep_50 #[rad]
    MTOW = struc.MTOW * g    #[N]
    b_st=b/np.cos(Sweep_50)  #[m]


    q_D = 0.5*anfp.rho_cruise*(1.4*anfp.V_cruise)**2       #[Pa] Dynamic pressure

    
    Omega_LE = 3.15*k_fle*Omega_ref*(q_D/q_ref)**0.25 \
    * ((MTOW * b_st)/(W_ref*b_ref))**0.145 #[N/m2]
    S_LE = b * 0.20 * MAC                  #DUMMY Equation calculates leading edge surface
    
    Omega_TE = 2.6 * Omega_ref * ((MTOW * b_st)/(W_ref * b_ref))**0.0544
    #Increase Omega_ref by 40 0r 100 for ss Fowler flap and ds Fowler flap
    #respectively
    
    return Omega_LE*S_LE + Omega_TE*S_LE

def WingWeight(Aircraft):
    #Calculates ideal wing box weight based on stresses and rib weight
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc

    MTOW=struc.MTOW             #[kg]

    Sweep_25=anfp.Sweep_25      #[rad]
    
    A=anfp.A                    #[-]
    c_r=anfp.c_r                #[m]
    c_t=anfp.c_t                #[m]
    taper=anfp.taper            #[-]
    t_c=anfp.tc                 #[-] thickness to chord
    eta_t=0.84                  #[-] assumption for transsonic supercritical section p347
    I_2_t=0.36                  #[-] assumption p348
    t_ref=1                     #[m] p351
    k_rib=0.5*10**-3            #[-] p351
    rho=1600                    #kg/m^3 Mid-Term
    n_ult=anfp.n_ult                  #[-]
    g=9.80665                   #m/s^2

    b,Sweep_EA,S,sigma_t,sigma_c,w_ic,b_st,R_ic,sigma_r=SharedParams(Aircraft)
    R_in= 1-R_wg(Aircraft)-R_en(Aircraft)-R_f(Aircraft)                                #[-] 
    eta_cp=1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper))+0.02*np.sin(Sweep_25) #[-]
    R_cant=A*(1+taper)/(4*t_c*np.cos(Sweep_EA))                                        #[-] 

    
    
    
    W_id_box=I_2_t*n_ult*R_in*MTOW*g*eta_cp*b_st*rho*g/sigma_r*(1.05*R_cant/eta_t+3.67) #[N]
    W_rib=k_rib*rho*S*g*(t_ref+t_c*(c_r+c_t)/2) #[N]
    
    return W_id_box,W_rib

def Total_Wing(Aircraft):
    return W_nid(Aircraft) +sum(WingWeight(Aircraft)) + LE_TE_Weight(Aircraft)

#def control_surfaces(Aircraft):
#    Omega_ref = 56 #[N/m2]
#    k_bal = 1 #1 unbalanced, 1.3 ae balanced, 1.54 mass balanced
#    S_ail = 20 #DUMMY
#    S_sp = 20 #DUMMY
#    S_ref = 10 #m2
#    
#    Omega_ail = 3*Omega_ref*k_bal*(S_ail/S_ref)**0.044
#    Omega_sp = 2.2*Omega_ref*(S_sp/S_ref)**0.032
#    return Omega_ail*S_ail + Omega_sp*S_sp

"""The next methods are proposed in 'A Brief Summary of the Accuracy of Some Methods of Prediction
and a Suggested 'First Approximation' of Greater Accuracy ' """
def Method1(Aircraft):
    anfp = Aircraft.ParAnFP
    b = anfp.b*3.28084 #in ft
    
    
    Ww = 5340 * (b/100)**3 * 0.453592 #kg
    return Ww


def Method2(Aircraft):
#    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    Wg = (struc.OEWratio*struc.MTOW) /0.453592 #lb
    
    Ww  = 0.114 * Wg  *0.453592 #kg
    
    return Ww

"""from Torenbeek 1982"""
def Tore(Aircraft):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    N = anfp.n_ult
    tc = anfp.tc
    cwr = 1
    b = anfp.b
    sweep = anfp.Sweep_50
    Sref =1
    WZF = struc.MTOW - struc.FW
    
    Ww = 0.00667*N**0.55*(tc*cwr)**-0.3*(b/cos(sweep))**1.05*(1+sqrt(1.905*cos(sweep)/b))*(WZF/Sref)**-0.3*WZF
    return Ww