# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:05:56 2019

@author: Nout
"""
import sys
import os
import numpy as np
from pathlib import Path
#os.chdir(Path(__file__).parents[1])
sys.path.append((os.path.abspath('../')))
print(os.getcwd())
from A22DSE.Parameters.TestAC280519 import TestAC
from A22DSE.Parameters.Par_Class_Atmos import Atmos
from A22DSE.Models.POPS.Current.payloadcalculations import *
#make shortcuts used throughout these tests:
payl = TestAC.ParPayload
ISA_model = Atmos()

def test_POPS_Area():
    A_inlet_new = InletArea(TestAC, ISA_model)  
    assert np.isclose(payl.A_inlet, A_inlet_new, rtol = 0.05)

def test_POPS_PayloadsMassdisprate():
    dispersionrate_new = PayloadsMassdisprate(TestAC,ISA_model)
    assert np.isclose(payl.dispersionrate, dispersionrate_new, rtol = 0.05)
    
def test_POPS_BurnerMass():
    m_burner_new = BurnerMass(TestAC)
    assert np.isclose(payl.m_burner, m_burner_new, rtol = 0.05)

def test_POPS_TankMass():
    m_tank_new = PayloadtankMass(TestAC)
    assert np.isclose(payl.m_tank, m_tank_new)