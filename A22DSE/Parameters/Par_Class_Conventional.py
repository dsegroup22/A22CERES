# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:55:52 2019

@author: Nout
"""
# =============================================================================
#                            IMPORT NECESSARY MODULES
# =============================================================================

import os
from pathlib import Path
import copy
import numpy as np
os.chdir(Path(__file__).parents[2])


from A22DSE.Models.POPS.Current.payloadcalculations import InletArea,\
BurnerMass,PayloadtankVolume,PayloadtankLength,PayloadtankMass,Payloadcg,PayloadtankLengthEllipse,\
PayloadtankMassEllipse,PayloadcgEllipse

from A22DSE.Models.Class_II_Weight.Class_II_Total import ClassIIWeightIteration
from A22DSE.Models.Layout.Current.Area import FusAreas

from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import xoe

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (Fuselage)
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model, ClassIAircraft, ClassI_AndAHalf, ComputeCD0
from A22DSE.Models.SC.TailSizing.horizontaltail import htail
from A22DSE.Models.SC.TailSizing.verticaltail import vtail
from A22DSE.Models.AnFP.Current.flightenvelope import flightenvelope
#shortcuts
Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc
sc = Conv.ParCntrl
Payload=Conv.ParPayload

ClassIAircraft()
ClassI_AndAHalf()
Conv.ParAnFP.CD0 = ComputeCD0(Conv)

# =============================================================================

#OEW position wrt mac
Conv.ParLayoutConfig.x_oe = xoe(Conv)

#engine position
Conv.ParProp.Engine_weight_Total = Conv.ParProp.Engine_weight*Conv.ParStruc.N_engines
Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%
Conv.ParLayoutConfig.x_engine = 0.25 #[-] dimensionless x/mac DUMMY


#fuel tank layout
Conv.ParLayoutConfig.b_fueltank = 0.60 * Conv.ParAnFP.b #Estimated from figure from Torenbeek p337 

Layout.TotalSidearea,Layout.S_wet_fuselage=FusAreas(Conv)


Conv.ParPayload.V_tank=PayloadtankVolume(Conv)
Conv.ParPayload.d_tank=0.8*Layout.h_fuselage #reserve 20% of fuselage space on the bottom for plumbing and pumps
Conv.ParPayload.A_inlet=InletArea(Conv,ISA_model)
Conv.ParPayload.d_inlet=np.sqrt(4*Conv.ParPayload.A_inlet/np.pi)
Conv.ParPayload.m_burner=BurnerMass(Conv)
Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259. # scale length based on mass compared to original PT6A-68Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259*(0.48/Conv.ParPayload.d_inlet)**2 # scale length based on mass compared to original PT6A-68


Conv.ParPayload.m_tank=PayloadtankMassEllipse(Conv)
Conv.ParPayload.l_tank=PayloadtankLengthEllipse(Conv)


Payload.xcg_tank,Payload.xcg_burner,Payload.x_burner_end,\
Payload.xcg_totalpayload_empty=PayloadcgEllipse(Conv)

anfp.rho_cruise=ISA_model.ISAFunc([anfp.h_cruise])[2]
anfp.q_dive=0.5*anfp.rho_cruise*(1.4*anfp.V_cruise)**2

#tail sizing 
#horizontal
#function gives Surface, weight, Aspect ratio, optimal arm etc
htail(Conv,ISA_model)
#vertical
Conv.ParLayoutConfig.Svt,Conv.ParLayoutConfig.xvt,\
Conv.ParLayoutConfig.Avt,Conv.ParLayoutConfig.trvt,\
Conv.ParLayoutConfig.Sweep25vt,Conv.ParLayoutConfig.Sweep50vt,\
Conv.ParLayoutConfig.cr_v, Conv.ParLayoutConfig.ct_v,\
Conv.ParLayoutConfig.b_v, Conv.ParLayoutConfig.Wvt=vtail(Conv)

#fuselage sizing
Layout = Conv.ParLayoutConfig
#Struct = Conv.ParStruc
#Layout.l_fuselage = 24 #[m] length of fuselage

Layout.l_fuselage, Layout.d_fuselage, Layout.dim_cabin, Layout.d_cockpit = Fuselage(Conv)
Layout.l_nose,Layout.l_cabin,Layout.l_tail=Layout.l_fuselage
Layout.l_fuselage = np.sum(Layout.l_fuselage)   
Layout.h_APU=0.2 #[m] dummy value  
Layout.h_fuselage = Layout.dim_cabin[0]
Layout.w_fuselage = Layout.dim_cabin[1]


Layout.x_apex_wing=Layout.x_lemac-anfp.y_MAC*np.tan(anfp.Sweep_LE)

# =============================================================================
#                            Flight Envelope
#==============================================================================
Conv.ParAnFP.n_ult, Conv.ParAnFP.V_stall, Conv.ParAnFP.V_dive = flightenvelope(Conv)
# =============================================================================
#                           CLASS II WEIGHTS STARTS HERE
# =============================================================================

struc.MTOW = ClassIIWeightIteration(Conv)
#WingWeightPlotter(Conv)

# =============================================================================
#                            Weight and Balance
#==============================================================================
















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
        
