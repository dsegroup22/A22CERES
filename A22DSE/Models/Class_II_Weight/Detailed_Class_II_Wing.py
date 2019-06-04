# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno & nikki
"""
import numpy as np
import scipy.integrate as integrate
import sys
sys.path.append('../../../')
from A22DSE.Models.STRUC.current.Loadingdiagram import Loading_Diagrams
from A22DSE.Parameters.Par_Class_Conventional import Conv
from math import *

def SharedParams(Aircraft):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    b=anfp.b
    Sweep_EA=anfp.Sweep_50
    S=anfp.S
    sigma_t=3*10**9/1.5
    sigma_c=1*10**9/1.5

    
    omega_ic=0.25 #[m]
    b_st=b/np.cos(Sweep_EA)

    R_ic = 1+2*omega_ic*b_st/S
    sigma_r=(0.5*(R_ic/sigma_t+1.25/sigma_c))**-1
    return b,Sweep_EA,S,sigma_t,sigma_c,omega_ic,b_st,R_ic,sigma_r

def R_wg(Aircraft):
    #Determines wing relief factor due to structure, can be more precies by
    #using exact y locations of wing group and CoP
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    MTOM = struc.MTOW
    M_w = struc.Wing_weight #Dummy change functions in diff_configs
    #y_wg
    #y_cp  
    return M_w/MTOM

def R_en(Aircraft):
    #Determines engine relief factor 
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    taper = anfp.taper
    n_ult = 2.5
    Sweep_25 =anfp.Sweep_25


    x_eng = config.x_engine
    x_cp = 1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper)) \
    +0.02*np.sin(Sweep_25)
    MTOM = struc.MTOW #kg
    M_eng = config.m_engine #kg
    
    return 3 * (x_eng**2 / x_cp) * (M_eng / MTOM)

def R_f(Aircraft):
    #Determines fuel relief factor, for layout it is necessary that inner
    #bulkhead coincides with wing root
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    b_f = config.b_fueltank
    b = anfp.b
    taper = anfp.taper
    MTOW = struc.MTOW #kg
    MZF = MTOW - struc.FW #kg
    return 0.5 * (b_f/b) * (1 + (3 * taper**2)/(1 + 2*taper)) * (1 - MZF/MTOW)
   
def W_nid(Aircraft):
    #Calculate weight penalties for several components
    #Tapered skin, fail safety margins, engine mouting, connection to the
    #fuselage, aerolasticity weight
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    anfp = Aircraft.ParAnfp
    
    g = 9.80665 #m/s2
    
    rho = 2000 #Specific weight wing box DUMMY kg/m3
    W_pp = 5000 * g #powerplant weight DUMMY [N]
    
    MTOW = struc.MTOW * g #in Newton
    Sweep_50 = anfp.Sweep_50
    W_G = MTOW - (struc.MZF*g) #Gross weight approx ZFW
    b = anfp.b
    taper = anfp.taper
    Sweep_25 = anfp.Sweep_25
    
    n_ult = 2.5
    x_cp = 1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper)) \
    +0.02*np.sin(Sweep_25)
    n_eng = anfp.n_engines
    b_st=b/np.cos(Sweep_50)
    stress_av = SharedParams(Aircraft)[8]

    #Penalties
    fail_safety = 0.18 * n_ult * W_G * x_cp * b_st * (rho*g/stress_av)
    engine = 0.015*(1 + 0.2*n_eng)*W_pp
    fus_connection = 0.0003 * n_ult * MTOW
    
    #Addittional Penalties
    #aerolasticity = W_ref * (q_D/q_ref) * (b*cos(sweep_LE)/b_ref)**3 * \
    #(tc_ref)**(-2) * (1 - sin(sweep_50)) * (1 - (M_D * cos (sweep_50)))**(-0.5)
    #Weight penalty for torsional stiffness of an aluminium wing box 
    #(we have composites)
    #skin_taper = incr * rho * g * S_box // communicate whether we add taper
    
    return fail_safety + engine + fus_connection  

def LE_TE_Weight(Aircraft):
    #Determines weight of LE and TE based on emperical relations
    S_ref = 10 #[m2]
    Omega_ref = 56 #[N/m2]
    k_fle = 1 #1.3 with slats
    b_ref = 50 #[m]
    W_ref = 10**6 #[N]
    return S_ref

def SharedParams(Aircraft):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    b=anfp.b
    Sweep_EA=anfp.Sweep_50
    S=anfp.S
    sigma_t=480*10**6/1.5 # N/m^2
    sigma_c=0.4*sigma_t # N/m^2 http://home.iitk.ac.in/~mohite/axial_compressive.pdf

    
    omega_ic=0.25 #[m]
    b_st=b/np.cos(Sweep_EA)

    R_ic = 1+2*omega_ic*b_st/S
    sigma_r=(0.5*(R_ic/sigma_t+1.25/sigma_c))**-1
    return b,Sweep_EA,S,sigma_t,sigma_c,omega_ic,b_st,R_ic,sigma_r


def WingWeight(Aircraft):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    MTOW=struc.MTOW

    Sweep_25=anfp.Sweep_25
    
    A=anfp.A
    c_r=anfp.c_r
    c_t=anfp.c_t
    taper=anfp.taper
    t_c=anfp.tc
    eta_t=0.84
    I_2_t=0.36
    t_ref=1
    k_rib=0.5*10**-3   
    rho=1600 #kg/m^3
    n_ult=2.5
    g=9.80665 #m/s^2
    #dummy values including safety factors

    b,Sweep_EA,S,sigma_t,sigma_c,omega_ic,b_st,R_ic,sigma_r=SharedParams(Aircraft)
    R_in= 1-R_wg(Conv)-R_en(Conv)-R_f(Conv)
    
    

    
    eta_cp=1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper))+0.02*np.sin(Sweep_25)
    
    sigma_shear=0.5*sigma_r
    R_cant=A*(1+taper)/(4*t_c*np.cos(Sweep_EA))

    #not used
    V,M=Loading_Diagrams(Aircraft)
    A=M/eta_t/sigma_t
    localA = lambda x:  A[int(round(x/(b/2)))]
    W_BL=2*g*rho*integrate.quad(localA,0,b_st)[0]
    
    
    W_BL2=I_2_t*rho*g/sigma_r*n_ult*MTOW*g*R_cant*eta_cp/eta_t*b_st

    W_SL=1.2*n_ult*MTOW*g*eta_cp*b_st*rho*g/sigma_shear

    W_IP_T=0.05*W_BL
    
    
    
    W_id_box=I_2_t*n_ult*R_in*MTOW*g*eta_cp*b_st*rho*g/sigma_r*(1.05*R_cant/eta_t+3.67)
    
    W_rib=k_rib*rho*S*g*(t_ref+t_c*(c_r+c_t)/2)
    
    return W_id_box,W_rib


