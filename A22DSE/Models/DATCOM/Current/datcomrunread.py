# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:58:22 2019

@author: menno
"""
import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])
print(os.getcwd())
#from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Models.DATCOM.Current.datcomconverter import PrintDatcom


import os

import numpy as np

import pyautogui
import time



def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def my_split(s):
    seps=['              ','             ','            ','            ','          ','         ','        ','       ','      ','     ','    ','   ','  ',' ']
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

def GetDerivatives(speed): #'fast' or 'slow' speed input
    
    PrintDatcom()
    os.chdir(Path(__file__).parents[0])
    os.startfile("datcom.exe",'open')
    time.sleep(0.1)

    #pyautogui.click(500, 500)
    pyautogui.typewrite('ceres.dat\n')
    
    
    #autopy.key.type_string('ceres.dat\n')
    #pynput.keyboard.Key.enter
    #keyboard.write('ceres.dat\n')
    
    os.chdir(Path(__file__).parents[4])
    
    file=open('A22DSE\Models\DATCOM\Current\datcom.out','r')
    
    lines=file.readlines()
    file.close()
    k=0
    for j in range(len(lines)):
        line=lines[j]
        if 'CONDITIONS' in line:
            if k==0 or k==2:
                dataline=my_split(lines[j+8].strip(),)
                C_Ds=np.array([])
                C_Ls=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[1].isalpha():
                        if not my_split(lines[j+8+i].strip())[2].isalpha():
                            C_Ds=np.append(C_Ds,float(my_split(lines[j+8+i].strip())[1]))
                            C_Ls=np.append(C_Ls,float(my_split(lines[j+8+i].strip())[2]))

                
            
                C_D_0=np.interp(0,C_Ls,C_Ds)
                C_L_as=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[7].isalpha():
                        C_L_as=np.append(C_L_as,float(my_split(lines[j+8+i].strip())[7]))
                C_L_a=np.average(C_L_as)
                C_l_bs=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[-1].isalpha():
                        C_l_bs=np.append(C_l_bs,float(my_split(lines[j+8+i].strip())[-1]))
                C_l_b=np.average(C_l_bs)
                C_m_as=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[-4].isalpha():
                        C_m_as=np.append(C_m_as,float(my_split(lines[j+8+i].strip())[-4]))
                C_m_a=np.average(C_m_as)            
                       
                C_Y_b,C_n_b=np.array(dataline[9:11]).astype(float)
#                w=np.array(['C_D_0','C_L_a','C_l_b','C_m_a','C_Y_b','C_n_b'])
#                x=C_D_0,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b=np.round(np.array([C_D_0,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b])*180/np.pi,5)
                #print(C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,j)
            if k==1 or k==3:
                dataline=my_split(lines[j+9].strip(),)
                C_L_adots=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[3].isalpha():
                        C_L_adots=np.append(C_L_adots,float(my_split(lines[j+9+i].strip())[3]))
                C_L_adot=np.average(C_L_adots)
                C_m_adots=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[4].isalpha():
                        C_m_adots=np.append(C_m_adots,float(my_split(lines[j+9+i].strip())[4]))
                C_m_adot=np.average(C_m_adots)
                C_l_ps=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[5].isalpha():
                        C_l_ps=np.append(C_l_ps,float(my_split(lines[j+9+i].strip())[5]))
                C_l_p=np.average(C_l_ps)
                C_Y_ps=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[6].isalpha():
                        C_Y_ps=np.append(C_Y_ps,float(my_split(lines[j+9+i].strip())[6]))
                C_Y_p=np.average(C_Y_ps)
                C_n_ps=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[7].isalpha():
                        C_n_ps=np.append(C_n_ps,float(my_split(lines[j+9+i].strip())[7]))
                C_n_p=np.average(C_n_ps)
                C_n_rs=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[8].isalpha():
                        C_n_rs=np.append(C_n_rs,float(my_split(lines[j+9+i].strip())[8]))
                C_n_r=np.average(C_n_rs)
                C_l_rs=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[9].isalpha():
                        C_l_rs=np.append(C_l_rs,float(my_split(lines[j+9+i].strip())[9]))
                C_l_r=np.average(C_l_rs)
    
    
                C_l_q,C_m_q=np.array(dataline[1:3]).astype(float)
#                y=np.array(['C_L_adot','C_m_adot', 'C_l_p','C_Y_p','C_n_p','C_n_r','C_l_r','C_l_q','C_m_q'])
#                z=C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q=np.round(np.array([C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q])*180/np.pi,5)
                #print(C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q,j)

            k+=1
            if speed == 'slow' and k==2:
                break
    return C_D_0,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q

#q=np.vstack((np.hstack((w,y)),np.hstack((x,z))))
#file=open('A22DSE\Models\DATCOM\Current\derivatives.csv','w')
#file.write('DihedralW,'+str(DHDADI_WG)+'\n')
#file.write('Dihedralht,'+str(DHDADI_HT)+'\n')
#for line in q.transpose():
#    file.write(str(line[0])+','+line[1]+'\n')
#file.close()