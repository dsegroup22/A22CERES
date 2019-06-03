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
import copy
import numpy as np
sys.path.append('../../')

from A22DSE.Models.Class_II_Weight.Class_II_LG import Class_II_Weight_LG
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import (WSandTW)
from A22DSE.Models.Class_II_Weight.Class_II_Wing import Wing_Geo, Basic_Wing
from A22DSE.Models.Layout.Current.gearlocation_tri import (PrelimCG_ranges,PositionsLG_Tri)
from A22DSE.Models.Class_II_Weight.tailsizing import (ctail,ttail)
from A22DSE.Models.POPS.Current.payloadcalculations import InletArea,\
BurnerMass,PayloadtankVolume,PayloadtankLength,PayloadtankMass

from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Wing import WingWeight
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg
from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (
        GetTotalFuselageLength, SurfaceFuselage)
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model
#shortcut
Layout = Conv.ParLayoutConfig
# =============================================================================


# =============================================================================
#                           CLASS II STARTS HERE
# =============================================================================


#CLass II weights & positions
Conv.ParStruc.Wf = SurfaceFuselage(Conv, 24, 2, 0.01,ISA_model) # isn't classII
Conv.ParStruc.LG_weight_tot,Conv.ParStruc.LG_weight_nose, \
Conv.ParStruc.LG_weight_main  = Class_II_Weight_LG(Conv)
Conv.ParStruc.Wing_weight = Basic_Wing(Conv)
Layout.x_lemac, Conv.ParStruc.Weight_FusGroup, Layout.xcg_fuselagegroup = oecg(Conv)


 
#preliminairy positions for tricycle landing gear (nose and main)
Conv.ParLayoutConfig.lg_l_main,Conv.ParLayoutConfig.lg_l_nose,\
Conv.ParLayoutConfig.lg_y_main, Conv.ParLayoutConfig.lg_x_main,\
Conv.ParLayoutConfig.lg_x_nose_min_F_n, Conv.ParLayoutConfig.lg_x_nose_max_F_n,\
Conv.ParLayoutConfig.lg_x_nose,Conv.ParLayoutConfig.lg_y_nose,\
Conv.ParLayoutConfig.z_cg = PositionsLG_Tri(Conv)

#engine position
Conv.ParLayoutConfig.m_engine = 5000 # [kg] DUMMY VALUE
Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%
Conv.ParLayoutConfig.x_engine = 0.25 #[-] dimensionless x/mac DUMMY

#wing layout -> up for change
Conv.ParLayoutConfig.x_CoP = WingWeight(Conv)[0] #[-] dimensionless x/mac DUMMY

#fuel tank layout
Conv.ParLayoutConfig.b_fueltank = 0.80 * Conv.ParAnFP.b #DUMMY value


# =============================================================================
#                          ITERATE HERE FOR NEW OEW RATIO
# =============================================================================


Conv.ParPayload.A_inlet=InletArea(Conv,ISA_model)
Conv.ParPayload.m_burner=BurnerMass(Conv)
Conv.ParPayload.V_tank=PayloadtankVolume(Conv)
Conv.ParPayload.m_tank=PayloadtankMass(Conv)
Conv.ParPayload.l_tank=PayloadtankLength(Conv)





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
        
