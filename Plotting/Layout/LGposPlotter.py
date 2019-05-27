# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:15:04 2019

@author: Nout
"""

import matplotlib.pyplot as plt
import sys
sys.path.append('../../')
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv


def LGposPlotter(Aircraft):
    layout = Aircraft.ParLayoutConfig
    x_cg = layout.x_cg
    y_cg = layout.y_cg
    z_cg = layout.z_cg
    y_main=layout.lg_y_main
    y_nose=layout.lg_y_nose
    x_main=layout.lg_x_main
    x_nose_min_F_n=layout.lg_x_nose_min_F_n
    x_nose_max_F_n=layout.lg_x_nose_max_F_n
    x_nose = layout.lg_x_nose
    
    plt.plot([y_main,-y_main,y_nose],[x_main,x_main,x_nose],'o')
    plt.plot([y_nose,y_nose],[x_nose_min_F_n,x_nose_max_F_n],'k--')
    plt.plot(y_cg,x_cg,'r',marker='$\\bigoplus$',alpha=0.5,linestyle='')
    plt.axis('equal')
    plt.ylim([0,round(max(x_cg)/10)*10+10])
    plt.grid()
    print('Track=',2*y_main,'m')
    print('z_cg=',z_cg,'m')
    plt.show()
    return 0
