# -*- coding= utf-8 -*-
"""
Created on Mon May 13 15=30=54 2019

@author= Nout
"""
import sys
import os
import copy
import numpy as np
sys.path.append('../../')

from A22DSE.Parameters.Par_Class_All import Aircraft
TestAC = Aircraft()

# =============================================================================
#               Reads .txt file
# =============================================================================

ParFile = open("ParametersConv.txt", 'r')
ParLst = []
for line in ParFile:
    line = line.split()
    ParLst.append(line)
    
# =============================================================================
#                            FORMATTING parameter lists
# =============================================================================
    
# =============================================================================
#                       Write all parameters from .txt file
# =============================================================================

AnFP = TestAC.ParAnFP
AnFP.Wing_config = 'high'
AnFP.A = 14.38
AnFP.e = 0.85
AnFP.CD0 = 0.028441657440709874
AnFP.S = 105.36164874506018
AnFP.TtoW = 0.79158

AnFP.Wing_config= 'high'
AnFP.A= 14.38
AnFP.e= 0.85
AnFP.CD0= 0.028441657440709874
AnFP.S= 105.36164874506018
AnFP.TtoW= 0.7915872657775996
AnFP.Mdd= 0.7
AnFP.h_cruise= 20000.0
AnFP.M_cruise= 0.7
AnFP.s_cruise= 1250000.0
AnFP.V_cruise= 206.52962329893498
AnFP.t_cruise= 6052.4005226636464
AnFP.CL_cruise= 1.2
AnFP.CL_max_cruise= 1.5
AnFP.c_j= 0.00016666666666666666
AnFP.SFC= 0.00016
AnFP.LD= 16
AnFP.CL_to= 1.2
AnFP.CD_to= 0.1
AnFP.fieldlen_to= 2500
AnFP.rho_SL= 1.225
AnFP.T_to= 200000
AnFP.Vr=50
AnFP.CL_land=1.4
AnFP.CD_land=0.3
AnFP.fieldlen_land=2500
AnFP.fuelused=1000
AnFP.operatingyears=15
AnFP.flighttime=4.853
AnFP.blockdist=2409.831
AnFP.Sweep25=18
AnFP.Cldes=0.56
AnFP.eta_airfoil=0.95
AnFP.max_t_loc=0.37
AnFP.alpha_0=-0.07853981633974483
AnFP.alpha_stall=0.23561944901923448
AnFP.delta_Y=3.08
AnFP.delta_alpha_C_L_max=0.03490658503988659
AnFP.C_L_to_C_l=0.83
AnFP.delta_C_L_max_cruise=-0.35
AnFP.delta_C_L_max_lowspeed=0
AnFP.n_engines=2
AnFP.wm_un=0
AnFP.We=2484
AnFP.Extrarange=500000
AnFP.WS=2087.9420117239574
AnFP.Thrust=174140.50117458578
AnFP.Sweep_25=0.3141592653589793
AnFP.Sweep_LE=0.338141536265473
AnFP.Sweep_50=0.28979739783395075
AnFP.b=38.92429201609151
AnFP.taper=0.4447296681703284
AnFP.c_r=3.7471859097209754
AnFP.c_t=1.6664847462027395
AnFP.MAC=2.8401188124041226
AnFP.y_MAC=8.484386223548203
AnFP.cl_alpha=0.09967000000000001
AnFP.cl_max=1.7122
AnFP.tc=0.12
AnFP.Cd0=0.008
AnFP.cm_0=-0.123
AnFP.LD_airfoil=90
AnFP.C_L_alpha_slow=5.6015543212917294
AnFP.C_L_max_slow=1.421126
AnFP.alpha_stall_slow=0.2100688518162947
AnFP.C_L_alpha_cruise=7.0967909791035044
AnFP.C_L_max_cruise=1.071126
AnFP.alpha_stall_cruise=0.10729780262151969

AnFP.disperRatePerTime=1.6522369863914796
AnFP.airtofuel=6
AnFP.m_payload=10000.0
AnFP.rho_payload=1121
AnFP.rho_alu=2700
AnFP.d_tank=1.5
AnFP.t_tank=0.003
AnFP.dispersionrate=0.008

#ControlLst
Cntrl = TestAC.ParCntrl
Cntrl.placeholder=None


#ParCostLst
Cost = TestAC.ParCostLst
Cost.Cengine=15000000
Cost.Cairframe=35000000
Cost.Cavionics=30000000
Cost.acmanuy=10
Cost.MHRmapflt=14
Cost.MHRmengbl=6
Cost.CEF8919=2.528888888888889
Cost.CEF7019=5.548888888888889
Cost.Fmat=2.25
Cost.ASP=25000000.0
Cost.rer=62
Cost.rmr=34
Cost.rtr=43
Cost.spil=60000
Cost.scpil=45000
Cost.Cfuel=2
Cost.FD=6.74
Cost.Fdiff=1.5
Cost.Fcad=0.8
Cost.Nrdte=6
Cost.Nst=2
Cost.Coil=15
Cost.Fobs=1
Cost.Fpror=0.1
Cost.Ffinr=0.05
Cost.Ftsf=0.2
Cost.Nrr=0.33
Cost.Nrm=0.9166666666666666
Cost.tpft=10
Cost.Fftoh=4.0
Cost.FfinM=0.1
Cost.Nprogram=150
Cost.Rlap=12


#ParStruc
Struct = TestAC.ParStruc
Struct.MTOW=22432.636306925804
Struct.FW=2350.5973162675846
Struct.N_engines=2
Struct.tail_angle=0.2617993877991494
Struct.OEWratio=0.4048582995951417
Struct.wfratioclimb=0.96383652375872975
Struct.fineness_c=8
Struct.fineness_n=1.25
Struct.fineness_t=2.0
Struct.Wf=2122.2319727509612
Struct.LG_weight_tot=499.63539133248111
Struct.LG_weight_nose=102.88385989351049
Struct.LG_weight_main=396.75153143897063
Struct.Wing_weight=5129.1127078379141
Struct.Weight_FusGroup=4279.9696589594678


#ParClassII
ClassII = TestAC.ParClassII_LG

ClassII.A_main=40
ClassII.B_main=0.16
ClassII.C_main=0.019
ClassII.D_main=1.5e-05
ClassII.A_nose=20
ClassII.B_nose=0.1
ClassII.C_nose=0
ClassII.D_nose=2e-06
ClassII.kuc_low_wing=1.0
ClassII.kuc_high_wing=1.08
ClassII.prelim_N_tire_main=8
ClassII.prelim_tire_diam=0.635
ClassII.psi=0.9948376736367678
ClassII.F_n_to_W=np.array([0.08, 0.15])
ClassII.rollreq=0.13962634015954636
ClassII.e_s=0.3


#ParLayoutConfig
Layout = TestAC.ParLayoutConfig
Layout.x_begin_emp=18
Layout.h_fuselage=1.6140567122346883
Layout.w_fuselage=2.8245992464107044
Layout.d_fuselage=2.1351963312637645
Layout.d_cockpit=2.1351963312637645
Layout.dim_cabin=np.array([1.61405671, 2.82459925])
Layout.d_engine=1.6
Layout.d_nacelle_engine=1.92
Layout.x_lemac=13.380674143304626
Layout.y_cg=np.array([0., 0.])
Layout.z_cg= np.array([ 1.88876977, 2.18876977])
Layout.y_nose= 1.44
Layout.z_cg_over_h_fus= 0.6
Layout.y_loc_eng= 7.84552225342896
Layout.l_fuselage= 24.020958726717353
Layout.Sht= 29.567392938934056
Layout.xht= 12.650743393439537
Layout.Aht= 4.15
Layout.trht= 0.442
Layout.Sweep25ht= 28.2
Layout.Wht= 941.40416320401698
Layout.Svt= 20.475894408535702
Layout.xvt= 12.01743133039394
Layout.Avt= 1.3
Layout.trvt= 0.646
Layout.Sweep25vt= 40.2
Layout.Wvt= 716.69813167200846
Layout.x_cg= np.array([ 14.49067153, 15.14490023])
Layout.lg_l_main= 1.2203357431371051
Layout.lg_l_nose= 1.2203357431371051
Layout.lg_y_main= 1.5010032103408226
Layout.lg_x_main= 15.515089302480265
Layout.lg_x_nose_min_F_n= 6.2877258349430836
Layout.lg_x_nose_max_F_n= 6.4189707861659819
Layout.lg_x_nose= 6.3533483105545328
Layout.lg_y_nose= 1.44
Layout.xcg_fuselagegroup= 13.706428635994566


#ConversTool
Convers = TestAC.ConversTool
Convers.ft2m= 0.3048
Convers.lbs2kg= 0.453592
Convers.mile2m= 1609.34
Convers.gallon2L= 3.78541
Convers.kts2ms= 0.514444444
Convers.km2nm= 0.539956803
Convers.lbftoN= 4.44822162