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
from A22DSE.Models.SUAVE.testcase2 import main
#ddata = 49
#AltitudeLst = data[:ddata, 0]
#MachLst     = data[::ddata, 1]
#EI.GetEI(AltitudeLst, MachLst, 100, Conv, ISA_model)

results = main()   
actualresults = results.segments.values()
mdot=None
time = None
for i in range(len(actualresults)):
    if i==0:
        time = actualresults[i].conditions.frames.inertial.time[:,0] 
        mdot=actualresults[i].conditions.weights.vehicle_mass_rate[:,0]
    else:
        mdot = np.append(mdot,actualresults[i].conditions.weights.vehicle_mass_rate[:,0])
        time = np.append(time,actualresults[i].conditions.frames.inertial.time[:,0] )


