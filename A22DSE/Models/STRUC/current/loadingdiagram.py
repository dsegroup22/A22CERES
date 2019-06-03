# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:51:16 2019

@author: rickv
"""

#loading diagrams

import numpy as np

#eliptical lift distribution
def eliptical(L,b):
    #function that returns an eliptical lift distribution, where L is the max lift and b the span
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    b=anfp.span
    x=np.linspace(-b/2,b/2,1000)
    return L**2*(1-(x*2/b)**2)**0.5

def Eliptical(Aircraft):
    #function that returns an eliptical lift distribution, where L is the max lift and b the span
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    MTOW=struc.MTOW
    b=anfp.b
    x=np.linspace(0,b/2,1000)
    return MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)

def V(Aircraft,m_engine,y_engine,L,b,g):
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    b=anfp.span
    x=np.linspace(-b/2,b/2,1000)
    OEW=struc.MTOW
    m_fuel=struc.FW
    #engines
    V_e=-np.heaviside((x+y_engine),1)*m_engine*g - np.heaviside(x-y_engine,1)*m_engine*g
    #fuselage
    V_f=-np.heaviside(x,1)*(OEW-2*m_engine)*g
    #lift
    liftdistr=eliptical(L,b)
    dx=b/len(x)
    V_l=[]
    V_l_i=0
    for i in liftdistr:
        i=i+1
        V_l_i=V_l_i+i*dx
        V_l.append(V_l_i)
    #total shear
    V=V_e+V_f+np.array(V_l)
    #moment
    M_l=[]
    M_l_i=0
    for j in V:
        M_l_i=M_l_i+j*dx
        M_l.append(M_l_i)
        
    
    return V,np.array(M_l)

    


















#
#x=np.linspace(-40,40,500)
#y=eliptical(x,100,80)