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
from A22DSE.Models.AnFP.Current.Class_II.WingDesign import TransPlanform 
from A22DSE.Models.AnFP.Current.Class_II.WingDesign.def_OswaldEfficiency import OswaldEfficiency
from A22DSE.Models.SC.TailSizing.fuselagelreq import fuselagereq
from A22DSE.Models.Layout.Current.Engine_Placements import Engines_placement
from A22DSE.Models.Prop.Current.Prop_Exec_engineselection_nengthrust import EngineChoice
from A22DSE.Models.SC.ControlSurface.aileron_sizing import aileron
from A22DSE.Models.DATCOM.Current.datcomrunread import C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,\
C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q

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
    Conv.ParAnFP.n_ult, Conv.ParAnFP.n_lim, \
    Conv.ParAnFP.V_stall, Conv.ParAnFP.V_dive = flightenvelope(Conv)
    
#    Conv.ParAnFP.C_L_design, Conv.ParAnFP.A = PlanformMain.GetARTransWing(
#    Conv, ISA_model, step, False)
    
    #Oswald Efficiency
#    anfp.e = OswaldEfficiency(Conv)
    #engine weight
    Conv.ParProp.Engine_weight_Total = Conv.ParProp.Engine_weight*Conv.ParStruc.N_engines
    
    
    
    #fuel tank layout
    Conv.ParLayoutConfig.b_fueltank = 0.60 * Conv.ParAnFP.b #Estimated from figure from Torenbeek p337 
    
    Conv.ParLayoutConfig.TotalSidearea,Conv.ParLayoutConfig.S_wet_fuselage,\
    Conv.ParLayoutConfig.S_front=FusAreas(Conv)
    
    
    Conv.ParPayload.V_tank=PayloadtankVolume(Conv)
    Conv.ParPayload.d_tank=0.5*Layout.d_fuselage
    Conv.ParPayload.A_inlet=InletArea(Conv,ISA_model)
    Conv.ParPayload.d_inlet=np.sqrt(4*Conv.ParPayload.A_inlet/np.pi)
    Conv.ParPayload.m_burner=BurnerMass(Conv)
    Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259. 
    # scale length based on mass compared to original 
    #PT6A-68Conv.ParPayload.l_burner=1.83388*Conv.ParPayload.m_burner/259*
    #(0.48/Conv.ParPayload.d_inlet)**2
    # scale length based on mass compared to original PT6A-68
    
    
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
    
    #positions lemacs of tails
    Layout.x_lemacv=Conv.ParAnFP.MAC*Layout.x_oe+Layout.x_lemac+Layout.xvt-0.25*Layout.mac_v
    Layout.x_lemach=Conv.ParAnFP.MAC*Layout.x_oe+Layout.x_lemac+Layout.xht-0.25*Layout.mac_h
    

    
    #fuselage sizing

    #Struct = Conv.ParStruc
    #Layout.l_fuselage = 24 #[m] length of fuselage
    Layout.l_freq = fuselagereq(Conv)
    Layout.l_fuselage, Layout.d_fuselage, Layout.dim_cabin, Layout.d_cockpit = Fuselage(Conv)
    Layout.l_nose,Layout.l_cabin,Layout.l_tail=Layout.l_fuselage
    Layout.l_fuselage = np.sum(Layout.l_fuselage)   
    Layout.h_APU=0.2 #[m] dummy value  
    Layout.h_fuselage = Layout.dim_cabin[0]
    Layout.w_fuselage = Layout.dim_cabin[1]
    
    
    Layout.x_apex_wing = Layout.x_lemac-anfp.y_MAC*np.tan(anfp.Sweep_LE)
    Layout.x_apex_ht = Layout.x_lemach-Layout.y_MACh*np.tan(Layout.sweepLEht)
    Layout.x_apex_vt = Layout.x_lemacv-Layout.y_MACv*np.tan(Layout.sweepLEvt)
    
    #engine selection
    EngineChoice(Conv,ISA_model,False)
    
    #engine placement
    Engines_placement(Conv)
    
    # Wing planform
    
    step = 100
    Conv.ParAnFP.C_L_design, Conv.ParAnFP.tc_w, Conv.ParAnFP.FWP = (

    TransPlanform.ComputePlanform(Conv, ISA_model,
                                  step, Conv.ParAnFP.A, False))
    
    #Control surface
    aileron(Conv)
    
    
    #Stability derivatives DATCOM [/rad]
    anfp.C_L_a,anfp.C_l_b,anfp.C_m_a,anfp.C_Y_b,anfp.C_n_b,anfp.C_L_adot,anfp.C_m_adot, anfp.C_l_p,\
    anfp.C_Y_p,anfp.C_n_p,anfp.C_n_r,anfp.C_l_r,anfp.C_l_q,anfp.C_m_q=C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,\
    C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q
    