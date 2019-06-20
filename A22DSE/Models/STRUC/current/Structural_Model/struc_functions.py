# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 21:59:07 2019

@author: rickv
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import warnings
sys.path.append('../../../../../../')
warnings.filterwarnings("ignore")
#from pathlib import Path
#os.chdir(Path(__file__).parents[6])

#general math functions to run the program

def arc_length(x, y):  #verified with circles and parabolas
    ''' 
    DESCRIPTION: function that calculates the length of a curve
    INPUT: arrays of x and y coordinates for a 2D curve (x,y)
    OUTPUT: curve length (arc)
    '''    
    npts = len(x)
    arc = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    for k in range(1, npts):
        arc = arc + np.sqrt((x[k] - x[k-1])**2 + (y[k] - y[k-1])**2)

    return arc

#structural wing model functions to calculate the torsional stiffness KTHETA
    
def chord(bi,Aircraft): #verified
    ''' 
    DESCRIPTION: function that calculates the chord at a span position
    INPUT: span position in the aircraft body system (bi)
    OUTPUT: chord length at the span position (chord)
    ''' 
    bi=abs(bi)
    c_r = Aircraft.ParAnFP.c_r
    c_t = Aircraft.ParAnFP.c_t
    b = Aircraft.ParAnFP.b
    chord = c_r - (c_r-c_t)*2/b*bi
    return chord

def skin_eq_upper(chord): #verified with data
    ''' 
    DESCRIPTION: fucntion that makes a 25th order polynomial fit for the airfoil
    INPUT: datafiles of upper airfoil and the chord length
    OUTPUT: polynomal function of the upper airfoil
    ''' 
#    #read datafile
#    f=open("NASASC20712data_1.txt", "r")
#    data_f=f.read()
#    data_f = data_f.split('\n')
#    
#    x1=[]
#    y1=[]
#    for row in data_f: 
#        x1.append(float(row[0:8]))
#        y1.append(float(row[9:18]))
        
    x1 = [0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.04, 
          0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 
          0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 
          0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 
          0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 
          0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 
          0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66,0.67, 
          0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78,0.79, 
          0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 
          0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    y1 = [0.0, 0.0092, 0.0141, 0.019, 0.0252, 0.0294, 0.0327, 0.0354, 0.0377, 
          0.0397, 0.0415, 0.0431, 0.0446, 0.0459, 0.0471, 0.0483, 0.0494, 
          0.0504, 0.0513, 0.0522, 0.053, 0.0537, 0.0544, 0.0551, 0.0557,
          0.0562, 0.0567, 0.0572, 0.0576, 0.058, 0.0584, 0.0587, 0.059, 0.0592, 
          0.0594, 0.0596, 0.0598, 0.0599, 0.06, 0.0601, 0.0601, 0.0601, 0.0601, 
          0.0601, 0.06, 0.0599, 0.0598, 0.0596, 0.0594, 0.0592, 0.059, 0.0587,
          0.0584, 0.0581, 0.0577, 0.0573, 0.0569, 0.0564, 0.0559, 0.0554, 
          0.0549, 0.0543, 0.0537, 0.053, 0.0523, 0.0516, 0.0508, 0.05, 0.0491,
          0.0482, 0.0472, 0.0462, 0.0451, 0.044, 0.0428, 0.0416, 0.0403, 0.039,
          0.0376, 0.0362, 0.0347, 0.0332, 0.0316, 0.03, 0.0283, 0.0266, 0.0248, 
          0.023, 0.0211, 0.0192, 0.0172, 0.0152, 0.0131, 0.011, 0.0088, 0.0065, 
          0.0042, 0.0018, -0.0007, -0.0033, -0.006, -0.0088, -0.0117]

    x1 = [i * chord for i in x1]
    y1 = [i * chord for i in y1]
    p1 = np.polyfit(x1, y1, 25)
    func1 = np.poly1d(p1)
    
    return func1

def skin_eq_lower(chord): #verified with data
    ''' 
    DESCRIPTION: fucntion that makes a 25th order polynomial fit for the airfoil
    INPUT: datafiles of lower airfoil and the chord length
    OUTPUT: polynomal function of the lower airfoil
    ''' 
#    #read datafile
#    f=open("NASASC20712data_2.txt", "r")
#    data_f=f.read()
#    data_f = data_f.split('\n')

    x2=[0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 
         0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2,
         0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32,
         0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44,
         0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56,
         0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68,
         0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 
         0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92,
         0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    y2=[-0.0, -0.0092, -0.0141, -0.019, -0.0252, -0.0294, -0.0327, -0.0353,
        -0.0376, -0.0396, -0.0414, -0.043, -0.0445, -0.0459, -0.0472, -0.0484,
        -0.0495, -0.0505, -0.0514, -0.0523, -0.0531, -0.0539, -0.0546, -0.0553,
        -0.0559, -0.0564, -0.0569, -0.0574, -0.0578, -0.0582, -0.0585, -0.0588, 
        -0.0591, -0.0593, -0.0595, -0.0596, -0.0597, -0.0598, -0.0598, -0.0598,
        -0.0598, -0.0597, -0.0596, -0.0594, -0.0592, -0.0589, -0.0586, -0.0582,
        -0.0578, -0.0573, -0.0567, -0.0561, -0.0554, -0.0546, -0.0537, -0.0528,
        -0.0518, -0.0508, -0.0496, -0.0484, -0.0471, -0.0457, -0.0443, -0.0429,
        -0.0414, -0.0398, -0.0382, -0.0366, -0.0349, -0.0332, -0.0315, -0.0298,
        -0.028, -0.0262, -0.0244, -0.0226, -0.0208, -0.0191, -0.0174, -0.0157,
        -0.0141, -0.0125, -0.011, -0.0095, -0.0082, -0.007, -0.0059, -0.005,
        -0.0043, -0.0038, -0.0035, -0.0033, -0.0034, -0.0036, -0.0041, -0.0049,
        -0.0059, -0.0072, -0.0087, -0.0095, -0.0106, -0.011, -0.0117]

#    for row in data_f: 
#        x2.append(float(row[0:8]))
#        y2.append(-1*float(row[11:18]))
#    print(x2, y2)
    x2 = [i * chord for i in x2]
    y2 = [i * chord for i in y2]
    p = np.polyfit(x2, y2, 25)
    func2 = np.poly1d(p)
    
    return func2


def Area(chord): #verified
    ''' 
    DESCRIPTION: function that calculates the areas of the cells of the wing (A1,A2,A3)
    INPUT: chord length (chord)
    OUTPUT: areas of the cells (A1,A2,A3)
    '''     
    x_rib1=0.2*chord
    x_rib2=0.6*chord
    skin_upper_eq=skin_eq_upper(chord)
    skin_lower_eq=skin_eq_lower(chord)
    int_upper=np.polyint(skin_upper_eq)
    int_lower=np.polyint(skin_lower_eq)
    A1=int_upper(x_rib1)-int_upper(0)  - int_lower(x_rib1) + int_lower(0)
    A2=int_upper(x_rib2)-int_upper(x_rib1) - int_lower(x_rib2) + int_lower(x_rib1)
    A3=int_upper(chord)-int_upper(x_rib2) - int_lower(chord) + int_lower(x_rib2)
    
    return A1,A2,A3

def S(chord): #verified
    ''' 
    DESCRIPTION: function that calculates the circumferance of the cells of the wing (S1,S2,S3)
    INPUT: chord length (chord)
    OUTPUT: circumferance of the cells (S1,S2,S3)
    '''    
    x_rib1=0.2*chord
    x_rib2=0.6*chord
    skin_upper_eq=skin_eq_upper(chord)
    skin_lower_eq=skin_eq_lower(chord)
    h_rib1=skin_upper_eq(x_rib1)-skin_lower_eq(x_rib1)
    h_rib2=skin_upper_eq(x_rib2)-skin_lower_eq(x_rib2)
    xI=np.linspace(0.,x_rib1,50)
    xII=np.linspace(x_rib1,x_rib2,50)
    xIII=np.linspace(x_rib2,chord,50)
    S1=arc_length(xI,  skin_upper_eq(xI))+arc_length(xI,  skin_lower_eq(xI))
    S2=arc_length(xII,  skin_upper_eq(xII))+arc_length(xII,  skin_lower_eq(xII))
    S3=arc_length(xIII,  skin_upper_eq(xIII))+arc_length(xIII,  skin_lower_eq(xIII))
    
    return S1,S2,S3,h_rib1,h_rib2

def TwistSolver(chord, Aircraft,t_skin,t_rib): #finished
    ''' 
    DESCRIPTION: function that calculates rate of twist of wing
    INPUT: chord length (chord), t_skin(t_skin), rib thickness (t_rib)
    OUTPUT: rate of twist (dthetadz)
    '''   
    G_alu=Aircraft.ParStruc.G_Al
    G_comp=Aircraft.ParStruc.G_comp
    
    A1,A2,A3=Area(chord)
    S1,S2,S3,h_rib1,h_rib2=S(chord)
    T=1 #unit torque to run the numerical calculation
    A=np.matrix([[0, 2*A1, 2*A2, 2*A3],  
       [-1,     1/(2*A1)*(S1/G_alu/t_skin+h_rib1/G_comp/t_rib),     -1/(2*A1)*(h_rib1/G_comp/t_rib),     0  ],
       [-1,  -1/(2*A2)*(h_rib1/G_comp/t_rib), 1/(2*A2)*((S2+h_rib1+h_rib2)/G_comp/t_rib),  -1/(2*A1)*(h_rib2/G_comp/t_rib) ],
       [-1, 0, -1/(2*A3)*(h_rib2/G_comp/t_rib), 1/(2*A3)*(S3/G_alu/t_skin+h_rib2/G_comp/t_rib)]])
    b=np.matrix([T ,0,0,0])
    b=np.matrix.transpose(b)
    dthetadz = np.linalg.solve(A, b)[0]
    return dthetadz

def TorsionalStiffness(chord, Aircraft,t_skin,t_rib):  #verified
    ''' 
    DESCRIPTION: function that calculates the torsional stiffness of wing section
    INPUT: chord length (chord), t_skin(t_skin), rib thickness (t_rib)
    OUTPUT: torsional stiffnes (Ktheta)
    '''    
    T=1 #unit torque to run the numerical calculation
    dthetadz=TwistSolver(chord,Aircraft,t_skin,t_rib)
    K_theta = T/dthetadz

    return K_theta


#moment of intertia calculator


def rib_moi(chord,Aircraft,t_rib): #checked and verified
    ''' 
    DESCRIPTION: function that calculates the moment of inertia of the ribs. 
    INPUT: locations of the ribs (x_rib1, x_rib2), tickness of the rib (t_rib),
    wing skin equations (eq_lowerskin, eq_upperskin)
    OUTPUT: moment of inertia ribs (moi_ribs)
    '''
    skin_upper_eq=skin_eq_upper(chord)
    skin_lower_eq=skin_eq_lower(chord)
    x_rib1=0.2*chord
    x_rib2=0.6*chord
    h_rib1=skin_upper_eq(x_rib1)-skin_lower_eq(x_rib1)
    h_rib2=skin_upper_eq(x_rib2)-skin_lower_eq(x_rib2)
    moi_ribs=1/12*t_rib*(h_rib1**3+h_rib2**3)
    
    return moi_ribs

def skin_moi(chord,Aircraft,t_skin): #fin
    '''
    DESCRIPTION: function that calculates the moment of inertia of the skin. 
    INPUT: tickness of the skin (t_skin), 
        wing skin equations (eq_lowerskin, eq_upperskin)
    OUTPUT: moment of inertia skin (moi_skin)    
    '''

    skin_upper_eq=skin_eq_upper(chord)
    skin_lower_eq=skin_eq_lower(chord)
    steps=100.
    dx=1/steps
    x=np.linspace(0.,chord,steps)
    moi_skin=0
    for i in x:
        y_upper=skin_upper_eq(i)
        y_lower=skin_lower_eq(i)
        moi_skin=moi_skin+y_upper**2*t_skin*dx+y_lower**2*t_skin*dx
    return moi_skin
    
def moi_root_stringers(chord, Aircraft): #multiple of 10, with min 20
    #initise
    n=Aircraft.ParStruc.n_stiff
    A=Aircraft.ParStruc.A_stiff
    skin_upper_eq=skin_eq_upper(chord)
    skin_lower_eq=skin_eq_lower(chord)
    c1=0.2*chord
    c2=0.4*chord
    c3=0.4*chord    
    n1=int(1/5*n)
    n2=int(2/5*n)
    n3=int(2/5*n)
    in_stri=[]
    #calculate moment of inertia list
    #cell 1
    ds=c1/(n1/2)
    x=0.2*chord
    for i in range(n1):
        inertia=A*(skin_upper_eq(x))**2+A*(skin_lower_eq(x))**2
        x=x-ds
        in_stri.append(inertia)
    #cell 2
    ds=(c2-1)/(n2/2)
    x=0.2*chord
    for j in range(n2):
        inertia=A*(skin_upper_eq(x))**2+A*(skin_lower_eq(x))**2
        x=x+ds
        in_stri.append(inertia)    
    #cell 3
    ds=c3/(n3/2)
    x=0.6*chord
    for k in range(n3):
        inertia=A*(skin_upper_eq(x))**2+A*(skin_lower_eq(x))**2
        x=x+ds
        in_stri.append(inertia)   
    
    
    return in_stri #list of all stringers with inertia


def moi_stringer(chord,Aircraft):  #n in multiples of 5 (min=20)
    c_r=Aircraft.ParAnFP.c_r
    factor=chord/c_r
    
    in_root=moi_root_stringers(chord, Aircraft)
    moi_stringers=factor*float(sum(in_root))
    
    return moi_stringers



def moi_wing(chord,Aircraft, t_skin, t_rib):
    ''' 
    DESCRIPTION: function that calculates the total moment of inertia of the wing (moi_wing)
    INPUT: moi functions of all the structural components
    OUTPUT: moment of inertia at a certain span position
    '''     
    
    moi_wing=skin_moi(chord,Aircraft, t_skin)+rib_moi(chord,Aircraft, t_rib)\
        +moi_stringer(chord,Aircraft)


    return moi_wing

def wing_struc_mass(Aircraft,t_skin,t_rib):
    ''' 
    DESCRIPTION: function that calculates the structural wing mass
    INPUT: Aircraft,t_skin,n,A,t_rib,rho_alu,rho_comp
    OUTPUT: wing structural mass, without systems (only material weight)
    '''     
    n=Aircraft.ParStruc.n_stiff
    A=Aircraft.ParStruc.A_stiff
    b=Aircraft.ParAnFP.b
    rho_alu=Aircraft.ParStruc.rho_Al
    rho_comp=Aircraft.ParStruc.rho_comp
    bi=np.linspace(-b/2,b/2,50)
    w_skin=0
    db=b/50
    for i in bi:
        chordi=chord(i,Aircraft)
        S1,S2,S3,h_rib1,h_rib2=S(chordi)
        #skin weight+rib weight
        A_skin_rho=(S1+S3)*t_skin*rho_alu+(S2+h_rib1+h_rib2)*t_rib*rho_comp
        w_skin=w_skin+A_skin_rho*db

    #stiffener weight
    MAC=Aircraft.ParAnFP.MAC
    c_r=Aircraft.ParAnFP.c_r
    factor=MAC/c_r
    n_avg=factor*n
    V=n_avg*A*b
    w_stiffeners=V*rho_alu
    
    #total weight
    w_total=w_skin+w_stiffeners
    
    return w_total

def EI(Aircraft,chord):
    ''' 
    DESCRIPTION: function that calculates the structural wing mass
    INPUT: Aircraft,t_skin,n,A,t_rib,rho_alu,rho_comp
    OUTPUT: wing structural mass, without systems (only material weight)
    '''   
    t_skin = Aircraft.ParStruc.t_skin
    t_rib = Aircraft.ParStruc.t_rib
    E_alu = float(Aircraft.ParStruc.E_Al)
    E_comp = float(Aircraft.ParStruc.E_comp)
    moi_stringer = moi_root_stringers(chord, Aircraft)
    moi_skin = skin_moi(chord,Aircraft,t_skin)
    moi_ribs = rib_moi(chord,Aircraft,t_rib)
    EI = moi_stringer*E_alu + moi_skin*0.5*(E_alu+E_comp)+moi_ribs*E_alu
    return t_rib


def Eliptical(Aircraft,steps):
    #function that returns an eliptical lift distribution, where L is the max lift and b the span
    b=Aircraft.ParAnFP.b
    MTOW=Aircraft.ParStruc.MTOW
    x=np.linspace(-b/2,b/2,steps)

    return 4*MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)


def Loading_Diagrams(Aircraft,steps):
    #bs
    anfp=Aircraft.ParAnFP
    struc=Aircraft.ParStruc
    layout=Aircraft.ParLayoutConfig
    prop = Aircraft.ParProp
    #initialise parameters
    b=anfp.b
    g=9.81
    m_engine=prop.Engine_weight
    y_engine1=Aircraft.ParLayoutConfig.y_eng_g2
    y_engine2=Aircraft.ParLayoutConfig.y_eng_g3 #dummy
    y_engine3=Aircraft.ParLayoutConfig.y_eng_g3+5. #dummy
    x=np.linspace(-b/2,b/2,steps)
    dx=b/steps
    MTOW=struc.MTOW*g
    m_fuel=struc.FW
    #engines
    V_e1=-np.heaviside((x-y_engine1),1)*m_engine*g*4
    V_e2=-np.heaviside((x-y_engine2),1)*m_engine*g*4
    V_e3=-np.heaviside((x-y_engine3),1)*m_engine*g*4
    V_e4=-np.heaviside((x+y_engine1),1)*m_engine*g*4
    V_e5=-np.heaviside((x+y_engine2),1)*m_engine*g*4
    V_e6=-np.heaviside((x+y_engine3),1)*m_engine*g*4
    V_e=V_e1+V_e2+V_e3 +V_e4+V_e5+V_e6
    #lift
    liftdistr=4*MTOW/(np.pi*b)*np.sqrt(1-4*x**2/b**2)
    V_l=[]
    V_l_i=0
    for i in liftdistr:
        i=i+1
        V_l_i=V_l_i+i*dx
        V_l.append(V_l_i)
    #fuselage
    w_fuselage=V_l[-1]-6*m_engine*g*4
    V_f=-np.heaviside(x,1)*w_fuselage
    #total shear
    V=V_e+V_f+V_l
    #moment
    M=[]
    M_l_i=0
    for j in V:
        M_l_i=M_l_i+j*dx
        M.append(M_l_i)
    chordi=chord(x,Aircraft) 
    
    p = np.polyfit(x, M, 25)
    M_po = np.poly1d(p)
    
#    u2= []
#    u2_i = 0
#    for k in range(len(x)):
#        chord_i=chordi[k]
#        EI_i=12669314 #EI(Aircraft,chord_i)
#        M_i=M[k]
#        u2_i = u2_i - 1/EI_i *M_i*dx
#        u2.append(u2_i)
#    u1=[]
#    u2_mid=u2[int(steps/2)]
#    for m in u2:
#        m=m+u2_mid
#        u1.append(m)
#        
#    u=[]
#    u_i=0
#    for l  in u1:
#        u_i=u_i-l*dx
#        u.append(u_i)
#        
#        
    return x, V, M, M_po

def defl(Aircraft, steps):
    x=Loading_Diagrams(Aircraft,steps)[0]
    M=Loading_Diagrams(Aircraft,steps)[2]
    chordi = chord(x, Aircraft)
#    EI_i = EI(Aircraft, chordi)
    
    return x, M, chordi#, EI


#x=np.linspace(0.,0.005,10)
#y=np.linspace(0.,0.010,10)
#xv, yv = np.meshgrid(x, y)
#
#z = np.ones(np.shape(xv))
#
#for i, xi in enumerate(x):
#    ylst=[]
#    for j, yi in enumerate(y):
#        t=wing_struc_mass(Conv,i,j)
#        z[i][j] = t
#         
#        
#        
#contour plots
    
#a=plt.contourf(xv,yv, z)
##plt.clabel(a, inline=True, fontsize=12)
#plt.title('Structural Wing Weight Sensitivity to Ribs and Skin Thickness')
#plt.xlabel('Wing Thickness [m]')
#plt.ylabel('Skin Thickness [m]')
#
#plt.show()


        
#a,b,c=Loading_Diagrams(Conv,1000)
#plt.plot(a,b)
#plt.title('Vertical Shear Diagram')
#plt.xlabel('Span Position [m]')
#plt.ylabel('Shear Force [N]')
#plt.show()
  
#plt.plot(a,c)
#plt.title('Bending Moment Diagram')
#plt.xlabel('Span Position [m]')
#plt.ylabel('Bending  Moment [Nm]')
#plt.show()
    
#plotting contour
#    
#x=np.linspace(0.,0.005,10)
#y=np.linspace(0.,0.01,10)
#xv, yv = np.meshgrid(x, y)
#
#z = np.ones(np.shape(xv))
#
#for i, xi in enumerate(x):
#    ylst=[]
#    for j, yi in enumerate(y):
#        t=TorsionalStiffness(1, Conv,i,j)
#        z[i][j] = t
#         
#a=plt.contour(xv,yv, z)
#plt.clabel(a, inline=True, fontsize=12)
#plt.title('Sensitivity of Torsional Stifness to Wing and Rib Thickness')
#plt.xlabel('Wing Thickness [m]')
#plt.ylabel('Rib Thickness [m]')
#
#plt.show()
#
#



