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
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
from A22DSE.Parameters.Par_Class_Conventional import Conv
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# =============================================================================
#
# =============================================================================
MTOW_I = 62e3
step = 20
CL_eq = np.linspace(0.2, 3., step)
MTOW = np.linspace(30000*9.81, 150000*9.81, step)
Aw = np.linspace(1, 18, step)
#Sweep = np.deg2rad(np.linspace(0, 5, 10))
#W_num = 10000
#W_denum = 0.76
sweep = np.deg2rad(5)
#
##def GetMTOW(CL_eqi, MTOWi, Awi):
##
##    q_des = FunctionsPlanform.DynamicPressEq(Conv, ISA_model)
###    Fprop = FunctionsPlanform.ComputeFprop(Conv, ISA_model, MTOWi)
##    Fprop = 8.5
##    CDp   = FunctionsPlanform.CDpCurlFunc(Conv, ISA_model, sweep)
##    CDpS  = CDp*Conv.ParAnFP.S
##    Theta1= FunctionsPlanform.ComputeTheta1(Conv, ISA_model)
##    Theta2= FunctionsPlanform.ComputeTheta2(Conv, ISA_model)
##    FWP   = FunctionsPlanform.FWP_subsonic(Theta1, Theta2, Conv, ISA_model, 
##                                           Awi, MTOWi, CL_eqi)
##    
##    
##    y = MTOWi - (MTOWi + CDpS*q_des*Fprop)/(W_denum + FWP)
##    return y
##
##Z = np.ones([np.size(Aw), np.size(CL_eq)])
##for i, MTOWi in enumerate(MTOW):
##    for j, Awi in enumerate(Aw):
###        print (CL_eqi)
##        
##       Z[i,j] = fsolve(GetMTOW, .75, args=(MTOWi, Awi))
##    
#X1,Y = np.meshgrid(MTOW,Aw)
#X2,Z = np.meshgrid(MTOW, CL_eq)
#
## =============================================================================
##                          Constraint I: Optimum CL
## =============================================================================
#CL_des = np.ones([np.size(Aw), np.size(CL_eq)])
#
#for i, MTOWi in enumerate(MTOW):
#    for j, Awi in enumerate(Aw):
#        CL_des[i][j] =float(FunctionsPlanform.GetOptCLCurve(
#                Conv, ISA_model, MTOWi, sweep, Awi))
#
## =============================================================================
##                        Constraint II: Optimum Aw
## =============================================================================
#Aw_des = np.ones([np.size(Aw), np.size(CL_eq)])
#
#for i, MTOWi in enumerate(MTOW):
#    for j, CL_eqi in enumerate(CL_eq):
#        Aw_des[i][j] = float(FunctionsPlanform.ComputeCurveII(Conv, 
#          ISA_model, CL_eqi, MTOWi))
#
#
## =============================================================================
##                    Constraint C1: Take-off Length <NOT DONE>
## =============================================================================
#
## =============================================================================
##                     Constraint C2: Wing & Tail Fraction
## =============================================================================
#        
## =============================================================================
##                                   PLOT
## =============================================================================
##
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
##ax.plot_surface(X, Z, Y)                         #MTOW, CL, Aw
#ax.plot_wireframe(X1, CL_des, Y)
#ax.plot_wireframe(X2, Z, Aw_des)
#
#
#fig, ax = plt.subplots()
#CS = ax.contour(X1, CL_des, Y)
#CT = ax.contour(X2, Z, Aw_des)
#ax.clabel(CT, inline=1, fontsize=10)

CL_des = []
for i, Awi in enumerate(Aw):
    CL_des.append(float(FunctionsPlanform.GetOptCLCurve(Conv, ISA_model, 
                                                  MTOW_I, sweep, Awi)))
    
Aw_des = []
for i, CL_eqi in enumerate(CL_eq):
    Aw_des.append(float(FunctionsPlanform.ComputeCurveII(Conv, 
                ISA_model, CL_eqi, MTOW_I)))
plt.figure(1)
plt.plot(CL_des, list(Aw))
plt.plot(list(CL_eq), Aw_des)

plt.show()


