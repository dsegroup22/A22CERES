# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:34:25 2019

@author: hksam
"""

import sys
sys.path.append('..')
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Parameters.Par_Class_Diff_Configs import ComputeCD0, ISA_model
#from A22DSE.Parameters.TestAC280519 import CreateTestAC
from A22DSE.Models.Class_II_Weight.Class_II_Wing import Wing_Geo
from A22DSE.Parameters.TestAC280519 import TestAC
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import (
        WSandTW)
import numpy as np

def test_CD0():
    ''' 
    INPUT:
    OUTPUT:
    DESCRIPTION:                                                            '''
    
    CD0_curr = ComputeCD0(TestAC)
    assert (np.isclose(CD0_curr, TestAC.ParAnFP.CD0))
    return

def test_WingGeo():
    ParAnFP = TestAC.ParAnFP
    WingGeo_Curr = Wing_Geo(TestAC)    
    WingGeoAC    = [ParAnFP.Sweep_25, ParAnFP.Sweep_LE, ParAnFP.Sweep_50,
                    ParAnFP.b, ParAnFP.taper, ParAnFP.c_r, ParAnFP.c_t,
                    ParAnFP.MAC, ParAnFP.y_MAC]
    assert (np.allclose(WingGeo_Curr, WingGeoAC))
    return
    
def test_WSandTW():
    out = WSandTW(False, TestAC,ISA_model)
    assert (np.isclose(out[0],Conv.ParStruc.MTOW))
        
    