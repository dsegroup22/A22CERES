# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:38:41 2019

@author: hksam
"""

import sys
import os
#sys.path.append('../../../../../../')
from pathlib import Path
os.chdir(Path(__file__).parents[6])
#print (os.getcwd())
import numpy as np
from A22DSE.Models.AnFP.Current.Class_II.WingDesign import FunctionsPlanform
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


MTOW_I = Conv.ParStruc.MTOW
CL_eq = np.linspace(0.3, 1.5, 25)
Aw = np.linspace(3, 15, 25)
sweep = np.deg2rad(5)

# =============================================================================
#                          Constraint I: Optimum CL
# =============================================================================
CL_des = []

for j, Awi in enumerate(Aw):
    CL_des.append(float(FunctionsPlanform.GetOptCLCurve(
            Conv, ISA_model, MTOW_I, sweep, Awi)))

# =============================================================================
#                        Constraint II: Optimum Aw
# =============================================================================
Aw_des = []

for j, CL_eqi in enumerate(CL_eq):
    Aw_des.append(float(FunctionsPlanform.ComputeCurveII(Conv, 
      ISA_model, CL_eqi, MTOW_I)))
    
    
plt.figure()
plt.plot(CL_des, Aw)
plt.plot(CL_eq, Aw_des)

plt.show()
