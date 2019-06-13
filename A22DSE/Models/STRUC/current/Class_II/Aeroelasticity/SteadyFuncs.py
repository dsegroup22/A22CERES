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

class airfoilAE(object):
    '''
    Kh = bending stiffness; Ktheta = torsional stiffness; xtheta = displacement
    of CG from EA; S = reference area; chord length is at 75% of span
    
    SUSPECT TO CHANGE SINCE ITHETA, STHETA ARE TBD.
    '''
    def __init__(self, mass, Kh, Ktheta, xtheta, rtheta, Aircraft):
        
        self.m  = mass
        self.xtheta = xtheta
        self.c  = Aircraft.ParAnFP.c_r/Aircraft.ParAnFP.c_t*0.75 
        self.b  = self.c/2                                   # half-chord
        self.Kh = Kh                                    #
        self.Ktheta = Ktheta                            #
        self.Stheta = self.m * self.xtheta * self.b     #
        self.rtheta = rtheta * self.b                   #
        self.Itheta = self.m*(self.rtheta*self.b)**2   #
        self.e      = Aircraft.ParAnFP.e                # [-]
        self.S      = 2 * self.b                        # [m²]
        self.CLa    = Aircraft.ParAnFP.cl_alpha         #[rad^(-1)]
        
    

def Init2DOFSS(par, Aircraft, ISA_model):
    
    M = np.matrix([[par.m, par.Stheta],
               [par.Stheta, par.Itheta]])
    K = np.matrix([[par.Kh, 0], [0, par.Ktheta]])
    A0 = np.matrix([[0 -1* par.S * par.CLa],
                    [0, 2 * par.S * par.e * par.b * par.CLa]])

    q = 0.5*ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[-1]* \
    Aircraft.ParAnFP.V_cruise
    
    def ComputeConstants():
        a4 = par.m * par.Itheta - par.Stheta**2
        a0 = par.Kh * (par.Ktheta -2 * par.e * par.b * q * par.S * par.CLa)
        a2 = (par.m * par.Ktheta + par.Itheta * par.Kh - (2* par.m * par.e *
              par.b + par.Stheta) * q * par.S * par.CLa)
        
        return a0, a2, a4
    
    a0, a2, a4 = ComputeConstants()
    return M, K, A0, a0, a2, a4