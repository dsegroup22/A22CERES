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

import numpy as np

def Eliptical(Aircraft,x):
    #function that returns an eliptical lift distribution, where L is the max lift and b the span
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    MTOW=struc.MTOW
    b=anfp.b
    return 4*MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)


def Loading_Diagrams(Aircraft):
    #bs
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    layout=Aircraft.ParLayoutConfig
    prop = Aircraft.ParProp
    #initialise parameters
    b=anfp.b
    m_engine=prop.Engine_weight
    y_engine=layout.y_engine
    x=np.linspace(0,b/2,100)
    dx=b/2/len(x)
    MTOW=struc.MTOW
    m_fuel=struc.FW
    #engines
    V_e=-np.heaviside((x-y_engine),1)*m_engine*g
    #lift
    liftdistr=4*MTOW*g/(np.pi*b)*np.sqrt(1-4*x**2/b**2)
    V_l=[]
    V_l_i=0
    for i in liftdistr:
        i=i+1
        V_l_i=V_l_i+i*dx
        V_l.append(V_l_i)
    #total shear
    V=V_e+np.array(V_l)
    V-=V[-1]
    #moment
    M_l=[]
    M_l_i=0
    for j in V:
        M_l_i=M_l_i+j*dx
        M_l.append(M_l_i)
    M_l-=M_l[-1]
    
    return x,V,np.array(M_l)

    
#
#def V_Diagram(Aircraft):
#    anfp=Aircraft.ParAnFP
#    struc=Aircraft.ParStruc
#    layout=Aircraft.ParLayoutConfig
#    m_engine=layout.m_engine
#    y_engine=layout.y_engine
#    b=anfp.b
#    x=np.linspace(b/2,1000)
#    MTOW=struc.MTOW
#    m_fuel=struc.FW
#    #engines
#    V_e=-np.heaviside((x+y_engine),1)*m_engine*g - np.heaviside(x-y_engine,1)*m_engine*g
#    #fuselage
#    V_f=-np.heaviside(x,1)*(MTOW-2*m_engine)*g
#    #lift
#    liftdistr=MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)
#    dx=b/len(x)
#    V_l=[]
#    V_l_i=0
#    for i in liftdistr:
#        i=i+1
#        V_l_i=V_l_i+i*dx
#        V_l.append(V_l_i)
#    #total shear
#    V=V_e+V_f+np.array(V_l)
#    #moment
#    M_l=[]
#    M_l_i=0
#    for j in V:
#        M_l_i=M_l_i+j*dx
#        M_l.append(M_l_i)
#        
#    
#    return V,np.array(M_l)

















#
#x=np.linspace(-40,40,500)
#y=eliptical(x,100,80)
    
class Diagrams(object):
   def __init__(self, Aircraft):
       self.halfspan = Aircraft.ParAnFP.b/2
       self.Forces = np.ones(8,1)
       self.Positions = np.arange(8)
       self.yrange = np.linspace(0,self.halfspan, 50)
   def VDiagram(self):
       V = np.zeros(self.yrange.shape)
       for i in range(len(self.yrange)):
            V = np.heaviside(self.yrange[i] - self.Positions, 0)*self.Forces
            
       return V
   def MDiagram(self):
       for i in range(len(self.VDiagram())):
           M = np.heaviside(self.yrange[i] - self.Positions, 0)\
           *self.VDiagram()*self.yrange[i]
            
       return M
   def GetForces(self):
       return None
       