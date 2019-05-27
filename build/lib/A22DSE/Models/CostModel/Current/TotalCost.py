# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:37:22 2019

@author: hksam
"""
from Raskom import crdte
from ProdCost import CmanFunc, CproMFunc, CapcMFunc
import numpy as np
import sys
sys.path.append('../')
from All_dic_Parameters import Parameters as par

# =============================================================================
#                                   Constants
# =============================================================================
MTOW = 150000 #kg
Vc   = 210  # m/s
Cer  = 3.5*10**7 # USD19
Nprogram = 350 # Number of aircraft
N_Engine = 4
# !!! NOTE: Nprogram == N_m
# =============================================================================
#                                       R&D
# =============================================================================
RnDCost = crdte(MTOW, Vc, Cer)[-1]/10**9

# =============================================================================
#                                   Production
# =============================================================================
CapcM = CapcMFunc(MTOW, Vc, Nprogram, Cer, N_Engine, Nprogram)
Cman  = CmanFunc(MTOW, Vc, Nprogram, Cer, N_Engine, Nprogram)
CproM = CproMFunc(Cman)
ProdPerACCost = CapcM/Nprogram/10**6
ManPerACCost  = Cman/Nprogram
# =============================================================================
#                                   Operations
# =============================================================================
# =============================================================================
#                                   EoL
# =============================================================================
