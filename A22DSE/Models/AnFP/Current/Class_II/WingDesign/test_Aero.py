# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:54:23 2019

@author: hksam
"""

import sys
import os
#sys.path.append('../../../../../../')
from pathlib import Path
os.chdir(Path(__file__).parents[6])

from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
import A22DSE.Models.AnFP.Current.Class_II.WingDesign.TransPlanform as WPF
import A22DSE.Models.AnFP.Current.Class_II.WingDesign.TransPlanFormFuncLst as \
FuncLst

test_AnFP = Aircraft()

# =============================================================================
#                               AnFP
# =============================================================================
'''
- Buffet onset happens at 0.75
- Mdes = 0.74
- Mdd = Mdes + 0.05
- change CL linspace to 0.3 - 0.9 or smthn
- Increase margin CL opt implicit function solver
- comment out CL climb constraint
- Mcrit = 0.95
'''
ac = test_AnFP
anfp = ac.ParAnFP
struc = ac.ParStruc
prop  = ac.ParProp
layout = ac.ParLayoutConfig

test_AnFP.ParAnFP.taper        = 0.235 # [-]
test_AnFP.ParStruc.MTOW        = 43090 #kg
test_AnFP.ParAnFP.n_ult        = 2.5
test_AnFP.ParStruc.FW          = 7255 #kg
test_AnFP.ParProp.SFC_cruise   = 0.07036/3600
test_AnFP.ParAnFP.MAC          = 3.80
test_AnFP.ParAnFP.Mdd          = 0.80
test_AnFP.ParAnFP.M_cruise     = 0.74
test_AnFP.ParAnFP.h_cruise     = 11000
struc.wfratio                  = struc.FW/struc.MTOW
struc.MZFW                     = 35.8e3
struc.Wing_weight              = 10.1 * struc.MTOW
layout.Wht                     = 1.9 * struc.MTOW
prop.Thrust_cruise             = 12500
prop.T_sl                      = 62000
anfp.V_cruise                  = 206
anfp.Thrust                    = 12500
prop.N_engines                 = 2
prop.Engine_weight             = 1422
anfp.s_cruise                  = 2389080



FWP = WPF.ComputePlanform(ac, ISA_model, 100, 8.43, True)



