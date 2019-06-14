# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:43:26 2019

@author: hksam
"""

#import sys
import numpy as np
import os
from pathlib import Path
os.chdir(Path(__file__).parents[6])
import numpy as np
import scipy.linalg as slin
import matplotlib.pyplot as plt
#import control.matlab as control
import A22DSE.Models.STRUC.current.Structural_Model.struc_functions as StrucFun
import A22DSE.Models.STRUC.current.Class_II.Aeroelasticity.SteadyFuncs as AE
#from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
#from A22DSE.Parameters.Par_Class_Conventional import Conv
# =============================================================================
#                               FUNCTIONS
# =============================================================================
def plotV4(X, Y, Z1, Z2, Z3, Z4):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(X, Y, Z1, color='black')
    ax.plot_wireframe(X, Y, Z2, color = 'blue')
    ax.plot_wireframe(X, Y, Z3, color = 'green')
    ax.plot_wireframe(X, Y, Z4, color = 'red')
    ax.set_title('wireframe');
    
    return

def plotV2(X, Y, Z1, Z2):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(X, Y, Z1, color='black')
    ax.plot_wireframe(X, Y, Z2, color = 'red')
    ax.set_title('wireframe');
    
    return

def plotContour(X,Y, Z1, Z2):
    
    plt.figure()
    cp = plt.contour(X,Z1,Y)
    plt.axhline(Z2)
    plt.clabel(cp, inline=True, fontsize=10)    
    return

def FindDrivingConstraint(V1, V2, V3):
    V_constr = np.ones(np.shape(V1))
    
    
    for i in range(len(V1[:][0])):
        for j in range(len(V1[0][:])):
            V_constr[i][j] = np.min([V1[i][j], V2[i][j], V3[i][j]])
    
    return V_constr

def Intersect(y,z):
    idx = int((np.argwhere(np.diff(np.sign(y 
            - z))).flatten()))
    
    x = np.average(y[idx] + z[idx])/2
    return x
    

# =============================================================================
#                                   MAIN
# =============================================================================
    
def ComputeElasticity(Aircraft, ISA_model, height, V_req, plot):
    
    # Constants
    xtheta = 0.4                             # assumed
    rtheta = 0.3                             # assumed
    CLdelta = np.deg2rad(1.8)                # procedure from paper
    CMacdelta = -0.010149
    n = Aircraft.ParStruc.n_stiff            #stiffeners
    A_stiff = Aircraft.ParStruc.A_stiff      # Area stiffeners
    
    # initialise airfoil object
    airfoil = AE.airfoilAE(0, 0, xtheta, 
                           rtheta, CLdelta, CMacdelta, Aircraft)
    
    t_skinLst = np.linspace(0.0005,0.005, 10)               #X
    t_ribLst  = np.linspace(0.0005, 0.005, 10)              #Y
    
    SKIN, RIB = np.meshgrid(t_skinLst, t_ribLst)
    
    KthetaLst = np.ones(np.shape(SKIN))
    for i, t_skin in enumerate(t_skinLst):
        for j, t_rib in enumerate(t_ribLst):
            KthetaLst[i][j] = (float(StrucFun.TorsionalStiffness(
                    airfoil.c, Aircraft, t_skin, t_rib)))
    
    
    KhLst = StrucFun.moi_wing(airfoil.c, Aircraft)*1e12
    
    Vdiv_sl = AE.ComputeDivSpeed(airfoil, KthetaLst, height, ISA_model)
    Vcr_sl  = AE.ComputeControlReversal(airfoil, KthetaLst, height, 
                                        ISA_model)
    
    Vfl_sl  = AE.ComputeFlutter(airfoil, KhLst, KthetaLst, height,
                                ISA_model)
    
    V_constr_sl = FindDrivingConstraint(Vdiv_sl, Vcr_sl, Vfl_sl[0])
    V_req_arr = np.ones(np.shape(SKIN)) * V_req
    # =====================================================================
    #                                   PLOTTING
    # =====================================================================
    if plot == True:
        plotV2(SKIN, RIB, V_constr_sl, V_req_arr)
        plotContour(SKIN, RIB, V_constr_sl, V_req)
        plotV4(SKIN, RIB, Vdiv_sl, Vcr_sl, Vfl_sl[0], V_req_arr)

    return Vdiv_sl, Vcr_sl, Vfl_sl
    # Compute mass of skin, rib combination
    
    #find thicknesses that satisfy constraints
def ComputeMinWB(Aircraft, ISA_model, height, V_constr):
    
    t_skinLst = np.linspace(0.0005,0.005, 10)               #X
    t_ribLst  = np.linspace(0.0005, 0.005, 10)              #Y
    rho_Al = Aircraft.ParStruc.rho_Al
    rho_comp = Aircraft.ParStruc.rho_comp
    A_stiff = Aircraft.ParStruc.A_stiff
    n       = Aircraft.ParStruc.n_stiff
    
    SKIN, RIB = np.meshgrid(t_skinLst, t_ribLst)
    
    V_valid = ComputeElasticity(Aircraft, ISA_model, height, V_constr, False)
    
    idx = np.where(V_valid > V_constr)
    
    dimLst = []
    massLst = []
    col_idx = list(idx[1])

    for j, rowi in enumerate(list(idx[0])):
        idy = col_idx[j]
        dimLst.append(([SKIN[rowi][idy], RIB[rowi][idy]]))
    

    for i, dimi in enumerate(dimLst):
        skin = dimi[0]
        rib  = dimi[1]
        massLst.append((StrucFun.wing_struc_mass(Aircraft, skin, n, A_stiff, 
                                        rib, rho_Al, rho_comp)))
        
    argdes = np.argmin(massLst)
    
    dim_des = dimLst[argdes]

    return dim_des

# Constants








# =============================================================================
#                                   LEGACY CODE
# =============================================================================
#Vdiv = []
#Vcr  = []
#
#for i, Ktheta in enumerate(KthetaLst):
#    
#    airfoil.Ktheta = Ktheta
#    Vdiv.append(AE.ComputeDivSpeed(airfoil, 20000, ISA_model))
#    Vcr.append(AE.ComputeControlReversal(airfoil, 20000, ISA_model))
#
#
#Vflut = []
#for i, Kh in enumerate(KhLst):
#    
#    airfoil.Kh = Kh
#    Vflut.append(AE.ComputeFlutter(airfoil, 0, ISA_model))
#    
##plt.clf()    
#plt.figure()
#
#plt.plot((KthetaLst), Vdiv, label = 'Divergence Speed')
#plt.plot((KthetaLst), Vcr, label = 'Reverse Control')
#plt.axhline(y = Conv.ParAnFP.V_cruise*1.15, color = 'r', label = 'Cruise')
#plt.axhline(y = Conv.ParAnFP.V_dive, color = 'g', label = 'Dive')
#plt.legend()
#
#
##
##plt.figure(2)
##plt.plot(KhLst, Vflut)
##
##plt.show()
    
