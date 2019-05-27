# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:28:20 2019

@author: Nout
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../../')

from A22DSE.Models.CostModel.Current.ProdCost import CmanFunc
from A22DSE.Models.CostModel.Current.TotalCost import TotalC

from A22DSE.Parameters.Par_Class_Diff_Configs import SensTestAc, ISA_model


# =============================================================================
# os.chdir(Path(__file__).parents[2])
# cwd = os.getcwd()
# print(cwd)
# =============================================================================
#from A22DSE.Models.CostModel.Current.ProdCost import CmanFunc


def InitSizeCost(Plots, Which_plot,N_cont_lines, N_colours,X_steps,Y_steps):

    fig, ax = plt.subplots()
    
    #store original values
    MTOW_org = SensTestAc.ParStruc.MTOW
    V_cruise_org = SensTestAc.ParAnFP.V_cruise
    CostEngine_org=SensTestAc.ParCostLst.Cengine

    
    #determine range for plots
    MTOW_lst = np.linspace(20000,40000,X_steps)
    V_cruise_lst = np.linspace(170,240,Y_steps)
    CostEngine_lst = np.linspace(0.5e7,4e7,X_steps)
    
    Zlst =np.zeros((X_steps,Y_steps))
    Wlst =np.zeros((X_steps,Y_steps))
    if Plots == True:
        labels = ['Manufacturing cost per AC [Million $ 2019]']    
        if (Which_plot ==1 or Which_plot ==3):
            #determine inputs
            firstin = MTOW_lst
            secondin = V_cruise_lst
            print('hi')
            #set axis labels
            ax.set_xlabel('MTOW [kg]')
            ax.set_ylabel('Vcruise [m/s]')
           
        if (Which_plot == 2 or Which_plot == 4):
            #determine inputs
            firstin = CostEngine_lst
            secondin = V_cruise_lst
            #set axis labels
            ax.set_xlabel('Engine Cost [million $ 2019]')
            ax.set_ylabel('Vcruise [m/s]')
            


        #determine Z and W
        index_y = 0
        for i in secondin:
            SensTestAc.ParAnFP.V_cruise = i
            W=0
            index_x = 0    
            for j in firstin:
                if (Which_plot ==1 or Which_plot ==3):
                    SensTestAc.ParStruc.MTOW = j
                elif (Which_plot ==2 or Which_plot ==4):
                    SensTestAc.ParCostLst.Cengine = j
                if(Which_plot ==1 or Which_plot ==2):        
                    Z = CmanFunc(SensTestAc,ISA_model,SensTestAc.ParCostLst.Cengine)/SensTestAc.ParCostLst.Nprogram/1e6
                if (Which_plot ==3 or Which_plot ==4):
                    Z = TotalC(SensTestAc,ISA_model)[1]
                    W = TotalC(SensTestAc,ISA_model)[0]
                Zlst[index_y,index_x] =Z
                Wlst[index_y,index_x] =W     
                index_x =index_x+ 1    
            index_y =index_y+ 1
        #make plots
        Zlst = np.array(Zlst)
        Wlst = np.array(Wlst)
        X, Y = np.meshgrid(firstin, secondin)
        X = X/1e6
        #CS = ax.contour(X,Y,Zlst,N_cont_lines,colors=['#808080', '#A0A0A0', '#C0C0C0'])
        CS = ax.contour(X,Y,Zlst,N_cont_lines, colors = 'black') #colors =['#FFFFFF', '#FFFFFF',\
        #'#FFFFFF', '#FFFFFF','#000000','#000000','#000000','#000000'] )
                                             
        if (Which_plot ==3 or Which_plot ==4):
            firstplot = ax.contourf(X, Y, Wlst,N_colours, cmap='jet')
            labels = ['Operational Costs [Billion $ 2019]']
            #labels and axes and stuff
            cbar = fig.colorbar(firstplot, orientation="vertical", pad=0.2)
            cbar.ax.invert_yaxis()
            cbar.set_label('Total Costs [Billion $ 2019]', labelpad=-40, y=1.05, rotation=0)
        CS.collections[0].set_label(labels[0])
        #CS.collections[4].set_label(labels[0])
        ax.clabel(CS, fontsize=9, inline=1, manual = False)
        plt.legend(loc='upper left')
        plt.show()      
    return 0




