# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:40:08 2019

@author: kamph
"""
import os
import sys
import numpy as np
from pathlib import Path
os.chdir(Path(__file__).parents[2])
sys.path.append('../../')
import matplotlib.pyplot as plt

## Sizing ##



def GetNoseLength_opt(Aircraft, D_f):

    fineness_n = Aircraft.ParStruc.fineness_n #Predetermined Fineness
    
    #Size requirement 
    UF = 1.2                        #[-]
    pax_height = 1.50*UF            #[m]
    
    #Nose length
    L_n = fineness_n*D_f            #[m]
    
    if D_f < pax_height:
        L_n = fineness_n*pax_height #[m]
    return L_n



def GetTailLength_opt(Aircraft, D_F):

    fineness_t = Aircraft.ParStruc.fineness_t #Predetermined Fineness
    L_t = D_f*fineness_t                                  #[m]
    return L_t

def GetCabinLength_rev(Aircraft, fineness_f, SF, L_n, L_t):
    #Constraints
#   Q_r = Aircraft.ParPayload.m_payload/Aircraft.ParPayload.rho_payload #volume
    A_inr = 0.636
    
    #design requirements
    ovalrate = 1.75
    D_eq = np.sqrt(A_inr*SF/(np.pi/4))
    
    
    #Calculate cabin using tail arm as a leading factor
    L_c = max(Aircraft.ParLayoutConfig.xvt, Aircraft.ParLayoutConfig.xht) - \
    L_n - L_t
        
    D_f = L_c/fineness_f
    
    if D_f<D_eq:
        D_f = D_eq
        
    h = D_f/np.sqrt(ovalrate)
    w = ovalrate*h

    return L_c, D_f, np.array([h, w])

def Fuselage_iter(Aircraft, fineness_f, SF):
    L_n = 2.67
    L_t = 4.27
    
    for i in range(1000):
        D_f = GetCabinLength_rev(Aircraft, fineness_f, SF, L_n, L_t)[1]
        L_n = GetNoseLength_opt(Aircraft, D_f)
        L_t = GetTailLength_opt(Aircraft, D_f)
    
    Q_r = Aircraft.ParPayload.m_payload/Aircraft.ParPayload.rho_payload
    
    Q_fus = D_f**2 * np.pi/4 * GetCabinLength_rev(Aircraft, fineness_f,  SF, L_n, L_t)[0]
    
    
    if Q_fus < Q_r:
        print('Fuselage too small')
    return L_n, GetCabinLength_rev(Aircraft, fineness_f, SF, L_n, L_t)[0], L_t,\
    GetCabinLength_rev(Aircraft, fineness_f, SF, L_n, L_t)[2], D_f

## Important to optimisation ##

def FusAreas_mod(Aircraft, fineness_f, SF):

    config = Aircraft.ParLayoutConfig

    
    l_nose= Fuselage_iter(Aircraft,fineness_f, SF)[0]
    l_cabin= Fuselage_iter(Aircraft,fineness_f, SF)[1]
    l_tail= Fuselage_iter(Aircraft,fineness_f, SF)[2]
    
    h_fuselage=Fuselage_iter(Aircraft, fineness_f, SF)[3][0]
    w_fuselage=Fuselage_iter(Aircraft, fineness_f, SF)[3][1]
    d_fuselage=Fuselage_iter(Aircraft, fineness_f, SF)[4]
    d_cockpit=config.d_cockpit
    
    h_APU=config.h_APU
    
    e=np.sqrt(1-(d_cockpit/2/l_nose)**2)

    Sw_nose=np.pi*(d_cockpit/2)**2*(1+l_nose/(d_cockpit/2*e)*np.arcsin(e))
    
    h=((h_fuselage-w_fuselage)/(h_fuselage+w_fuselage))**2
    Sw_cabin=np.pi*(h_fuselage+w_fuselage)/2*(1+3*h/(10+np.sqrt(4-3*h)))*l_cabin
    
    
    l_fullcone=d_fuselage*l_tail/(d_fuselage-h_APU)
    l_imagcone=l_fullcone-l_tail
    Sw_fullcone=np.pi*d_fuselage/2*np.sqrt(l_fullcone**2-(d_fuselage/2)**2)
    Sw_imagcone=np.pi*h_APU/2*np.sqrt(l_imagcone**2-(h_APU/2)**2)
    Sw_tail=Sw_fullcone-Sw_imagcone
    
    S_wet=Sw_nose+Sw_cabin+Sw_tail
    return S_wet

def friction_coef(Aircraft, fineness_f, SF):
    #INPUT: V_cruise, atmospheric conditions, span, wetted area
    #OUTPUT: friction coefficient
    anfp = Aircraft.ParAnFP
    V = anfp.V_cruise #Cruise speed
    b = anfp.b #Span
    
    mu = 1.43226e-5 #dynamic friction
    rho = 0.0880349 #density
    nu = mu / rho #kinematic friction
    
    S_wet = FusAreas_mod(Aircraft, fineness_f, SF)
    
    Re = (S_wet / b) * V / nu
    C_fe = 0.00258 + 0.00102*np.exp(-6.28e-9 * Re) + 0.00295*np.exp(-2.01e-8*\
                                   Re)
    return C_fe

def CD0_diff(Aircraft, fineness_f, SF):
    anfp = Aircraft.ParAnFP
    S = anfp.S
    C_fe = friction_coef(Aircraft, fineness_f, SF)
    S_fus = FusAreas_mod(Aircraft, fineness_f, SF)
    CD0_fus = C_fe *(S_fus/S)
    return CD0_fus

#def FuselageWeight_opt(Aircraft, fineness_f):
#    anfp = Aircraft.ParAnFP
#    struc = Aircraft.ParStruc
#    
#    SF0 = 1
#    dSF = 0.01
#    L_freq = max(Aircraft.ParLayoutConfig.xvt, Aircraft.ParLayoutConfig.xht)
#    
#    h_fuselage= Fus_Dim_opt(Aircraft, L_freq, SF0, dSF, fineness_f)[2][0]    #[m]
#    w_fuselage=Fus_Dim_opt(Aircraft, L_freq, SF0, dSF, fineness_f)[2][0]    #[m]
#
#    l_fuselage=sum(Fus_Dim_opt(Aircraft, L_freq, SF0, dSF, fineness_f)[0])    #[m]
#    K_inl=1.                      #roskam page 77 part V
#    MTOMlbs = struc.MTOW/Aircraft.ConversTool.lbs2kg
#    q_Dpsf = anfp.q_dive/Aircraft.ConversTool.psf2Pa
#    
#    
#    #Roskam part V (Chapter 5.3)
#    #roskam: equation 5.26 (commercial)
#    W_f=2*10.43*K_inl**1.42*(q_Dpsf/100)**0.283*(MTOMlbs/1000)**0.95*\
#    (l_fuselage/h_fuselage)**0.71
#
#    #roskam: equation 5.28 (militairy)
#    W_f_mil=2*11.03*K_inl**1.23*(q_Dpsf/100)**0.245*(MTOMlbs/1000)**0.98*\
#    (l_fuselage/h_fuselage)**0.61
#    
#    
##    torenbeek method  (Chapter 8.3.3)  
#    l_ref=1.5 #[m]
#    n_ult=2.5
#    d_fuselage=np.average([h_fuselage,w_fuselage])    
#    
#    C_shell=60          #[N/m^3]
#    Omega_fl=160        #[N/m^2]
#    
#    W_shell=C_shell*d_fuselage**2*l_fuselage
#    W_bulkheads=C_shell*d_fuselage**2*l_ref
#    
#    W_fl=Omega_fl*n_ult**0.5*d_fuselage*l_fuselage
#    W_f_tor=W_shell+W_bulkheads+W_fl
#    return W_f*Aircraft.ConversTool.lbf2N,W_f_mil*Aircraft.ConversTool.lbf2N,W_f_tor #[N]
#

lst = []
lst1 = []

for i in np.arange(2, 20 ,0.5):
    CD0 = CD0_diff(Conv, i, 1.5)
    #W_f = FuselageWeight_opt(Conv, i)
    lst.append(CD0)
    #lst1.append(W_f)
    
plt.figure()    
plt.plot(np.arange(2, 20, 0.5),lst)
#plt.figure(2)
#plt.plot(np.arange(2, 12.5, 0.5),lst1)
plt.ylabel('some numbers')
plt.show()
