# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:51:07 2019

@author: kamph
"""


import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])
print(os.getcwd())
from A22DSE.Models.Class_II_Weight.Detailed_Class_II_Fuselage import FuselageWeight
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Parameters.TestAC280519 import TestAC
import numpy as np

def test_fuselage_weight():
    TestAC.ParAnFP.q_dive = 0.5* TestAC.ParAnFP.V_cruise**2 * 0.0880349
    TestAC.ParAnFP.n_ult = Conv.ParAnFP.n_ult
    Fuse_W = FuselageWeight(TestAC)[0] / 9.80665
    number = TestAC.ParStruc.Wf
    assert(np.isclose(Fuse_W, number, rtol = 0.10))

