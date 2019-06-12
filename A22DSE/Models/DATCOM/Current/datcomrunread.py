# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:58:22 2019

@author: menno
"""
import subprocess
import os
from pathlib import Path
import numpy as np
import pynput
import pyautogui
import time


os.chdir(Path(__file__).parents[0])
os.startfile("datcom.exe",'open')
time.sleep(0.1)

#pyautogui.click(500, 500)
pyautogui.typewrite('ceres.dat\n')
#pynput.keyboard.Key.enter


os.chdir(Path(__file__).parents[4])

file=open('A22DSE\Models\DATCOM\Current\datcom.out','r')

lines=file.readlines()


def my_split(s):
    seps=['              ','             ','            ','            ','          ','         ','        ','       ','      ','     ','    ','   ','  ',' ']
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res
k=0
for j in range(len(lines)):
    line=lines[j]
    if line==' -----------------------  FLIGHT CONDITIONS  ------------------------           --------------  REFERENCE DIMENSIONS  ------------\n':
        if k==0 or k==2:
            dataline=my_split(lines[j+8].strip(),)
            C_L_as=np.array([])
            for i in range(6):
                C_L_as=np.append(C_L_as,float(my_split(lines[j+8+i].strip())[7]))
            C_L_a=np.average(C_L_as)
            C_l_bs=np.array([])
            for i in range(6):
                C_l_bs=np.append(C_l_bs,float(my_split(lines[j+8+i].strip())[-1]))
            C_l_b=np.average(C_l_bs)
                   
            C_m_a,C_Y_b,C_n_b=np.array(dataline[8:11]).astype(float)
            C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b=np.round(np.array([C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b])*180/np.pi,5)
            #print(C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,j)
        if k==1 or k==3:
            dataline=my_split(lines[j+9].strip(),)
            C_L_adots=np.array([])
            for i in range(6):
                C_L_adots=np.append(C_L_adots,float(my_split(lines[j+9+i].strip())[3]))
            C_L_adot=np.average(C_L_adots)
            C_m_adots=np.array([])
            for i in range(6):
                C_m_adots=np.append(C_m_adots,float(my_split(lines[j+9+i].strip())[4]))
            C_m_adot=np.average(C_m_adots)
            C_l_ps=np.array([])
            for i in range(6):
                C_l_ps=np.append(C_l_ps,float(my_split(lines[j+9+i].strip())[5]))
            C_l_p=np.average(C_l_ps)
            C_Y_ps=np.array([])
            for i in range(6):
                C_Y_ps=np.append(C_Y_ps,float(my_split(lines[j+9+i].strip())[6]))
            C_Y_p=np.average(C_Y_ps)
            C_n_ps=np.array([])
            for i in range(6):
                C_n_ps=np.append(C_n_ps,float(my_split(lines[j+9+i].strip())[7]))
            C_n_p=np.average(C_n_ps)
            C_n_rs=np.array([])
            for i in range(6):
                C_n_rs=np.append(C_n_rs,float(my_split(lines[j+9+i].strip())[8]))
            C_n_r=np.average(C_n_rs)
            C_l_rs=np.array([])
            for i in range(6):
                C_l_rs=np.append(C_l_rs,float(my_split(lines[j+9+i].strip())[3]))
            C_l_r=np.average(C_l_rs)


            C_l_q,C_m_q=np.array(dataline[1:3]).astype(float)
            C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q=np.round(np.array([C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q])*180/np.pi,5)
            #print(C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q,j)
        
        k+=1
        