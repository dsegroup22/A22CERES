# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:18:58 2019

@author: hksam
"""
import sys
sys.path.append('../../../../')
import numpy as np
from A22CERES.A22DSE.Models.EI.FuelBurn import GetEngineProp, GetFuelBurn
from A22CERES.A22DSE.Models.EI.classEILst import pollutantLst

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
    AFstoic = 15.6
    R = AF/AFstoic
    
    #Convert kerosene to molar mass
    molar_ker = FuelMass/MM_ker
    
    if 0.90 < R <= 1.00:
        
        #Mole per mole kerosene
        f_CO2 = 10
        f_H2O = 11
        f_N   = 58.28
        f_O   = 15.5       
        
        #Convert to kg
        CO2 = f_CO2 * molar_ker * MM_CO2
        H2O = f_H2O *  molar_ker * MM_H2O
        N2  = f_N * molar_ker * MM_N2
        CO  = 0
        H2  = 0
        O2  = 0
        
        ## convert in kg
        
        return [CO2, CO, H2O, H2, N2, O2]
        
    elif 0 < R <= .90:
        
        #Product Factors Constants       
        f_CO2 = 10
        f_H2O = 11
        f_N   = 3.76 * f_O/R
        f_O   = f_O/R -15.5
        
        #Convert to kg
        CO2 = f_CO2 * molar_ker * MM_CO2
        H2O = f_H2O *  molar_ker * MM_H2O
        N2  = f_N * molar_ker * MM_N2
        CO  = 0
        H2  = 0
        O2  = f_O * molar_ker * MM_O2
        return [CO2, CO, H2O, H2, N2, O2]
    
    elif R > 1.00:
        
        ## case when CO == 0
        
        #Mole per mole kerosene
        
        f_CO2 = 10
#        f_CO  = 20 - 31/R
        f_N   = 58.28/R
        f_H   = 31 - 31/R
        f_O   = 31/R - 20
        
        #Convert to kg
        CO2 = f_CO2 * molar_ker * MM_CO2
        H2O = f_O * molar_ker * MM_H2O
        N2  = f_N * molar_ker * MM_N2
        CO  = 0
        H2  = f_H * molar_ker * MM_H2
        O2  = 0
        
        return [CO2, CO, H2O, H2, N2, O2]
    
    else:
        return ValueError("Negative Air-to-Fuel ratio!")
        
    return None #should not get here
    
def GetEI(AltitudeProfile, MachProfile, resolution):
    
    '''
    INPUT: Masses of the polluting reaction products
    OUTPUT: Returns the CO2-eq. [kg] of the burnt fuel AND 
    the radiative forcing of the fuel burn [W/m2]
    DESCRIPTION:
    '''
    EngineProp=[]
    if len(AltitudeProfile)==len(MachProfile):
        for i in range(len(AltitudeProfile)):            
            EngineProp.append(GetEngineProp(AltitudeProfile[i],\
                                            MachProfile[i])[0,4])
    else:
        raise "Error: length of Altitude Profile list and Mach Profile list\
        different"
        
    Fuel = GetFuelBurn(EngineProp, resolution)
    AF = "get inlet area rho*V**L"/np.array(EngineProp)
    
    Products = []
    for i in range(len(AF)):
        Products.append(GetReactionProducts(AF, EngineProp))
    
    return Fuel, EIGWP, EIRF
    

#
#def GetFuelBurn(mdot):
#    
#    '''
#    INPUT: air-to-fuel ratio, mass fuel flow
#    OUTPUT: reaction products decomposition
#    DESCRIPTION: Reads fuel burn from .txt file output 
#    '''


    