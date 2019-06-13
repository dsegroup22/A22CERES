# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:49:51 2019

@author: hksam
"""

import numpy as np
import sys
sys.path.append('../../../../../../')
import numpy as np
import scipy.linalg as slin
import matplotlib.pyplot as plt
import control.matlab as control
import A22DSE.Models.STRUC.current.Structural_Model.struc_functions as StrucFun

class airfoilAE(object):
    '''
    Kh = bending stiffness; Ktheta = torsional stiffness; xtheta = displacement
    of CG from EA; S = reference area; chord length is at 75% of span
    
    SUSPECT TO CHANGE SINCE ITHETA, STHETA ARE TBD.
    '''
    def __init__(self, mass, c, Kh, Ktheta, xtheta, rtheta, CLtheta, 
                 CMacdelta, Aircraft):
        
        self.m  = mass
        self.c  = c
        self.xtheta = xtheta * c
        self.b  = self.c/2                              # half-chord
        self.Kh = Kh                                    #
        self.Ktheta = Ktheta * c                        #
        self.Stheta = self.m * self.xtheta * self.b     #
        self.rtheta = rtheta * c                        #
        self.Itheta = self.m*(self.rtheta*self.b)**2    #
        self.e      = 0.3                               # [-]
        self.S      = Aircraft.ParAnFP.S / c            # [m²]
        self.CLa    = Aircraft.ParAnFP.C_L_alpha_cruise #[rad^(-1)]
        self.CLtheta = CLtheta                          # -1.8 / rad
        self.CMacdelta = CMacdelta                      #

def Init2DOFSS(par, Aircraft, ISA_model):
    
    # Constants
    RegFact = 1.15
    
    
    M = np.matrix([[par.m, par.Stheta],
               [par.Stheta, par.Itheta]])
    K = np.matrix([[par.Kh, 0], [0, par.Ktheta]])
    A0 = np.matrix([[0 -1* par.S * par.CLa],
                    [0, 2 * par.S * par.e * par.b * par.CLa]])

    V = np.min([Aircraft.ParAnFP.V_cruise*RegFact, Aircraft.ParAnFP.V_dive])
    q = 0.5*ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[-1] * V**2

    def ComputeConstants():
        a4 = par.m * par.Itheta - par.Stheta**2
        a0 = par.Kh * (par.Ktheta -2 * par.e * par.b * q * par.S * par.CLa)
        a2 = (par.m * par.Ktheta + par.Itheta * par.Kh - (2* par.m * par.e *
              par.b + par.Stheta) * q * par.S * par.CLa)
        
        return a0, a2, a4
    
    a0, a2, a4 = ComputeConstants()
    
    return M, K, A0, a0, a2, a4


def ComputeDivSpeed(par, height, ISA_model):
    '''
    INPUT: --
    OUTPUT: returns Divergence Speed
    DESCRIPTION: Divergence speed is the speed at which the aerodynamic forces
    result in unstable or marginally stable aircraft.
    '''
    q = par.Ktheta/(par.CLa * par.e * par.c * par.S)
    T, p, rho = ISA_model.ISAFunc([height])
    
    return np.sqrt(q/(0.5*rho))

def ComputeControlReversal(par, height, ISA_model):

    q = -par.CLtheta * par.Ktheta / (par.CLa * par.CMacdelta * par.c * par.S)
    T, p, rho = ISA_model.ISAFunc([height])
    
    return np.sqrt(q/(0.5*rho))

def ComputeFlutter(par, height, ISA_model):
    
    # Dynamic Pressure
    T, p, rho = ISA_model.ISAFunc([height])
    q = 0.5 * rho
    
    # Compute Natural Frequencies
    w_h = np.sqrt(par.Kh / par.m)
    w_theta = np.sqrt(par.Ktheta / par.Itheta)
    
    whwtheta = w_h/w_theta
    
    # two conditions 
    REQ1 = par.xtheta * (par.xtheta + 2 * par.e - 2 * par.e * (whwtheta)**2 * \
                         (1 + 2 * par.e * par.xtheta / par.rtheta**2))
    
    REQ2 = par.xtheta + 2 * par.e + whwtheta**2 * (par.xtheta - 2 * par.e + 
            4 * par.e * (par.xtheta / par.rtheta)**2)
    
#    print(REQ1, REQ2)
    
    # Determine Constants
    C0 = (1 - (whwtheta)**2)**2 + 4 * (par.xtheta / par.rtheta)**2 * \
    whwtheta**2
    C1 = -2 * (par.xtheta + 2 * par.e + whwtheta**2 * (par.xtheta - 2 * par.e \
                + 4 * par.e * par.xtheta**2/par.rtheta**2))
    C2 = (par.xtheta + 2 * par.e)**2
    
    Q1 = (-C1 + np.sqrt(C1**2 -4 * C2 * C0))/(2 * C2)
    Q2 = (-C1 - np.sqrt(C1**2 -4 * C2 * C0))/(2 * C2)
    print(Q1, Q2)
    if np.isnan(Q1) or np.isnan(Q2):
        return None
    
    q1 = Q1 / (par.S * par.b * par.CLa) * par.Ktheta
    q2 = Q2 / (par.S * par.b * par.CLa) * par.Ktheta
    
    q1 = q1/q
    q2 = q1/q
    
    return np.sqrt(q1), np.sqrt(q2)
    
    

    


