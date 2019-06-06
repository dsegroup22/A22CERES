# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:10:26 2019

@author: hksam
"""
import numpy as np
import matplotlib.pyplot as plt
#from All_dic_Parameters import Parameters as par
Mr = np.array([1.,2.,3.,4.,5.,6.,7.,8.])
Mnr = np.array([1.,2.,3.,4.,5.,6.,7.])

def RecurrCostFunc(Aircraft):
    
    Struct = Aircraft.ParStruct
    ConversTool = Aircraft.ConversTool
    CompMass = Struct.CompMass
    
    #INPUT: Mass of components [kg]
    #OUTPUT: Cost per component in USD 2K$
    #Description: Computes the cost for each component
    #             in 2Ky$. In the following order:
    #             [Wing, Empennage, Fuselage, LG, Installed Engines
    #             Systems, Payload, Final Assembly]
    
    RecurrTable = np.array([900, 2331, 967, 221, 374,
                            452, 564, 65])
    
    RecurrTable = RecurrTable/ConversTool.lbs2kg
    
    CostPerComp = CompMass*RecurrTable
    
    # Turn cost to 2K$
    Infl = 1.0447 # [%]
    
    CostPerComp = CostPerComp*Infl
    
    return CostPerComp

#Non-recurring costs
# Takes a vector with 7 aircraft weight parameters in kg as an input
# Order of the inputs:
# Wing, Empennage, Fuselage, Landing Gear, Engines, Systems, Payloads
# Cost output is in 2002 USD
def nrcosts(Aircraft):
    
    Struct = Aircraft.ParStruct
    ConversTool = Aircraft.ConversTool
    CompMass = Struct.CompMass
    
    cost=0
    factor=np.array([17731,52156,32093,2499,8691,34307,10763]) #Cost factors in $/lbs
    cost=CompMass/ConversTool.lbs2kg*factor #Multiplies costs factors by weight in lbs
    return cost

def piechartcosts(CompMass):
    if np.size(CompMass) == 7:
        labels = ['Wing', 'Empennage', 'Fuselage', 'Landing Gear', 'Engines',
                  'Systems', 'Payloads']
        plt.pie(nrcosts(CompMass),labels=labels, autopct='%1.1f%%', shadow=True, pctdistance=1.5, labeldistance=1.2)

    elif np.size(CompMass) == 8:
        labels = ['Wing', 'Empennage', 'Fuselage', 'Landing Gear', 'Engines', 
                  'Systems', 'Payloads', "Final Assembly"]
        plt.pie(RecurrCostFunc(CompMass),labels=labels, autopct='%1.1f%%', shadow=True)
    return plt.show()
piechartcosts(Mnr)


