# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""
import os
from pathlib import Path
os.chdir(Path(__file__).parents[2])
from A22DSE.Parameters.Par_Class_Conventional import Conv

anfp=Conv.ParAnFP
Layout=Conv.ParLayoutConfig
Conversion=Conv.ConversTool
Struc=Conv.ParStruc


f=open('CERES.dat','r+')

lines=f.readlines()
















f.close()
