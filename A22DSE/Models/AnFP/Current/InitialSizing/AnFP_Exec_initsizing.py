import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../../../../../')
import A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_flightprofile as fp
#import AnFP_def_Atmosphere_T_p_rho as atmosphere

#from All_dic_Parameters import Parameters as par
#from A22DSE.Parameters.Par_Class_All import Aircraft
#from A22DSE.Parameters.Par_Class_Atmos import Atmos
#from A22DSE.Parameters.Par_Class_Conv1 import Conv
#from A22DSE.Parameters.Par_Class_Atmos import Atmos

# =============================================================================
#                           WING LOADING and OTHER RATIOS
# =============================================================================



# =============================================================================
# def ComputeCD0(WS, MTOW):
#     #INPUT: WS (matrix of type float), MTOW (type float)
#     #OUTPUT: Return CD0 in matrix form
#     #Description: From wing loading and iterated MTOW, acquire wetted area
#     #             and friction drag, which CD0 can be directedly computed
# 
#     # CONSTANTS obtained from Roskam read from graphs
#     ft2m = 0.3048
#     ibs2kg = 0.459532666
#     a = -2.5229
#     b = 1.000
#     c = 0.1628
#     d = 0.7316
#     
#     Swet = np.power(10,(c+d*np.log10(MTOW/ibs2kg))) #Calculation of wetted area
#     S = MTOW/WS/ft2m**2                      # MTOW divided by wing loading    
#     # compute secondary parameters
#     f = np.power(10, a+b*np.log10(Swet)) 
#     CD0 = f/S
#     
#     return CD0
# =============================================================================

# =============================================================================
#                                   TAKE-OFF
# =============================================================================
def TWTakeoff(ws,Aircraft):
    #INPUT: wing loading and takeoff cl
    #OUTPUT: TW for wing loading and Cl where columns represent clto and rows W/S
    #Description: Calculate required thrust to weight for takeoff roll and 35ft obtstacle.
    AnFP = Aircraft.ParAnFP
    CL_to = np.linspace(AnFP.CL_to,AnFP.CL_to,1)
    sigmato = 1 #Ratio of density at to location relative to S.L. standard density
    return (37.5/3.28/47.880172)*np.matrix(ws).T/(AnFP.fieldlen_to*sigmato*np.matrix(CL_to))

# =============================================================================
#                                   CLIMB
# =============================================================================


#def TWClimb(CL_TO, CL_A, A, e, N_Engine, CD0):
def TWClimb(Aircraft):
    #INPUT: MTOW [kg] in float, CL_take-off as numpy float matrix,
    #       Aspect ratio in float, Oswald factor in float
    #       , Amount of engines in int, Zero-lift drag in float 
    #OUTPUT: Returns to-be-designed Thrust-to-Weight for climb performance
    #Description: Computes the to-be-designed TW for given input according to
    #            The CS25 climb requirement as discussed in pg. 170 Roskam
    #               Chapter 3, FAR 25.111, etc.
    
    
    # config: 1 = En-route Clean; 2 = Initial TO-fl; 3 = Transition TO-fl, LG
    #         4 = Second-segment TO-fl; 5 = AEO balked landing L-fl, LG
    #         6 = OEI balked landing A-Fl, LG
    
    AnFP = Aircraft.ParAnFP
    Struc = Aircraft.ParStruc
    muAscend = [1.25, 1.2, 1., 1.2]
    muBalked = [1.3, 1.5]
    dCD0_Ascend = np.matrix([0.,0.015, 0.035, 0.015])    
    dCD0_Balked = np.matrix([0.065, 0.04])
    de_TOFlaps  = 0.05
    de_LandFlaps = 0.10
    e = AnFP.e
    CD0 = AnFP.CD0
    A = AnFP.A
    N_Engine = Struc.N_engines
    CL_to = np.linspace(AnFP.CL_to,AnFP.CL_to,1)
    CL_land = np.linspace(AnFP.CL_land,AnFP.CL_land,1)
    
    #CS25 CGR requirement for EN-ROUTE CLIMB REQUIREMENT: 25.121
    def SelectCGRAscend(N_Engine):
        if N_Engine == 2:
            CGR_clean = 0.012; CGR_init = 0.012; CGR_trans = 0; CGR_2nd = 0.024
            
        elif N_Engine == 3:
            CGR_clean = 0.015; CGR_init = 0.015; CGR_trans = 0.03
            CGR_2nd = 0.027
            
        elif N_Engine == 4:
            CGR_clean = 0.017; CGR_init = 0.012; CGR_trans = 0.05
            CGR_2nd = 0.03
            
        else:
            return None
        
        return np.matrix([CGR_clean, CGR_init, CGR_trans, CGR_2nd])
    
    def SelectCGRBalked(N_Engine):
        if N_Engine == 2:
            CGR_AEO = 0.032; CGR_OEI = 0.021
            
        elif N_Engine == 3:
            CGR_AEO = 0.032; CGR_OEI = 0.024
            
        elif N_Engine == 4:
            CGR_AEO = 0.032; CGR_OEI = 0.027
            
        else:
            return None
        
        return np.matrix([CGR_AEO, CGR_OEI])
  
    
    def ComputeLD(CL, mu, dCD0, de):
        #INPUT: MTOW [kg] in float, CL_take-off as float matrix,
        #       Aspect ratio in float, Oswald factor in float,
        #       Zero-lift drag in float
        #OUTPUT: Returns the Lift-to-Drag ratio in a float matrix.
        #Description: Computes the LD values of CL_TO vector and associated
        #             Correcting factor (mu) depending on its velocity,
        #             e.g. V2 = 1.2VTO. See pg. 146 Chapter 3 Roskam pt.1
        #CS25 CGR requirement for EN-ROUTE CLIMB REQUIREMENT: 25.111 pg. 164
        
        
        # Drag polar
        CL_Corrected = CL/np.matrix(np.power(mu,2)).T       # Column: CL change
        kCL2 = np.power(CL_Corrected,2)/(np.pi*A*(e+de))
        
        CD = CD0 + kCL2 + np.matrix(dCD0).T
        
        LD = CL_Corrected/CD                       # Change column: CL; row: mu
        
        
        #TODO correct for density
        
        return LD

    def ComputeTW(CL, CGR, mu, dCD0, de):
        #INPUT: Climb Gradient, float vector of 4x1, N_Engine in int
        #OUTPUT: Thrust-to-Weight that is most killing and thus to-be-designed
        #Description: Computes TW from the acquired matrix of LD values and
        #            CGR requirements from CS25.
        #           !!! NOTE to self: CGR[0] is intended to be added to
        #           first row of LD matrix
        
        LD = ComputeLD(CL, mu, dCD0, de)
        
        TW = (N_Engine/(N_Engine-1))*(1/np.matrix(LD) + np.matrix(CGR).T)
        
        TW_design = np.zeros([np.size(CL),1])      # Initiate array

        for i in range(np.shape(TW)[1]):
            TW_design[i] = np.max(TW[:,i])
        return TW_design
    
    CGR_Ascend = SelectCGRAscend(N_Engine)
    CGR_Balked = SelectCGRBalked(N_Engine)
    
    if np.size(CGR_Ascend) < 4:
        return ValueError("Contact the author; Incorrect #Engines")
    
    TWAscend = ComputeTW(CL_to, 
                         CGR_Ascend, muAscend, dCD0_Ascend, de_TOFlaps)
    TWBalked = ComputeTW(CL_land, 
                         CGR_Balked, muBalked, dCD0_Balked, de_LandFlaps)
    
    TW = np.append(TWAscend, TWBalked)
    
    CorrectForTemperature = 0.8
    return np.max(TW)/CorrectForTemperature

#def TWCeilingClimb(WS, A, e, hCeiling, CD0,wfratioclimb):
def TWCeilingClimb(WS, Aircraft, ISA_model):
    
    #INPUT: Wing loading as float vector , Aspect ratio in float,
    #       Oswald factor as float, Service ceiling [m] in float
    #       Zero-lift drag in float.
    #OUTPUT: Returns Thrust-over-weight for service ceiling corrected for alt.
    #Description: Given the service ceiling requirement of CS25 of a Jet
    #             airplane, the Thrust-over-weight can be derived from
    #             equation (3.34)-(3.36) Roskam in 3.4.10 pg. 150 Roskam Pt. 1
    #             The TW is corrected for altitude.
    #CS25 constant (for jet transport aircraft):
    AnFP = Aircraft.ParAnFP
    Convers = Aircraft.ConversTool
    Struc = Aircraft.ParStruc
    
    RoC = 100*Convers.ft2m/60                                  # meters per second
    ISAFunc = ISA_model.ISAFunc
    #Compute optimum Vclimb = f(WS, CD0, rho, A,e):
    rho = ISAFunc([AnFP.h_cruise])[2]
    WS = WS*(0.99*0.99*0.995*Struc.wfratioclimb)
    Vclimb = np.sqrt(2*WS/(rho*np.sqrt(AnFP.CD0*np.pi*AnFP.A*AnFP.e)))
#    print(Vclimb)
    LDmax = 0.5*np.sqrt(np.pi*AnFP.A*AnFP.e/AnFP.CD0)    #Maximum L/D
    TWmax = RoC/Vclimb + 1/LDmax
    
    #Correct for altitude
    TWmax = TWmax * 1.225/rho
    
    return TWmax
# =============================================================================
#                                   CRUISE
# =============================================================================


def TWCruise(ws,Aircraft, ISA_model):
    #INPUT: Wing loading, range(in meters), cruise altitude, CD0, aspect ratio,
    #   oswald efficiency, thrust specific fuel consumption
    #OUTPUT: Thrust to weight ratio and fuel fraction
    #Description: Given a wing loading and cruise altitude find the optimum 
    #velocity for max range.
    AnFP = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    hcruise = AnFP.h_cruise
    CD0 = AnFP.CD0
    A = AnFP.A
    e = AnFP.e
    SFC = AnFP.SFC
    wfratioclimb = struc.wfratioclimb
    #Calculate atmospheric conditions at cruise alt
    atmos = ISA_model.ISAFunc([hcruise])
    
    #Calculate CL for optimum range for jet
    CL = np.sqrt(CD0*np.pi*A*e/3)
    LD = CL/(CD0+CL**2/(np.pi*A*e))

    ws = ws*(0.99*0.99*0.995*wfratioclimb)

    #Find speed and dynamic pressure for optimum range dependant on W/S
    v = np.sqrt(ws/(CL*0.5*atmos[2]))
    q = 0.5*atmos[2]*v**2

    #Find TW for W/S at S.L.
    TW = (CD0+(CL**2)/(np.pi*A*e))*q/ws*1.225/atmos[2]

    #Find fuel fraction begin/end (W5/W6)
    #wfratiocruise = np.exp(Range*SFC/(v*LD))
    
    #Obtain fuel fraction by 1-Wend/WTO fraction
    #wfratio = 1-(0.99*0.99*0.995*wfratioclimb/wfratiocruise*0.99*0.992)

    return TW, v

def Rangecorrect(ws0, Aircraft, ISA_model):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    wfratioclimb = struc.wfratioclimb
    CD0 = anfp.CD0
    A = anfp.A
    e = anfp.e
    Range = anfp.s_cruise
    SFC = anfp.SFC
    Mdd = anfp.Mdd
    hcruise = anfp.h_cruise
    #INPUT: Initial wing loading, climb fuel fraction, CD0, A, e, Range, Specific Fuel Consumption
    #Mach divergence and altitude
    #OUTPUT: Fuel ratio relative to MTOW
    dw = 0.001
    w = 1
    #Correct ws at cruise due to fuel burnt during takeoff taxi and climb
    ws = ws0*(0.99*0.99*0.995*wfratioclimb)
    rtotal = 0
    atmos = ISA_model.ISAFunc([hcruise])
    #Start loop that calculates range per weight burned.
    while rtotal < Range:
        #Calculate CL and v for Mdd
        v = Mdd*np.sqrt(1.4*287.05*atmos[0])
        CLtest = 2*ws/(atmos[2]*(v**2))
        #If CLtest is larger than the optimum CL for range then
        if CLtest > (CD0*np.pi*A*e/3):
            CL = CLtest
            v = v
            
        else:
            CL = (CD0*np.pi*A*e/3)
            v = np.sqrt(2*ws/(CL*atmos[2]))
        #Calculate lift to drag for discritisation
        LD = CL/(CD0+CL**2/(np.pi*A*e))
        #Breguet delta range increase due to delta weight decrease
        dr = v/SFC/LD*dw
        rtotal += dr
        #print(v,LD,rtotal,w)
        w -= dw
    wfratiocruise = 1/w
    wfratio = 1-(0.99*0.99*0.995*wfratioclimb/wfratiocruise*0.99*0.992)
    return wfratio
    
    
    

def TWCruisemax(ws,Aircraft, ISA_model):
    #INPUT: Wing loading, cruise altitude, CD0, aspect ratio,
    #   oswald efficiency, Mach drag divergence and wfratio climb
    #OUTPUT: Thrust to weight ratio
    #Description: Given a wing loading and cruise altitude find the thrust 
    #to weight required.
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    hcruise = anfp.h_cruise
    CD0 = anfp.CD0
    A = anfp.A
    e= anfp.e
    Mdd = anfp.Mdd
    wfratioclimb = struc.wfratioclimb
    
    #Calculate atmospheric conditions at cruise alt
    atmos = ISA_model.ISAFunc([hcruise])
    
    #Find speed and dynamic pressure for optimum range dependant on W/S
    v = Mdd*np.sqrt(1.4*287.05*atmos[0])
    q = 0.5*atmos[2]*v**2

    #Find TW for W/S at S.L.
    ws = ws*(0.99*0.99*0.995*wfratioclimb)
    CL = ws/(q)
    TW = (CD0+(CL**2)/(np.pi*A*e))*q/ws*1.225/atmos[2]
    
    return TW

def WScruise(Aircraft,Atmos_model):
    #INPUT: W/S, Mach divergence, altitude, CD0, A, e
    #OUTPUT: Velocity divergence, W/S max allowable.
    #Description: maximum wing loading where aircraft would become speed 
    #unstable at cruise.
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    
    Mdd = anfp.Mdd
    hcruise = anfp.h_cruise
    CD0 = anfp.CD0
    A = anfp.A
    e = anfp.e
    wfratioclimb = struc.wfratioclimb
    #Calculate atmospheric conditions at cruise alt
    atmos = Atmos_model.ISAFunc([hcruise])
    #Calculate drag divergence velocity
    vdd = np.sqrt(atmos[0]*1.4*287.05)*Mdd
    #Calculate minimum wing loading for stable speed response
    ws = np.sqrt(CD0*np.pi*A*e)*(vdd**2)*atmos[2]*0.5/(0.99*0.99*0.995*wfratioclimb)
    return vdd, ws

def WScruise2(Aircraft, Atmos_model):
    
    #INPUT: W/S, Mach divergence, altitude, CD0, A, e
    #OUTPUT: Velocity divergence, W/S max allowable.
    #Description: maximum wing loading where aircraft would become speed 
    #unstable at cruise.
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    
    Mdd = anfp.Mdd
    hcruise = anfp.h_cruise
    CD0 = anfp.CD0
    A = anfp.A
    e = anfp.e
    wfratioclimb = struc.wfratioclimb
    
    #Calculate atmospheric conditions at cruise alt
    atmos = Atmos_model.ISAFunc([hcruise])
    #Calculate drag divergence velocity
    vdd = np.sqrt(atmos[0]*1.4*287.05)*Mdd
    #Calculate minimum wing loading for stable speed response
    ws = np.sqrt(CD0*np.pi*A*e/3)*(vdd**2)*atmos[2]*0.5/(0.99*0.99*0.995*wfratioclimb)
    return vdd, ws

def WSCruisestall(Aircraft, Atmos_model):
    #INPUT: W/S, Mach divergence, altitude, CD0, A, e
    #OUTPUT: Velocity divergence, W/S max allowable.
    #Description: maximum wing loading where aircraft would become speed 
    #unstable at cruise.
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    CLmax = anfp.CL_max_cruise
    Mdd = anfp.Mdd
    hcruise = anfp.h_cruise
    wfratioclimb = struc.wfratioclimb
    #Calculate atmospheric conditions at cruise alt
    T,press,rho = Atmos_model.ISAFunc([hcruise])
    #Calculate drag divergence velocity
    vdd = np.sqrt(T*1.4*287.05)*Mdd
    #Calculate minimum wing loading for stable speed response
    ws = 0.5*rho*vdd**2*CLmax/(0.99*0.99*0.995*wfratioclimb)
    return ws

# =============================================================================
#                                   DESCEND
# =============================================================================
###Descend###

# =============================================================================
#                                   LANDING
# =============================================================================
###Landing###

def WSLanding(Aircraft):
    #INPUT: Field length, Landing CL
    #OUTPUT: Limiting W/S
    #Description: Finds W/S limiting for landing based on Roskam empirical.
    anfp = Aircraft.ParAnFP
    
    fieldlen_land = anfp.fieldlen_land
    clland = np.linspace(anfp.CL_land,anfp.CL_land,1)
    vapp = np.sqrt(fieldlen_land/(0.6*0.3/(0.5144**2)/3.28))
    vs0 = vapp/1.3
    sigmaland = 1 #Ratio of density at to location relative to S.L. standard density
    return 0.5*1.225*sigmaland*vs0**2*clland







# =============================================================================
#                                  MAIN BODY
# =============================================================================


#def WSandTW(Plots,OEWratio,wfratioclimb, Range,SFC,hcruise,A,e,Mdd,CD0,N_Engine,payload,fieldlen_to,fieldlen_land,clto,clland):
def WSandTW(Plots, Aircraft, ISA_model):
    
    AnFP = Aircraft.ParAnFP
    Struc = Aircraft.ParStruc
    # TODO: change constants here to using only from object
    #################################################
    #use this format for inputs:
    
    #OEWratio = 1/2.47 #Ratio of OEW to MTOW from Statistical data of stratospheric aircraft
    #wfratioclimb = 0.8
    #Range = 2500*10**3
    #SFC = 0.667
    #hcruise = 20000
    #A = 22
    #e = 0.85
    #Mdd = 0.72
    #CD0 = 0.02
    #N_Engine = 2
    #payload = 10000
    #fieldlen_to = 2500 #Meters
    #fieldlen_land = 2500 #Meters
    #clto = np.linspace(1.8,1.8,1) #CL takeoff
    #clland = np.linspace(2.4,2.4,1) #CL Landing
    #################################################
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    payl = Aircraft.ParPayload
    wsinit = 100
    wsfinal = 7000  
    ws = np.linspace(wsinit,wsfinal,1000) #Wing Loading 

    error = 1
    while error > 10**-3:
        TWtakeoff = TWTakeoff(ws,Aircraft)               #Calculation of TW limits for takeoff
        TWcruise = TWCruise(ws,Aircraft, ISA_model)[0]           #Calculation of TW for cruise at optimum CL for range.
        WSlanding = WSLanding(Aircraft)                                 #Wing loading for landing
        vdd,wsdd = WScruise(Aircraft, ISA_model)                       #Velocity drag divergence and max wing loading for speed stability.
        vdd2,wsdd2 = WScruise2(Aircraft, ISA_model)                   #Velocity drag divergence and max wing loading for optimum range cruise speed
        TWclimb = TWClimb(Aircraft)                       #Worst case TW required for climb gradients
        TWceiling = TWCeilingClimb(ws, Aircraft, ISA_model)             #Worst case TW for ceiling climb
        TWcruisemax = TWCruisemax(ws,Aircraft, ISA_model)              #Max cruise speed thrust requirement
        wscruisestall = WSCruisestall(Aircraft, ISA_model)
        
        Aircraft.ParAnFP.WS =  min(wsdd,min(WSlanding),wscruisestall)
        wsmin = min(wsdd,min(WSlanding),wscruisestall)#Obtain leftmost wing loading line.
        v = TWCruise(wsmin,Aircraft, ISA_model)[1]               #Calculate cruise velocity and Fuel Weight ratio relative to MTOW
                                                  #Estimate for MTOW
        
        index = np.where(ws == ws.flat[np.abs(ws - wsmin).argmin()])
        TW = float(max(TWtakeoff[index],TWceiling[index],TWclimb,TWcruisemax[index])) #Choose max TW values
        Aircraft.ParAnFP.TtoW = TW
        oldwfratioclimb = Aircraft.ParStruc.wfratioclimb
        Aircraft.ParStruc.wfratioclimb, wfcruise = fp.FuelFractions(Aircraft,ISA_model)
        error = abs((Aircraft.ParStruc.wfratioclimb)-oldwfratioclimb)
        

        #wfratio = Rangecorrect(wsmin,Aircraft, ISA_model) #Calculate range with 0.72 mach constraint if needed
        wfratio = 1-wfcruise
        payratio = 1-wfratio-struc.OEWratio                                               #Calculation of the payload ratio relative to MTOW
        MTOW = payl.m_payload/payratio
        
        MTOW = 1.1*MTOW #safety factor
#MTOW,TW,payratio, wfratio, wsmin, WSlanding, TWtakeoff, wsdd, wsdd2, TWclimb, TWceiling, TWcruise, TWcruisemax, wf = WSandTW()

    #print('\n MTOW: ', MTOW,'kg', '\n', 'Wing Surface Area: ', MTOW/(wsmin/9.80665),'m^2', '\n', 'Thrust: ', TW*MTOW*9.80665 ,'N', '\n','Payload fraction: ', payratio,'\n','Fuel fraction: ', wfratio,'\n','Wing Loading: ', wsmin, 'N/m^2', '\n','T/W: ', TW )
    if Plots == True:
        
        plt.plot([WSlanding,WSlanding],[0,2]) #Plot wing loading line for landing
        plt.plot(ws,TWtakeoff, label='Takeoff T/W') #Plot TW for takeoff
        plt.plot([0,wsdd2],[max(TWcruise),max(TWcruise)], label='Cruise T/W') #Plot TW for cruise
        plt.plot([wsdd,wsdd],[0,2],'r--',label='W/S Speed Stability') #Plot wing loading for speed stability at cruise altitude
        plt.plot([wsdd2,wsdd2],[0,2],'g--',label='W/S Cruise Speed') #Plot wing loading for cruise speed at cruise altitude.
        plt.plot([wscruisestall,wscruisestall],[0,2],'y--',label='W/S Cruise Stall') #Plot wing loading for stall at cruise altitude and Mmo.
        plt.plot([wsinit,wsfinal],[TWclimb,TWclimb], label='T/W Climb') #Plot TW for worst case climb gradient.
        plt.plot(ws,TWceiling, label='T/W Ceiling Climb') #Plot TW for ceiling climb
        plt.plot(ws,TWcruisemax)
        #plt.plot([wsmin,wsmin*(0.99*0.99*0.995*struc.wfratioclimb),(1-wfratio)*wsmin],[TW,TW/(0.99*0.99*0.995*struc.wfratioclimb),TW/(1-wfratio)], label='Cruise W/S & T/W Change')
        
        plt.axis((0,8000,0,1))
        plt.xlabel('W/S [N/m^2]')
        plt.ylabel('T/W')
        plt.legend()
        
        plt.show()
        
    return (MTOW, wfratio*MTOW, MTOW/(wsmin/9.80665), TW*MTOW*9.80665, TW, wsmin)



##OEWratio = 1/2.47 #Ratio of OEW to MTOW from Statistical data of stratospheric aircraft
##wfratioclimb = 0.8
##Range = 2500*10**3
##SFC = 0.667/3600
##hcruise = 20000
##A = 22
##e = 0.85
##Mdd = 0.72
##CD0 = 0.02
##N_Engine = 2
##payload = 10000
##fieldlen_to = 2500 #Meters
##fieldlen_land = 2500 #Meters
##clto = np.linspace(1.8,1.8,1) #CL takeoff
##clland = np.linspace(2.4,2.4,1) #CL Landing
##CLmax = 1.5
##
##WSandTW(True,OEWratio,wfratioclimb, Range,SFC,hcruise,A,e,Mdd,CD0,N_Engine,payload,fieldlen_to,fieldlen_land,clto,clland)

# =============================================================================
# wsmin = 2400#min(wsdd,min(WSlanding)) #Obtain leftmost wing loading line.
# v = TWCruise(wsmin,Range,hcruise,CD0,A,e,SFC,wfratioclimb)[1] #Calculate cruise velocity and Fuel Weight ratio relative to MTOW
# wfratio = Rangecorrect(wsmin,wfratioclimb,CD0, A, e, Range, SFC, Mdd, hcruise) #Calculate range with 0.72 mach constraint if needed
# payratio = 1-wfratio-OEWratio #Calculation of the payload ratio relative to MTOW
# MTOW = payload/payratio #Estimate for MTOW
# 
# index = np.where(ws == ws.flat[np.abs(ws - wsmin).argmin()])
# 
# TW = max(TWtakeoff[index],TWceiling[index],TWclimb,TWcruisemax[index]) #Choose max TW values
# 
# print('\n MTOW: ', MTOW,'kg', '\n', 'Wing Surface Area: ', MTOW/(wsmin/9.80665),'m^2', '\n', 'Thrust: ', TW*MTOW*9.80665 ,'N', '\n','Payload fraction: ', payratio,'\n','Fuel fraction: ', wfratio,'\n','Wing Loading: ', wsmin, 'N/m^2', '\n','T/W: ', TW )
# 
# plt.plot([WSlanding,WSlanding],[0,2]) #Plot wing loading line for landing
# plt.plot(ws,TWtakeoff, label='Takeoff T/W') #Plot TW for takeoff
# plt.plot([0,wsdd2],[max(TWcruise),max(TWcruise)], label='Cruise T/W') #Plot TW for cruise
# plt.plot([wsdd,wsdd],[0,2],'r--',label='W/S Speed Stability') #Plot wing loading for speed stability at cruise altitude
# plt.plot([wsdd2,wsdd2],[0,2],'g--',label='W/S Optimum Range Speed') #Plot wing loading for cruise speed at cruise altitude.
# plt.plot([wsinit,wsfinal],[TWclimb,TWclimb], label='T/W Climb') #Plot TW for worst case climb gradient.
# plt.plot(ws,TWceiling, label='T/W Ceiling Climb') #Plot TW for ceiling climb
# plt.plot(ws,TWcruisemax, label='T/W Maximum Operating Mach')
# plt.plot([wsmin,wsmin*(0.99*0.99*0.995*wfratioclimb),(1-wfratio)*wsmin],[TW,TW/(0.99*0.99*0.995*wfratioclimb),TW/(1-wfratio)], label='Cruise W/S & T/W Change')
# 
# plt.axis((0,4000,0,1.5))
# plt.xlabel('W/S [N/m^2]')
# plt.ylabel('T/W')
# plt.legend()
# 
# plt.show()
# =============================================================================
