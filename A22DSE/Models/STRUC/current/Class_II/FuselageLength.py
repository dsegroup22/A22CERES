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
    
    #constraints
    Q_r = Aircraft.ParPayload.m_payload/Aircraft.ParPayload.rho_payload #volume
    A_inr = 0.636
    
    #design requirements
    ovalrate = 1.75
    D_eq = np.sqrt(A_inr*SF/(np.pi/4))
    h_c = D_eq/np.sqrt(ovalrate)
    w_c = ovalrate*h_c
    
    L_c = D_eq*fineness_f
    
    A_f = np.pi/4*(h_c*w_c)

    Q_fus = A_f * (L_c - 2 * D_eq)
    
    if A_f < A_inr*1.20:
#        print("Combustion engine does not fit in fuselage.")
        return False, False, False
    
    if (Q_fus < Q_r):
#        print("Volume requirement not met")        
        return False, False, False

    return L_c, D_eq, np.array([h_c, w_c])

def GetNoseLength(Aircraft, fineness_n, D_f):
    
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
    
    D_f = GetCabinLength(Aircraft, fineness_f, SF)[1]
    L_t = D_f*fineness_t
#    print (l_t)
    return L_t

def GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                      fineness_t, SF, L_freq):   
    
    L_c, D_c, dim_c = GetCabinLength(Aircraft, fineness_f, SF)

    L_n = GetNoseLength(Aircraft, fineness_n, D_c)
    L_t = GetTailLength(Aircraft, fineness_t, fineness_f, SF)
    if L_c == False or L_n == False:
        return False
    L_total = np.sum([L_c, L_n, L_t])
    
#    print(L_n, L_c , L_t)
    if L_total < L_freq:
#        print("Fuselage length required not met.")
        return np.array([L_n, L_c , L_t])
    return np.array([L_n, L_c , L_t])

def GetTotalFuselageLength(Aircraft, L_freq, SF0, dSF):

    
    Struct = Aircraft.ParStruc
    SFi = SF0
    fineness_f = Struct.fineness_c
    fineness_n = Struct.fineness_n
    fineness_t = Struct.fineness_t
    
    L_fi = np.sum(GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                                fineness_t, SFi, L_freq))
    dSFi = dSF
    
    while L_fi < L_freq:
        SFi += dSFi
        L_fi = np.sum(GetFuselageLength(Aircraft, fineness_f, fineness_n, 
                                fineness_t, SFi, L_freq))

        
    L_req = GetFuselageLength(Aircraft, fineness_f, fineness_n,
                                     fineness_t, SFi, L_freq)
    D_eq, dim_cabin = GetCabinLength(Aircraft, fineness_f, SFi)[1:]
    D_n = np.sqrt(dim_cabin[0]*dim_cabin[1])
    if D_n < 1.50*1.20:
        D_n = 1.50*1.20
    return L_req, D_eq, dim_cabin, D_n

def SurfaceFuselage(Aircraft, L_freq, SF0, dSF, ISA_model):
    
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
    
    
    
    