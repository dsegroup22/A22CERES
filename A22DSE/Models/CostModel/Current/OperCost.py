# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:28:55 2019

@author: Thomas Verduyn
"""
import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])
import numpy as np
from A22DSE.Models.CostModel.Current.ProdCost import CmanFunc
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model

def Uannbl(tbl):
    #Annual utilization in block hours
    return 1e3*(6.053*tbl+5.7-np.sqrt(37.771*tbl**2+13.494*tbl+32.490))

def tground(Aircraft):
    Struc = Aircraft.ParStruc
    Convers=Aircraft.ConversTool
    return 0.51*10**(-6)*Struc.MTOW/Convers.lbs2kg+0.125

def Coper(Aircraft,doc):
    tgm=tground(Aircraft)
    par=Aircraft.ParCostLst
    Convers=Aircraft.ConversTool
    FlightOp=Aircraft.ParAnFP
    
    Rbl=FlightOp.Rangeclimbcruise/1000.*Convers.km2nm
#    print (Rbl)
    tflt=FlightOp.tclimbcruise/3600.
    tbl=tgm+tflt
#    print (tbl)
    Vbl=Rbl/tbl
#    print (Vbl)
#    print (Uannbl(tbl))
    years=FlightOp.operatingyears
    acpyp1=8
    acpyp2=16
    acpy1=12
    ac=0
    Rblann=Vbl*Uannbl(tbl)
#    print ('rblann',Rblann)
    ctot=0
#    print ('Annual operating costs per aircraft in million USD is:',\
#           round(1.75*Rblann*doc*1e-6,2))
    for i in range(years):
        if i==0:
            ac+=acpy1
            Cops=1.6*doc*Rblann*ac
            Copsy1 = 1.6*doc*Rblann*acpy1
            ctot+=Cops
        if i<=7 and i>0:
            ac+=acpyp1
            Cops=1.6*doc*Rblann*ac
            ctot+=Cops
        if i>7:
            ac+=acpyp2
            Cops=1.6*doc*Rblann*ac
            ctot+=Cops
#        print ('The operational costs for year', i,'in billion USD equals:',\
#               round(Cops*1e-9,2))
#    print ('The total operating costs over 15 years in billion USD equals:',\
#           round(ctot*1e-9,2))
    return ctot, 1.6*Rblann*doc*1e-6, Copsy1
    
def DOC(docflt,docmaint,docdepr,doclnr,frt):
    #COSTS IS PER NM!!!!
    #Converted to 2019 USD in other functions
    doc=sum([docflt,docmaint,docdepr,doclnr])/(1-0.07-frt)
    return doc


def DOCflt(Aircraft, Cman):
    #INPUT:Rbl/tbl, Flight hours/year, Ne
    #OUPUT Flight costs in 2019 USD
    #Description: Consists of crew, Fuel and insurance costs
    tgm=tground(Aircraft)
    par=Aircraft.ParCostLst
    Convers=Aircraft.ConversTool
    Struct=Aircraft.ParStruc
    FlightOp=Aircraft.ParAnFP
    Prop=Aircraft.ParProp
    Payload=Aircraft.ParPayload
    
    Ne=Prop.N_engines
    Nprogram=Payload.fleetsize_y15
    Rbl=FlightOp.Rangeclimbcruise/1000*Convers.km2nm
    tflt=FlightOp.tclimbcruise/3600.
    tbl=tgm+tflt
    Vbl=Rbl/tbl
    #print (tbl)
    AH=tbl*250      #Could multiply by 2
    Wfused=Struct.FW/Convers.lbs2kg
    #print (Wfused)
    #print (Rbl)
    #print (par.Cfuel/par.CEF8919)
    #print (par.FD)
    
    #Crew costs
    Cpilot=(1+0.26)/Vbl*par.spil/AH+10/Vbl
    Ccopilot=(1+0.26)/Vbl*par.scpil/AH+10/Vbl
    Ccrew=Cpilot+Ccopilot
    
    #Fuel/Oil costs
    Cpol=Wfused/Rbl*(par.Cfuel/par.CEF8919)/par.FD+0.7*Ne*tbl/Rbl*par.Coil
    #Use eq below if above doenst work
#    Cpol=1.05*Wfused/Rbl*par.Cfuel/par.FD
    #print (Cpol)
    
    #Insurance costs
    ManPerACCost  = Cman/Nprogram/par.CEF8919
    Cins=ManPerACCost*(1+par.Fpror)*0.030/(Uannbl(tbl)*Vbl)
    #Can use below if above is wrong
    #Cins=0.02*DOC  
    return sum([Ccrew,Cpol,Cins])*par.CEF8919

def DOCmaint(Aircraft,Cman):
    #INPUT:CHECK MHRmapflt value
    #OUTPUT:
    #Description:Costs for operational maintenance
    par=Aircraft.ParCostLst
    Convers=Aircraft.ConversTool
    FlightOp=Aircraft.ParAnFP
    Prop=Aircraft.ParProp
    Payload=Aircraft.ParPayload
    
    tgm=tground(Aircraft)
    Rbl=FlightOp.Rangeclimbcruise/1000*Convers.km2nm
    tflt=FlightOp.tclimbcruise/3600.
    tbl=tgm+tflt
    Vbl=Rbl/tbl
    Rlap=par.Rlap
    Ne=Prop.N_engines
    Nprogram=Payload.fleetsize_y15
    ManPerACCost  = Cman/Nprogram/par.CEF8919
    AEP=ManPerACCost*(1+par.Fpror)
    EP=Prop.Engine_cost*1e6/par.CEF8919
    Hem=5000        
      
    #Labour costs of airframe and systems maintenance
    MHRmapbl=par.MHRmapflt*tflt/tbl
    Clabop=1.03*MHRmapbl*Rlap/Vbl
    
    #Labour costs of engine maintenance
    Clabeng=1.03*1.3*Ne*par.MHRmengbl*Rlap/Vbl
    
    #Costs of airfame maintenance materials
    Cmatapblhr=30+0.79*10**(-5)*(AEP-Ne*EP)
    Cmatap=1.03*Cmatapblhr/Vbl
        
    #Costs of engine maintenance materials
    Khem=0.021*Hem/100+0.769
    Cmatengblhr=5.43*10**(-5)*EP*(1.5-0.47)/Khem
    Cmateng=1.03*1.3*Ne*(Cmatengblhr)/Vbl
    
    #Cost of applied maintenace per nm
    flab=0.9
    fmat=0.3
    Camb=1.03*(flab*(MHRmapbl*Rlap+Ne*par.MHRmengbl*Rlap)+\
               fmat*(Cmatapblhr+Ne*Cmatengblhr))/Vbl
#    print (Clabop,Clabeng,Cmatap,Cmateng,Camb)
    return sum([Clabop,Clabeng,Cmatap,Cmateng,Camb])*par.CEF8919

def DOCdepr(Aircraft,Cman):
    #Cost due to depriciation of the aircraft
    par=Aircraft.ParCostLst
    Convers=Aircraft.ConversTool
    FlightOp=Aircraft.ParAnFP
    Prop=Aircraft.ParProp
    Payload=Aircraft.ParPayload
    
    tgm=tground(Aircraft)
    Rbl=FlightOp.Rangeclimbcruise/1000.*Convers.km2nm
    tflt=FlightOp.tclimbcruise/3600.
    tbl=tgm+tflt
    Vbl=Rbl/tbl
    ASP=par.ASP/par.CEF8919
    EP=Prop.Engine_cost*1e6/par.CEF8919
    Ne=Prop.N_engines
    Nprogram=Payload.fleetsize_y15
    
    #Costs of aircraft depriciation
    ManPerACCost  = Cman/Nprogram/par.CEF8919 #AC cost
#    print (ManPerACCost)
    AEP=ManPerACCost*(1+par.Fpror)
    Cdap=0.85*(AEP-Ne*EP-ASP)/(10*Uannbl(tbl)*Vbl)
    
    #Cost of engine depriciation
    Cdeng=(0.85*Ne*EP)/(7*Uannbl(tbl)*Vbl)
    
    #Cost of depriciation of avionics system
    Cdav=ASP/(5*Uannbl(tbl)*Vbl)
    
    #Costs of depriciation of airplane spare parts
    Cdapsp=(0.85*0.1*(AEP-Ne*EP))/(10*Uannbl(tbl)*Vbl)
    
    #Costs of depriciation of engine spare parts depriciation
    Cdengsp=(0.85*0.5*Ne*EP*1.50)/(7*Uannbl(tbl)*Vbl)
    
#    print (np.array([Cdap,Cdeng,Cdav,Cdapsp,Cdengsp])/sum([Cdap,Cdeng,Cdav,Cdapsp,Cdengsp]))
    return sum([Cdap,Cdeng,Cdav,Cdapsp,Cdengsp])*par.CEF8919

def DOClnr(Aircraft):
    #Costs due to landing/navigation fees and taxes
     par=Aircraft.ParCostLst
     Convers=Aircraft.ConversTool
     Struct=Aircraft.ParStruc
     FlightOp=Aircraft.ParAnFP
     MTOW=Struct.MTOW/Convers.lbs2kg
     tgm=tground(Aircraft)
     Rbl=FlightOp.Rangeclimbcruise/1000.*Convers.km2nm
     tflt=FlightOp.tclimbcruise/3600.
     tbl=tgm+tflt
     Vbl=Rbl/tbl    

     
     #Indirect operating costs due to landing fees
     Clf=0.002*MTOW/(Vbl*tbl)
     
     #Costs of navigation fees
     Cnf=10/(Vbl*tbl)
     
     #Direct costs of registery taxes
     frt=0.001+10**(-8)*MTOW
     return sum([Clf,Cnf])*par.CEF8919,frt
 

Cer  = 4.5e6 # USD19
Cman=CmanFunc(Conv, ISA_model, Cer)
docflt=DOCflt(Conv,Cman)
docmaint=DOCmaint(Conv,Cman)
docdepr=DOCdepr(Conv,Cman)
doclnr=DOClnr(Conv)[0]
frt=DOClnr(Conv)[1]
x=DOC(docflt,docmaint,docdepr,doclnr,frt)
tot=Coper(Conv,x)

    
#DOC(DOCflt,DOCmaint,DOCdepr,DOClnr,frt)
#Uann*Vbl*DOC___ to get costs per ac per year

