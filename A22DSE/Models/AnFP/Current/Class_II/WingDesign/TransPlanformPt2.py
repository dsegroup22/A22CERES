# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:48:33 2019

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
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =============================================================================
#                       SELECTION VARIABLES AND CONSTANTS
# =============================================================================
res = 100
plot = False

CL_i = np.linspace(0.3, 1.2, res)
sweep_opt = (FormFuncs.ComputePartialSweepOpt(Conv))
#tc_w  = np.linspace(0.10, 0.15, 4)
Mdd = 0.82
Aw_i = np.linspace(1.5, 25, res)
TSFC = 0.061243
CL, Aw = np.meshgrid(CL_i, Aw_i)

theta2 = FormFuncs.ComputeTheta2(Conv, ISA_model)
theta3 = FormFuncs.ComputeTheta3(Conv, ISA_model)
Fprop = FormFuncs.ComputeFprop(Conv, ISA_model, TSFC)

# =============================================================================
#                       COMPUTE CONTOURS
# =============================================================================

    # wing penalty function contours
FWP   = FormFuncs.ComputeFWP(Conv, Fprop, theta2, theta3, Aw, CL, sweep_opt)
# t/c contours

# L/D contours


# =============================================================================
#                       COMPUTE PARTIAL OPTIMA
# =============================================================================

    # Optimum Aw
Aw_opt = FormFuncs.ComputePartialAwOpt(Conv, ISA_model,
                        theta2, theta3, Fprop, TSFC, sweep_opt, CL_i)

    # Optimum CL w.r.t. Aw
CL_optLst = []
for i, Awi in enumerate(Aw_i):
    
    y = FormFuncs.ComputePartialCLopt(Conv, 
        ISA_model, theta2, theta3, Fprop, TSFC, Awi, sweep_opt, CL_i)
    CL_optLst.append(float(y.x))
#    if i%10 == 0:
#        print(y.success)
        
# =============================================================================
#                       CONSTRAINTS
# =============================================================================
    
    # Span-loading / Take-off field length
WB = FormFuncs.ComputeSpanLoading(Conv, ISA_model, Fprop, theta2, theta3,
                                  TSFC, sweep_opt, CL_i)
    
# =============================================================================
#                       PLOTTING
# =============================================================================

if plot == True:
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(CL, Aw, FWP, color='black')
    ax.set_title('wireframe');
    
    plt.figure(2)
    cp = plt.contour(CL, Aw, FWP, 20)
    plt.plot(CL_i, Aw_opt, color = 'r', linestyle = 'dashed',
             label = r'Partial optimum $\hat{C}_L$')
    plt.plot(CL_optLst, Aw_i, color = 'orange', linestyle = 'dashed',
             label = r'Partial optimum $A_w$')
    plt.xlim((CL_i[0], CL_i[-1]))
    plt.ylim((Aw_i[0], Aw_i[-1]))
    plt.xlabel(r'$\hat{C}_L$')
    plt.ylabel(r'$A_w$')
    plt.clabel(cp, inline=True, 
              fontsize=10)
    plt.legend(loc = 2)
    plt.title(r'WPF in $\hat{C}_L$ - $A_w$ design space')