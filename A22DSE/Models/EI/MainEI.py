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
#from A22DSE.Models.SUAVE.testcase2 import main
#from A22DSE.Parameters.Par_Class_Conventional import Conv

##results = main()[0]  
##actualresults = results.segments.values()
##mdot=None
##time = None
##V = None
##rho = None
#PollutantsHigh = EI.PollutantArrHigh()
#PollutantsLow  = EI.PollutantArrLow()
#
##for i in range(len(actualresults)):
##    
##    if i==0:
##        time = actualresults[i].conditions.frames.inertial.time[:,0]
##        mdot=actualresults[i].conditions.weights.vehicle_mass_rate[:,0]
##        V = actualresults[i].conditions.freestream.velocity[:,0]
##        rho = actualresults[i].conditions.freestream.density[:,0]
##        
##    else:
##        mdot = np.append(mdot,actualresults[i].conditions.weights.vehicle_mass_rate[:,0])
##        time = np.append(time,actualresults[i].conditions.frames.inertial.time[:,0])
##        V = np.append(V,actualresults[i].conditions.freestream.velocity[:,0])
##        rho = np.append(rho,actualresults[i].conditions.freestream.density[:,0])

Mair = rho*np.pi*(Conv.ParProp.Engine_diameter)**2/4*Conv.ParProp.N_engines *\
        V
AF = rho*np.pi*(Conv.ParProp.Engine_diameter)**2/4*Conv.ParProp.N_engines/mdot

EIGWP_0, EIRF_0 = EI.GetEI(AF, mdot, time, Conv, ISA_model, PollutantsLow,Mair)
EIGWP_1, EIRF_1 = EI.GetEI(AF, mdot, time, Conv, ISA_model, PollutantsHigh,
                           Mair)

EIGWP20_1 = np.sum(EIGWP_1[:,0])
EIGWP100_1 = np.sum(EIGWP_1[:,1])

#print("Minimum bound - GWP, RF", EIGWP_0, EIRF_0)
print("Max bound - GWP20, GWP100, RF", EIGWP20_1, EIGWP100_1, EIRF_1)











