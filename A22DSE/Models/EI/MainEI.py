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
#from A22DSE.Parameters.Par_Class_Conventional  import Conv

#results = main()[0]  
#actualresults = results.segments.values()
#mdot=None
#time = None
#V = None
#rho = None
#PollutantsHigh = EI.PollutantArrHigh()
##PollutantsLow  = EI.PollutantArrLow()
#
#for i in range(len(actualresults)):
#    
#    if i==0:
#        time = actualresults[i].conditions.frames.inertial.time[:,0]
#        mdot=actualresults[i].conditions.weights.vehicle_mass_rate[:,0]
#        V = actualresults[i].conditions.freestream.velocity[:,0]
#        rho = actualresults[i].conditions.freestream.density[:,0]
#        
#    else:
#        mdot = np.append(mdot,actualresults[i].conditions.weights.vehicle_mass_rate[:,0])
#        time = np.append(time,actualresults[i].conditions.frames.inertial.time[:,0])
#        V = np.append(V,actualresults[i].conditions.freestream.velocity[:,0])
#        rho = np.append(rho,actualresults[i].conditions.freestream.density[:,0])
#
#Mair = rho*np.pi*(Conv.ParProp.Engine_diameter)**2/4*Conv.ParProp.N_engines *\
#        V
#AF = rho*np.pi*(Conv.ParProp.Engine_diameter)**2/4*Conv.ParProp.N_engines/mdot
#
##EIGWP_0, EIRF_0 = EI.GetEI(AF, mdot, time, Conv, ISA_model,PollutantsLow,Mair)
#EIGWP_1, EIRF_1 = EI.GetEI(AF, mdot, time, Conv, ISA_model, PollutantsHigh,
#                           Mair)
##
EIGWP20_1 = np.sum(EIGWP_1[:,0])
EIGWP100_1 = np.sum(EIGWP_1[:,1])

n_ac = 12
a1 = 8      # 8 aircraft / year
a2 = 16     # 16 aircraft / year

#compute for total operations
EIGWPsum20  = 0  # iterator
EIGWPsum100 = 0  # iterator
t_mission   = 15 #years
fpd         = 4  # flights per day
opertime    = 250 #days

for year in range(t_mission):
    
    if year > 6:
        n_ac = n_ac + a2 * year
        EIGWPsum20 += EIGWP20_1 * n_ac * opertime * fpd
        EIGWPsum100 += EIGWP100_1 * n_ac * opertime * fpd
    else:
        n_ac = n_ac + a1 * year
        EIGWPsum20 += EIGWP20_1 * n_ac * opertime * fpd
        EIGWPsum100 += EIGWP100_1 * n_ac * opertime * fpd
        


#print("Minimum bound - GWP, RF", EIGWP_0, EIRF_0)
print("Lower bound - GWP20, GWP100, RF", EIGWPsum20/1e9*1.25, 
      EIGWPsum100/1e9*1.25, EIRF_1)


# =============================================================================
#                           Alternative
# =============================================================================


GWPLst = EI.PollutantGWP()
RFLst  = EI.PollutantRF()
IndicesH = EI.EmissionIndexHigh()
IndicesL = EI.EmissionIndexLow()
Mfuel = Conv.ParStruc.FW
MassAtmos = 5.5e18
# Compute GWP per flight

    #emission per flight
emissionLst = np.ones(np.shape(GWPLst))

def ComputeEmissions(GWP, RF, Products, Mfuel):
    for i in range(len(GWPLst[0,:])):
        emissionLst[:,i] = GWP[:,i] * Products * Mfuel
    
    emission_RF = Products * RF.T * Mfuel
    
    n_ac = 12
    a1 = 8      # 8 aircraft / year
    a2 = 16     # 16 aircraft / year
    
    #compute for total operations
    t_mission   = 15 #years
    fpd         = 4  # flights per day
    opertime    = 250 #days
    
    #copy emissionLst
    SumEmission = np.ones(np.shape(emissionLst))
    SumRF       = np.ones(np.shape(emission_RF))
    SumMfuel    = 0
    
    for year in range(t_mission):
        
        if year > 6: # +16 a.c. after 7 years
            n_ac = n_ac + a2 * year
            SumEmission += emissionLst * fpd * opertime * n_ac
            SumRF       += emission_RF * fpd * opertime * n_ac
            SumMfuel    += Mfuel * fpd * opertime *n_ac
        else:
            n_ac = n_ac + a1 * year
            SumEmission += emissionLst * fpd * opertime * n_ac
            SumRF       += emission_RF * fpd * opertime * n_ac
            SumMfuel    += Mfuel * fpd * opertime *n_ac

#    SumEmission = SumEmission/1e3
    SumEmission20 = SumEmission[:,0]
    SumEmission100 = SumEmission[:,1]
    
    SumRF       = np.average(SumRF)/MassAtmos
    
    return np.sum(SumEmission20), np.sum(SumEmission100), SumRF, SumMfuel

SumEmission20H, SumEmission100H, RFH, TotalFuel = ComputeEmissions(GWPLst, RFLst,
                    IndicesH,  Mfuel)

SumEmission20L, SumEmission100L, RFL, TotalFuel = ComputeEmissions(GWPLst,RFLst,
                                                IndicesL, Mfuel)
print('Upper bound - GWP20, GWP100, RF', SumEmission20H/1e9, SumEmission100H/1e9, RFH)
print('Lower bound - GWP20, GWP100, RF', SumEmission20L/1e9, SumEmission100L/1e9, RFL)


