# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:34:25 2019

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
# =============================================================================
#
# =============================================================================
CL_eq = np.linspace(0.5, 1.5, 100)
#MTOWi = np.linspace(20000, 30000, 3)
Aw = np.linspace(5, 15, 100)
#Sweep = np.deg2rad(np.linspace(0, 5, 10))
W_num = 10000
W_denum = 0.76
sweep = np.deg2rad(5)

def GetMTOW(MTOWi, Awi, CL_eqi):
    q_des = FunctionsPlanform.DynamicPressEq(Conv, ISA_model)
    Fprop = FunctionsPlanform.ComputeFprop(Conv, ISA_model, MTOWi)
    CDp   = FunctionsPlanform.CDpCurlFunc(Conv, ISA_model, sweep)
    CDpS  = CDp*Conv.ParAnFP.S
    Theta1= FunctionsPlanform.ComputeTheta1(Conv, ISA_model)
    Theta2= FunctionsPlanform.ComputeTheta2(Conv, ISA_model)
    FWP   = FunctionsPlanform.FWP_subsonic(Theta1, Theta2, Conv, ISA_model, 
                                           Awi, MTOWi, CL_eqi)
    
    
    y = MTOWi - (MTOWi + CDpS*q_des*Fprop)/(W_denum + FWP)
    return y

Z = np.ones([np.size(Aw), np.size(CL_eq)])
for i, Awi in enumerate(Aw):
    for j, CL_eqi in enumerate(CL_eq):
#        print (CL_eqi)
        
       Z[i,j] = fsolve(GetMTOW, Conv.ParStruc.MTOW, args=(Awi, CL_eqi))

X,Y = np.meshgrid(Aw,CL_eq)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
    
    