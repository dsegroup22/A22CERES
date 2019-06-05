# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:54:31 2019

@author: Nout
"""
import sys
import os
from pathlib import Path
import copy
import numpy as np

os.chdir(Path(__file__).parents[3])
from A22DSE.Models.Class_II_Weight.Class_II_LG import Class_II_Weight_LG
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassIAircraft

from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Wing import Total_Wing
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Fuselage import FuselageWeight

from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg

Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc

def ClassIIWeight_MTOW(Conv):
    
    #CLass II weights & positions
    Conv.ParStruc.LG_weight_tot,Conv.ParStruc.LG_weight_nose, \
    Conv.ParStruc.LG_weight_main  = Class_II_Weight_LG(Conv)
    
    struc.Wing_weight=2*Total_Wing(Conv)/ISA_model.g0 # [kg] whole wing (2 sides)
    struc.Wf=FuselageWeight(Conv)[0]/ISA_model.g0 #[kg]
    
    Layout.x_lemac, Conv.ParStruc.Weight_FusGroup,Conv.ParStruc.Weight_WingGroup,\
    Layout.xcg_fuselagegroup = oecg(Conv)
    
    OEW = struc.Weight_WingGroup + struc.Weight_FusGroup #[kg]
    MTOW = OEW + struc.FW + Conv.ParPayload.m_payload

    return MTOW


def ClassIIWeightIteration(Conv):
    
    MTOW_old = struc.MTOW
    struc.MTOW = ClassIIWeight_MTOW(Conv)
    error = abs((MTOW_old-struc.MTOW)/MTOW_old)
    
# =============================================================================
# # =============================================================================
# #                          ITERATE HERE FOR NEW MTOW
# # =============================================================================
#     
#     while(error>0.01):
#          print(struc.MTOW)
#          WingSurface_Thrust_FuelWeight(Conv)
#          MTOW_old = struc.MTOW
#          struc.MTOW = ClassIIWeight_MTOW(Conv)
#          error = abs((MTOW_old-struc.MTOW)/MTOW_old)
#     return struc.MTOW
# =============================================================================