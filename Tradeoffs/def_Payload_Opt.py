
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
os.chdir(Path(__file__).parents[1])

from A22DSE.Parameters.Par_Class_Diff_Configs import SensTestAc, ISA_model
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import WSandTW
from A22DSE.Models.POPS.Current.cruisecalculations import CruiseRange, CruiseTime
from A22DSE.Models.CostModel.Current.TotalCost import TotalC
from A22DSE.Models.CostModel.Current.OperCost import tground
def Payload_optimiser_wf(payload_lst):
        
    index_x = 0
    wf_lst = np.zeros(len(payload_lst))
    for payload in payload_lst:
        
        SensTestAc.ParPayload.m_payload = payload
        
        wf = WSandTW(False,SensTestAc, ISA_model)[1]

        #append values to the appropriate list
        wf_lst[index_x] = wf
        
        index_x +=1
    return wf_lst

    
def Payload_optimiser_fleety1(payload_lst):
    
     index_x = 0
     fleetsize_lst = np.zeros(len(payload_lst))
     Copsy1_lst = np.zeros(len(payload_lst))
     TotalPayloadYear1 = SensTestAc.ParPayload.TotalPayloadYear1
     OperationalDays = SensTestAc.ParPayload.OperationalDays
     turnaroundtime = SensTestAc.ParPayload.turnaroundtime   
     for payload in payload_lst:
         SensTestAc.ParPayload.m_payload = payload
         SensTestAc.ParAnFP.s_cruise = CruiseRange(SensTestAc)
         tcruiseclimb = WSandTW(False,SensTestAc, ISA_model)[-1]
         
         tcruise = CruiseTime(SensTestAc, ISA_model)
         timeground = tground(SensTestAc)
         
         time = 2*(tcruiseclimb-tcruise)+tcruise + turnaroundtime +timeground
                 
         flightsperyear = OperationalDays*(24*3600/time)
         
         
         Fleet_size = np.ceil(TotalPayloadYear1/payload/flightsperyear)
         
         fleetsize_lst[index_x] = Fleet_size
         
         SensTestAc.ParCostLst.acmanuy = Fleet_size
         
         #check if number of aircraft is indeed the largest factor in operating costs
         SensTestAc.ParStruc.MTOW = WSandTW(False,SensTestAc, ISA_model)[0]
         Copsy1 = TotalC(SensTestAc, ISA_model)[1]
         Copsy1_lst[index_x] = Copsy1
         index_x +=1
     return fleetsize_lst, flightsperyear

    
def Payload_optimiser_Both(X_steps):
    
    payload_lst = np.linspace(5000.,20000.,X_steps)
    
    wf_lst = Payload_optimiser_wf(payload_lst)
    fleetsize_lst, flightsperyear = Payload_optimiser_fleety1(payload_lst)
    
    wf_tot_y1 = wf_lst*fleetsize_lst*flightsperyear
    
    f1 = abs(wf_tot_y1/(wf_tot_y1[-1]-wf_tot_y1[0]))
    f2 = abs(fleetsize_lst/(fleetsize_lst[-1]-fleetsize_lst[0]))  
    
    #plt.plot(payload_lst,wf_tot_y1)
    #plt.xlabel('Payload mass per ac [kg]')
    #plt.ylabel('Total burned in year 1 [kg]')
    return payload_lst, f1,f2

def OptimiserPlotter(Which_one, X_steps, w1, w2):
    payload_lst, f1,f2 = Payload_optimiser_Both(X_steps)
    
    f3 = w1*f1+w2*f2
    
    w1 = round(w1,2)
    w2 = round(w2,2)
    if Which_one ==1:
        plt.plot(payload_lst,f3, label = 'w1 = '+str(w1)+', w2 = '+str(w2))
        
    if Which_one ==2:
        plt.plot(payload_lst,f3)
        plt.plot(payload_lst,f1)
        plt.step(payload_lst,f2)
        
        
def Sens_Opt_Payload(Which_one,X_steps, sens_steps):
    #X_steps: amount of steps for 
    w1lst = np.linspace(0.2,0.8,sens_steps)
    for i in w1lst:
        OptimiserPlotter(Which_one,X_steps,i, 1-i)
    
    plt.xlabel('Payload mass per AC [kg]')
    plt.ylabel('Weighted score [-]')
    plt.legend(loc='upper left')
    plt.show()
    
    