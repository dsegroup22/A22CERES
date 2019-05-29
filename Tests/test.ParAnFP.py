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
os.chdir(Path(__file__).parents[1])
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22CERES.A22DSE.Parameters.Par_Class_Diff_Configs import ComputeCD0
from A22DSE.Parameters.TestAC280519 import TestAC
#from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_CD0 import CD0


def test_CD0():
    CD0_curr = ComputeCD0(TestAC)
    assert (np.isclose(CD0_curr, TestAC.ParAnFP.CD0))
    
    
    