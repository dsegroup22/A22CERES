# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:06 2019

@author: Nout
"""
import sys
import os
from pathlib import Path
import copy
import numpy as np
os.chdir(Path(__file__).parents[5])

from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_flightprofile import FuelFractions
from A22DSE.Parameters.Par_Class_Atmos import Atmos

ISA_model = Atmos()

def WingSurface_Thrust_FuelWeight(Aircraft):
    struc= Aircraft.ParStruc
    Layout = Aircraft.ParLayoutConfig
    anfp = Aircraft.ParAnFP
    
    #calculate Surface based on current mtow etc.
    MTOW = struc.MTOW
    anfp.S = MTOW/anfp.WS*9.80665
    anfp.Thrust = MTOW*anfp.TtoW*9.80665
    struc.FW = MTOW*struc.wfratio
    
def Wfratio_flighttime_flightrange(Aircraft):

     Aircraft.ParStruc.wfratioclimb, wfcruise, Aircraft.ParAnFP.Rangeclimbcruise,\
     Aircraft.ParAnFP.Timeclimbcruise = FuelFractions(Aircraft,ISA_model)
     Aircraft.ParStruc.wfratio = 1-wfcruise