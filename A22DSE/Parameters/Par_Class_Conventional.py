       
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:55:52 2019

@author: Nout



THIS FILE IS USED FOR THE FINAL DESIGN OF THE AIRCRAFT. IF YOU WANT TO ADD
PARAMETERS OBTAINED FROM CLASS II SIZING, 
GO TO A22DSE.Models.def_Collection_ClassII_Sizing
IF YOU HAVE A MORE ADVANCED SIZING METHOD, PLEASE TELL ME BEFORE YOU APPEND IT
ANYWHERE.
"""
# =============================================================================
#                            IMPORT NECESSARY MODULES
# =============================================================================

import os
from pathlib import Path
os.chdir(Path(__file__).parents[2])
import time

from A22DSE.Parameters.Par_Class_Diff_Configs import (Conv, ClassIAircraft,\
PrelimTail, ClassI_AndAHalf, ComputeCD0)
from A22DSE.Models.def_Collection_ClassII_Sizing import ClassIISizing
from A22DSE.Models.Class_II_Weight.Class_II_Total import ClassIIWeightIteration
from A22DSE.Models.AnFP.Current.Class_II.\
WingDesign.TransPlanform import ClassII_Planform
#shortcuts
Layout = Conv.ParLayoutConfig
anfp = Conv.ParAnFP
struc= Conv.ParStruc
assert isinstance(Conv.ParCntrl, object)
sc = Conv.ParCntrl
Payload=Conv.ParPayload
Payload.m_payload = 9700.
def TotalAC(Conv):
    start_time = time.time()
    #CLASS I
    ClassIAircraft(Conv)
    ClassI_AndAHalf(Conv)
    PrelimTail(Conv)
    ComputeCD0(Conv)
    
    Conv.ParAnFP.TtoW = Conv.ParAnFP.TtoW+0.15
    
    #CLASS II
    
    ClassIISizing(Conv)
    ClassIIWeightIteration(Conv)
    ClassII_Planform(Conv)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
TotalAC(Conv)
# =============================================================================
# #saving object as txt file
# =============================================================================

#file_path = 'A22DSE\Parameters\ParametersConv.txt'
#if os.path.isfile(file_path):
with open('A22DSE\Parameters\ParametersConv.txt', 'w+') as f:
    print('ParAnFP', file = f)
    print(vars(Conv.ParAnFP), file=f)
    print('\n\n ParPayload', file = f)
    print(vars(Conv.ParPayload), file=f)
    print('\n\n ParCntrl', file = f)
    print(vars(Conv.ParCntrl), file=f)
    print('\n\n ParCostLst', file = f)
    print(vars(Conv.ParCostLst), file=f)
    print('\n\n ParStruc', file = f)
    print(vars(Conv.ParStruc), file=f)
    print('\n\n ParProp', file = f)
    print(vars(Conv.ParProp), file=f)
    print('\n\n ParClassII', file = f)
    print(vars(Conv.ParClassII_LG), file =f)
    print('\n\n ParLayoutConfig',file =f)
    print(vars(Conv.ParLayoutConfig), file =f)
    print('\n\n ConversTool', file = f)
    print(vars(Conv.ConversTool), file=f)


s = open("A22DSE\Parameters\ParametersConv.txt").read()
s = s.replace(',', '\n')
f = open("A22DSE\Parameters\ParametersConv.txt", 'w')
f.write(s)
f.close()

     

