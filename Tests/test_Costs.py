# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:06:17 2019

@author: Nout
"""

import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])
from A22DSE.Models.CostModel.Current.TotalCost import TotalC
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
from A22DSE.Parameters.Par_Class_Conventional import Conv

def test_Cost():
    Cost = TotalC(Conv, ISA_model)[0]
    print(Cost)
    #110 is maximum requirement
    assert (Cost<110)