# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:26:40 2019

@author: Nikki
"""

'Fuselage sizing optimisation'
import numpy as np
from math import *

import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import GetTotalFuselageLength
from A22DSE.Models.Layout.Current.gearlocation_tri import PositionsLG_Tri
from A22DSE.Models.Layout.Current.Area import FusAreas
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_CD0 import CD0

def tailcone_angle(Aircraft):
    config = Aircraft.ParLayoutConfig
    
    Rotation_Angle = 14 * np.pi/180
    Dim = GetTotalFuselageLength(Aircraft, 8, 2, 2, 24, 1, 0.1)
    x_LG = config.lg_x_main
    Len = sum(Dim[0])
    l_main = config.lg_l_main
    
    h_tailcone = (Len-x_LG)* tan(Rotation_Angle)
    tailcone_angle = atan((h_tailcone - l_main)/(Len-x_LG))
    tailcone_angle = tailcone_angle * 180/np.pi
    return Dim, x_LG, Len, l_main, h_tailcone, tailcone_angle

