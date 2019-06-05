# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:55:52 2019

@author: Nout
"""
# =============================================================================
#                            IMPORT NECESSARY MODULES
# =============================================================================

import sys
import os
from pathlib import Path
import copy
import numpy as np
#sys.path.append('../../')
os.chdir(Path(__file__).parents[2])

#print(os.getcwd())


from A22DSE.Models.Layout.Current.gearlocation_tri import (PrelimCG_ranges,PositionsLG_Tri)
from A22DSE.Models.Class_II_Weight.tailsizing import (ctail,ttail)
from A22DSE.Models.POPS.Current.payloadcalculations import InletArea,\
BurnerMass,PayloadtankVolume,PayloadtankLength,PayloadtankMass
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_def_InitsizingUncoupled import WingSurface_Thrust_FuelWeight

from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Wing import Total_Wing
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Fuselage import FuselageWeight
from A22DSE.Models.Class_II_Weight.Class_II_Total import ClassIIWeight_MTOW

from A22DSE.Models.Layout.Current.Sidearea import Area
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import SurfaceFuselage
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model


from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (
        GetTotalFuselageLength, SurfaceFuselage)
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassIAircraft, ClassI_AndAHalf, ComputeCD0

#shortcuts
Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc

ClassIAircraft()
ClassI_AndAHalf()
Conv.ParAnFP.CD0 = ComputeCD0(Conv)

# =============================================================================

#engine position
Conv.ParLayoutConfig.m_engine = 5000 # [kg] DUMMY VALUE
Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%
Conv.ParLayoutConfig.x_engine = 0.25 #[-] dimensionless x/mac DUMMY


#fuel tank layout
Conv.ParLayoutConfig.b_fueltank = 0.80 * Conv.ParAnFP.b #DUMMY value

Layout.TotalSidearea=Area(Conv)

Conv.ParPayload.A_inlet=InletArea(Conv,ISA_model)
Conv.ParPayload.m_burner=BurnerMass(Conv)
Conv.ParPayload.V_tank=PayloadtankVolume(Conv)
Conv.ParPayload.m_tank=PayloadtankMass(Conv)
Conv.ParPayload.l_tank=PayloadtankLength(Conv)

anfp.rho_cruise=ISA_model.ISAFunc([anfp.h_cruise])[2]
anfp.q_dive=0.5*anfp.rho_cruise*(1.4*anfp.V_cruise)**2


#print(struc.MTOW)
struc.MTOW = ClassIIWeight_MTOW(Conv)
#print(struc.MTOW)
# =============================================================================
#                           CLASS II WEIGHTS STARTS HERE
# =============================================================================

 
#preliminairy positions for tricycle landing gear (nose and main)
Conv.ParLayoutConfig.lg_l_main,Conv.ParLayoutConfig.lg_l_nose,\
Conv.ParLayoutConfig.lg_y_main, Conv.ParLayoutConfig.lg_x_main,\
Conv.ParLayoutConfig.lg_x_nose_min_F_n, Conv.ParLayoutConfig.lg_x_nose_max_F_n,\
Conv.ParLayoutConfig.lg_x_nose,Conv.ParLayoutConfig.lg_y_nose,\
Conv.ParLayoutConfig.z_cg = PositionsLG_Tri(Conv)




# =============================================================================
# #saving object as txt file
# =============================================================================

file_path = 'A22DSE\Parameters\ParametersConv.txt'
if os.path.isfile(file_path):
    with open('A22DSE\Parameters\ParametersConv.txt', 'w') as f:
        print('ParAnFP', file = f)
        print(vars(Conv.ParAnFP), file=f)
        print('\n\n ParPayload', file = f)
        print(vars(Conv.ParPayload), file=f)
        print('\n\n ParCntrl', file = f)
        print(vars(Conv.ParCntrl), file=f)
        print('\n\n ParCostLst', file = f)
        print(vars(Conv.ParCostLst), file=f)
        print('\n\n ParStruc', file = f)
        print(vars(Conv.ParStruc), file=f)
        print('\n\n ParClassII', file = f)
        print(vars(Conv.ParClassII_LG), file =f)
        print('\n\n ParLayoutConfig',file =f)
        print(vars(Conv.ParLayoutConfig), file =f)
        print('\n\n ConversTool', file = f)
        print(vars(Conv.ConversTool), file=f)
    
    
    s = open("A22DSE\Parameters\ParametersConv.txt").read()
    s = s.replace(',', '\n')
    f = open("A22DSE\Parameters\ParametersConv.txt", 'w')
    f.write(s)
    f.close()
        
