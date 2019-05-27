# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:34:25 2019

@author: hksam
"""

import sys
sys.path.append('../../../../../')

import numpy as np
from A22DSE.Models.AnFP.Class_II.WingDesign.Functions import (OptimalARWing,
                                                              ComputeCL_eq,
                                                              CDpCurlFunc
                                                              )
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model

# =============================================================================
#
# =============================================================================
CL_eq = np.linspace(0.5, 1.5, 3)
ws = np.linspace(20000, 30000, 3)
Aw = np.linspace(5, 15, 3)
Sweep = np.deg2rad(np.linspace(15, 40, 3))

#Fprop = 3 # dummy
#Cdc = np.average([0.0005, 0.0010])
#

