# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:43:26 2019

@author: hksam
"""

import sys
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
from A22DSE.Parameters.Par_Class_Conventional import Conv

mass = 1000
bi   = Conv.ParAnFP.b/2
c    = StrucFun.chord(bi, Conv)
StrucFun.t_skin
Ktheta = StrucFun.TorsionalStiffness(c, StrucFun.t_skin, StrucFun.t_rib)
xtheta = 2
rtheta = 3
CLtheta = 57.3
CMacdelta = 57.3

airfoil = AE.airfoilAE(mass, Ktheta, xtheta, rtheta, CLtheta, CMacdelta, Conv)