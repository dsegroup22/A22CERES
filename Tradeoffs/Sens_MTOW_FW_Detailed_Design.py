# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:20:05 2019

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

def Sensitivity_New_MTOW_FW(Which_Plot, X_steps,Y_steps):
    start_time = time.time()
    #define plot tools
    fig, ax = plt.subplots()
    
    #initialise aircraft
    TestAC = Aircraft()
    anfp = TestAC.ParAnFP
    struc = TestAC.ParStruc
    prop = TestAC.ParProp
    TestAC.ParPayload.m_payload = 9700.
    #lists of varaying input parameters
    OEWmargin_lst = np.linspace(1.05,1.13,X_steps)    
    Thrustmargin_lst = np.linspace(345.,1845.,X_steps)
    altitude_lst = np.linspace(18000.,21000.,Y_steps)
    
    #lists for output parameters
    MTOW_lst = np.zeros((X_steps,Y_steps)) 
    FW_lst = np.zeros((X_steps,Y_steps))
    
    for i in range(Y_steps):
        anfp.h_cruise = altitude_lst[i]
        for j in range(X_steps):
            if Which_Plot ==1:
                struc.FoS_OEW = OEWmargin_lst[j]
            if Which_Plot == 2:
                prop.SafetyMarginEngine = Thrustmargin_lst[j]
            
            TotalAC(TestAC)
            
            MTOW_lst[j,i] = struc.MTOW
            FW_lst[j,i] = struc.FW
    
    #for plotting
    if Which_Plot == 1:    
        X = OEWmargin_lst
        ax.set_xlabel('Safety margin in OEW[-]')
            
    elif Which_Plot == 2:
        X = Thrustmargin_lst-935
        ax.set_xlabel('Difference in thrust per engine[N]')
    Y = altitude_lst
    ax.set_ylabel('cruise altitude [m]')            
    #contour lines        
    CS = ax.contour(X,Y,FW_lst,10, colors =['#FFFFFF', '#FFFFFF','#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000','#000000'] )
    labels = ['Fuel weight [kg]']
    CS.collections[0].set_label(labels[0])
    CS.collections[6].set_label(labels[0])
    
    
    #contour colours
    firstplot = ax.contourf(X, Y, MTOW_lst,16, cmap='Greys_r')
    
    #labels and axes and stuff
    ax.clabel(CS, inline=1, fontsize=10)
    cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
    cbar.ax.invert_yaxis()
    cbar.set_label('MTOW [kg]', labelpad=-40, y=1.05, rotation=0)
    plt.legend(loc='upper left')
    plt.show() 
    
    #check total time needed
    print("--- %s seconds ---" % (time.time() - start_time))


# =============================================================================
# for i in range(1,3):
#     Sensitivity_New_MTOW_FW(i,20,20)
# =============================================================================
