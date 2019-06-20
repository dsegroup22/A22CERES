# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 09:53:58 2019

@author: tomhu
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m
#from mpl_toolkits.mplot3d import Axes3D

RNDACT = np.array([3.1, 0.92, 1.92])
MNAACT = np.array([114.24,62.2,107.45])
MNOACT = np.array([56.41,53.29,69.62])
RnDcont = np.array([0.25,0.2,0.15])
MnAcont = np.array([0.15,0.1,0.05])
MnOcont=np.array([0.25,0.2,0.15])
Req =np.array([4.48,112.89,44.80])

x = np.array([r'Preliminary Design', r'Class I Design', r'Class II Design'])

RNDCUR = np.multiply(RNDACT,1+RnDcont)
MNACUR = np.multiply(MNAACT,1+MnAcont)
MNOCUR = np.multiply(MNOACT,1+MnOcont)

RNDSPEC = np.ones(RNDACT.shape)*Req[0]
MNASPEC = np.ones(RNDACT.shape)*Req[1]
MNOSPEC = np.ones(RNDACT.shape)*Req[2]

RNDTAR = np.multiply(RNDSPEC,1-RnDcont)
MNATAR = np.multiply(MNASPEC,1-MnAcont)
MNOTAR = np.multiply(MNOSPEC,1-MnOcont)

plt.clf
plt.figure(1)
a = plt.plot(x,RNDACT)
c = plt.plot(x,RNDCUR)
b = plt.plot(x,RNDSPEC)
d = plt.plot(x,RNDTAR)
plt.legend(['Actual', 'Current','Specification', 'Target'],loc='best')
plt.ylabel(r'Billion USD')
plt.show()

plt.figure(2)
a = plt.plot(x,MNOACT)
c = plt.plot(x,MNOCUR)
b = plt.plot(x,MNOSPEC)
d = plt.plot(x,MNOTAR)
plt.ylabel(r'Million USD')
plt.legend(['Actual', 'Current','Specification', 'Target'],loc='best')
plt.show()

plt.figure(3)
a = plt.plot(x,MNAACT)
c = plt.plot(x,MNACUR)
b = plt.plot(x,MNASPEC)
d = plt.plot(x,MNATAR)
plt.ylabel(r'Million USD')
plt.legend(['Actual', 'Current','Specification', 'Target'],loc='best')
plt.show()


