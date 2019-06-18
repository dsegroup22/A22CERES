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
from A22DSE.Models.STRUC.current.Class_II.Aeroelasticity import SteadyMain
#from A22DSE.Parameters.Par_Class_Conventional import Conv
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

'''
ASSUMPTIONS

- Cl_climb constraint 1.03/1.1
'''

# =============================================================================
#                       SELECTION VARIABLES AND CONSTANTS
# =============================================================================

def ComputePlanform(Aircraft, ISA_model, res, Aw, plot):
#    res = 500
    
    CL_i = np.linspace(0.4, 1.1, res)
    sweep_i = np.linspace(np.deg2rad(0), np.deg2rad(40), res)
    #tc_w  = np.linspace(0.10, 0.15, 4)
    TSFC = Aircraft.ParProp.SFC_cruise*3600
    CL, sweep = np.meshgrid(CL_i, sweep_i)
    theta2 = FormFuncs.ComputeTheta2(Aircraft, ISA_model)
    theta3 = FormFuncs.ComputeTheta3(Aircraft, ISA_model)
    Fprop = FormFuncs.ComputeFprop(Aircraft, ISA_model, TSFC)
    
    # =========================================================================
    #                       COMPUTE CONTOURS
    # =========================================================================
    
    # wing penalty function contours
    FWP   = FormFuncs.ComputeFWP(Aircraft, Fprop, theta2, theta3, Aw, 
                                 CL, sweep)
    
    # t/c contours
    
    # L/D contours
    
    
    # =========================================================================
    #                       COMPUTE PARTIAL OPTIMA
    # =========================================================================
    
    # Optimum sweep
    
    sweep_opt = (FormFuncs.ComputePartialSweepOpt(Aircraft))
#    print(sweep_opt)
    # Optimum CL for minimum FWP
    CL_optLst = []
    for i, sweepi in enumerate(sweep_i):
        y = FormFuncs.ComputePartialCLopt(Aircraft, 
            ISA_model, theta2, theta3, Fprop, TSFC, Aw, sweepi, CL_i)
        CL_optLst.append(float(y.x))
#        if i%10 == 0:
#            print(y.success)
    
    def Intersect(y,z):
        idx = int((np.argwhere(np.diff(np.sign(y 
                - z))).flatten()))
        
        x = np.average(y[idx] + z[idx])/2
        return x
    
    # Optimum CL/CD
# =============================================================================
#                       CONSTRAINTS
# =============================================================================
        
        # Span-loading / Take-off field length
    WB = FormFuncs.ComputeSpanLoadingCL(Aircraft, ISA_model, Fprop, theta2, 
                                      theta3, TSFC, sweep_opt, Aw, CL_i)
        
    CL_buffet = 0.91  # NASA paper of airfoil  NASA SC( 2)-0714
    onset_margin = 1.40 # Regulations require 30% margin betw. onset and cruise
    CL_lim    = CL_buffet/onset_margin #+10% higher than certification
    CL_climb  = 1.03/1.1
    
# =============================================================================
#                           Design Parameters
# =============================================================================
    
#    CL_des = Intersect(CL_optLst, CL_i)
    CL_des = CL_lim
    tc_des = (FormFuncs.Compute_tc_limit(Aircraft, CL_des, sweep_opt)/
              np.cos(sweep_opt)**2)
    FWP_opt = FormFuncs.ComputeFWP(Aircraft, Fprop, theta2, theta3, Aw, 
                                   CL_des, sweep_opt)
# =============================================================================
#                       PLOTTING
# =============================================================================
    
    if plot == True:
        plt.clf()
        plt.figure(1)
        ax = plt.axes(projection='3d')
        ax.plot_wireframe(np.rad2deg(sweep), CL, FWP, color='black')
        ax.set_title('wireframe');
        
        plt.figure(2)
        cp = plt.contour(np.rad2deg(sweep), CL, FWP, 20)
        plt.plot(np.rad2deg(sweep_i), CL_optLst, color = 'r', 
                 linestyle ='dashed',
                 label = r'Partial optimum $\hat{C}_L$')
        plt.axvline(np.rad2deg(sweep_opt), color = 'orange', 
                    linestyle = 'dashed',
                    label = r'Partial optimum $\Lambda_w$')
        plt.axhline(CL_lim, linestyle = 'dashed', color = 'm',
                    label = 'Buffet Limit')
        plt.axhline(CL_climb, linestyle = 'dashed', color = 'c',
                    label = r'$C_{L_{climb}}$ constraint')
        
        plt.axvline()
        plt.ylim((CL_i[0], CL_i[-1]))
        plt.xlim((np.rad2deg(sweep_i[0]), np.rad2deg(sweep_i[-1])))
        plt.xlabel(r'$\Lambda_w$')
        plt.ylabel(r'$\hat{C}_L$')
        plt.clabel(cp, inline=True, 
                  fontsize=10)
        plt.legend(loc = 3)
        plt.title(r'WPF in $\Lambda_w$ - $\hat{C}_L$ design space')
    
    return CL_des, tc_des, FWP_opt


def ClassII_Planform(Aircraft):
    
    struc = Aircraft.ParStruc
    step = 100
    Aircraft.ParAnFP.C_L_design, Aircraft.ParAnFP.tc_w, Aircraft.ParAnFP.FWP = (
    ComputePlanform(Aircraft, ISA_model, step, Aircraft.ParAnFP.A, False))
#    Aircraft.ParAnFP.S = Aircraft.ParStruc.MTOW / \
#    (ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[-1]*0.5*\
#    Aircraft.ParAnFP.V_cruise**2 * Aircraft.ParAnFP.C_L_design*1.025)*9.81
# =============================================================================
#                                   WING BOX
# =============================================================================

    struc.t_skin, struc.t_rib = SteadyMain.ComputeMaxAwStruct(Aircraft, 
        ISA_model, 0, Aircraft.ParAnFP.V_dive, np.arange(10, 15, 1))
    
    return