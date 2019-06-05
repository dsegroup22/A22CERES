# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:06 2019

@author: Nout
"""

def WingSurface_Thrust_FuelWeight(Conv):
    struc= Conv.ParStruc
    Layout = Conv.ParLayoutConfig
    anfp = Conv.ParAnFP
    
    #calculate Surface based on current mtow etc.
    MTOW = struc.MTOW
    anfp.S = MTOW*anfp.WS
    anfp.Thrust = MTOW*anfp.TtoW
    struc.FW = MTOW*struc.wfratio
    