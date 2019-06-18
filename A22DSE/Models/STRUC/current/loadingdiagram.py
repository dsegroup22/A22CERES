# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:51:16 2019

@author: rickv
"""

#loading diagrams
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def Eliptical(Aircraft,steps):
    #function that returns an eliptical lift distribution, where L is the max lift and b the span
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    MTOW=struc.MTOW
    b=anfp.b
    return 4*MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)


def Loading_Diagrams(Aircraft,steps):
    #bs
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    layout=Aircraft.ParLayoutConfig
    prop = Aircraft.ParProp
    #initialise parameters
    b=anfp.b
    m_engine=prop.Engine_weight
    y_engine1=layout.y_engine
    y_engine2=10 #dummy
    y_engine3=15 #dummy
    x=np.linspace(-b/2,b/2,steps)
    dx=b/steps
    MTOW=struc.MTOW
    m_fuel=struc.FW
    g=9.81
    #engines
    V_e1=-np.heaviside((x-y_engine1),1)*m_engine
    V_e2=-np.heaviside((x-y_engine2),1)*m_engine
    V_e3=-np.heaviside((x-y_engine3),1)*m_engine
    V_e4=-np.heaviside((x+y_engine1),1)*m_engine
    V_e5=-np.heaviside((x+y_engine2),1)*m_engine
    V_e6=-np.heaviside((x+y_engine3),1)*m_engine
    V_e=V_e1+V_e2+V_e3+V_e4+V_e5+V_e6
    #lift
    liftdistr=4*MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)
    V_l=[]
    V_l_i=0
    for i in liftdistr:
        i=i+1
        V_l_i=V_l_i+i*dx
        V_l.append(V_l_i)
    #fuselage
    w_fuselage=V_l[-1]-6*m_engine
    V_f=-np.heaviside(x,1)*w_fuselage
    #total shear
    V=V_e+V_f+V_e+V_l
    #moment
    M=[]
    M_l_i=0
    for j in V:
        M_l_i=M_l_i+j*dx
        M.append(M_l_i)
    
    return x, M

       