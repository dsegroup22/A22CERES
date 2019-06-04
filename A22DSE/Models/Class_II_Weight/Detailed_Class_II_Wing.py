# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np
import scipy.integrate as integrate
import sys
sys.path.append('../../../')
from A22DSE.Models.STRUC.current.Loadingdiagram import Loading_Diagrams
from A22DSE.Parameters.Par_Class_Conventional import Conv
from math import *


def R_wg(Aircraft):
    #Determines wing relief factor due to structure, can be more precies by
    #using exact y locations of wing group and CoP
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    MTOW = struc.MTOW
    W_w = struc.Wing_weight #Dummy change functions in diff_configs
    #y_wg
    #y_cp  
    return W_w/MTOW

def R_en(Aircraft):
    #Determines engine relief factor 
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig


    x_eng = config.x_engine
    x_cp = config.x_CoP
    MTOW = struc.MTOW
    W_eng = config.m_engine
    return 3 * (x_eng**2 / x_cp) * (W_eng / MTOW)

def R_f(Aircraft):
    #Determines fuel relief factor, for layout it is necessary that inner
    #bulkhead coincides with wing root
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    b_f = config.b_fueltank
    b = anfp.b
    taper = anfp.taper
    MTOW = struc.MTOW
    MZF = MTOW - struc.FW
    return 0.5 * (b_f/b) * (1 + (3 * taper**2)/(1 + 2*taper)) * (1 - MZF/MTOW)
    
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
    rho=2000
    n_ult=2.5
    g=9.80665
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
    print (t_c*(c_r+c_t)/2)
    return W_id_box,W_rib


