# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:20:05 2019

@author: Nout
"""
import os
from pathlib import Path
os.chdir(Path(__file__).parents[2])
print(os.getcwd())
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Conventional import TotalAC
import numpy as np
import matplotlib.pyplot as plt

def Sensitivity_New_MTOW_FW(Which_Plot, X_steps,Y_steps):
    
    #define plot tools
    fig, ax = plt.subplots()
    
    #initialise aircraft
    TestAC = Aircraft()
    anfp = TestAC.ParAnFP
    struc = TestAC.ParStruc
    prop = TestAC.ParProp
    
    #lists of varaying input parameters
    OEWmargin_lst = np.linspace(1,1.3,X_steps)    
    Thrustmargin_lst = np.linspace(345.,1845.,X_steps)
    altitude_lst = np.linspace(17000,23000,Y_steps)
    
    #lists for output parameters
    MTOW_lst = np.zeros((X_steps,Y_steps)) 
    FW_lst = np.zeros((X_steps,Y_steps))
    
    for i in range(Y_steps):
        anfp.h_cruise = altitude_lst[i]
        for j in range(X_steps):
            if Which_Plot ==1:
                struc.FoS_OEW = OEWmargin_lst[j]
            
            TotalAC(TestAC)
            
            MTOW_lst[j,i] = struc.MTOW
            FW_lst[j,i] = struc.FW
                
            
    CS = ax.contour(OEWmargin_lst,altitude_lst,MTOW_lst,8, colors = 'black') #colors =['#FFFFFF', '#FFFFFF',\
        #'#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'] )
    plt.show() 