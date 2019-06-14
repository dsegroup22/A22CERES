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
import A22DSE.Models.STRUC.current.Class_II.Aeroelasticity.SteadyMain as AE
#from A22DSE.Models.DATCOM.Current.datcomrunread import C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,\
#C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q

def ClassIISizing(Aircraft):
    #get shortcuts
    Layout = Aircraft.ParLayoutConfig
    anfp = Aircraft.ParAnFP
    struc= Aircraft.ParStruc
    sc = Aircraft.ParCntrl
    Payload=Aircraft.ParPayload
    prop = Aircraft.ParProp

# =============================================================================
#                           STRUCTURES
# =============================================================================
    struc.rho_Al = 2830                         #kg/m³
    struc.rho_comp = 1600                       #kg/m³
    struc.A_stiff  = 0.00158                    # m²
    struc.n_stiff  = 40
    
    #OEW position wrt mac
    Aircraft.ParLayoutConfig.x_oe = xoe(Aircraft)
# =============================================================================
#                           WING PLANFORM DESIGN
# =============================================================================
    Aircraft.ParAnFP.n_ult, Aircraft.ParAnFP.n_lim, \
    Aircraft.ParAnFP.V_stall, Aircraft.ParAnFP.V_dive = flightenvelope(Aircraft)
    
#    Aircraft.ParAnFP.C_L_design, Aircraft.ParAnFP.A = PlanformMain.GetARTransWing(
#    Aircraft, ISA_model, step, False)
    
    #Oswald Efficiency
    anfp.e = OswaldEfficiency(Aircraft)
    #engine weight
    Aircraft.ParProp.Engine_weight_Total = Aircraft.ParProp.Engine_weight*Aircraft.ParStruc.N_engines
    
    
    
    #fuel tank layout
    Aircraft.ParLayoutConfig.b_fueltank = 0.60 * Aircraft.ParAnFP.b #Estimated from figure from Torenbeek p337 
    
    Aircraft.ParLayoutConfig.TotalSidearea,Aircraft.ParLayoutConfig.S_wet_fuselage,\
    Aircraft.ParLayoutConfig.S_front=FusAreas(Aircraft)
    
    
    Aircraft.ParPayload.V_tank=PayloadtankVolume(Aircraft)
    Aircraft.ParPayload.d_tank=0.5*Layout.d_fuselage
    Aircraft.ParPayload.A_inlet=InletArea(Aircraft,ISA_model)
    Aircraft.ParPayload.d_inlet=np.sqrt(4*Aircraft.ParPayload.A_inlet/np.pi)
    Aircraft.ParPayload.m_burner=BurnerMass(Aircraft)
    Aircraft.ParPayload.l_burner=1.83388*Aircraft.ParPayload.m_burner/259. 
    # scale length based on mass compared to original 
    #PT6A-68Aircraft.ParPayload.l_burner=1.83388*Aircraft.ParPayload.m_burner/259*
    #(0.48/Aircraft.ParPayload.d_inlet)**2
    # scale length based on mass compared to original PT6A-68
    
    
    Aircraft.ParPayload.m_tank=PayloadtankMass(Aircraft)
    Aircraft.ParPayload.l_tank=PayloadtankLength(Aircraft)
    
    
    Payload.xcg_tank,Payload.xcg_burner,Payload.x_burner_end,\
    Payload.xcg_totalpayload_empty,Payload.xcg_tank_fwd,Payload.xcg_burner_fwd, \
    Payload.x_burner_end_fwd,Payload.xcg_totalpayload_empty_fwd=Payloadcg(Aircraft)
    
    anfp.rho_cruise=ISA_model.ISAFunc([anfp.h_cruise])[2]
    anfp.q_dive=0.5*anfp.rho_cruise*(1.4*anfp.V_cruise)**2
    
    #tail sizing 
    #horizontal
    #function gives Surface, weight, Aspect ratio, optimal arm etc
    htail(Aircraft,ISA_model)
   
    #vertical
    vtail(Aircraft)
    
    #positions lemacs of tails
    Layout.x_lemacv=Aircraft.ParAnFP.MAC*Layout.x_oe+Layout.x_lemac+Layout.xvt-0.25*Layout.mac_v
    Layout.x_lemach=Aircraft.ParAnFP.MAC*Layout.x_oe+Layout.x_lemac+Layout.xht-0.25*Layout.mac_h
    

    
    #fuselage sizing

    #Struct = Aircraft.ParStruc
    #Layout.l_fuselage = 24 #[m] length of fuselage
    Layout.l_freq = fuselagereq(Aircraft)
    Layout.l_fuselage, Layout.d_fuselage, Layout.dim_cabin, Layout.d_cockpit = Fuselage(Aircraft)
    Layout.l_nose,Layout.l_cabin,Layout.l_tail=Layout.l_fuselage
    Layout.l_fuselage = np.sum(Layout.l_fuselage)   
    Layout.h_APU=0.2 #[m] dummy value  
    Layout.h_fuselage = Layout.dim_cabin[0]
    Layout.w_fuselage = Layout.dim_cabin[1]
    
    
    Layout.x_apex_wing = Layout.x_lemac-anfp.y_MAC*np.tan(anfp.Sweep_LE)
    Layout.x_apex_ht = Layout.x_lemach-Layout.y_MACh*np.tan(Layout.sweepLEht)
    Layout.x_apex_vt = Layout.x_lemacv-Layout.y_MACv*np.tan(Layout.sweepLEvt)
    Layout.x_begin_emp = Layout.l_nose+Layout.l_cabin
    #engine selection
    EngineChoice(Aircraft,ISA_model,False)
    
    #Control surface
    aileron(Aircraft)
    
    #engine placement
    Engines_placement(Aircraft)    
   
    #Stability derivatives DATCOM [/rad]
#    anfp.C_L_a,anfp.C_l_b,anfp.C_m_a,anfp.C_Y_b,anfp.C_n_b,anfp.C_L_adot,anfp.C_m_adot, anfp.C_l_p,\
#    anfp.C_Y_p,anfp.C_n_p,anfp.C_n_r,anfp.C_l_r,anfp.C_l_q,anfp.C_m_q=C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,\
#    C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q
    
# =============================================================================
#                                   WING BOX
# =============================================================================

    struc.t_skin, struc.t_rib = AE.ComputeMinWB(Aircraft, 
    ISA_model, 0, anfp.V_max_TO)
    




