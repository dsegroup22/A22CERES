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
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (GetFuselageLength, GetCabinLength)

def Useful_for_me(Aircraft, L_freq, SF0, dSF, finesness_f, fineness_n, fineness_t):
    '''
    INPUT: Aircraft object, req. fuselage length, initial size factor, step
    size
    OUTPUT: returns the fuselage length, eq. diameter, cabin dimensions and
    nose diameter
    DESCRIPTION: Runs the above functions to determine the final fuselage di-
    mensions that satisfy the two requirements: Q_fus > Q_r and L_f > L_freq
    '''
    #constraints and constants
    Q_r = Aircraft.ParPayload.m_payload/Aircraft.ParPayload.rho_payload
    A_inr = 0.636
    SFi = SF0
    
    #fineness_f = Struct.fineness_c
    #fineness_n = Struct.fineness_n
    #fineness_t = Struct.fineness_t
    
 
    #iterator
    dSFi = dSF
    
    #initial values
    L_fi = np.sum(GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                                fineness_t, SFi, L_freq))
    D_eq = GetCabinLength(Aircraft, fineness_f, SFi)[1]
    Q_fus = A_inr * SFi * (L_fi - 2 * D_eq)
    
    while L_fi < L_freq or Q_fus < Q_r:
#        print("im in")
        SFi += dSFi
        L_fi = np.sum(GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                                fineness_t, SFi, L_freq))
        D_eq = GetCabinLength(Aircraft, fineness_f, SFi)[1]
        Q_fus = A_inr * SFi * (L_fi -2 * D_eq)
        
    L_fi = GetFuselageLength(Aircraft, fineness_f, fineness_n,
                                     fineness_t, SFi, L_freq)
    D_eq, dim_cabin = GetCabinLength(Aircraft, fineness_f, SFi)[1:]
    D_n = np.sqrt(dim_cabin[0]*dim_cabin[1])
    if D_n < 1.50*1.20:
        D_n = 1.50*1.20
        
#    print (Q_fus, Q_r, L_fi)
    return L_fi, D_eq, dim_cabin, D_n

def FusAreas(Aircraft, L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t):

    config = Aircraft.ParLayoutConfig

    
    l_nose= Useful_for_me(Aircraft,L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t)[0][0]
    l_cabin= Useful_for_me(Aircraft,L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t)[0][1]
    l_tail= Useful_for_me(Aircraft,L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t)[0][2]
    
    h_fuselage=config.h_fuselage
    w_fuselage=config.w_fuselage
    d_fuselage=config.d_fuselage
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
    #print (e,Sw_nose,Sw_cabin,Sw_tail)
    return S_wet

def friction_coef(Aircraft, L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t):
    #INPUT: V_cruise, atmospheric conditions, span, wetted area
    #OUTPUT: friction coefficient
    anfp = Aircraft.ParAnFP
    V = anfp.V_cruise #Cruise speed
    b = anfp.b #Span
    
    mu = 1.43226e-5 #dynamic friction
    rho = 0.0880349 #density
    nu = mu / rho #kinematic friction
    
    S_wet = FusAreas(Aircraft, L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t)
    
    Re = (S_wet / b) * V / nu
    C_fe = 0.00258 + 0.00102*np.exp(-6.28e-9 * Re) + 0.00295*np.exp(-2.01e-8*\
                                   Re)
    return C_fe

def CD0_diff(Aircraft, L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t):
    #INPUT: 
    
    anfp = Aircraft.ParAnFP
    S = anfp.S
    C_fe = friction_coef(Aircraft, L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t)
    S_fus = FusAreas(Aircraft, L_freq, SF0, dSF, fineness_f, fineness_n, fineness_t)
    CD0_fus = C_fe *(S_fus/S)
    return CD0_fus

lst = np.empty((4, 4, 4))

for i in range(0,4):
    fineness_f = 8 + i
    for j in range(0,4):
        fineness_n = 1.2 + i * 0.5
        for k in range(0,4):
            fineness_t = 2 + i
            lst[i][j][k] = CD0_diff(Conv, 24, 2, 0.01, fineness_f, fineness_n ,fineness_t)
            
            
fig = plt.figure()
ax = plt.axes(projection ='3d')
x = lst[0]
y = lst[1]
z = lst[2]
ax.scatter3D(x, y, z);
plt.show()
            
    