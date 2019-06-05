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
CL_eq = np.linspace(0.5, 1.5, 25)
MTOW = np.linspace(200000, 1500000, 25)
Aw = np.linspace(4, 15, 25)
#Sweep = np.deg2rad(np.linspace(0, 5, 10))
W_num = 10000
W_denum = 0.76
sweep = np.deg2rad(5)

def GetMTOW(CL_eqi, MTOWi, Awi ):

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
for i, MTOWi in enumerate(MTOW):
    for j, Awi in enumerate(Aw):
#        print (CL_eqi)
        
       Z[i,j] = fsolve(GetMTOW, .75, args=(MTOWi, Awi))

X,Y = np.meshgrid(MTOW,Aw)

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(X, Y, Z)
#
#fig, ax = plt.subplots()
#CS = ax.contour(X, Y, Z)
#ax.clabel(CS, inline=1, fontsize=10)
    