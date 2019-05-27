# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
#import sys.path.append(Documents\DSE\A22DSE\CostModel\All_dic_Parameters.py)

import sys
sys.path.append('../')

from All_dic_Parameters import Parameters as par
#Non-recurring costs
# Takes a vector with 7 aircraft weight parameters in kg as an input
# Order of the inputs:
# Wing, Empennage, Fuselage, Landing Gear, Engines, Systems, Payloads
# Cost output is in 2002 USD
def nrcosts(CompMass):
    cost=0
    factor=np.array([17731,52156,32093,2499,8691,34307,10763])    #Cost factors in $/lbs
    cost=CompMass*par.get("lbs2kg")*factor    #Multiplies costs factors by weight in lbs
    return cost

def taartplot(CompMass):
    labels = ['Wing', 'Empennage', 'Fuselage', 'Landing Gear', 'Engines', 'Systems', 'Payloads']
    plt.pie(nrcosts(CompMass),labels=labels, autopct='%1.1f%%')
    return plt.show()

