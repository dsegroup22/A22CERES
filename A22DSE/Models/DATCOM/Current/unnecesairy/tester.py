# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:17:56 2019

@author: menno
"""
import numpy as np

a=np.array([0])
for i in range(25):
    a=np.append(a,a[-1]+0.04)