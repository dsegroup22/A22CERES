# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt


def PayloadtankVolume(Aircraft):
    payl=Aircraft.ParPayload
    m_payload=payl.m_payload
    rho_payload=payl.rho_payload
    #outputs Payload tank volume
    #inputs total Payload mass and Payload density

    return m_payload/rho_payload #[m^3]


##diameters=np.arange(1,2.5,0.01)
##weights=np.array([])
##
##for D in diameters:
##    weights=np.append(weights,PayloadtankMass(10000,1121,D,0.003,2700))
##
##plt.plot(diameters,weights)
##plt.show()

