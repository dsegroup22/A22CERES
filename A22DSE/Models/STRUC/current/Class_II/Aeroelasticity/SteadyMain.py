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

mass = Conv.ParStruc.Wing_weight / Conv.ParAnFP.b
bi   = Conv.ParAnFP.b/2
c    = StrucFun.chord(bi, Conv)

t_skinLst = np.linspace(0.0005,0.005, 10)
t_ribLst  = np.linspace(0.0005, 0.005, 10)

SKIN, RIB = np.meshgrid(t_skinLst, t_ribLst)

KthetaLst = []
for i, t_skin in enumerate(t_skinLst):
    KthetaLst.append(float(StrucFun.TorsionalStiffness(c, t_skin,
                                                 t_ribLst[i])))

#Ktheta =    7e6
xtheta = 0.4
rtheta = 0.3
CLdelta = np.deg2rad(1.8)
Kh     = 6.0390733142853239e-05 * 1e12
CMacdelta = -0.010149
KhLst = np.linspace(15e6, 20e6, 100)

#mass, c, Kh, Ktheta, xtheta, rtheta, CLtheta, 
#                 CMacdelta, Aircraft

airfoil = AE.airfoilAE(mass, c, Kh, KthetaLst[0], xtheta, 
                       rtheta, CLdelta, CMacdelta, Conv)

Vdiv = []
Vcr  = []

for i, Ktheta in enumerate(KthetaLst):
    
    airfoil.Ktheta = Ktheta
    Vdiv.append(AE.ComputeDivSpeed(airfoil, 20000, ISA_model))
    Vcr.append(AE.ComputeControlReversal(airfoil, 20000, ISA_model))


Vflut = []
for i, Kh in enumerate(KhLst):
    
    airfoil.Kh = Kh
    Vflut.append(AE.ComputeFlutter(airfoil, 0, ISA_model))
    
#plt.clf()    
plt.figure()

plt.plot((KthetaLst), Vdiv, label = 'Divergence Speed')
plt.plot((KthetaLst), Vcr, label = 'Reverse Control')
plt.axhline(y = Conv.ParAnFP.V_cruise*1.15, color = 'r', label = 'Cruise')
plt.axhline(y = Conv.ParAnFP.V_dive, color = 'g', label = 'Dive')
plt.legend()


#
#plt.figure(2)
#plt.plot(KhLst, Vflut)
#
#plt.show()