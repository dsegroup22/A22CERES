# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:49:11 2019

@author: Nout


THIS FILE IS USED FOR EVERY CALCULATION OF THE SECOND CLASS SIZING
"""

import os
from pathlib import Path
import numpy as np
os.chdir(Path(__file__).parents[2])


from A22DSE.Models.POPS.Current.payloadcalculations import InletArea,\
BurnerMass,PayloadtankVolume,PayloadtankLength,PayloadtankMass,Payloadcg

from A22DSE.Models.Layout.Current.Area import FusAreas
from A22DSE.Models.Class_II_Weight.SC_curve_and_cg import xoe
from A22DSE.Parameters.Par_Class_Diff_Configs import (ISA_model)
from A22DSE.Models.STRUC.current.Class_II.FuselageLength import (Fuselage)
from A22DSE.Models.SC.TailSizing.horizontaltail import htail
from A22DSE.Models.SC.TailSizing.verticaltail import vtail
from A22DSE.Models.AnFP.Current.flightenvelope import flightenvelope
from A22DSE.Models.AnFP.Current.Class_II.WingDesign import PlanformMain 
from A22DSE.Models.AnFP.Current.Class_II.WingDesign.def_OswaldEfficiency import OswaldEfficiency


def ClassIISizing(Conv):
    #get shortcuts
    Layout = Conv.ParLayoutConfig
    anfp = Conv.ParAnFP
    struc= Conv.ParStruc
    sc = Conv.ParCntrl
    Payload=Conv.ParPayload

    #OEW position wrt mac
    Conv.ParLayoutConfig.x_oe = xoe(Conv)
# =============================================================================
#                           WING PLANFORM DESIGN
# =============================================================================
    Conv.ParAnFP.n_ult, Conv.ParAnFP.V_stall, Conv.ParAnFP.V_dive = flightenvelope(Conv)
    
    step = 50
    Conv.ParAnFP.C_L_design, Conv.ParAnFP.A = PlanformMain.GetARTransWing(
    Conv, ISA_model, step, False)
    
    #Oswald Efficiency
    anfp.e = OswaldEfficiency(Conv)
    #engine position
    Conv.ParProp.Engine_weight_Total = Conv.ParProp.Engine_weight*Conv.ParStruc.N_engines
    Conv.ParLayoutConfig.y_engine = Conv.ParAnFP.b/2*0.25 #[m] engine at 25%
    Conv.ParLayoutConfig.x_engine = 0.25 #[-] dimensionless x/mac DUMMY
    
    
    #fuel tank layout
    Conv.ParLayoutConfig.b_fueltank = 0.60 * Conv.ParAnFP.b #Estimated from figure from Torenbeek p337 
    
    Layout.TotalSidearea,Layout.S_wet_fuselage,Layout.S_front=FusAreas(Conv)
    
    
    Conv.ParPayload.V_tank=PayloadtankVolume(Conv)
    Conv.ParPayload.d_tank=0.5*Layout.d_fuselage
    Conv.ParPayload.A_inlet=InletArea(Conv,ISA_model)
    Conv.ParPayload.d_inlet=np.sqrt(4*Conv.ParPayload.A_inlet/np.pi)
    Conv.ParPayload.m_burner=BurnerMass(Conv)
    Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259. # scale length based on mass compared to original PT6A-68Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259*(0.48/Conv.ParPayload.d_inlet)**2 # scale length based on mass compared to original PT6A-68
    
    
    Conv.ParPayload.m_tank=PayloadtankMass(Conv)
    Conv.ParPayload.l_tank=PayloadtankLength(Conv)
    
    
    Payload.xcg_tank,Payload.xcg_burner,Payload.x_burner_end,\
    Payload.xcg_totalpayload_empty=Payloadcg(Conv)
    
    anfp.rho_cruise=ISA_model.ISAFunc([anfp.h_cruise])[2]
    anfp.q_dive=0.5*anfp.rho_cruise*(1.4*anfp.V_cruise)**2
    
    #tail sizing 
    #horizontal
    #function gives Surface, weight, Aspect ratio, optimal arm etc
    htail(Conv,ISA_model)
    #vertical
    vtail(Conv)
    
    #fuselage sizing

    #Struct = Conv.ParStruc
    #Layout.l_fuselage = 24 #[m] length of fuselage
    
    Layout.l_fuselage, Layout.d_fuselage, Layout.dim_cabin, Layout.d_cockpit = Fuselage(Conv)
    Layout.l_nose,Layout.l_cabin,Layout.l_tail=Layout.l_fuselage
    Layout.l_fuselage = np.sum(Layout.l_fuselage)   
    Layout.h_APU=0.2 #[m] dummy value  
    Layout.h_fuselage = Layout.dim_cabin[0]
    Layout.w_fuselage = Layout.dim_cabin[1]
    
    
    Layout.x_apex_wing=Layout.x_lemac-anfp.y_MAC*np.tan(anfp.Sweep_LE)
    

