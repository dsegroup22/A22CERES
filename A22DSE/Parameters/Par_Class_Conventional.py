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
print(os.getcwd())
from A22DSE.Models.Class_II_Weight.Class_II_LG import Class_II_Weight_LG
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import (WSandTW)
from A22DSE.Models.Class_II_Weight.Class_II_Wing import Wing_Geo, Basic_Wing
from A22DSE.Models.Layout.Current.gearlocation_tri import (PrelimCG_ranges,PositionsLG_Tri)
from A22DSE.Models.Class_II_Weight.tailsizing import (ctail,ttail)
from A22DSE.Models.POPS.Current.payloadcalculations import InletArea,\
BurnerMass,PayloadtankVolume,PayloadtankLength,PayloadtankMass

from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Wing import Total_Wing
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Fuselage import FuselageWeight

from A22DSE.Models.Layout.Current.Sidearea import Area
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg
<<<<<<< HEAD
from A22DSE.Models.STRUC.current.Class_II.FuselageLength import SurfaceFuselage
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model

=======
from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (
        GetTotalFuselageLength, SurfaceFuselage)
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassIAircraft
>>>>>>> 1164ad689d6a58ef0785f5a44d15c1841d02b7c4
#shortcut
Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc

# =============================================================================


# =============================================================================
#                           CLASS II STARTS HERE
# =============================================================================

# =============================================================================
#                          ITERATE HERE FOR NEW OEW RATIO
# =============================================================================

def ClassIIWeight_OEWratio():

    #CLass II weights & positions
    Conv.ParStruc.Wf = SurfaceFuselage(Conv, 24, 2, 0.01,ISA_model) # =fuselage
    Conv.ParStruc.LG_weight_tot,Conv.ParStruc.LG_weight_nose, \
    Conv.ParStruc.LG_weight_main  = Class_II_Weight_LG(Conv)
    Conv.ParStruc.Wing_weight = Basic_Wing(Conv)
    
    struc.Wing_weight=2*Total_Wing(Conv)/ISA_model.g0 # [kg] whole wing (2 sides)
    struc.Wf=FuselageWeight(Conv)[0]/ISA_model.g0 #[kg]
    
    Layout.x_lemac, Conv.ParStruc.Weight_FusGroup,Conv.ParStruc.Weight_WingGroup,\
    Layout.xcg_fuselagegroup = oecg(Conv)
    
    OEW = struc.Weight_WingGroup + struc.Weight_FusGroup #[kg]
    MTOW = OEW + struc.FW + Conv.ParPayload.m_payload
    
    OEWratio = OEW/MTOW
    return OEWratio

def ClassII_Iteration():
    OEWratio_old = struc.OEWratio
    struc.OEWratio = ClassIIWeight_OEWratio()
    error = abs((struc.OEWratio-OEWratio_old)/OEWratio_old)
    
    while(error>0.01):
        print(struc.OEWratio)
        ClassIAircraft()
        OEWratio_old = struc.OEWratio
        
        struc.OEWratio = ClassIIWeight_OEWratio()
        
        error = abs((struc.OEWratio-OEWratio_old)/OEWratio_old)
    return struc.OEWratio
 
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
        
