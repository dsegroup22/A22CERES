# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np
from A22DSE.Parameters.Par_Class_Atmos import Atmos


def FuselageWeight(Aircraft):
    anfp = Aircraft.ParAnFP
    q_D = 0.5*Atmos.rho*(1.4*anfp.V_cruise)**2*anfp.S