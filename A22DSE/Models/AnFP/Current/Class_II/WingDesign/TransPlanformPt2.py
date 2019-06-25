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
from A22DSE.Models.STRUC.current.Class_II.Aeroelasticity import SteadyMain
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
#from A22DSE.Parameters.Par_Class_Conventional import Conv
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =============================================================================
#                       SELECTION VARIABLES AND CONSTANTS
# =============================================================================

def ComputeAwPlanform(Aircraft, ISA_model, res, plot):

    CL_i = np.linspace(0.3, 1.0, res)
    sweep_opt = (FormFuncs.ComputePartialSweepOpt(Aircraft))
    sweep_opt = np.deg2rad(0)
    #tc_w  = np.linspace(0.10, 0.15, 4)
    Aw_i = np.linspace(4, 25, res)
    TSFC = Aircraft.ParProp.SFC_cruise*3600
    CL, Aw = np.meshgrid(CL_i, Aw_i)
    
    theta2 = FormFuncs.ComputeTheta2(Aircraft, ISA_model)
    theta3 = FormFuncs.ComputeTheta3(Aircraft, ISA_model)
    Fprop = FormFuncs.ComputeFprop(Aircraft, ISA_model, TSFC)
    
# =============================================================================
#                       COMPUTE CONTOURS
# =============================================================================
    
        # wing penalty function contours
    FWP= FormFuncs.ComputeFWP(Aircraft, Fprop, theta2, 
                              theta3, Aw, CL, sweep_opt)
        # t/c contours
    
        # L/D contours
    
    
# =============================================================================
#                       COMPUTE PARTIAL OPTIMA
# =============================================================================
    
        # Optimum Aw
    Aw_opt = FormFuncs.ComputePartialAwOpt(Aircraft, ISA_model,
                            theta2, theta3, Fprop, TSFC, sweep_opt, CL_i)
    
        # Optimum CL w.r.t. Aw
    CL_optLst = []
    for i, Awi in enumerate(Aw_i):
        
        y = FormFuncs.ComputePartialCLopt(Aircraft, 
            ISA_model, theta2, theta3, Fprop, TSFC, Awi, sweep_opt, CL_i)
        CL_optLst.append(float(y.x))
    #    if i%10 == 0:
    #        print(y.success)
            
# =============================================================================
#                       CONSTRAINTS
# =============================================================================
    
        # Span-loading / Take-off field length
    WB = FormFuncs.ComputeSpanLoading(Aircraft, ISA_model, Fprop,theta2,theta3,
                                      TSFC, sweep_opt, CL_i)
        # Buffeting Limit
    CL_buffet = 0.75  # NASA paper of airfoil  NASA SC( 2)-0714
    onset_margin = .30 # Regulations require 30% margin betw. onset and cruise
    CL_lim    = CL_buffet*(1-onset_margin) #+10% higher than certification
    
        # Climb CL constraint
    CL_climb  = 1.03/1.1
        
        # Aw constraint from flutter
    
    #Aw_flut = SteadyMain.ComputeMaxAwStruct(Aircraft, ISA_model, 0,
    #        Aircraft.ParAnFP.V_dive, np.arange(10, 15, 1))[1]
    Aw_flut = 13
# =============================================================================
#                       PLOTTING
# =============================================================================
    
    if plot == True:
        lwdth = 2
        mksize = 4
        plt.rcParams.update({'font.size': 10})
        plt.clf()
        fig = plt.figure(1)
        ax = plt.axes(projection='3d')
        ax.plot_wireframe(CL, Aw, FWP, color='black')
        ax.set_title('wireframe');
        
        plt.figure(2)
        cp = plt.contour(CL, Aw, FWP, 10, colors = 'black')
        plt.plot(CL_i, Aw_opt, color = 'r', linestyle = 'dashed',
                 label = r'Partial optimum $\hat{C}_L$', linewidth = lwdth,
                 markersize = mksize, marker = 'o')
        plt.plot(CL_optLst, Aw_i, color = 'orange', linestyle = 'solid',
                 markersize = mksize, marker = 'v',
                 label = r'Partial optimum $A_w$', linewidth = lwdth)
    #    plt.plot(CL_i, WB, linestyle = 'dashed', color = 'purple')
        plt.axvline(CL_lim, linestyle = 'dashdot', color ='g',
                    label = 'Buffet Limit', linewidth = lwdth)
        plt.axhline(Aw_flut, linestyle = 'dotted', color = 'm',
                    label = 'Aeroelastic constraint', linewidth = lwdth)
        plt.xlim((CL_i[0], CL_i[-1]))
        plt.ylim((Aw_i[0], Aw_i[-1]))
        plt.xlabel(r'$\hat{C}_L$')
        plt.ylabel(r'$A_w$')
        plt.clabel(cp, inline=True, 
                  fontsize=12)
        plt.legend(loc = 1)
        plt.title(r'WPF in $\hat{C}_L$ - $A_w$ design space')
        
    return