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

mass = 1000
bi   = Conv.ParAnFP.b/2
c    = StrucFun.chord(bi, Conv)

t_skinLst = np.linspace(0,0.005, 10)
t_ribLst  = np.linspace(0, 0.005, 10)



#Ktheta =    7e6
xtheta = 2
rtheta = 3
CLdelta = np.deg2rad(1.8)
Kh     = 16e6
CMacdelta = -0.010149


#mass, c, Kh, Ktheta, xtheta, rtheta, CLtheta, 
#                 CMacdelta, Aircraft

airfoil = AE.airfoilAE(mass, c, Kh, Ktheta, xtheta, 
                       rtheta, CLdelta, CMacdelta, Conv)

KthetaLst = []

for i, t_skin in enumerate(t_skinlst):
    KthetaLst.append(StrucFun.TorsionalStiffness(airfoil.c, t_skin,
                                                 t_ribLst[i]))
Vdiv = AE.ComputeDivSpeed(airfoil, 20000, ISA_model)
Vcr  = AE.ComputeControlReversal(airfoil, 20000, ISA_model)
print (Vdiv, Vcr)

