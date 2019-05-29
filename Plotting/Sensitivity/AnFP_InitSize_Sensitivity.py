# -*- coding: utf-8 -*-
"""
Created on Fri May 10 11:43:45 2019

@author: Nout
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../../')

from A22DSE.Parameters.Par_Class_Diff_Configs import SensTestAc, ISA_model
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import WSandTW

def InitSizeSens(Plots, Which_plot,N_cont_lines, N_colours,X_steps,Y_steps):
    
#INPUTS:
#

#=======================PARAMETERS=============================================
    #original parameters
    A_org = SensTestAc.ParAnFP.A
    e_org = SensTestAc.ParAnFP.e
    Range_org = SensTestAc.ParAnFP.s_cruise
    hcruise_org=SensTestAc.ParAnFP.h_cruise
    payload_org =SensTestAc.ParPayload.m_payload
    CD0_org = SensTestAc.ParAnFP.CD0
    #wfratioclimb_org = SensTestAc.ParStruc.wfratioclimb
    
    #create lists, these are later used for plotting
    A_lst = np.linspace(5,25,X_steps)
    e_lst = np.linspace(0.7,1.,Y_steps)
    Range_lst = np.linspace(1500000,3000000,X_steps)
    hcruise_lst = np.linspace(15000,23000,Y_steps)
    payload_lst = np.linspace(5000,20000,X_steps)
    CD0_lst = np.linspace(0.01,0.05, Y_steps)
    wfratioclimb_lst = np.linspace(0.7,0.99,Y_steps)
    oewratio_lst = np.linspace(0.2,0.7,X_steps)
#==============================================================================  
    

    if Plots == True:
#                           MTOW AND WF PLOTS        
#===============================FIRST PLOT=====================================
        #for the first plot (MTOW against A and e)
        if Which_plot == 1:
            #for Fuel Weight & MTOW versus Aspect ratio and Oswald factor

            #generate index for first loop
            index_y = -1
            #initialise 2d arrays for plotting values
            MTOW_lst =np.zeros((X_steps,Y_steps))
            wf_ratio_lst = np.zeros((X_steps,Y_steps))
            for i in A_lst:
                print(i)
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1
                A = i
                for j in e_lst:
                    index_x = index_x+1
                    e = j
                    
                    #adjust A and e
                    SensTestAc.ParAnFP.A = A
                    SensTestAc.ParAnFP.e = e
                    #determine MTOW and wf for this aspect ratio
                    MTOW =WSandTW(False,SensTestAc, ISA_model)[0]
                    #MTOW = WSandTW(aero, struct)
                    wf_ratio = WSandTW(False,SensTestAc, ISA_model)[1]
                    
                    #append values to the appropriate lists
                    MTOW_lst[index_y,index_x] = MTOW 
                    wf_ratio_lst[index_y,index_x] = wf_ratio
                    
            #reset to original values:
            SensTestAc.ParAnFP.A = A_org
            SensTestAc.ParAnFP.e = e_org
                    
            #plotting            
            Z = np.array(MTOW_lst)
            W = np.array(wf_ratio_lst)
            X, Y = np.meshgrid(e_lst,A_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('Oswald factor [-]')
            ax.set_ylabel('Aspect ratio [-]')
            labels = ['MTOW [kg]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Fuel Weight[kg]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show()      
#==============================================================================

#===============================SECOND PLOT====================================            
            
                #for the second plot (MTOW against Range and altitude)
        if Which_plot == 2:
            #generate index for first loop
            index_y = -1
            #initialise 2d arrays for plotting values
            MTOW_lst =np.zeros((X_steps,Y_steps))
            wf_ratio_lst = np.zeros((X_steps,Y_steps))
            for i in Range_lst:
                print(i)
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1
                Range = i
                for j in hcruise_lst:
                    index_x = index_x+1
                    hcruise = j
                    
                    #adjust A and e
                    SensTestAc.ParAnFP.h_cruise = hcruise
                    SensTestAc.ParAnFP.s_cruise = Range
                    #determine MTOW and wf for this aspect ratio
                    MTOW =WSandTW(False,SensTestAc, ISA_model)[0]
                    #MTOW = WSandTW(aero, struct)
                    wf_ratio = WSandTW(False,SensTestAc, ISA_model)[1]
                    #append values to the appropriate lists
                    MTOW_lst[index_y,index_x] = MTOW 
                    wf_ratio_lst[index_y,index_x] = wf_ratio
            
                        #reset to original values:
            SensTestAc.ParAnFP.h_cruise = hcruise_org
            SensTestAc.ParAnFP.s_cruise = Range_org
                    
            #plotting            
            Z = np.array(MTOW_lst)
            W = np.array(wf_ratio_lst)
            X, Y = np.meshgrid(hcruise_lst, Range_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('altitude [m]')
            ax.set_ylabel('range [m]')
            labels = ['MTOW [kg]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Fuel Weight [kg]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show() 
            
    
#==============================================================================
            
#===============================THIRD PLOT====================================  
            
        if Which_plot == 3: 
             #generate index for first loop
            index_y = -1

            #initialise 2d arrays for plotting values
            MTOW_lst =np.zeros((X_steps,Y_steps))
            wf_ratio_lst = np.zeros((X_steps,Y_steps))
            for i in payload_lst:
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1

                payload = i
                for j in CD0_lst:
                    index_x = index_x+1
                    CD0 = j
    
                    #adjust A and e
                    SensTestAc.ParAnFP.CD0 = CD0
                    SensTestAc.ParPayload.m_payload = payload
                    #determine MTOW and wf for this aspect ratio
                    MTOW =WSandTW(False,SensTestAc, ISA_model)[0]
                    #MTOW = WSandTW(aero, struct)
                    wf_ratio = WSandTW(False,SensTestAc, ISA_model)[1]
                    #append values to the appropriate lists
                    MTOW_lst[index_y,index_x] = MTOW 
                    wf_ratio_lst[index_y,index_x] = wf_ratio
                    
            #reset to original values
            SensTestAc.ParAnFP.CD0 = CD0_org
            SensTestAc.ParPayload.m_payload = payload_org
            
            #plotting            
            Z = np.array(MTOW_lst)
            W = np.array(wf_ratio_lst)
            X, Y = np.meshgrid(CD0_lst, payload_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('CD0 [-]')
            ax.set_ylabel('payload mass [kg]')
            labels = ['MTOW [kg]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Fuel Weight[kg]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show() 
            
#==============================================================================
#                               S AND TW PLOTS
#===============================FOURTH PLOT====================================    
            
        if Which_plot == 4:
            #for Fuel Weight & MTOW versus Aspect ratio and Oswald factor
            #generate index for first loop
            index_y = -1
            #initialise 2d arrays for plotting values
            S_lst =np.zeros((X_steps,Y_steps))
            TW_lst = np.zeros((X_steps,Y_steps))
            for i in A_lst:
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1
                A = i
                for j in e_lst:
                    index_x = index_x+1
                    e = j
                    #adjust A and e
                    SensTestAc.ParAnFP.A = A
                    SensTestAc.ParAnFP.e = e
                    #determine MTOW and wf for this aspect ratio
                    S =WSandTW(False,SensTestAc, ISA_model)[2]
                    #MTOW = WSandTW(aero, struct)
                    TW = WSandTW(False,SensTestAc, ISA_model)[3]
                    
                    
                    #append values to the appropriate lists
                    S_lst[index_y,index_x] = S 
                    TW_lst[index_y,index_x] = TW
            
            #reset to original values:
            SensTestAc.ParAnFP.A = A_org
            SensTestAc.ParAnFP.e = e_org
            
            #plotting            
            Z = np.array(S_lst)
            W = np.array(TW_lst)
            X, Y = np.meshgrid(e_lst,A_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('Oswald factor [-]')
            ax.set_ylabel('Aspect ratio [-]')
            labels = ['Wing surface [m2]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Thrust [N]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show()      
            
            
        if Which_plot == 5:
            #generate index for first loop
            index_y = -1
            #initialise 2d arrays for plotting values
            S_lst =np.zeros((X_steps,Y_steps))
            TW_lst = np.zeros((X_steps,Y_steps))
            for i in Range_lst:
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1
                Range = i
                for j in hcruise_lst:
                    index_x = index_x+1
                    hcruise = j
                    
                     #adjust A and e
                    SensTestAc.ParAnFP.h_cruise = hcruise
                    SensTestAc.ParAnFP.s_cruise = Range
                    #determine MTOW and wf for this aspect ratio
                    S =WSandTW(False,SensTestAc, ISA_model)[2]
                    #MTOW = WSandTW(aero, struct)
                    TW = WSandTW(False,SensTestAc, ISA_model)[3]
                    #append values to the appropriate lists
                    S_lst[index_y,index_x] = S
                    TW_lst[index_y,index_x] = TW
                    
            #reset to org values
            SensTestAc.ParAnFP.h_cruise = hcruise_org
            SensTestAc.ParAnFP.s_cruise = Range_org
            
            #plotting            
            Z = np.array(S_lst)
            W = np.array(TW_lst)
            X, Y = np.meshgrid(hcruise_lst, Range_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('altitude [m]')
            ax.set_ylabel('range [m]')
            labels = ['Wing surface [m2]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Thrust [N]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show()   
            
            
        if Which_plot == 6: 
             #generate index for first loop
            index_y = -1

            #initialise 2d arrays for plotting values
            S_lst =np.zeros((X_steps,Y_steps))
            TW_lst = np.zeros((X_steps,Y_steps))
            for i in payload_lst:
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1

                payload = i
                for j in CD0_lst:
                    index_x = index_x+1
                    CD0 = j
                    SensTestAc.ParAnFP.CD0 = CD0
                    SensTestAc.ParPayload.m_payload = payload
                    #determine MTOW and wf for this aspect ratio
                    S =WSandTW(False,SensTestAc, ISA_model)[2]
                    #MTOW = WSandTW(aero, struct)
                    TW = WSandTW(False,SensTestAc, ISA_model)[3]#append values to the appropriate lists
                    S_lst[index_y,index_x] = S
                    TW_lst[index_y,index_x] = TW
                    
            #reset to org values
            SensTestAc.ParAnFP.CD0 = CD0_org
            SensTestAc.ParPayload.m_payload = payload_org
            
            #plotting            
            Z = np.array(S_lst)
            W = np.array(TW_lst)
            X, Y = np.meshgrid(CD0_lst, payload_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
        '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('CD0 [-]')
            ax.set_ylabel('payload mass [kg]')
            labels = ['Wing surface [m2]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Thrust [N]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show() 
            
            
            
# =============================================================================
#                           RESERVE CONFIGURATION             
        if Which_plot == 7:
            #generate index for first loop
            index_y = -1
            #initialise 2d arrays for plotting values
            MTOW_lst =np.zeros((X_steps,Y_steps))
            wf_ratio_lst = np.zeros((X_steps,Y_steps))
            for i in payload_lst:
                #generate index for second loop
                index_x = -1
                index_y =index_y+ 1
                payload = i
                for j in oewratio_lst:
                    index_x = index_x+1
                    OEWratio = j
                    
                    #adjust A and e
                    SensTestAc.ParStruc.OEWratio = OEWratio
                    SensTestAc.ParPayload.m_payload = payload
                    #determine MTOW and wf for this aspect ratio
                    MTOW =WSandTW(False,SensTestAc, ISA_model)[2]
                    #MTOW = WSandTW(aero, struct)
                    wf_ratio = WSandTW(False,SensTestAc, ISA_model)[3]
                    #append values to the appropriate lists
                    MTOW_lst[index_y,index_x] = MTOW 
                    wf_ratio_lst[index_y,index_x] = wf_ratio
            
                        #reset to original values:
            #SensTestAc.ParStruc = wfratioclimb_org
            SensTestAc.ParAnFP.s_cruise = Range_org
                    
            #plotting            
            Z = np.array(MTOW_lst)
            W = np.array(wf_ratio_lst)
            X, Y = np.meshgrid(oewratio_lst, payload_lst)
            fig, ax = plt.subplots()
            CS = ax.contour(X,Y,Z,N_cont_lines,colors =['#FFFFFF', '#FFFFFF',\
       '#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'])
            firstplot = ax.contourf(X, Y, W,N_colours, cmap='gray')
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            ax.set_xlabel('OEW/MTOW [-]')
            ax.set_ylabel('payload mass [kg]')
            labels = ['Wing surface [m^2]']
            CS.collections[0].set_label(labels[0])
            CS.collections[4].set_label(labels[0])
            #for final version, set manual = True
            ax.clabel(CS, fontsize=9, inline=1, manual = False)
            cbar.set_label('Thrust [N]', labelpad=-40, y=1.05, rotation=0)
            plt.legend(loc='upper left')
            plt.show() 
            
    return(0)


            
for i in range(0,1):
    InitSizeSens(True,i,8,20,12,12)

