# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:34:25 2019

@author: hksam
"""

import sys
sys.path.append('../../')
import os
from pathlib import Path 
import numpy as np
#os.chdir(Path(__file__).parents[1])
from A22CERES.A22DSE.Parameters.Par_Class_Conventional import Conv
from A22CERES.A22DSE.Parameters.Par_Class_Diff_Configs import ComputeCD0
from A22CERES.A22DSE.Models.Class_II_Weight.Class_II_Wing import Wing_Geo
from A22CERES.A22DSE.Parameters.TestAC280519 import TestAC
#from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_CD0 import CD0

 # return [Sweep_25_rad, Sweep_LE, Sweep_50, b, Taper, c_r, c_t, c_mac, y_mac]
def test_CD0():
    ''' 
    INPUT:
    OUTPUT:
    DESCRIPTION:                                                            '''
    CD0_curr = ComputeCD0(TestAC)
    assert (np.isclose(CD0_curr, TestAC.ParAnFP.CD0))
    return

def test_WingGeo():
    
    WingGeo_Curr = Wing_Geo(TestAC)
    
    
    
    
    return
    
    
    