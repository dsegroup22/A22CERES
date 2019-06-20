# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:37:45 2019

@author: menno
"""
import numpy as np
import matplotlib.pyplot as plt
import gc
import os


from pathlib import Path
os.chdir(Path(__file__).parents[4])
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Models.DATCOM.Current.datcomconvertermatlab import GetDerivatives






steps=20

dihedralrange = np.linspace(-10,2,steps)
twistrange = np.linspace(-7,-1,steps)

parameters=np.array(['C_D_0','C_D_cruise','C_L_a','C_l_b','C_m_a','C_Y_b','C_n_b','C_L_adot',\
          'C_m_adot', 'C_l_p','C_Y_p','C_n_p','C_n_r','C_l_r','C_l_q','C_m_q'])
def name(**variables):
    return [x for x in variables]

def greek(letter):
    if letter=='b':
        return r'\beta'
    if letter=='a':
        return r'\alpha'
    if letter=='adot':
        return r'\.\alpha'
    else:
        return letter

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


for parameter in parameters:
    data=np.zeros(len(dihedralrange))
    title=r'$'+parameter[0].split('_')[0]+\
    '_{'+parameter.split('_')[1]+'_{'+greek(parameter.split('_')[2])+'}}$ [$rad^{-1}$]'
    if hasNumbers(parameter):
        title=r'$'+parameter[0].split('_')[0]+\
    '_{'+parameter.split('_')[1]+'_{'+greek(parameter.split('_')[2])+'}}$ [-]'
    
    for tw in twistrange:
        subdata=np.array([])
        for dh in dihedralrange:
            Conv.ParAnFP.dhwing=dh/180*np.pi
            Conv.ParAnFP.twwing=tw/180*np.pi
            C_D_0,C_D_cruise,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,C_L_adot,C_m_adot,\
        C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q=GetDerivatives(Conv,'hihg')
            
            subdata=np.append(subdata,vars()[parameter])
    
        data=np.vstack((data,subdata))
    data=data[1:]
    
    plt.clf()
    plt.figure(figsize=(7,6))
    contours=plt.contour(dihedralrange,twistrange,data,levels=[0,100000])
    plt.clabel(contours, inline=True, fontsize=14)
    plt.contourf(dihedralrange,twistrange,data,cmap='Greys',levels=50)
    plt.colorbar()
    plt.title(title,fontsize=18,horizontalalignment='center')
    plt.tick_params(labelsize=14)
    plt.xlabel(r'$\Gamma_{wing}$ [$^{\circ}$]',fontsize=14)
    plt.ylabel('Wing Twist [$^{\circ}$]',fontsize=14)
    plt.savefig(r'A22DSE\Models\DATCOM\Current\Plots\Wing\''[:-1]+parameter+  "wing.png",pad_inches=0.5)

    print(parameter)


