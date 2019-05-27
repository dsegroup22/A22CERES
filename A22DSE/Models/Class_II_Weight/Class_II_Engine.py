# -*- coding: utf-8 -*-
"""
Created on Mon May 20 18:49:22 2019

@author: lujingyi
"""
from math import sqrt
bp = 4.6
T_to = 200000
n = 2
a0 = 343 
eta_nozz = 0.97
eta_tf = 0.75
T_t4 = 1650 #turbine inlet temperature in K 1350-1650
G = T_t4/600-1.25
mdot = T_to*(1+bp)/(n*a0*sqrt(5*eta_nozz*G*(1+eta_tf*bp)))
print(mdot)
rho0 = 1.225
Cl = 9.8        #reference engine: B catagory
deltal = 0.05
ln = Cl*(sqrt(mdot*(1+0.2*bp)/(rho0*a0*(1+bp))+deltal))
print(ln)