# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:52:35 2019

@author: hksam
"""
import numpy as np
import sys
sys.path.append('../')
from All_dic_Parameters import Parameters as par


#!!!NOTE: MTOW is lbs

def Wampr(MTOW):
    return 10**(0.1936+0.8645*np.log10(MTOW)) #AMPR weight

def MHRManProg(MTOW, Vmax, Nprogram):
    MHRman_prog = 28.984 * np.power(Wampr(MTOW), 0.740) *\
    np.power(Vmax,0.543) * np.power(Nprogram, 0.524) * par.get("Fdiff")

    return MHRman_prog

def MHRToolProg(MTOW, Wampr, Vmax, Nprogram, Nrm):
    cost = 4.0127*Wampr(MTOW)**0.764*Vmax**.899*Nprogram**0.178*Nrm**0.066* \
            par.get('Fdiff') 

    return cost

def MHRmanr(MTOW,Vmax,Nrdte,Fdiff):
    return 28.984*Wampr(MTOW)**0.740*Vmax**0.543*Nrdte**0.524*Fdiff

def cmat(MTOW,Vmax,Nrdte, Fmat):
    cost= 37.632*Fmat*Wampr(MTOW)**0.689*Vmax**0.624*Nrdte**0.792\
    *par.get('CEF7019')
    return cost

def MHRtoolr(MTOW,Vmax,Nrdte,Nrr,Fdiff):
    return 4.0127*Wampr(MTOW)**0.764*Vmax**0.899*Nrdte**0.178*Nrr**0.066*Fdiff

def eas(Vc):
    Vkeas=Vc*np.sqrt(par.get('rho_cruise')/par.get('rho_SL'))/par.get('kts2ms')
    return Vkeas
