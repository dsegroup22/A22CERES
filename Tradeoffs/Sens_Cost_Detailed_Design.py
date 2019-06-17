# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:50:02 2019

@author: Nout
"""

import time


import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Conventional import TotalAC
from A22DSE.Models.CostModel.Current.TotalCost import TotalC
import numpy as np
import matplotlib.pyplot as plt

def Sens_Cost_Detailed(Which_Plot,X_steps,Y_steps):
    start_time = time.time()
    #define plot tools
    fig, ax = plt.subplots()
    
    #initialise aircraft
    TestAC = Aircraft()
    anfp = TestAC.ParAnFP
    struc = TestAC.ParStruc
    prop = TestAC.ParProp
    payload = TestAC.ParPayload
    
    #lists of varaying input parameters
    OEWmargin_lst = np.linspace(1,1.15,X_steps)    
    Thrustmargin_lst = np.linspace(345.,1845.,X_steps)
    payload_lst = np.linspace(7000.,11500.,Y_steps)
    
    #lists for output parameters
    TotalC_lst = np.zeros((X_steps,Y_steps)) 
    OperC_lst = np.zeros((X_steps,Y_steps))
    
    for i in range(Y_steps):
        payload.m_payload = payload_lst[i]
        for j in range(X_steps):
            if Which_Plot ==1:
                struc.FoS_OEW = OEWmargin_lst[j]
            if Which_Plot == 2:
                prop.SafetyMarginEngine = Thrustmargin_lst[j]
            
            TotalAC(TestAC)
            
            TotalC_lst[j,i] = TotalC(SensTestAc,ISA_model)[1]
            OperC_lst[j,i] = TotalC(SensTestAc,ISA_model)[0]
    
    #for plotting
    if Which_Plot == 1:    
        X = OEWmargin_lst
        ax.set_xlabel('Safety margin in OEW[-]')
            
    elif Which_Plot == 2:
        X = Thrustmargin_lst
        ax.set_xlabel('Correction for Thrust level[N]')
    Y = payload_lst
    ax.set_ylabel('payload mass [kg]')            
    #contour lines        
    CS = ax.contour(X,Y,OperC_lst,8, colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'] )
    ax.clabel(CS, inline=1, fontsize=10)
    #contour colours
    firstplot = ax.contourf(X, Y, TotalC_lst,8, cmap='Greys_r')
    
    #labels and axes and stuff
    labels = ['Fuel weight [kg]']
    CS.collections[0].set_label(labels[0])
    cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
    cbar.ax.invert_yaxis()
    cbar.set_label('MTOW [kg]', labelpad=-40, y=1.05, rotation=0)
    plt.legend(loc='upper left')
    plt.show() 
    
    #check total time needed
    print("--- %s seconds ---" % (time.time() - start_time))