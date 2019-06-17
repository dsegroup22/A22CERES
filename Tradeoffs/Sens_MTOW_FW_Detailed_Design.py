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
    OEWmargin_lst = np.linspace(1,1.2,X_steps)    
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
        labels = ['Operational Costs [Billion $ 2019]']
    elif Which_Plot == 2:
        X = Thrustmargin_lst
    
    Y = altitude_lst
                
    #contour lines        
    CS = ax.contour(X,Y,MTOW_lst,8, colors = 'black') #colors =['#FFFFFF', '#FFFFFF',\
        #'#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'] )
    ax.clabel(CS, inline=1, fontsize=10)
    #contour colours
    firstplot = ax.contourf(X, Y, FW_lst,8, cmap='jet')
    
    #labels and axes and stuff
    cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
    cbar.ax.invert_yaxis()
    cbar.set_label('Total Costs [Billion $ 2019]', labelpad=-40, y=1.05, rotation=0)
    plt.show() 
    print("--- %s seconds ---" % (time.time() - start_time))