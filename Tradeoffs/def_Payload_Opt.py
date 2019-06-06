
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
os.chdir(Path(__file__).parents[1])

from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_def_InitsizingUncoupled import Wfratio_flighttime_flightrange
from A22DSE.Models.POPS.Current.cruisecalculations import CruiseRange, CruiseTime
from A22DSE.Models.CostModel.Current.OperCost import tground
from A22DSE.Models.Class_II_Weight.Class_II_Total import ClassIIWeightIteration

struc= Conv.ParStruc

def Payload_optimiser_wf(payload_lst):
#DESCRIPTION:
#   generate a list of fuel weights per ac per flight for different payload weights
#INPUTS:
#   list of payloads for which you want to calculate the fuel weights per ac per flight
#OUTPUTS:
#   list of fuel weights per ac per flight [kg]
    index_x = 0
    wf_lst = np.zeros(len(payload_lst))
    for payload in payload_lst:
        
        Conv.ParPayload.m_payload = payload #[kg]        
        mtow = ClassIIWeightIteration(Conv) #generate appropriate fuel weight for each 
        
        #append values to the appropriate list
        wf_lst[index_x] = struc.FW #[kg]
        index_x +=1
    return wf_lst

    
def Payload_optimiser_fleety1(payload_lst):
#DESCRIPTION:
#   Calculates the amount of ac needed to fulfill the 0.2 Teragram SO2 req
#   of year 1. based on the flight time per ac and payload per ac.
#   based on 250 operational days, the remaining days are used for buffer.
#INPUT: list of payloads
#OUTPUT: list of fleetsize for each payload size in payload_lst
    
     index_x = 0
     #set size of lists
     fleetsize_lst = np.zeros(len(payload_lst))
     flightsperyear_lst = np.zeros(len(payload_lst))

     #get payload requirement and operational days, plus turnaround time.
     TotalPayloadYear1 = Conv.ParPayload.TotalPayloadYear1
     OperationalDays = Conv.ParPayload.OperationalDays
     turnaroundtime = Conv.ParPayload.turnaroundtime   
     
     for payload in payload_lst:
         
         Conv.ParPayload.m_payload = payload
         Conv.ParAnFP.s_cruise = CruiseRange(Conv)
         tcruise = CruiseTime(Conv, ISA_model)
         
         Wfratio_flighttime_flightrange(Conv)
         
         
         #get all partial times, to get total time
         tcruiseclimb = Conv.ParAnFP.Timeclimbcruise 
         timeground = tground(Conv)
         time = 2*(tcruiseclimb-tcruise)+tcruise + turnaroundtime +timeground
         
         #compute flights per year, based on continuous running, buffer is in
         # operational days, not daily time.
         flightsperyear = OperationalDays*(24*3600/time)
         
         #get fleetsize from flights per year etc
         Fleet_size = np.ceil(TotalPayloadYear1/payload/flightsperyear)
         
         fleetsize_lst[index_x] = Fleet_size
         flightsperyear_lst[index_x] = flightsperyear
         index_x +=1
     return fleetsize_lst, flightsperyear_lst

    
def Payload_optimiser_Both(X_steps):
#DESCRIPTION;
#            calculate the total fuel weight of year 1, and normalise both functions wrt
#            their extremes. Its possible to plot the functions in this def.
#INPUTS:     integer X_steps: number of steps to discretise payload
#OUTPUTS:    lists payload, f1 and f2
#            f1 and f2 are normalised functions of fuel weight and fleet size
#            respectively.
    
    payload_lst = np.linspace(9000.,11000.,X_steps)
    wf_lst = Payload_optimiser_wf(payload_lst)
    fleetsize_lst, flightsperyear = Payload_optimiser_fleety1(payload_lst)
    
    wf_tot_y1 = wf_lst*fleetsize_lst*flightsperyear
    
    f1 = abs(wf_tot_y1/(wf_tot_y1[-1]-wf_tot_y1[0]))
    f2 = abs(fleetsize_lst/(fleetsize_lst[-1]-fleetsize_lst[0]))  
    plot = False
    if plot:
        plt.step(payload_lst,fleetsize_lst)#,'-ob',markersize=4)
        plt.xlabel('Payload mass per ac [kg]')
        plt.ylabel('Fleet size in year 1')
    return payload_lst, f1,f2

def OptimiserPlotter(Which_one, X_steps, w1, w2):
#DESCRIPTION: plots the combine function of f1 and f2, called f3. f3 is sum of
#             f1 and f2 weighted accordingly.
#INPUTS: Which_one: which plot
#        X_steps, resolution of payload
#        float w1, w2 weights of f1 and f2 respectively.
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
#DESCRIPTION: Plots several f3 for different weights.
    w1lst = np.linspace(0.2,0.8,sens_steps)
    for i in w1lst:
        OptimiserPlotter(Which_one,X_steps,i, 1-i)
    
    plt.xlabel('Payload mass per AC [kg]')
    plt.ylabel('Weighted score [-]')
    plt.legend(loc='upper left')
    plt.show()
    
    