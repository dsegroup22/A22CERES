# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:54:31 2019

@author: Nout
"""
# =============================================================================
#                      IMPORT NECESSARY FUNCTIONS AND SHORTCUTS
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
os.chdir(Path(__file__).parents[3])
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_def_InitsizingUncoupled\
 import WingSurface_Thrust_FuelWeight, Wfratio_flighttime_flightrange
from A22DSE.Models.Class_II_Weight.Class_II_LG import Class_II_Weight_LG
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassI_AndAHalf, ComputeCD0
from A22DSE.Models.Prop.Current.Prop_Exec_engineselection_nengthrust import EngineChoice
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Wing import Total_Wing
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Fuselage import FuselageWeight
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg
from A22DSE.Models.def_Collection_ClassII_Sizing import ClassIISizing


# =============================================================================



def ClassIIWeight_MTOW(Aircraft):
    Layout = Aircraft.ParLayoutConfig
    struc= Aircraft.ParStruc
#DESCRIPTION:
    #NEEDS TO BE AFTER CLASS 1.5
    #get all weights from every file
    #fuselage, lg and wing weights needed for the oecg function
    #from the oecg function, get fuselage group, and wing group weight
    #append all the newly calculated weights in the object Conv    
#INPUTS: Conventional Aircraft
#OUTPUTS: float MTOW
    #and updates masses of Fuselage, Wing, LG,
    
    #CLass II weights & positions
    Aircraft.ParStruc.LG_weight_tot,Aircraft.ParStruc.LG_weight_nose, \
    Aircraft.ParStruc.LG_weight_main  = Class_II_Weight_LG(Aircraft)
    
    struc.Wing_weight=2*Total_Wing(Aircraft)/ISA_model.g0 # [kg] whole wing (2 sides)
    
    struc.Wf=FuselageWeight(Aircraft)[0]/ISA_model.g0 #[kg]
    
    #get the wing group and fuselage group
    Layout.x_lemac, Aircraft.ParStruc.Weight_FusGroup,Aircraft.ParStruc.Weight_WingGroup,\
    Layout.xcg_fuselagegroup = oecg(Aircraft)
    Layout.x_lemacv=Conv.ParAnFP.MAC*Layout.x_oe+Layout.x_lemacw+Layout.xv-0.25*Layout.mac_v
    Layout.x_lemach=Conv.ParAnFP.MAC*Layout.x_oe+Layout.x_lemacw+Layout.xh-0.25*Layout.mac_h
    #calculate new OEW and new MTOW
    struc.OEW = struc.Weight_WingGroup + struc.Weight_FusGroup #[kg]
    MTOW = struc.OEW + struc.FW + Aircraft.ParPayload.m_payload
    struc.OEWratio = struc.OEW/struc.MTOW
    return MTOW


def ClassIIWeightIteration(Aircraft):
    struc= Aircraft.ParStruc
    
#DESCRIPTION:
#   This function iterates the MTOW for 20 iterations, or less if it converges 
#   earlier. If it converges, it returns the updated MTOW, if not, it returns
#   an error. It updates the values taken from 
#INPUTS:
#   
#   
    
    MTOW_old = struc.MTOW
    struc.MTOW = ClassIIWeight_MTOW(Aircraft)
    error = abs((MTOW_old-struc.MTOW)/MTOW_old)

# =============================================================================
#                          ITERATE HERE FOR NEW MTOW
# =============================================================================
    itcount = 0
    while(itcount<8):
         #update values for CD0, wfratio, S, Thrust, tail size, etc.
         ComputeCD0(Aircraft)
         Wfratio_flighttime_flightrange(Aircraft)
         WingSurface_Thrust_FuelWeight(Aircraft)
         ClassI_AndAHalf()
         ClassIISizing(Conv)
         
        
         #chose correct engines
         EngineChoice(Aircraft,ISA_model,False)
         
         #get new wingweight over MTOW
         struc.Mw_Mtow = struc.Wing_weight/struc.MTOW
         
         #calculate old and new masses
         MTOW_old = struc.MTOW
         struc.MTOW = ClassIIWeight_MTOW(Aircraft)
         #check if error is small enough, if it is, return MTOW
         error = abs((MTOW_old-struc.MTOW)/MTOW_old)
         if error<0.01:
             break
         itcount+=1    
         
    #if after 20 iterations, still not converged, error occurs
#    if error>0.01:
#        raise ValueError('The MTOW does not converge') 



def WingWeightPlotter(Aircraft):
    anfp = Aircraft.ParAnFP
    # I used this to plot the wingweight versus the span, other than that it 
    #has no use
    # inputs: range of span
    #outputs: no values, just a plot of wingweight vs span
    b_lst = np.linspace(5.,50.,100)
    wingweightlst = []
    for i in b_lst:
        anfp.b = i
        Wing_weight=2*Total_Wing(Aircraft)/ISA_model.g0 # [kg] whole wing (2 sides)
        wingweightlst.append(Wing_weight)
    plt.plot(b_lst,wingweightlst)
