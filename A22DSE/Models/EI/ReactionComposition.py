# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:18:58 2019

@author: hksam
"""
import sys
import os
from pathlib import Path
os.chdir(Path(__file__).parents[3])
import numpy as np
from A22DSE.Models.EI.FuelBurn import GetEngineProp, GetFuelBurn
from A22DSE.Models.EI.classEILst import pollutantLst, pollutant

def PollutantGWP():
    
    # array is defined as [GWP20, GWP100, GWP500]
    CO2 = np.array([1,1,1]) 
    CO  = np.array([10, 3.0, 0]) #from IPCC paper
    H2O = np.array([-0.001,0.0005,0]) #from Near-surface RF paper
    N2O = np.array([268, 298, 190])   # IPCC

#    
    return np.array([CO2, CO, H2O, N2O])

def PollutantRF():
    CO2 = np.array([1.985])  #IPCC 5ARF 2013
    CO = np.array([0.024])   # CO paper
    H2O = np.array([0.004])  #
    N2O = np.array([0.193])  # IPCC 5ARF 2013
    
    return np.array([CO2, CO, H2O, N2O])

def EmissionIndexLow():
    
                    #CO2, CO, H2O, N2O    
    return np.array([3.16, 0.002, 1.24, 0.012])

def EmissionIndexHigh():
    
                    #CO2, CO, H2O, N2O    
    return np.array([3.16, 0.003, 1.24, 0.017])

def PollutantArrHigh():
    
    # array is defined as [GWP20, GWP100, GWP500]
    CO2 = np.array([np.array([1,1,1]), np.array([4.08])])
    CO  = np.array([np.array([14, 4.4, 0]), np.array([0.024])])
    H2O = np.array([np.array([-0.001,0.0005,0]), np.array([0.004])])      
    H2 = np.array([np.array([0,0,0]), np.array([0])])
    N2 = np.array([np.array([0,0,0]), np.array([0])])
    O2 = np.array([np.array([0,0,0]), np.array([0])])

#    
    return np.array([CO2, CO, H2O, H2, N2, O2])


def GetReactionProducts(AF, FuelMass):
    '''
    INPUT: air-to-fuel ratio, FuelMass at time step
    OUTPUT: reaction products decomposition: [CO2, CO, H2O, H2, N2, O2]
    DESCRIPTION: programmes the method shown in this Algerian paper: "Evolution
    de la composition des gaz brules Lors de la combustion du kerosene"
    '''
    
    ## CONSTANTS
    f_O = 15.5
    MM_CO2 = 44.009/1000
#    MM_CO = 28.0/1000
    MM_H2O = 18.0/1000
    MM_H2 = 2.016/1000
    MM_N2 = 28.0/1000
    MM_O2 = 32.0/1000
    MM_ker = 142.18/1000
    
    #Get R value
    AFstoic = 1
    R = AF/AFstoic
    
    #Convert kerosene to molar mass
    molar_ker = FuelMass/MM_ker
    out = []
    for i, Ri in enumerate(R):
        f_O = 15.5
        if 0.90 < Ri <= 1.00:
#            print('In 0.90 < Ri < 1.00', Ri)             
            #Mole per mole kerosene
            f_CO2 = 10
            f_H2O = 11
            f_N   = 58.28
            f_O   = 15.5       
            
            #Convert to kg
            CO2 = f_CO2 * molar_ker[i] * MM_CO2
            H2O = f_H2O *  molar_ker[i] * MM_H2O
            N2  = f_N * molar_ker[i] * MM_N2
            CO  = 0
            H2  = 0
            O2  = 0
            
            ## convert in kg
            
            out.append([CO2, CO, H2O, H2, N2, O2])
            
        elif 0.5 < Ri <= .90:
#            print('In 0.< Ri < .90', Ri)            
            #Product Factors Constants       
            f_CO2 = 10
            f_H2O = 11
            f_N   = 3.76 * f_O/Ri
            f_O   = f_O/Ri - 15.5
            
            #Convert to kg
            CO2 = f_CO2 * molar_ker[i] * MM_CO2
            H2O = f_H2O *  molar_ker[i] * MM_H2O
            N2  = f_N * molar_ker[i] * MM_N2
            CO  = 0
            H2  = 0
            O2  = f_O * molar_ker[i] * MM_O2
            out.append([CO2, CO, H2O, H2, N2, O2])
        
        elif 1.00 < Ri <= 1.55:
#            print('In Ri > 1.00', Ri)
            ## case when CO == 0
            
            #Mole per mole kerosene
            
            f_CO2 = 10
    #        f_CO  = 20 - 31/Ri
            f_N   = 58.28/Ri
            f_H   = 31 - 31/Ri
            f_O   = 31/Ri - 20
            
            #Convert to kg
            CO2 = f_CO2 * molar_ker[i] * MM_CO2
            H2O = f_O * molar_ker[i] * MM_H2O
            N2  = f_N * molar_ker[i] * MM_N2
            CO  = 0
            H2  = f_H * molar_ker[i] * MM_H2
            O2  = 0
            
            out.append([CO2, CO, H2O, H2, N2, O2])
        
        elif Ri > 1.55 or Ri < 0.5:
            '''
            Not considered
            '''
#            print('In Ri > 1.55', Ri)
            CO2 = 0
            H2O = 0
            N2  = 0
            CO  = 0
            H2  = 0
            O2  = 0
            out.append([CO2, CO, H2O, H2, N2, O2])
        
        else:
#            print(Ri)
            return ValueError("Negative Air-to-Fuel ratio!")
        
    return out            
#        return None #should not get here
    
def GetEI(AF, mdot, time, Aircraft, ISA_model, Pollutants, Mair):
    
    '''
    INPUT: Masses of the polluting reaction products
    OUTPUT: Returns the CO2-eq. [kg] of the burnt fuel AND 
    the radiative forcing of the fuel burn [W/m2]
    DESCRIPTION:
    '''

    Products = np.array(GetReactionProducts(AF, mdot))
    GWP = []
    RF = []
    M_atmos = 5.5e18
    dt = time[1:] - time[:-1]
#    print(len(Products))
    for j, Product in enumerate(Products[1:]):
        for i, producti in enumerate(Product):
#            print(dt[j])
            GWPi = producti * Pollutants[i][0] * dt[j]
            RFi  = producti*1e6/M_atmos * Pollutants[i][1]
            GWP.append(GWPi)
            RF.append(RFi)
    
    EIGWP = np.array(GWP)
    EIRF = np.sum(RF)/len(RF)

    return EIGWP, EIRF, Products

# =============================================================================
#                               LEGACY
# =============================================================================

#def PollutantArrLow():
#    
#    # array is defined as [GWP20, GWP100, GWP500]
#    CO2 = np.array([np.array([1,1,1]), np.array([1.985])])
#    CO  = np.array([np.array([2.8,1.0,0]), np.array([0.024])])
#    H2O = np.array([np.array([-0.004,0.002,0]), np.array([0.034])])      
##    CH4 = pollutant('CH4', np.array([63,21,9]), 0.507)
##    N2O = pollutant('N2O', np.array([270,298, 190]), 0.983)
#    H2 = np.array([np.array([0,0,0]), np.array([0])])
#    N2 = np.array([np.array([0,0,0]), np.array([0])])
#    O2 = np.array([np.array([0,0,0]), np.array([0])])
#
##
#    return np.array([CO2, CO, H2O, H2, N2, O2])