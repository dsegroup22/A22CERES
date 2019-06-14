# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:42:58 2019

@author: hksam
"""

import sys
import os
from pathlib import Path
os.chdir(Path(__file__).parents[3])
import numpy as np
from A22DSE.Models.EI.FuelBurn import GetEngineProp, GetFuelBurn
from A22DSE.Models.EI.classEILst import (pollutantLst)
import A22DSE.Models.EI.ReactionComposition as EI
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model

ddata = 49
AltitudeLst = data[:ddata, 0]
MachLst     = data[::ddata, 1]
EI.GetEI(AltitudeLst, MachLst, 100, Conv, ISA_model)



