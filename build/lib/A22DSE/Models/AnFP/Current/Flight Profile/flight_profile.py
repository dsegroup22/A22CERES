# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:32:12 2019

@author: Atiqah
"""

from math import cos, sin, tan, sqrt, pi, e
import matplotlib.pyplot as plt
import numpy as np
from All_dic_Parameters import Parameters as par

#Description: Calculate the distance for the take-off phase from V=0 to V=Vlof (excluding airborne phase); any hard-coded parameters are subject to change and is only a first estimate
#Input: Wing Surface Area, Weight, CD0, Aspect Ratio, Oswald efficiency factor, Thrust-to-Weight, Lift-to-Drag
#Ouput: flight profile graphs


dt = 1 #[s] time increment

CD0 = 0.012 #at take-off (ground run) <subject to change>
A = 13 #aspect ratio <subject to change>
ef = 0.85 #Oswald's efficiency factor <subject to change>
k = 1/(pi*A*ef)

#atmospheric properties during take-off
g = par.get('g_0') #[m/s2] #gravitational acceleration at sea-level
rho = 1.225 #[kg/m3] #density at sea level


S = 90 #par.get('S') #[m2] #wing surface area <subject to change>
W_in = 60000 #par.get('MTOW')
W = 60000 #par.get('MTOW') #par.get('TOW') #[kg] #subject to change based on  OEW Class I estimation method + payload weight
V = 0 #[m/s] #velocity at start of take-off

#mf_to = 0.2 #[kg/s] #mass fuel flow during take-off #need to be determine
SFC = 16*10e-6 #[kg/N/s] #specific fuel consumption <subject to change>
#SFC = 0.667
T = 200000 #[N] #maximum thrust at take-off <subject to change>
mf_to = SFC*T

CD_to = 0.2 #par.get('CD_to') #[-] #drag coefficient during 1st phase of take-off <subject to change>
CL_to = 1 #par.get('CL_to') #[-] #lift coefficient during 1st phase of take-off <subject to change>

t = 0 #[s] #initial time
dt = 1 #[s] #time increment
mu = 0.03 #[-] #frictional viscosity during 1st phase take-off of main and nose landing gear <subject to change>
Vr = 50 #[m/s] #speed at which nose should be rotated up <subject to change>
s = 0 #[m] #initial distance

distance = [0] #[m] #list of distances
time = [0] #[s] #list of time
alt = 0 #[m] #initial altitude
weight = [W] #[kg] 
altitude = [0] #15.24 scrreen height provided by CS25
w_to = []
#V=0 to V=Vr
print ('loop 1 - for 1st phase of take-off')
while V < Vr:  
    a = (1/W)*(T-CD_to*.5*rho*V**2*S-mu*(W*g-CL_to*.5*rho*V**2*S)) #acceleration during 1st phase of take-off
    print (a)
    V = V + a*dt #velocity increment
    print(V)
    W = W - mf_to*dt #weight decrease 
    w_to.append(W)
    weight.append(W)
    s = s + V*dt #distance during 1st phase of take-off
    t= t + dt
    time.append(t)
    distance.append(s)
    altitude.append(0)
    if s>2500:
        break 
print ('end of loop 1')

CD1 = 0.2 #[-] #drag coefficient during 2nd phase of take-off <subject to change>
CL1 = 1.5 #[-] #lift coefficient during 2nd phase of take-off <subject to change>
mu1 = 0.5 #[-] #frictional viscosity during 2nd phase of take-off <subject to change>
L = CL1*.5*rho*V**2*S #[N] #initial lift during 2nd phase of take-off
aoa = 5*pi/180 #[rad] #nost up aoa during 2nd phase of take-off <subject to change>
#print(L)
#print(W)
#V=Vr to V=Vlof
print ('loop 2 - for 2nd phase of take-off')
while L < W*g: #during lift-off speed the lift = weight
    #print('in loop')
    a = (1/W)*(T*cos(aoa)-CD1*.5*rho*V**2*S-mu1*(W*g-CL1*.5*rho*V**2*S-T*sin(aoa))) #acceleration during 2nd phase of take-off
    #print (a)
    V = V + a*dt
    #print (V)
    W = W - mf_to*dt
    w_to.append(W)
    weight.append(W)
    s = s + V*dt
    t = t + dt
    time.append(t)
    distance.append(s)
    altitude.append(0)
    L = CL1*.5*rho*V**2*S
print ('end of loop 2')

aoa_climbout = 10*pi/180 #angle of attack during climbout <subject to change>
s_tra=V**2/0.15/g*sin(aoa_climbout) #[m] #distance during climbout
alt_scr=15.24 #[m] #screen height constraints by CS25
slop=alt_scr/s_tra

print ('loop 3 - for climbout phase of take-off')
while alt<=alt_scr:
    alt=alt+V*sin(slop)*dt 
    print(alt)
    s = s + V*cos(slop)*dt 
    t = t + dt
    time.append(t)
    altitude.append(alt)
    distance.append(s)
print ('end of loop 3')


#t = 0
TtoW = 0.68 #from pere <subject to change>
LtoD = 1/sqrt(4*k*CD0) #maximising Lift
Z = 1 + sqrt(1+3/((LtoD**2)*((TtoW)**2)))
max_roc = (((W*g/S)*Z/(3*rho*CD0))**0.5)*((TtoW)**1.5)*(1-Z/6-3/(2*((TtoW)**2)*(LtoD**2)*Z))


print ('loop 4 - for climbing')

w_climb = []
v_climb = []
roc = []

#while int(max_roc) ==! 0:      
while alt <= 20000:
    if alt <= 11000:
        temp = 15.04 - 0.00649*alt
        p = 101.29*((temp+273.1)/288.08)**(5.256)
        rho_alt = p/(0.2869*(temp+273.1))
        SFC_climb1= SFC*rho_alt/rho
        T = TtoW*(W*g)
        mf_cl1 = SFC_climb1*T
        #mf_cl1 = 1 #specific fuel consumption for the first climb phase <subject to change>
        W = W-mf_cl1*dt 
        w_climb.append(W)
        weight.append(W)
        Z = 1 + sqrt(1+3/((LtoD**2)*((TtoW*rho_alt/rho)**2))) 
        V_max_roc = sqrt((TtoW*(W*g/S)/(3*rho_alt*CD0))*(1+sqrt(1+3/(LtoD**2*TtoW**2))))
        print(V_max_roc)
        v_climb.append(V_max_roc)
        max_roc = (((W*g/S)*Z/(3*rho_alt*CD0))**0.5)*((TtoW*rho_alt/rho)**1.5)*(1-Z/6-3/(2*((TtoW*rho_alt/rho)**2)*(LtoD**2)*Z))
        print(max_roc)
        roc.append(max_roc)
        s = s + sqrt(V_max_roc**2+max_roc**2)*dt
        alt = alt + max_roc*dt
        if int(max_roc) == 0: #when roc = 0 with the current TtoW, TtoW must be increased
           break
#            TtoW = 0.9
#            alt = altitude[-1]
        #max_roc = int(max_roc)
        distance.append(s)
        altitude.append(alt)
        #print(alt)
        t = t + dt
        time.append(t)
    if 11000 <= alt < 20000:
       # mf_cl2 = 1 #specific fuel consumption for the second climb phase <subject to change>
       # W =W-mf_cl2*dt
        temp = -56.46
        p = 22.65*e**(1.73-0.000157*alt)
        rho_alt = p/(0.2869*(temp+273.1))
        SFC_climb2= SFC*rho_alt/rho
        T = TtoW*(W*g)
        mf_cl2 = SFC_climb2*T
        W =W-mf_cl2*dt
        w_climb.append(W)
        weight.append(W)
        Z = 1 + sqrt(1+3/((LtoD**2)*((TtoW*rho_alt/rho)**2)))
        V_max_roc = sqrt((TtoW*(W*g/S)/(3*rho_alt*CD0))*(1+sqrt(1+3/(LtoD**2*TtoW**2))))
        print(V_max_roc)
        v_climb.append(V_max_roc)
        max_roc = ((W*g/S)*Z/(3*rho_alt*CD0))**0.5*(TtoW*rho_alt/rho)**1.5*(1-Z/6-3/(2*(TtoW*rho_alt/rho)**2*LtoD**2*Z))
        print(max_roc)
        roc.append(max_roc)
        s = s + sqrt(V_max_roc**2+max_roc**2)*dt
        #print(max_roc)
        alt = alt + max_roc*dt
        if int(max_roc) == 0:  #when roc = 0 with the current TtoW, TtoW must be increased
            break
#            TtoW = 0.9
#            alt = altitude[-1]
        distance.append(s)
        altitude.append(alt)
        #print(alt)
        t = t + dt
        time.append(t)
print ('end of loop 4')
#
#payload_in = par.get('m_sulphur') #[kg]
#payload = par.get('m_sulphur') #[kg]
#dispersalrate = par.get('dispersionrate_pertime') #[kg/s]
#timeinject = payload / dispersalrate
#mf_cr = 1 #specific fuel consumption at cruise
#V_cruise = par.get('M_cruise')*par.get('a_cruise')
#
#
#SFC_cruise = 22.7*10e-6
#print ('loop 5 - for cruising')
#while payload >= 0:
#    altitude.append(par.get('h_cruise'))
#    payload = payload - dispersalrate*dt
#    W = W - mf_cr*dt-dispersalrate*dt
#    weight.append(W)
#    s = s + V_cruise*dt
#    t = t + dt
#    distance.append(s)
#    time.append(t)
#print ('end of loop 5')
#
##Descent  20km to 10km to 0km
##assumption that we have small flight path angle
#
#flight_path = 3*pi/180 #[rad] #flight path angle during descent <subject to change>
#aoa = -6*pi/180 #[rad] #aoa during descent <subject to change>
#CL_ds = 0.5 #[-] #lift coefficient during descent <subject to change>
#rho_cruise = par.get('rho_cruise')
#TtoW = 0.5
#
#print ('loop 6 - for descent phase')
#while alt >= 0:
#    if alt >= 11000:
#        mf_ds1 = 0.2 #specific fuel consumption during descent phase 1 <subject to change>
#        W = W - mf_ds1*dt
#        weight.append(W)
#        temp = -56.46
#        p = 22.65*e**(1.73-0.000157*alt)
#        rho_alt = p/(0.2869*(temp+273.1))
##        SFC_ds1= SFC_cruise*rho_alt/rho_cruise
##        T = TtoW*(W*g)
##        mf_ds1 = SFC_ds1*T
##        W =W-mf_ds1*dt
##        weight.append(W)
#        #print(rho_alt)
#        V_ds = sqrt(2*W*g/(rho_alt*S*CL_ds))
#        V_ds_x = V_ds*cos(flight_path)
#        rod = V_ds*sin(flight_path)
#        alt = alt-rod*dt
#        #print(alt)
#        altitude.append(alt)
#        s = s + V_ds_x*dt
#        t = t+dt
#        distance.append(s)
#        time.append(t)
#    if alt < 11000:
#        mf_ds2 = 0.2 #specific fuel consumption during descent phase 2 <subject to change>
#        W = W -mf_ds2*dt
#        weight.append(W)
#        temp = 15.04 - 0.00649*alt
#        p = 101.29*((temp+273.1)/288.08)**(5.256)
#        rho_alt = p/(0.2869*(temp+273.1))
##        SFC_ds2= SFC_cruise*rho_alt/rho_cruise
##        T = TtoW*(W*g)
##        print(T)
##        mf_ds2 = SFC_ds2*T
##        W =W-mf_ds2*dt
##        print(W)
##        weight.append(W)
#        #print(rho_alt)
#        V_ds = sqrt(2*W*g/(rho_alt*S*CL_ds))
#        V_ds_x = V_ds*cos(flight_path)
#        rod = V_ds*sin(flight_path)
#        alt = alt-rod*dt
#        altitude.append(alt)
#        s = s + V_ds_x*dt
#        t = t+dt
#        distance.append(s)
#        time.append(t)
#print ('end of loop 6')

W2W1 = w_climb[-1]/w_climb[0]
#climbff = (w_climb[0]-w_climb[-1])/(W_in-payload_in-W)

#plt.plot(np.array(time[:52]),np.array(altitude[:52]))
plt.figure(1)
plt.plot(np.array(time)/60,np.array(altitude)/1000)
plt.xlabel('Time [min]')
plt.ylabel('Altitude [km]')
plt.figure(2)
plt.plot(np.array(distance)/1000,np.array(altitude)/1000)
plt.xlabel('Distance [km]')
plt.ylabel('Altitude [km]')
plt.show()