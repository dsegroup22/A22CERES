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

'''
ASSUMPTIONS

 - r_theta can be varied by varying mass distribution, it is assumed to be 0.3
 - x_theta can be varied by varying mass distribution, it is assumed to be 0.4
 - contingency value for wing (group) weight is 15%, as wiring and secondary
     structure is not sized and also to account for simplification in approach.
'''


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
#            print(V1[i][j], V2[i][j], V3[i][j])
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
    
def ComputeElasticity(Aircraft, par, ISA_model, height, V_req, t_skinLst,
                      t_ribLst, plot):
    '''
    V_req := Design velocity of aircraft
    '''
#    # Constants
#    xtheta = 0.4                             # assumed
#    rtheta = 0.3                             # assumed
#    CLdelta = np.deg2rad(1.8)                # procedure from paper
#    CMacdelta = -0.010149
#    n = Aircraft.ParStruc.n_stiff            #stiffeners
#    A_stiff = Aircraft.ParStruc.A_stiff      # Area stiffeners
#    
#    # initialise airfoil object
#    airfoil = AE.airfoilAE(0, 0, xtheta, 
#                           rtheta, CLdelta, CMacdelta, Aircraft)
    
#    t_skinLst = np.arange(0.001,0.0045, 0.0005)               #X
#    t_ribLst  = np.arange(0.001, 0.0045, 0.0005)              #Y
    
    SKIN, RIB = np.meshgrid(t_skinLst, t_ribLst)
    
    KthetaLst = np.ones(np.shape(SKIN))
    KhLst     = np.ones(np.shape(SKIN))
    for i, t_skin in enumerate(t_skinLst):
        for j, t_rib in enumerate(t_ribLst):
            KthetaLst[i][j] = (float(StrucFun.TorsionalStiffness(
                    par.c, Aircraft, t_skin, t_rib)))
            KhLst[i][j] = StrucFun.moi_wing(par.c, Aircraft, t_skin, t_rib)
    
    Vdiv = AE.ComputeDivSpeed(par, KthetaLst, height, ISA_model)
    Vcr  = AE.ComputeControlReversal(par, KthetaLst, height, 
                                        ISA_model)
    
    Vfl  = AE.ComputeFlutter(par, KhLst, KthetaLst, height,
                                ISA_model)
    print(Vdiv, Vcr, Vfl[0])
    V_constr = FindDrivingConstraint(Vdiv, Vcr, Vfl[0])
    V_req_arr = np.ones(np.shape(SKIN)) * V_req
    # =====================================================================
    #                                   PLOTTING
    # =====================================================================
    if plot == True:
        plotV2(SKIN, RIB, V_constr, V_req_arr)
        plotContour(SKIN, RIB, V_constr, V_req)
        plotV4(SKIN, RIB, Vdiv, Vcr, Vfl[0], V_req_arr)

    return V_constr,Vdiv, Vfl, Vcr
    # Compute mass of skin, rib combination
    
    #find thicknesses that satisfy constraints
def ComputeMinWB(Aircraft, par, ISA_model, height, V_constr, t_skinLst,
                 t_ribLst):
    
    # contingency factorsCOM\Current\ceres.dat
    
    uncert = 0.15
    
#    t_skinLst = np.arange(0.001,0.0045, 0.0005)               #X
#    t_ribLst  = np.arange(0.001, 0.0045, 0.0005)              #Y
    
    SKIN, RIB = np.meshgrid(t_skinLst, t_ribLst)
    
    V_AE = ComputeElasticity(Aircraft, par, ISA_model,
                                height, V_constr, t_skinLst, t_ribLst, False)
#    print(V_valid, V_constr)
    idx = np.where(V_AE > V_constr)

    if len(idx[0]) == 0:
        return [-1, -1]
    dimLst = []
    massLst = []
    col_idx = list(idx[1])
    
    for j, rowi in enumerate(list(idx[0])):
        idy = col_idx[j]
        dimLst.append(([SKIN[rowi][idy], RIB[rowi][idy]]))

    for i, dimi in enumerate(dimLst):
        skin = dimi[0]
        rib  = dimi[1]
        massLst.append((StrucFun.wing_struc_mass(Aircraft, skin, rib)))
        
    argdes = np.argmin(massLst)
    
    dim_des = dimLst[argdes]
    
    if massLst[argdes] > Aircraft.ParStruc.Weight_WingGroup * (1-uncert):
#        print(massLst[argdes])
        return [-1, -1]
    
    return dim_des

def ComputeMaxAwStruct(Aircraft, ISA_model, height, V_constr,
                       Aw):
    
    # Constants
    xtheta = 0.4                             # assumed
    rtheta = 0.4                             # assumed
    CLdelta = np.deg2rad(1.8)                # procedure from paper
    CMacdelta = -0.010
#    n = Aircraft.ParStruc.n_stiff            #stiffeners
#    A_stiff = Aircraft.ParStruc.A_stiff      # Area stiffeners
    S_ac = Aircraft.ParAnFP.S
    t_skinLst = np.arange(0.0005, 0.0055, 0.0005)
    t_ribLst = np.arange(0.0005, 0.0055, 0.0005)

    dim_des = []
    mass_des = []
    for Awi in Aw:
        b_ac = np.sqrt(Awi * S_ac)
        
        # initialise airfoil object
        a = AE.airfoilAE(b_ac, 0, 0, xtheta,
                               rtheta, CLdelta, CMacdelta, Aircraft)
#        print(a.c, a.xtheta)
        dim_desi = ComputeMinWB(Aircraft, a, ISA_model, height, V_constr,
                                t_skinLst, t_ribLst)
#        print(dim_desi)
        dim_des.append(dim_desi)
        mass_des.append(StrucFun.wing_struc_mass(Aircraft, 
                                                 dim_desi[0], dim_desi[1]))
    
    idmax = np.argmax(mass_des)
    
    return dim_des[idmax], Aw[idmax]


#ComputeMaxAwStruct(Conv, ISA_model, 0, Conv.ParAnFP.V_cruise*1.15, np.arange(10, 16, 1))





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
    