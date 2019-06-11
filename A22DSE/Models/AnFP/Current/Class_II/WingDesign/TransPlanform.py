# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:34:11 2019

@author: hksam
"""

import sys
import os
#sys.path.append('../../../../../../')
from pathlib import Path
os.chdir(Path(__file__).parents[6])
#print (os.getcwd())
import numpy as np
import A22DSE.Models.AnFP.\
Current.Class_II.WingDesign.TransPlanFormFuncLst as FormFuncs
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
#from A22DSE.Parameters.Par_Class_Conventional import Conv
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =============================================================================
#                       SELECTION VARIABLES AND CONSTANTS
# =============================================================================
res = 500
plot = True

CL_i = np.linspace(0.3, 1.00, res)
sweep_i = np.linspace(np.deg2rad(0), np.deg2rad(40), res)
#tc_w  = np.linspace(0.10, 0.15, 4)
Mdd = 0.78
Aw = 17.5
TSFC = 0.061243
CL, sweep = np.meshgrid(CL_i, sweep_i)

theta2 = FormFuncs.ComputeTheta2(Conv, ISA_model)
theta3 = FormFuncs.ComputeTheta3(Conv, ISA_model)
Fprop = FormFuncs.ComputeFprop(Conv, ISA_model, TSFC)

# =============================================================================
#                       COMPUTE CONTOURS
# =============================================================================

# wing penalty function contours
FWP   = FormFuncs.ComputeFWP(Conv, Fprop, theta2, theta3, Aw, CL, sweep)

# t/c contours

# L/D contours


# =============================================================================
#                       COMPUTE PARTIAL OPTIMA
# =============================================================================

# Optimum sweep
sweep_opt = (FormFuncs.ComputePartialSweepOpt(Conv))

# Optimum CL for minimum FWP
CL_optLst = []
for i, sweepi in enumerate(sweep_i):
    y = FormFuncs.ComputePartialCLopt(Conv, 
        ISA_model, theta2, theta3, Fprop, TSFC, Aw, sweepi, CL_i)
    CL_optLst.append(float(y.x))
#    if i%10 == 0:
#        print(y.success)

def Intersect(y,z):
    idx = int((np.argwhere(np.diff(np.sign(y 
            - z))).flatten()))
    
    x = np.average(y[idx] + z[idx])/2
    return x

CL_des = Intersect(CL_optLst, CL_i)
tc_des = (FormFuncs.Compute_tc_limit(Conv, CL_des, sweep_opt)/
          np.cos(sweep_opt)**2)
FWP_opt = FormFuncs.ComputeFWP(Conv, Fprop, theta2, theta3, Aw, CL_des, sweep_opt)
# Optimum CL/CD


# =============================================================================
#                       PLOTTING
# =============================================================================

if plot == True:
    plt.clf()
    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(np.rad2deg(sweep), CL, FWP, color='black')
    ax.set_title('wireframe');
    
    plt.figure(2)
    cp = plt.contour(np.rad2deg(sweep), CL, FWP, 30)
    plt.plot(np.rad2deg(sweep_i), CL_optLst, color = 'r', linestyle ='dashed',
             label = r'Partial optimum $\hat{C}_L$')
    plt.axvline(np.rad2deg(sweep_opt), color = 'orange', linestyle = 'dashed',
                label = r'Partial optimum $\Lambda_w$')
    plt.ylim((CL_i[0], CL_i[-1]))
    plt.xlim((np.rad2deg(sweep_i[0]), np.rad2deg(sweep_i[-1])))
    plt.xlabel(r'$\Lambda_w$')
    plt.ylabel(r'$\hat{C}_L$')
    plt.clabel(cp, inline=True, 
              fontsize=10)
    plt.legend(loc = 3)
    plt.title(r'WPF in $\Lambda_w$ - $\hat{C}_L$ design space')
    