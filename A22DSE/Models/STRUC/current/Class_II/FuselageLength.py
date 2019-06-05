# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:53:40 2019

@author: hksam
"""

import sys
sys.path.append('../../../../../')
import numpy as np


# =============================================================================
#                           WORK IN PROGRESS
# =============================================================================

def GetCabinLength(Aircraft, fineness_f, SF):
    '''
    INPUT: Aircraft object, float fuselage fineness ratio, size factor (SF)
    OUTPUT: returns cabin length, eq. diameter, and cabin dimensions
    DESCRIPTION: Computes the required cabin length for given fineness ratio.
    The cross-section must be larger than the required inlet area. Therefore,
    A_inr is multiplied by a constant SF which increments the cross-section
    for the desired fineness ratio.
    '''
    #constraints
#    Q_r = Aircraft.ParPayload.m_payload/Aircraft.ParPayload.rho_payload #volume
    A_inr = 0.636
    
    #design requirements
    ovalrate = 1.75
    D_eq = np.sqrt(A_inr*SF/(np.pi/4))
    h_c = D_eq/np.sqrt(ovalrate)
    w_c = ovalrate*h_c
    
    L_c = D_eq*fineness_f
    
#    A_f = np.pi/4*(h_c*w_c)
#    if A_f < A_inr*1.20:
#        print("Combustion engine does not fit in fuselage.")

    return L_c, D_eq, np.array([h_c, w_c])

def GetNoseLength(Aircraft, fineness_n, D_f):
    '''
    INPUT: Aircraft object, float nose fineness ratio, eq. diameter of the cab-
    in fuselage.
    OUTPUT: length of the nose section of the fuselage.
    DESCRIPTION: Given a fineness ratio, returns the nose section length. If
    the eq. diameter of the cabin is smaller than the req. height of the cock-
    pit, then the length shall instead be based on the minimum cockpit height.
    '''
    # minimum req. :
    UF = 1.20
    pax_height = 1.50*UF
    
    
    L_n = fineness_n*D_f
    if D_f < pax_height:
#        print ("Tiny cockpit")
        L_n = fineness_n*pax_height
        return L_n
#    print (l_n)    
    return L_n

def GetTailLength(Aircraft, fineness_t, fineness_f, SF):
    '''
    INPUT: Aircraft object, float tail fineness ratio, cabin fineness ratio,
    size factor
    OUTPUT: returns tail length
    DESCRIPTION: based on the fineness ratio of the tail, returns the length of
    the tail section.
    '''    
    D_f = GetCabinLength(Aircraft, fineness_f, SF)[1]
    L_t = D_f*fineness_t
#    print (l_t)
    return L_t

def GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                      fineness_t, SF, L_freq):   
    '''
    INPUT: Aircraft object, all fineness ratios, size factor, required fuselage
    length
    OUTPUT: Numpy array of the section lengths
    DESCRIPTION: Calls the three functions that compute the section lengths and
    returns an array of the section lengths. Pretty redundant function IMO.
    '''    
    L_c, D_c, dim_c = GetCabinLength(Aircraft, fineness_f, SF)

    L_n = GetNoseLength(Aircraft, fineness_n, D_c)
    L_t = GetTailLength(Aircraft, fineness_t, fineness_f, SF)
    
    if L_c == False or L_n == False:
        return False
    
#    L_total = np.sum([L_c, L_n, L_t])
#    if L_total < L_freq:
#        print("Fuselage length required not met.")
#        return np.array([L_n, L_c , L_t])
    
    return np.array([L_n, L_c , L_t])


def GetTotalFuselageLength(Aircraft, L_freq, SF0, dSF):
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
    Struct = Aircraft.ParStruc
    SFi = SF0
    fineness_f = Struct.fineness_c
    fineness_n = Struct.fineness_n
    fineness_t = Struct.fineness_t
    
 
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



def SurfaceFuselage(Aircraft, L_freq, SF0, dSF, ISA_model):
    '''
    INPUT: Aircraft object, req. fuselage length, initial size factor,
    step size, ISA model
    OUTPUT: Returns fuselage weight
    DESCRIPTION: Computes the fuselage weight according to Torenbeek Aircraft
    Design.
    '''    
    L_f, D_eq, dim_cabin, D_n = GetTotalFuselageLength(Aircraft, L_freq, SF0,
                                                         dSF)
    
#    def ComputeSh(Sw):
#        return 0.2917*Sw - 1.16666
#    Sh = ComputeSh(Aircraft.ParAnFP.S)      

    L_n, L_c, L_t = L_f
#    print (L_n, L_c, L_t)
    kwf = 0.23
    V_D = 1.4*eas(Aircraft, ISA_model)
    l_t = Aircraft.ParLayoutConfig.xht
    
    S_n = np.pi*D_n*L_n
    S_c = np.pi*D_eq*L_c
    S_t = np.pi*D_eq*L_t
    SG = S_n+S_c+S_t
        
    Wf = (kwf*np.sqrt(V_D*l_t/(np.sum(dim_cabin)))*SG**1.2)
    return Wf
    
def eas(Aircraft, ISA_model):
    Vc = Aircraft.ParAnFP.V_cruise
    AtmosCruise = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])
    ConversTool = Aircraft.ConversTool
    Vkeas=Vc*np.sqrt(AtmosCruise[2]/ISA_model.rho0)/ConversTool.kts2ms
    return Vkeas
    
    
    
    