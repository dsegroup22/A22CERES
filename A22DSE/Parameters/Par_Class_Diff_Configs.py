# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:30:54 2019

@author: Nout
"""
import sys
import os
#from pathlib import Path
import copy
import numpy as np
#sys.path.append('../')
#os.chdir(Path(__file__).parents[2])
#print(os.getcwd())
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Atmos import Atmos
from A22DSE.Models.POPS.Current.cruisecalculations import (CruiseRange,
                                                           CruiseTime)
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import (
        WSandTW)
from A22DSE.Models.Class_II_Weight.Class_II_Wing import Wing_Geo, Basic_Wing
from A22DSE.Models.Layout.Current.gearlocation_tri import (PrelimCG_ranges,
                                                           PositionsLG_Tri)
from A22DSE.Models.Class_II_Weight.tailsizing import (ctail,ttail)
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_CD0 import CD0
from A22DSE.Models.AnFP.Current.AirfoilSelection.airfoilNASASC20712 import (
        Airfoil)
from A22DSE.Models.AnFP.Current.Class_II.WingDesign.C_L_curve import\
 (C_L_CurveCruise,C_L_CurveLowSpeed)
from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (
        GetTotalFuselageLength, SurfaceFuselage)
#from A22DSE.Models.CostModel.Current.TotalS import SummaryCost
# =============================================================================
#                               ISA MODEL
# =============================================================================
ISA_model = Atmos()

# ===============================CONFIGURATION 1===============================
#                             conventional aircraft
# =============================================================================

Conv = Aircraft()

#Parameters not determined from functionss
Conv.ParAnFP.A = 14.38
Conv.ParAnFP.CD0 = 0.015
Conv.ParAnFP.e = 0.85
Conv.ParAnFP.M_cruise = 0.7
Conv.ParAnFP.Mdd = 0.7
Conv.ParAnFP.T_to = 200000
#Parameters useful to class II estimation
Conv.ParAnFP.n_engines = 2      #Number of wing mounted engines
Conv.ParAnFP.wm_un = 0          #Undercarriage in the wing on (1) or off (0)
#Conv.ParAnFP.CD0 = 0.008
Conv.ParAnFP.We = 2484           #[kg] weight per engine


#parameters from functions

##ANFP parameters
Conv.ParAnFP.s_cruise = CruiseRange(Conv)
Conv.ParAnFP.t_cruise = CruiseTime(Conv, ISA_model)
Conv.ParAnFP.V_cruise = Conv.ParAnFP.Get_V_cruise()
Conv.ParPayload.disperRatePerTime = (Conv.ParPayload.m_payload
/Conv.ParAnFP.t_cruise)
Conv.ParAnFP.Extrarange = 500*10**3 #[m]


Conv.ParStruc.MTOW, Conv.ParStruc.FW, Conv.ParAnFP.S, Conv.ParAnFP.Thrust, Conv.ParAnFP.TtoW, Conv.ParAnFP.WS, \
                    Conv.ParAnFP.dclimbcruise, Conv.ParAnFP.tclimbcruise, Conv.ParAnFP.TWactcruise  = WSandTW(False,Conv,ISA_model)


    
    
#Geometry: Sweep 0.25, le, 0.50 in radians, Span in meters, taper ratio, root, tip , MAC in meters
Conv.ParAnFP.Sweep_25, Conv.ParAnFP.Sweep_LE, Conv.ParAnFP.Sweep_50, Conv.ParAnFP.b,Conv.ParAnFP.taper,\
Conv.ParAnFP.c_r, Conv.ParAnFP.c_t, Conv.ParAnFP.MAC, Conv.ParAnFP.y_MAC = Wing_Geo(Conv)


    
#Airfoil parameters
# =============================================================================
# Conv.ParAnFP.cl_alpha = Airfoil(Conv)[0] #clalpha [/deg]
# Conv.ParAnFP.cl_max = Airfoil(Conv)[1] #maximum lift coefficient of airfoil [-]
# Conv.ParAnFP.tc = Airfoil(Conv)[2] #thickness to chord ratio [-]
# Conv.ParAnFP.CD0_airfoil = Airfoil(Conv)[3] #zero-lift drag [-]
# =============================================================================

Conv.ParAnFP.cl_alpha,Conv.ParAnFP.cl_max,Conv.ParAnFP.tc,Conv.ParAnFP.Cd0, Conv.ParAnFP.cm_0 = Airfoil(Conv)
#Conv.ParAnFP.cl_alpha = clalpha [/deg]
#Conv.ParAnFP.cl_max = maximum lift coefficient of airfoil [-]
#Conv.ParAnFP.tc  thickness to chord ratio [-]
#Conv.ParAnFP.Cd0 zero-lift drag [-]

Conv.ParAnFP.LD_airfoil = 90 #lift to drag ratio [-] at Cldes = 0.55 obtained from graph of Cl/Cd




#PRELIMINAIRY ENGINE POSITION
Conv.ParLayoutConfig.y_loc_eng = Conv.ParAnFP.b/8#b/3 #[m] DUMMY VALUE

#PRELIMINAIRY FUSELAGE DESIGN
Layout = Conv.ParLayoutConfig
#Struct = Conv.ParStruc
#Layout.l_fuselage = 24 #[m] length of fuselage
Layout.l_fuselage, Layout.d_fuselage, Layout.dim_cabin, Layout.d_cockpit = (
        GetTotalFuselageLength(Conv, 24, 2, 0.01))
Layout.l_fuselage = np.sum(Layout.l_fuselage)

Layout.h_fuselage = Layout.dim_cabin[0]
Layout.w_fuselage = Layout.dim_cabin[1]



#Wing lift curve (d_fuselage needed)
Conv.ParAnFP.C_L_alpha_slow,Conv.ParAnFP.C_L_max_slow,\
Conv.ParAnFP.alpha_stall_slow=C_L_CurveLowSpeed(Conv)[1:] #all in radians where applicable
Conv.ParAnFP.C_L_alpha_cruise,Conv.ParAnFP.C_L_max_cruise,\
Conv.ParAnFP.alpha_stall_cruise=C_L_CurveCruise(Conv)[1:] #all in radians where applicable

#Horizontal, Vertical tail design

Conv.ParLayoutConfig.Sht,Conv.ParLayoutConfig.xht,\
Conv.ParLayoutConfig.Aht,Conv.ParLayoutConfig.trht,\
Conv.ParLayoutConfig.Sweep25ht,Conv.ParLayoutConfig.Wht,\
Conv.ParLayoutConfig.Svt,Conv.ParLayoutConfig.xvt,\
Conv.ParLayoutConfig.Avt,Conv.ParLayoutConfig.trvt,\
Conv.ParLayoutConfig.Sweep25vt,Conv.ParLayoutConfig.Wvt = ctail(Conv)




#preliminairy positions for tricycle landing gear (nose and main)
Conv.ParLayoutConfig.x_cg= PrelimCG_ranges(Conv) 
Conv.ParLayoutConfig.lg_l_main,Conv.ParLayoutConfig.lg_l_nose,\
Conv.ParLayoutConfig.lg_y_main, Conv.ParLayoutConfig.lg_x_main,\
Conv.ParLayoutConfig.lg_x_nose_min_F_n, Conv.ParLayoutConfig.lg_x_nose_max_F_n,\
Conv.ParLayoutConfig.lg_x_nose,Conv.ParLayoutConfig.lg_y_nose,\
Conv.ParLayoutConfig.z_cg = PositionsLG_Tri(Conv)


Conv.ParLayoutConfig.m_engine = 5000 # [kg] DUMMY VALUE
Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%


def ComputeCD0(Aircraft):
#DETERMINE CD0, AND ITERATE FOR THE MTOW ETC.
    error = 1
    while error > 10e-3:
        Sold = Aircraft.ParAnFP.S
        AnFP = Aircraft.ParAnFP
        
        AnFP.CD0 = CD0(Aircraft)[0]
        Aircraft.ParStruc.MTOW, Aircraft.ParStruc.FW, AnFP.S, AnFP.Thrust,\
        AnFP.TtoW,AnFP.WS,AnFP.dfinal,AnFP.tfinal, , Conv.ParAnFP.TWactcruise\
        = WSandTW(False,Aircraft,ISA_model)
    
        
        AnFP.Sweep_25, AnFP.Sweep_LE, AnFP.Sweep_50, \
        AnFP.b, AnFP.taper, AnFP.c_r, AnFP.c_t,\
        AnFP.MAC,AnFP.y_MAC = Wing_Geo(Aircraft)
        
        error = abs((AnFP.S-Sold)/Sold)
    CD0_opt = AnFP.CD0
    return CD0_opt
Conv.ParAnFP.CD0 = ComputeCD0(Conv)
#Horizontal, Vertical tail design

Conv.ParLayoutConfig.Sht,Conv.ParLayoutConfig.xht,\
Conv.ParLayoutConfig.Aht,Conv.ParLayoutConfig.trht,\
Conv.ParLayoutConfig.Sweep25ht,Conv.ParLayoutConfig.Wht,\
Conv.ParLayoutConfig.Svt,Conv.ParLayoutConfig.xvt,\
Conv.ParLayoutConfig.Avt,Conv.ParLayoutConfig.trvt,\
Conv.ParLayoutConfig.Sweep25vt,Conv.ParLayoutConfig.Wvt = ttail(Conv)

 

# =============================================================================
#                              CANARD CONFIGURATION
# =============================================================================
# =============================================================================
# 
# Can = Aircraft()
# 
# 
# #Parameters not determined from functionss
# Can.ParAnFP.A = 20.51
# Can.ParAnFP.CD0 = 0.02
# Can.ParAnFP.e = 0.85
# Can.ParAnFP.M_cruise = 0.7
# Can.ParAnFP.Mdd = 0.7
# Can.ParAnFP.T_to = 200000
# Can.ParAnFP.Sweep25 = 18.      #[deg] Sweep at quarter chord
# #Parameters useful to class II estimation
# Can.ParAnFP.n_engines = 2      #Number of wing mounted engines
# Can.ParAnFP.wm_un = 0          #Undercarriage in the wing on (1) or off (0)
# #Can.ParAnFP.CD0 = 0.008
# Can.ParAnFP.We = 3000           #[kg] weight per engine      
# 
# 
# 
# 
# Can.ParAnFP.s_cruise = CruiseRange(Can)
# Can.ParAnFP.t_cruise = CruiseTime(Can, ISA_model)
# Can.ParAnFP.V_cruise = Can.ParAnFP.Get_V_cruise()
# Can.ParPayload.disperRatePerTime = (Can.ParPayload.m_payload
# /Can.ParAnFP.t_cruise)
# Can.ParAnFP.Extrarange = 500*10**3 #[m]
# 
# Can.ParStruc.MTOW, Can.ParStruc.FW, Can.ParAnFP.S, Can.ParAnFP.Thrust, Can.ParAnFP.TtoW, Can.ParAnFP.WS  = WSandTW(False,Can,ISA_model)
# 
# #Added for CD0
# Can.ParLayoutConfig.d_fuselage = 3 #[m] DUMMY VALUE
# Can.ParLayoutConfig.l_fuselage = 24 #[m] DUMMY VALUE
# Can.ParAnFP.tc = Conv.ParAnFP.tc #thickness to chord ratio [-]
# #Geometry: Sweep 0.25, le, 0.50 in radians, 
# #Span in meters, taper ratio, root, tip , MAC in meters
# Can.ParAnFP.Sweep_25, Can.ParAnFP.Sweep_LE, Can.ParAnFP.Sweep_50, \
# Can.ParAnFP.b, Can.ParAnFP.taper, Can.ParAnFP.c_r, Can.ParAnFP.c_t, \
# Can.ParAnFP.MAC, Conv.ParAnFP.y_MAC = Wing_Geo(Can)
# Can.ParLayoutConfig.Sht = 0
# Can.ParLayoutConfig.Svt = 0
# 
# error = 1
# 
# 
# while error > 10e-3:
#     sold = Can.ParAnFP.S
#     Can.ParAnFP.CD0 = CD0(Can)[0]
#     Can.ParStruc.MTOW, Can.ParStruc.FW, Can.ParAnFP.S, Can.ParAnFP.Thrust, Can.ParAnFP.TtoW, Can.ParAnFP.WS  = WSandTW(False,Can,ISA_model)
#     Can.ParAnFP.Sweep_25, Can.ParAnFP.Sweep_LE, Can.ParAnFP.Sweep_50, Can.ParAnFP.b, Can.ParAnFP.taper, Can.ParAnFP.c_r, Can.ParAnFP.c_t, Can.ParAnFP.MAC, Conv.ParAnFP.y_MAC = Wing_Geo(Can)
#     error = abs((Can.ParAnFP.S-sold)/sold)
# 
# 
# 
# =============================================================================


# =============================================================================
# 
# =============================================================================

# =============================TEST AC FOR SENSITIVITY=========================
SensTestAc = copy.deepcopy(Conv)
# =============================================================================

