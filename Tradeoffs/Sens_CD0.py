# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 12:34:47 2019

@author: Nout
"""

import time
import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Conventional import TotalAC
import numpy as np
import matplotlib.pyplot as plt

def Sens_CD0(X_steps):
    
    start_time = time.time()
    #define plot tools
    fig, ax = plt.subplots()
    
    #initialise aircraft
    TestAC = Aircraft()
    anfp = TestAC.ParAnFP
    struc = TestAC.ParStruc
    prop = TestAC.ParProp
    TestAC.ParPayload.m_payload = 9700.
    #lists
    CD0_lst = np.linspace(0.015,0.0285,X_steps)
    MTOW_lst = np.zeros(X_steps)
    FW_lst = np.zeros(X_steps)
    
    for i in range(X_steps):
        anfp.CD0 = CD0_lst[i]
        
        print(anfp.CD0)
        print('\n\n')
        TotalAC(TestAC,CD0_lst[i])
        MTOW_lst[i] = struc.MTOW
        FW_lst[i] = struc.FW    
    
    
    color = 'tab:red'
    ax.set_xlabel('CD0 [-]')
    ax.set_ylabel('MTOW [kg]', color=color)
    ax.plot(CD0_lst,MTOW_lst, color=color, label ='MTOW')
    ax.tick_params(axis='y', labelcolor=color)
    ax.legend(loc=2)
    
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('Fuel weight [-]', color=color)  # we already handled the x-label with ax1
    ax2.plot(CD0_lst,FW_lst,'--', color=color, label ='Fuel Weight')
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    ax2.legend(loc=9)
    plt.show()
        
        
        
        
        
    print("--- %s seconds ---" % (time.time() - start_time))
