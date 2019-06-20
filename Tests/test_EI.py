# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:40:04 2019

@author: hksam
"""

import sys
import numpy as np
import sys
import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])

from A22DSE.Models.EI.ReactionComposition import GetReactionProducts


def test_GetReactionProducts():
    import numpy as np 
    TestResult = []
    
    ## CONSTANTS
    MM_CO2 = 44.009/1000
    MM_CO = 28.0/1000
    MM_H2O = 18.0/1000
    MM_H2 = 2.016/1000
    MM_N2 = 28.0/1000
    MM_O2 = 32.0/1000
    MM_ker = np.array([142.18/1000])
    
    MolarLst = np.array([MM_CO2, MM_CO, MM_H2O, MM_H2, MM_N2, MM_O2])
    
    # test 1: R == 1:
    test1 = GetReactionProducts(np.array([15.6]), MM_ker)[0]/MolarLst
    
    TestResult.append(np.allclose([10.,11., 58.28], [test1[::2]]))
    
    # test 2: R < .9:
    
    test2 = GetReactionProducts(np.array([15.6*0.9]), MM_ker)[0]/MolarLst
    TestResult.append(np.allclose([10, 0, 11, 0, 65., 1.8], test2, 
                                  rtol = 0.05))
    
    # test 3: R > 1.00:
    
    test3 = GetReactionProducts(np.array([15.6*1.10]), MM_ker)[0]/MolarLst
    TestResult.append(np.allclose([10, 0, 8.2, 2.8, 52.5, 0], test3,
                                  rtol = 0.05))
    
    assert TestResult == [True, True, True]
    
#    return test1
    
    
