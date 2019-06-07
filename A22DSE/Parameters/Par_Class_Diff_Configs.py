# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:30:54 2019

@author: Nout
"""
import sys
import os
from pathlib import Path
import copy
import numpy as np
#sys.path.append('../')
os.chdir(Path(__file__).parents[2])
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
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_def_InitsizingUncoupled\
 import WingSurface_Thrust_FuelWeight
from A22DSE.Models.AnFP.Current.Class_II.WingDesign.CLMaxPrediction \
import CLMAX
from A22DSE.Models.AnFP.Current.InitialSizing.Sweep import wing_sweep

#from A22DSE.Models.CostModel.Current.TotalS import SummaryCost
# =============================================================================
#                               ISA MODEL
# =============================================================================
ISA_model = Atmos()

# ===============================CONFIGURATION 1===============================
#                             conventional aircraft
# =============================================================================

Conv = Aircraft()


def ComputeCD0(Aircraft):
#DETERMINE CD0, AND ITERATE FOR THE MTOW ETC.
    error = 1
    while error > 10e-3:
        Sold = Aircraft.ParAnFP.S
        AnFP = Aircraft.ParAnFP
        
        AnFP.CD0 = CD0(Aircraft)[0]
# =============================================================================
#         Aircraft.ParStruc.MTOW, Aircraft.ParStruc.FW, AnFP.S, AnFP.Thrust,\
#         AnFP.TtoW,AnFP.WS,AnFP.dfinal,AnFP.tfinal,Conv.ParAnFP.TWactcruise\
#         = WSandTW(False,Aircraft,ISA_model)
# =============================================================================
        
        WingSurface_Thrust_FuelWeight(Conv)
    
        
        AnFP.Sweep_25, AnFP.Sweep_LE, AnFP.Sweep_50, \
        AnFP.b, AnFP.taper, AnFP.c_r, AnFP.c_t,\
        AnFP.MAC,AnFP.y_MAC = Wing_Geo(Aircraft)
        
        error = abs((AnFP.S-Sold)/Sold)
    CD0_opt = AnFP.CD0
    return CD0_opt
    

def ClassIAircraft():
    #Parameters not determined from functionss
    Conv.ParAnFP.A = 14.38
    Conv.ParAnFP.CD0 = 0.015
    Conv.ParAnFP.e = 0.85
    Conv.ParAnFP.M_cruise = 0.7
    Conv.ParAnFP.Mdd = 0.7
    Conv.ParAnFP.T_to = 200000
    #Parameters useful to class II estimation
    Conv.ParAnFP.wm_un = 0          #Undercarriage in the wing on (1) or off (0)
    #Conv.ParAnFP.CD0 = 0.008
    Conv.ParProp.Engine_weight = 2484           #[kg] weight per engine
    Conv.ParAnFP.tc = 0.12

    
    
    #parameters from functions
    
    ##ANFP parameters
    Conv.ParAnFP.Sweep25 = wing_sweep(Conv)
    Conv.ParAnFP.s_cruise = CruiseRange(Conv)
    Conv.ParAnFP.t_cruise = CruiseTime(Conv, ISA_model)
    Conv.ParAnFP.V_cruise = Conv.ParAnFP.Get_V_cruise()
    Conv.ParPayload.disperRatePerTime = (Conv.ParPayload.m_payload
    /Conv.ParAnFP.t_cruise)
    Conv.ParAnFP.Extrarange = 500*10**3 #[m]
    
    
    Conv.ParStruc.MTOW, Conv.ParStruc.FW, Conv.ParAnFP.S, Conv.ParAnFP.Thrust, Conv.ParAnFP.TtoW, Conv.ParAnFP.WS, \
                        Conv.ParAnFP.dclimbcruise, Conv.ParAnFP.tclimbcruise, Conv.ParAnFP.TWactcruise  = WSandTW(False,Conv,ISA_model)
    
    Conv.ParStruc.wfratio = Conv.ParStruc.FW/Conv.ParStruc.MTOW
    
def ClassI_AndAHalf():

    #Geometry: Sweep 0.25, le, 0.50 in radians, Span in meters, taper ratio, root, tip , MAC in meters
    Conv.ParAnFP.Sweep_25, Conv.ParAnFP.Sweep_LE, Conv.ParAnFP.Sweep_50, Conv.ParAnFP.b,Conv.ParAnFP.taper,\
    Conv.ParAnFP.c_r, Conv.ParAnFP.c_t, Conv.ParAnFP.MAC, Conv.ParAnFP.y_MAC = Wing_Geo(Conv)
    


    

    Conv.ParAnFP.cl_alpha,Conv.ParAnFP.cl_max,Conv.ParAnFP.tc,Conv.ParAnFP.Cd0,\
    Conv.ParAnFP.cm_0 = Airfoil(Conv)
    Conv.ParAnFP.Sweep25 = wing_sweep(Conv)
    
    Conv.ParAnFP.LD_airfoil = 90 #lift to drag ratio [-] at Cldes = 0.55 obtained from graph of Cl/Cd
    
    
    
    
    #PRELIMINAIRY ENGINE POSITION
    Conv.ParLayoutConfig.y_loc_eng = Conv.ParAnFP.b/8#b/3 #[m] DUMMY VALUE
    
    #PRELIMINAIRY FUSELAGE DESIGN
    Layout = Conv.ParLayoutConfig
    #Struct = Conv.ParStruc
    #Layout.l_fuselage = 24 #[m] length of fuselage
    Layout.l_fuselage, Layout.d_fuselage, Layout.dim_cabin, Layout.d_cockpit = (
            GetTotalFuselageLength(Conv, 40, 2, 0.01))
    
    Layout.l_nose,Layout.l_cabin,Layout.l_tail=Layout.l_fuselage
    Layout.l_fuselage = np.sum(Layout.l_fuselage)
    
    Layout.h_APU=0.2 #[m] dummy value
    
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
    Layout.c_rht,Layout.c_tht,Layout.bh,\
    Conv.ParLayoutConfig.Sweep25ht,Conv.ParLayoutConfig.Wht,\
    Conv.ParLayoutConfig.Svt,Conv.ParLayoutConfig.xvt,\
    Conv.ParLayoutConfig.Avt,Conv.ParLayoutConfig.trvt,\
    Layout.c_rvt,Layout.c_tvt,Layout.bv,\
    Conv.ParLayoutConfig.Sweep25vt,Conv.ParLayoutConfig.Wvt = ctail(Conv)

  
    
    
    
    #preliminairy positions for tricycle landing gear (nose and main)
    Conv.ParLayoutConfig.x_cg= PrelimCG_ranges(Conv)
    Conv.ParLayoutConfig.x_cg_wrt_MAC=(Conv.ParLayoutConfig.x_cg-Conv.ParLayoutConfig.x_lemac)\
    /Conv.ParAnFP.MAC
    Conv.ParLayoutConfig.lg_l_main,Conv.ParLayoutConfig.lg_l_nose,\
    Conv.ParLayoutConfig.lg_y_main, Conv.ParLayoutConfig.lg_x_main,\
    Conv.ParLayoutConfig.lg_x_nose_min_F_n, Conv.ParLayoutConfig.lg_x_nose_max_F_n,\
    Conv.ParLayoutConfig.lg_x_nose,Conv.ParLayoutConfig.lg_y_nose,\
    Conv.ParLayoutConfig.z_cg = PositionsLG_Tri(Conv)
    
    
    Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%
    
    
    Conv.ParAnFP.CLMAX = CLMAX(Conv).GetCLMAX()
    
    #Horizontal, Vertical tail design
    
#    Conv.ParLayoutConfig.Sht,Conv.ParLayoutConfig.xht,\
#    Conv.ParLayoutConfig.Aht,Conv.ParLayoutConfig.trht,\
#    Conv.ParLayoutConfig.Sweep25ht,Conv.ParLayoutConfig.Wht,\
#    Conv.ParLayoutConfig.Svt,Conv.ParLayoutConfig.xvt,\
#    Conv.ParLayoutConfig.Avt,Conv.ParLayoutConfig.trvt,\
#    Conv.ParLayoutConfig.Sweep25vt,Conv.ParLayoutConfig.Wvt = ttail(Conv)



ClassIAircraft()
ClassI_AndAHalf()
Conv.ParAnFP.CD0 = ComputeCD0(Conv)
# 
# =============================================================================

# =============================TEST AC FOR SENSITIVITY=========================
SensTestAc = copy.deepcopy(Conv)
# =============================================================================

