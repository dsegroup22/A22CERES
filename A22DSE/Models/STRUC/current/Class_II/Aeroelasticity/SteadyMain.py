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
import control.matlab as control
import A22DSE.Models.STRUC.current.Structural_Model.struc_functions as StrucFun
import A22DSE.Models.STRUC.current.Class_II.Aeroelasticity.SteadyFuncs as AE
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
#from A22DSE.Parameters.Par_Class_Conventional import Conv
# =============================================================================
#                               FUNCTIONS
# =============================================================================
def plotV4(X, Y, Z1, Z2, Z3, Z4):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(SKIN, RIB, Z1, color='black')
    ax.plot_wireframe(SKIN, RIB, Z2, color = 'blue')
    ax.plot_wireframe(SKIN, RIB, Z3, color = 'green')
    ax.plot_wireframe(SKIN, RIB, Z4, color = 'red')
    ax.set_title('wireframe');
    
    return

def plotV2(X, Y, Z1, Z2):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(SKIN, RIB, Z1, color='black')
    ax.plot_wireframe(SKIN, RIB, Z2, color = 'red')
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
# =============================================================================
#                                   MAIN
# =============================================================================
# Constants
xtheta = 0.4
rtheta = 0.3
CLdelta = np.deg2rad(1.8)
CMacdelta = -0.010149
n = 20                                   # #stiffeners
A_stiff = 3.6*10**-5                     # Area stiffeners
rho_Al  = 2830
rho_comp = 1600


# initialise airfoil object
airfoil = AE.airfoilAE(0, 0, xtheta, 
                       rtheta, CLdelta, CMacdelta, Conv)

t_skinLst = np.linspace(0.0005,0.005, 10)               #X
t_ribLst  = np.linspace(0.0005, 0.005, 10)              #Y

SKIN, RIB = np.meshgrid(t_skinLst, t_ribLst)

KthetaLst = np.ones(np.shape(SKIN))
for i, t_skin in enumerate(t_skinLst):
    for j, t_rib in enumerate(t_ribLst):
        KthetaLst[i][j] = (float(StrucFun.TorsionalStiffness(airfoil.c, t_skin,
                                                 t_rib)))


KhLst = StrucFun.moi_wing(airfoil.c, SKIN, RIB, n, Conv, A_stiff) * 1e12

# divergence speed
Vdiv_sl = AE.ComputeDivSpeed(airfoil, KthetaLst, 0, ISA_model)
Vdiv_cr = AE.ComputeDivSpeed(airfoil, KthetaLst, 20000, ISA_model)

# reverse control speed
Vcr_sl  = AE.ComputeControlReversal(airfoil, KthetaLst, 0, ISA_model)
Vcr_cr  = AE.ComputeControlReversal(airfoil, KthetaLst, 20000, ISA_model)

# flutter speed
Vfl_sl  = AE.ComputeFlutter(airfoil, KhLst, KthetaLst, 0, ISA_model)
Vfl_cr  = AE.ComputeFlutter(airfoil, KhLst, KthetaLst, 20000, ISA_model)

# Compute the driving constraint
V_constr_sl = FindDrivingConstraint(Vdiv_sl, Vcr_sl, Vfl_sl[0])
V_constr_cr = FindDrivingConstraint(Vdiv_cr, Vcr_cr, Vfl_cr[0])

# constraint
V_TO    = np.ones(np.shape(SKIN)) * Conv.ParAnFP.V_max_TO
V_cr    = np.ones(np.shape(SKIN)) * Conv.ParAnFP.V_dive


# Compute mass of skin, rib combination
mass = StrucFun.wing_struc_mass(Conv, SKIN, n, A_stiff, RIB, rho_Al, rho_comp)

# =============================================================================
#                                   PLOTTING
# =============================================================================
#plotV2(SKIN, RIB, V_constr_sl, V_TO)
#plotV2(SKIN, RIB, V_constr_cr, V_cr)
#plotContour(SKIN, RIB, V_constr_sl, Conv.ParAnFP.V_max_TO)
#plotContour(SKIN, RIB, V_constr_cr, Conv.ParAnFP.V_dive)
#plotV4(SKIN, RIB, Vdiv_sl, Vcr_sl, Vfl_sl[0], V_TO)
#plotV4(SKIN, RIB, Vdiv_cr, Vcr_cr, Vfl_cr[0], V_cr)



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