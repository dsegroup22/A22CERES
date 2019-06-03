
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from pathlib import Path
os.chdir(Path(__file__).parents[1])

from A22DSE.Parameters.Par_Class_Diff_Configs import SensTestAc, ISA_model
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import WSandTW
from A22DSE.Models.POPS.Current.cruisecalculations import CruiseRange, CruiseTime
def Payload_optimiser_wf(payload_lst):
        
    index_x = 0
    wf_lst = np.zeros(len(payload_lst))
    for i in payload_lst:
        payload = i
    
        SensTestAc.ParPayload.m_payload = payload
        
        wf = WSandTW(False,SensTestAc, ISA_model)[1]

        #append values to the appropriate list
        wf_lst[index_x] = wf
        
        index_x +=1
    return wf_lst

    
def Payload_optimiser_fleet(payload_lst):
    
     index_x = 0
     fleetsize_lst = np.zeros(len(payload_lst))
     
     TotalPayloadYear1 = SensTestAc.ParPayload.TotalPayloadYear1
     OperationalDays = SensTestAc.ParPayload.OperationalDays
     turnaroundtime = SensTestAc.ParPayload.turnaroundtime   
     for i in payload_lst:
         payload = i
         SensTestAc.ParPayload.m_payload = payload
         SensTestAc.ParAnFP.s_cruise = CruiseRange(SensTestAc)
         tcruiseclimb = WSandTW(False,SensTestAc, ISA_model)[-1]
         
         tcruise = CruiseTime(SensTestAc, ISA_model)
         
         time = 2*(tcruiseclimb-tcruise)+tcruise + turnaroundtime
                 
         flightsperyear = OperationalDays*(24*3600/time)
         
         
         Fleet_size = np.round(TotalPayloadYear1/payload/flightsperyear)
         
         fleetsize_lst[index_x] = Fleet_size
         
         index_x +=1
     #f1 = interp1d(payload_lst, fleetsize_lst, kind ='previous')
     fig, ax = plt.subplots()
     #plt.step(payload_lst,fleetsize_lst)
     return fleetsize_lst
    
def Payload_optimiser_Both(X_steps):
    payload_lst = np.linspace(5000.,20000.,X_steps)
    
    wf_lst = Payload_optimiser_wf(payload_lst)
    fleetsize_lst = Payload_optimiser_fleet(payload_lst)
    
    TotalFuelWeightYear1 = wf_lst*fleetsize_lst
    print(TotalFuelWeightYear1)
    
    f1 = abs(wf_lst/(wf_lst[-1]-wf_lst[0]))
    f2 = abs(fleetsize_lst/(fleetsize_lst[-1]-fleetsize_lst[0]))  
    f3 = f1+f2
    
    print(wf_lst)
    print(fleetsize_lst)
    print(f1)
    print(f2)      
    return payload_lst, f1,f2,f3
def OptimiserPlotter(X_steps):
    payload_lst, f1,f2,f3 = Payload_optimiser_Both(X_steps)
    
    fig, ax = plt.subplots()
    plt.plot(payload_lst,f1)
    plt.step(payload_lst,f2)
    plt.plot(payload_lst,f3)
