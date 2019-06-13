# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 21:59:07 2019

@author: rickv
"""

import matplotlib.pyplot as plt
import numpy as np


#structural wing model functions

def chord(bi,Aircraft): #verified
    ''' 
    DESCRIPTION: function that calculates the chord at a span position
    INPUT: span position in the aircraft body system (bi)
    OUTPUT: chord length at the span position (chord)
    ''' 
    bi=abs(bi)
    c_r = Conv.ParAnFP.c_r
    c_t = Conv.ParAnFP.c_t
    b = Conv.ParAnFP.b
    chord = c_r - (c_r-c_t)*2/b*bi
    return chord

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

def skin_eq_upper(chord): #verified with data
    ''' 
    DESCRIPTION: fucntion that makes a 25th order polynomial fit for the airfoil
    INPUT: datafiles of upper airfoil and the chord length
    OUTPUT: polynomal function of the upper airfoil
    ''' 
    #read datafile
    f=open("NASASC20712data_1.txt", "r")
    data_f=f.read()
    data_f = data_f.split('\n')
    
    x1=[]
    y1=[]
    for row in data_f: 
        x1.append(float(row[0:8]))
        y1.append(float(row[9:18]))
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
    #read datafile
    f=open("NASASC20712data_2.txt", "r")
    data_f=f.read()
    data_f = data_f.split('\n')

    x2=[]
    y2=[]

    for row in data_f: 
        x2.append(float(row[0:8]))
        y2.append(-1*float(row[11:18]))
    x2 = [i * chord for i in x2]
    y2 = [i * chord for i in y2]
    p = np.polyfit(x2, y2, 25)
    func2 = np.poly1d(p)
    
    return func2

def moi_stringer(t,b,h): #fin
    ''' 
    DESCRIPTION: fucntion that moment of inertia of a stringer
    INPUT: stringer dimensions widht (b), height (h), thickness (t)
    OUTPUT: moment of inertia stringer
    ''' 
    return 1/12*b*h**3+(h/2)**2*(b+h)*t

def rib_moi(chord,t_rib): #fin
    ''' 
    DESCRIPTION: function that calculates the moment of inertia of the ribs. 
    INPUT: locations of the ribs (x_rib1, x_rib2), tickness of the rib (t_rib),
    wing skin equations (eq_lowerskin, eq_upperskin)
    OUTPUT: moment of inertia ribs (moi_ribs)
    ''' 
    x_rib1=0.2*chord
    x_rib2=0.6*chord
    h_rib1=eq_upperskin(x_rib1)-eq_lowerskin(x_rib1)
    h_rib2=eq_upperskin(x_rib2)-eq_lowerskin(x_rib2)
    moi_ribs=1/12*t_rib*(h_rib1**3+h_rib2**3)
    
    return moi_ribs

def skin_moi(x,t_skin): #needs to be checked
    '''
    DESCRIPTION: function that calculates the moment of inertia of the skin. 
    INPUT: tickness of the rib (t_rib), 
        wing skin equations (eq_lowerskin, eq_upperskin)
    OUTPUT: moment of inertia skin (moi_skin)    
    '''
    skin_upper_eq=skin_eq_upper(chord)
    skin_lower_eq=skin_eq_lower(chord)
    steps=len(x)
    dx=1/steps
    moi_skin=0
    for i in x:
        y_upper=skin_eq_upper()
        y_lower=skin_eq_lower()
        moi_skin=moi_skin+y_upper**2*t_skin*dx+y_lower**2*t_skin*dx
        
    return moi_skin
    
def moi_wing(x,t_skin,t_rib):
    
    
    return moi_wing

def Area(chord): #verified
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

def S(chord): #finished
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

t_skin=0.003175
t_rib=0.02

def TwistSolver(chord, t_skin,t_rib): #finished
    A1,A2,A3=Area(chord)
    S1,S2,S3,h_rib1,h_rib2=S(chord)
    G_alu=26.9e9
    G_comp=5e9
    T=1 #unit torque to run the numerical calculation
    A=np.matrix([[0, 2*A1, 2*A2, 2*A3],  
       [-1, 1/(2*A1)*(S1/G_alu/t_skin+h_rib1/G_comp/t_rib), -1/(2*A1)*(h_rib1/G_comp/t_rib),0  ],
       [-1,  -1/(2*A2)*(h_rib1/G_comp/t_rib), 1/(2*A1)*(S2/G_alu/t_skin+h_rib2/G_comp/t_rib+h_rib1/G_comp/t_rib),  -1/(2*A1)*(h_rib2/G_comp/t_rib) ],
       [-1, 0, -1/(2*A1)*(h_rib2/G_comp/t_rib), 1/(2*A3)*(S3/G_alu/t_skin+h_rib2/G_comp/t_rib)]])
    b=np.matrix([T ,0,0,0])
    b=np.matrix.transpose(b)
    dthetadz = np.linalg.solve(A, b)[0]
    return dthetadz

def TorsionalStiffness(chord,t_skin,t_rib):  #finished
    T=1 #unit torque to run the numerical calculation
    dthetadz=TwistSolver(chord,t_skin,t_rib)
    
    return (T/dthetadz)





