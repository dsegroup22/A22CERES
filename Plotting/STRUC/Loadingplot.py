# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:21:46 2019

@author: menno
"""





import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../../')
from A22DSE.Models.STRUC.current.Loadingdiagram import Loading_Diagrams
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv


plt.plot(Loading_Diagrams(Conv)[1])
plt.show()


