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
from A22DSE.Models.Class_II_Weight.Class_II_Total import ClassIIWeight_MTOW,ClassIIWeightIteration, WingWeightPlotter

from A22DSE.Models.Layout.Current.Area import FusAreas
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import oecg

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import SurfaceFuselage

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (
        GetTotalFuselageLength, SurfaceFuselage)
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassIAircraft, ClassI_AndAHalf, ComputeCD0
from A22DSE.Models.SC.TailSizing.horizontaltail import convtail
from A22DSE.Models.SC.TailSizing.verticaltail import vtail

#shortcuts
Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc
sc = Conv.ParCntrl

ClassIAircraft()
ClassI_AndAHalf()
Conv.ParAnFP.CD0 = ComputeCD0(Conv)

# =============================================================================

#engine position
Conv.ParProp.Engine_weight_Total = Conv.ParProp.Engine_weight*Conv.ParStruc.N_engines
Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%
Conv.ParLayoutConfig.x_engine = 0.25 #[-] dimensionless x/mac DUMMY


#fuel tank layout
Conv.ParLayoutConfig.b_fueltank = 0.60 * Conv.ParAnFP.b #Estimated from figure from Torenbeek p337 

Layout.TotalSidearea,Layout.S_wet_fuselage=FusAreas(Conv)


Conv.ParPayload.V_tank=PayloadtankVolume(Conv)
Conv.ParPayload.d_tank=Layout.d_fuselage
Conv.ParPayload.A_inlet=InletArea(Conv,ISA_model)
Conv.ParPayload.d_inlet=np.sqrt(4*Conv.ParPayload.A_inlet/np.pi)
Conv.ParPayload.m_burner=BurnerMass(Conv)
Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259 # scale length based on mass compared to original PT6A-68Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259*(0.48/Conv.ParPayload.d_inlet)**2 # scale length based on mass compared to original PT6A-68

Payload=Conv.ParPayload

Conv.ParPayload.m_tank=PayloadtankMass(Conv)
Conv.ParPayload.l_tank=PayloadtankLength(Conv)
#Conv.ParPayload.xcg_burner=0.85*Layout.l_fuselage # burner @ 85 % of fuselage
#Conv.ParPayload.xcg_tank=Conv.ParPayload.xcg_burner-(Conv.ParPayload.l_tank+Conv.ParPayload.l_burner)/2 # most aft poossible position: place tank directly ahead of the payload
Conv.ParPayload.xcg_tank=Layout.l_nose+Layout.l_cabin-(Conv.ParPayload.l_tank-Conv.ParPayload.d_tank)/2 # most aft possible position: cylindrical tank section ennds at end of cylindrical cabin section
Conv.ParPayload.xcg_burner=Conv.ParPayload.xcg_tank+(Conv.ParPayload.l_tank+Conv.ParPayload.l_burner)/2 # placed directly aft of the tank
Conv.ParPayload.x_burner_end=Conv.ParPayload.xcg_burner+Conv.ParPayload.l_burner/2 # check that the burner does not extend further than the fuselage
Conv.ParPayload.xcg_totalpayload_empty=(Payload.xcg_tank*Payload.m_tank+Payload.xcg_burner*Payload.m_burner)\
/(Payload.m_tank+Payload.m_burner)


anfp.rho_cruise=ISA_model.ISAFunc([anfp.h_cruise])[2]
anfp.q_dive=0.5*anfp.rho_cruise*(1.4*anfp.V_cruise)**2

#tail sizing 
#horizontal
Conv.ParLayoutConfig.Cr_h, Conv.ParLayoutConfig.Ct_h, Conv.ParLayoutConfig.b_h, \
Conv.ParLayoutConfig.sweepLEht, Conv.ParLayoutConfig.sweep25ht, Conv.ParLayoutConfig.sweep50ht, \
Conv.ParLayoutConfig.trht, Conv.ParLayoutConfig.Aht, Conv.ParLayoutConfig.Wht, Conv.ParLayoutConfig.Sht, \
Conv.ParLayoutConfig.xht = convtail(Conv,ISA_model)
#vertical
Conv.ParLayoutConfig.Svt,Conv.ParLayoutConfig.xvt,\
Conv.ParLayoutConfig.Avt,Conv.ParLayoutConfig.trvt,\
Conv.ParLayoutConfig.Sweep25vt,Conv.ParLayoutConfig.Sweep50vt,\
Conv.ParLayoutConfig.cr_v, Conv.ParLayoutConfig.ct_v,\
Conv.ParLayoutConfig.b_v, Conv.ParLayoutConfig.Wvt=vtail(Conv)





# =============================================================================
#                           CLASS II WEIGHTS STARTS HERE
# =============================================================================


struc.MTOW = ClassIIWeightIteration(Conv)
#WingWeightPlotter(Conv)



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
        print('\n\n ParProp', file = f)
        print(vars(Conv.ParProp), file=f)
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
        
