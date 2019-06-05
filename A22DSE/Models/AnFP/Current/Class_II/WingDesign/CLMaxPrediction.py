# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:15:25 2019

@author: tomhu
"""

"""CRITICAL SECTION METHOD"""
"""
INPUTS: Re, Mach, span
OUTPUTS: CLMAX, AOA@CLMAX
Method: give the clmax(airfoil) at every section (here it's the same 
everywhere), compute for a range of AOA the CL distribution, check if they
are within a margin prior specified. Here the VLM used will be XFLR5 and data 
from NASA SC(2)-0712
"""
#import os
#from pathlib import Path
##import copy
#os.chdir(Path(__file__).parents[6])
#from A22DSE.Parameters.Par_Class_Conventional import Conv
#import matplotlib.pyplot as plt
#import numpy as np


#print(os.getcwd())

#def GetRe(rho, V, L, Visc):
#    Re = rho*V*L/Visc
#    return Re
#
#rho = [1.225, Conv.ParAnFP.rho_cruise]
#V = [84,109,206]
#L = [Conv.ParAnFP.c_t,Conv.ParAnFP.c_r]
#Visc = [1.802*10**-5 , 10**-5]
#R = 287
#T = [15+273.15, 216.650]
#gamma = 1.4
#
#Re = []
#M = []
#for i in range(len(rho)):
#    for Vi in V:
#        for Li in L:
#            Re.append(GetRe(rho[i], Vi, Li, Visc[i]))
#            M.append(Vi/(R*T[i]*gamma)**0.5)
#plot = False
#            
#if plot:
#    plt.figure(1)
#    plt.scatter(np.arange(len(Re)),Re)
#    plt.grid()
#    plt.figure(2)
#    plt.scatter(np.arange(len(M)),M)
#    plt.grid()
#    plt.show()
#    print(min(Re),max(Re))
    
    
"""Philips Alley Method"""

class CLMAX (object):
    def __init__(self, Aircraft):
        self.CL_cl = 0.69
        self.sweep = Aircraft.ParAnFP.Sweep_25
        self.AR = Aircraft.ParAnFP.A
        self.CLa = Aircraft.ParAnFP.C_L_alpha_cruise
        self.Omega = 0        
        self.kLam1 = 0.25
        self.kLam2 = 0.6
        self.Clmax = Aircraft.ParAnFP.cl_max
        self.CL_Clmax = self.CL_cl*self.Clmax
        self.CL_Clmax_noOm = self.CL_Clmax
        self.kLs = CLMAX.GetkLs(self)
        self.kLlam = CLMAX.GetkLlam(self)
        self.kLOmega = CLMAX.GetkLOmega(self)
        
        
    def GetCLMAX(self):
        
        if self.Omega == 0:
            CLMAXi = self.CL_cl * self.kLs*self.kLlam*(self.Clmax)
        else:
            CLMAXi = self.CL_cl * self.kLs*self.kLlam\
            *(self.clmax-self.kLOmega*self.CLa * self.Omega)
        return CLMAXi  
    
    
    def GetkLs(self):
        
        kLs = 1 + (0.0042*self.AR - 0.068)*(1+2.3*self.CLa)*self.Omega\
        /self.Clmax
        return kLs        
    
    def GetkLlam(self):
        kLlam = 1 + self.kLam1*self.sweep - self.kLam2*self.sweep**1.2
        return kLlam
    
    def GetkLOmega(self):
        if self.Omega ==0: #since if Omega is zero, there would be a divide
            # by zero error
            return 0
        else: 
            kLOmega = (1-self.CL_Clmax/self.CL_Clmax_noOm)/(self.CLa\
                      *self.Omega/self.Clmax)
            return kLOmega
        
        
        
        
        
        
        
        
        
        
        