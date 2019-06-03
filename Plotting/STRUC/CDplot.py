# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:21:46 2019

@author: menno
"""

Cruise=False
LowSpeed=False



Cruise=True
#LowSpeed=True




import matplotlib.pyplot as plt
plt.clf()
import numpy as np
import sys
sys.path.append('../../')
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv
from A22DSE.Models.STRUC.current.loadingdiagram import V_Diagram
anfp=Conv.ParAnFP

plt.plot(V_Diagram(Conv))
plt.show()


