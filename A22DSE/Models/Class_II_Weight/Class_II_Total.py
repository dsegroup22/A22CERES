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
import matplotlib.pyplot as plt
os.chdir(Path(__file__).parents[3])
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_def_InitsizingUncoupled\
 import WingSurface_Thrust_FuelWeight, Wfratio_flighttime_flightrange
from A22DSE.Models.Class_II_Weight.Class_II_LG import Class_II_Weight_LG
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassIAircraft, ClassI_AndAHalf, ComputeCD0
from A22DSE.Models.Prop.Current.Prop_Exec_engineselection_nengthrust import EngineChoice
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Wing import Total_Wing
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Fuselage import FuselageWeight
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg

Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc

def ClassIIWeight_MTOW(Conv):
    #inputs: Conventional Aircraft
    #get all weights from every file
    #fuselage, lg and wing wheights needed for the oecg function
    #from the oecg function, get fuselage group, and wing group weight
    
    #CLass II weights & positions
    Conv.ParStruc.LG_weight_tot,Conv.ParStruc.LG_weight_nose, \
    Conv.ParStruc.LG_weight_main  = Class_II_Weight_LG(Conv)
    struc.Wing_weight=2*Total_Wing(Conv)/ISA_model.g0 # [kg] whole wing (2 sides)
    struc.Wf=FuselageWeight(Conv)[0]/ISA_model.g0 #[kg]
    
    #get the wing group and fuselage group
    Layout.x_lemac, Conv.ParStruc.Weight_FusGroup,Conv.ParStruc.Weight_WingGroup,\
    Layout.xcg_fuselagegroup = oecg(Conv)
    
    #calculate new OEW and new MTOW
    struc.OEW = struc.Weight_WingGroup + struc.Weight_FusGroup #[kg]
    MTOW = struc.OEW + struc.FW + Conv.ParPayload.m_payload
    struc.OEWratio = struc.OEW/struc.MTOW
    return MTOW


def ClassIIWeightIteration(Conv):
    
    
    MTOW_old = struc.MTOW
    struc.MTOW = ClassIIWeight_MTOW(Conv)
    error = abs((MTOW_old-struc.MTOW)/MTOW_old)
    #print(struc.MTOW)
# =============================================================================
#                          ITERATE HERE FOR NEW MTOW
# =============================================================================
    itcount = 0
    while(itcount<12):
        
         Conv.ParAnFP.CD0 = ComputeCD0(Conv)
         Wfratio_flighttime_flightrange(Conv)
         WingSurface_Thrust_FuelWeight(Conv)
         ClassI_AndAHalf()
         EngineChoice(Conv,ISA_model,False)
         struc.Mw_Mtow = struc.Wing_weight/struc.MTOW
         
         MTOW_old = struc.MTOW
         struc.MTOW = ClassIIWeight_MTOW(Conv)


         #print for checking stuff
         
# =============================================================================
#          print(struc.Wf)
#          print(struc.OEW/struc.MTOW)
#          print('\n')
# =============================================================================

         error = abs((MTOW_old-struc.MTOW)/MTOW_old)
         if error<0.01:
# =============================================================================
#              print(struc.MTOW)
# =============================================================================
             #print('dab')
             #print(itcount)
             return struc.MTOW
         itcount+=1
    return struc.MTOW








def WingWeightPlotter(Conv):
    b_lst = np.linspace(5.,50.,100)
    wingweightlst = []
    for i in b_lst:
        anfp.b = i
        Wing_weight=2*Total_Wing(Conv)/ISA_model.g0 # [kg] whole wing (2 sides)
        wingweightlst.append(Wing_weight)
    plt.plot(b_lst,wingweightlst)
