# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:09:35 2019

@author: Nout
"""

import time
import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Conventional import TotalAC
from A22DSE.Parameters.Par_Class_Atmos import Atmos
from A22DSE.Models.CostModel.Current.TotalCost import TotalC
import numpy as np
import matplotlib.pyplot as plt

def Sens_alt(X_steps):
    
    start_time = time.time()
    #define plot tools
    fig, ax = plt.subplots()
    
    #initialise aircraft
    TestAC = Aircraft()
    ISA_model = Atmos()
    anfp = TestAC.ParAnFP
    struc = TestAC.ParStruc
    prop = TestAC.ParProp
    TestAC.ParPayload.m_payload = 9700.
    
    #lists
    altitude_lst = np.linspace(18000.,21000.,X_steps)
    MTOW_lst = np.zeros(X_steps)
    TotalC_lst = np.zeros(X_steps)
    
    for i in range(X_steps):
        anfp.h_cruise = altitude_lst[i]
        TotalAC(TestAC)
        MTOW_lst[i] = struc.MTOW
        TotalC_lst[i] = TotalC(TestAC,ISA_model)[0]    
    
    
    color = 'tab:red'
    ax.set_xlabel('Cruising Altitude [m]')
    ax.set_ylabel('MTOW [kg]', color=color)
    ax.plot(altitude_lst,MTOW_lst, color=color, label ='MTOW')
    ax.tick_params(axis='y', labelcolor=color)
    ax.legend(loc=2)
    
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('Total Costs [Billion $ 2019]', color=color)  # we already handled the x-label with ax1
    ax2.plot(altitude_lst,TotalC_lst,'--', color=color, label ='Total Cost')
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    ax2.legend(loc=9)
    plt.show()
        
        
        
        
        
    print("--- %s seconds ---" % (time.time() - start_time))
