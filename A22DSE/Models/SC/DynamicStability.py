# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:03:23 2019

@author: lujingyi
"""
from math import radians,pi,sin,cos
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
m      = struc.MTOW        	  # mass after climb [kg]

# aerodynamic properties
e      = anfp.e       # Oswald factor [ ]
CD0    = anfp.CD0     # Zero lift drag coefficient [ ]
CLa    = anfp.C_L_alpha_cruise# Slope of CL-alpha curve [ ]

# Longitudinal stability
Cma    = 1    #anfp.C_m_a   # longitudinal stabilty [ ]
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

rho    = 0.089            # [kg/m^3]  (air density)
W      = m*g			  #	[N]       (aircraft weight)

# Constant values concerning aircraft inertia

muc    = m/(rho*S*c)
mub    = m/(rho*S*b)
KX2    = 0.019
KZ2    = 0.042
KXZ    = 0.002
KY2    = 1.25*1.114

# Aerodynamic constants

Cmac   = 0                 # Moment coefficient about the aerodynamic centre [ ]
CNwa   = CLa   		       # Wing normal force slope [ ]
CNha   = 2*pi*Ah/(Ah+2)    # Stabiliser normal force slope [ ]
depsda = 4/(A+2)           # Downwash gradient [ ]

# Lift and drag coefficient

CL = 2*W/(rho*V0**2*S)               # Lift coefficient [ ]
CD = CD0 + (CLa*alpha0)**2/(pi*A*e)  # Drag coefficient [ ]

# Stabiblity derivatives

CX0    = W*sin(th0)/(0.5*rho*V0**2*S)
CXu    = -0.02792
CXa    = -0.47966
CXadot = +0.08330
CXq    = -0.28170
CXde   = -0.03728

CZ0    = -W*cos(th0)/(0.5*rho*V0**2*S)
CZu    = -0.37616
CZa    = -5.74340
CZadot = -0.00350
CZq    = -5.66290
CZde   = -0.69612

Cmu    = +0.06990
Cmadot = +0.17800
Cmq    = -8.79415

CYb    = -0.7500
CYbdot =  0     
CYp    = -0.0304
CYr    = +0.8495
CYda   = -0.0400
CYdr   = +0.2300

Clb    = -0.10260
Clp    = -0.71085
Clr    = +0.23760
Clda   = -0.23088
Cldr   = +0.03440

Cnb    =  +0.1348
Cnbdot =   0     
Cnp    =  -0.0602
Cnr    =  -0.2061
Cnda   =  -0.0120
Cndr   =  -0.0939