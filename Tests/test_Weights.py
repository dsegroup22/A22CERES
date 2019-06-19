# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:51:07 2019

@author: kamph
"""

import sys
sys.path.append('..')
import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])
#sys.path.append('..')
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Parameters.Par_Class_Diff_Configs import ComputeCD0, ISA_model
#from A22DSE.Parameters.TestAC280519 import CreateTestAC
from A22DSE.Models.Class_II_Weight.Class_II_Wing import Wing_Geo
from A22DSE.Parameters.TestAC280519 import TestAC
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import (
        WSandTW)
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_def_InitsizingUncoupled\
import WingSurface_Thrust_FuelWeight, Wfratio_flighttime_flightrange
import numpy as np


