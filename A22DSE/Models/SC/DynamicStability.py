# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:03:23 2019

@author: lujingyi
"""
from math import radians,pi,sin,cos,sqrt,tan
# Parameter abbreviation
anfp = Conv.ParAnFP
layout = Conv.ParLayoutConfig
struc = Conv.ParStruc

# Stationary flight condition

hp0    = 20000        # pressure altitude in the stationary flight condition [m]
V0     = anfp.V_cruise# true airspeed in the stationary flight condition [m/sec]
alpha0 = radians(3)   # angle of attack in the stationary flight condition [rad]
th0    = 0       	  # pitch angle in the stationary flight condition [rad]

# Aircraft mass
m      = struc.MTOW*struc.wfratioclimb       	  # mass after climb [kg]

# aerodynamic properties
e      = anfp.e       # Oswald factor [ ]
CD0    = anfp.CD0     # Zero lift drag coefficient [ ]
CLa    = anfp.C_L_alpha_cruise# Slope of CL-alpha curve [ ]

# Longitudinal stability
Cma    = -0.25*anfp.MAC*CLa #anfp.C_m_a  #0.01 #p143 # longitudinal stabilty [ ]
Cmde   = 1            # elevator effectiveness [ ]   !!!!!!!!!!!!!

# Aircraft geometry

S      = anfp.S	          # wing area [m^2]
Sh     = layout.Sht       # stabiliser area [m^2]
Sh_S   = Sh/S	          # [ ]
lh     = layout.xht       # tail length [m]
c      = anfp.MAC	      # mean aerodynamic cord [m]
lh_c   = lh/c	          # [ ]
b      = anfp.b	          # wing span [m]
bh     = layout.bh	      # stabilser span [m]
A      = b**2/S            # wing aspect ratio [ ]
Ah     = bh**2/Sh          # stabilser aspect ratio [ ]
Vh_V   = 1		          # [ ]
ih     = -2*pi/180        # stabiliser angle of incidence [rad] !!!!!!!!!!!!!!!!

# Constant values concerning atmosphere and gravity

rho0   = 1.2250           # air density at sea level [kg/m^3] 
R      = 287.05           # specific gas constant [m^2/sec^2K]
g      = 9.81             # [m/sec^2] (gravity constant)
gamma  = 1.4
T_cruise = 273.15-56.5    
rho    = 0.089            # [kg/m^3]  (air density)
W      = m*g			  #	[N]       (aircraft weight)

# Constant values concerning aircraft inertia

muc    = m/(rho*S*c)
mub    = m/(rho*S*b)
I_xx   = m*2.2046*((layout.l_fuselage*3.28)**2)/810*1.35
I_yy   = m*2.2046*((b*3.28)**2)/1870*1.35
I_zz   = m*2.2046*((0.5*(layout.l_fuselage+b)*3.28)**2)/770*1.35
KX2    = I_xx/(m*b*b)
KZ2    = I_zz/(m*b*b)
KY2    = I_yy/(m*c*c)
KXZ    = 0.002
#print(KX2,KZ2,KY2,KXZ)

#KX2    = 0.019
#KZ2    = 0.042
#KXZ    = 0.002
#KY2    = 1.25*1.114

# Aerodynamic constants

Cmac   = 0                 # Moment coefficient about the aerodynamic centre [ ]
CNwa   = CLa   		       # Wing normal force slope [ ]
CNha   = 2*pi*Ah/(Ah+2)    # Stabiliser normal force slope [ ]
depsda = 4/(A+2)           # Downwash gradient [ ]

# Lift and drag coefficient

CL = 2*W/(rho*V0**2*S)               # Lift coefficient [ ]
CD = CD0 + (CLa*alpha0)**2/(pi*A*e)  # Drag coefficient [ ]
M1 = anfp.M_cruise
CLu = M1**2/(1-M1**2)*CL    #??? figure 135
CDu = (2*CL**2)/(pi*A*e) * M1**2/(1-M1**2) #M1* (-16*W**2/(rho**2*(gamma*R*T_cruise)**2*M1**5*S**2*pi*A*e))

# Stabiblity derivatives

CX0    = W*sin(th0)/(0.5*rho*V0**2*S)
CXu    = -CDu #-0.2792  #(CLu*sin(alpha0)-CDu*cos(alpha0))/c #-0.02792  #Clu,Cdu p136,133
CXa    = -2*CL/(pi*A*e)*CLa+CL      #-0.47966  #p139
#CXadot = +0.08330
#CXq    = -0.28170
#CXde   = -0.03728

CZ0    = -W*cos(th0)/(0.5*rho*V0**2*S)
CZu    = -CLu    #-0.37616  #-Clu p134 
CZa    = -CLu-CD    #-5.74340  #p139
deda = (2*0.14)/(pi*A)*180/pi
CZadot = -2*anfp.CLhalpha*0.95*1*deda     #anfp.C_L_adot    #-0.00350 #p141
CZq    = -2*anfp.CLhalpha*layout.xht/c*0.95*0.18        #anfp.C_l_q       #-5.66290 #144
#CZde   = -0.69612

#Cmu    = +0.06990  #p138 table
Cmadot = -2.2*anfp.CLhalpha*0.95*layout.xht*deda#anfp.C_m_adot    #+0.17800
Cmq    = -2.2*anfp.CLhalpha*0.95*layout.xht  #anfp.C_m_q       #-8.79415 #145

betav = sqrt(1-M1**2)
CLvbeta= 2*pi*layout.Avt/(2.+ sqrt(4.+layout.Avt*(betav/0.95)**2*(1.+(tan(radians(layout.Sweep50vt))/betav)**2)))
CYb    = anfp.C_Y_b       #-0.7500
CYbdot =  0     
CYp    = -2*CLvbeta*layout.bv/b*0.95*layout.Svt/S  #anfp.C_Y_p       #-0.0304 #p150
CYr    = CLvbeta*(2*layout.xvt/b)*0.95*layout.Svt/S   #+0.8495          #p157
#CYda   = -0.0400
#CYdr   = +0.2300

Clb    = anfp.C_l_b       #-0.10260
Clp    = -2*CLvbeta*(layout.bv/b)**2*0.95*layout.Svt/S    #anfp.C_l_p       #-0.71085 #p152
Clr    = CLvbeta*(2*layout.xvt*layout.bv/(b**2))*0.95*layout.Svt/S   #anfp.C_l_r       #+0.23760 #p161
#Clda   = -0.23088
#Cldr   = +0.03440

Cnb    =  anfp.C_n_b      #+0.1348
Cnbdot =   0     
Cnp    =  2*CLvbeta*(layout.bv/b)*(layout.xvt/b)*0.95*layout.Svt/S #anfp.C_n_p      #-0.0602  #154
Cnr    =  -CLvbeta*(2*layout.xvt/b)**2*0.95*layout.Svt/S    #anfp.C_n_r      #-0.2061  #p161
#Cnda   =  -0.0120
#Cndr   =  -0.0939


#--------------------------------------------------------------------------
#-------------eigenvalues for dynamic motions---------------------
#--------------------------------------------------------------------------

#short period 
A1 = 4* muc**2 * KY2
B1 = -2 * muc *(KY2*CZa + Cmadot+ Cmq )
C1 = CZa * Cmq  - 2*muc * Cma
labda_real_1 = - B1 / (2*A1)
labda_imag_1  =  (sqrt(4*A1*C1-B1**2))/(2*A1)
labda_c1 = complex(labda_real_1,labda_imag_1)
labda_1 = labda_c1 * (V0/c)
#print(labda_c1)
labda_c2 = complex(labda_real_1, -labda_imag_1)
labda_2 = labda_c2 * (V0/c)

T1 = -0.693/labda_real_1*c/V0
omega01 = sqrt(labda_real_1**2+labda_imag_1**2)*V0/c
xi1 = -labda_imag_1/sqrt(labda_real_1**2+labda_imag_1**2)
P1 = 2*pi/omega01/sqrt(1-xi1**2) 
 



#phugoid 
A2 = -4 * muc**2 
B2 = 2 * muc * CXu
C2 = -CZu  * CZ0 
labda_real_2 = - B2 / (2*A2)
labda_imag_2  =  (sqrt(4*A2*C2-B2**2))/(2*A2)
labda_c3 = complex(labda_real_2,labda_imag_2 )
labda_3 = labda_c3 *(V0/c)
labda_c4 = complex(labda_real_2, -labda_imag_2)
labda_4 = labda_c4*(V0/c) 

T2 = -0.693/labda_real_2*c/V0
omega02 = sqrt(labda_real_2**2+labda_imag_2**2)*V0/c
xi2 = -labda_imag_2/sqrt(labda_real_2**2+labda_imag_2**2)
P2 = 2*pi/omega02/sqrt(1-xi2**2) 

#Aperiodic 
labda_c5 = Clp / (4 * mub * KX2)
labda_5 = labda_c5*(V0/c) 

T5 = -0.693/labda_c5*b/V0


#Dutch roll 
#Eigenvalue
A3 = 8 * mub**2 * KZ2
B3 = -2 * mub * (Cnr + 2*KZ2 * CYb)
C3 = 4 * mub * Cnb + CYb * Cnr 
labda_real_3 = - B3 / (2*A3)
labda_imag_3  =  (sqrt(4*A3*C3-B3**2))/(2*A3)
labda_c6 = complex(labda_real_3,labda_imag_3 )
labda_6 = labda_c6*(V0/c) 
labda_c7 = complex(labda_real_3, -labda_imag_3)
labda_7 = labda_c7*(V0/c) 

T3 = -0.693/labda_real_3*b/V0
omega03 = sqrt(labda_real_3**2+labda_imag_3**2)*V0/b
xi3 = -labda_imag_3/sqrt(labda_real_3**2+labda_imag_3**2)
P3 = 2*pi/omega03/sqrt(1-xi2**2) 


# Spiral 

#Eigenvalue
labda_c8 = (2 * CL *(Clb* Cnr - Cnb * Clr ))/(Clp *(CYb * Cnr + 4*mub * Cnb) - Cnp *(CYb * Clr + 4 * mub * Clb ))
labda_8 = labda_c8*(V0/c) 
T8 = -0.693/labda_c8*b/V0