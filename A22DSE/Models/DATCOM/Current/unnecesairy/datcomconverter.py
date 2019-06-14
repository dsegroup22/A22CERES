# -*- coding: utf-8 -*-9
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""

import os
import pyautogui
import time
from pathlib import Path
#os.chdir(Path(__file__).parents[4])
print (os.getcwd())
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Models.DATCOM.Current.datcomconvertermatlab import PrintMatlab

anfp=Conv.ParAnFP
Layout=Conv.ParLayoutConfig
Conversion=Conv.ConversTool
Struc=Conv.ParStruc

def printer(a):
    return print(lines[a]), print(len(lines[a]))
def PrintDatcom():
    
    import numpy as np
    XW,ZW,ALIW,XH,ALIH,XV,ZV,NX,X,ZU,ZL,R,S,h,P,CHRDTP_WG,SSPN_WG,SSPNE_WG,\
CHRDR_WG,SAVSI_WG,CHSTAT_WG,TWISTA_WG,DHDADI_WG,TC_WG\
,CHRDTP_HT,SSPN_HT,SSPNE_HT,CHRDR_HT,SAVSI_HT,CHSTAT_HT\
,TWISTA_HT,DHDADI_HT,CHRDTP_VT,SSPN_VT,SSPNE_VT,CHRDR_VT,SAVSI_VT,CHSTAT_VT,ZH=PrintMatlab()

    file=open('A22DSE\Models\DATCOM\Current\CERESorig.dat','r')
    
    lines=file.readlines()
    
    
    #printer(4)
    a=lines[4].split(',')[0]+','
    b=lines[4].split(',')[1].split('=')[0]+'='+str(round(float(Struc.MTOW/Conversion.lbs2kg),1))+','
    c=lines[4].split(',')[2]
    lines[4]=a+b+c
    #printer(4)
    
    
    #printer(5)
    a=lines[5].split(',')[0].split('=')[0]+'='+str(round(float(anfp.S/Conversion.ft2m**2),1))+','
    b=lines[5].split(',')[1].split('=')[0]+'='+str(round(float(anfp.MAC/Conversion.ft2m),1))+','
    c=lines[5].split(',')[2].split('=')[0]+'='+str(2*SSPN_WG)+'$ \n'
    lines[5]=a+b+c
    #printer(5)
    
    
    #printer(6)
    a=lines[6].split(',')[0].split('=')[0]+'='+str(round(float(np.average(Layout.x_cg)/Conversion.ft2m),1))+','
    b=lines[6].split(',')[1].split('=')[0]+'='+str(round(float((Layout.z_cg_over_h_fus-0.5)*Layout.h_fuselage/Conversion.ft2m*2),1))+','
    c=lines[6].split(',')[2].split('=')[0]+'='+str(XW)+','
    d=lines[6].split(',')[3].split('=')[0]+'='+str(ZW)+','
    e=lines[6].split(',')[4]+','
    f=lines[6].split(',')[5].split('=')[0]+'='+str(XH)+','
    g=lines[6].split(',')[6]
    lines[6]=a+b+c+d+e+f+g
    #printer(6)
    
    #printer(7)
    a=lines[7].split(',')[0].split('=')[0]+'='+str(ZH)+','
    b=lines[7].split(',')[1].split('=')[0]+'='+str(ALIH)+','
    c=lines[7].split(',')[2].split('=')[0]+'='+str(XV)+','
    d=lines[7].split(',')[3].split('=')[0]+'='+str(ZV)+','
    e=lines[7].split(',')[4]
    lines[7]=a+b+c+d+e
    #printer(7)
    
    #printer(8)
    a=lines[8].split(',')[0].split('=')[0]+'='+str(NX)+','
    b=lines[8].split(',')[1]+','
    c=lines[8].split(',')[2]
    lines[8]=a+b+c
    #printer(8)
    
    
    a='  X='
    b=np.array2string(X,separator=',').replace(' ','').replace('[','').replace(']','')
    c=', \n'
    lines[9]=a+b+c
    
    
    a='  ZU='
    b=np.array2string(ZU,separator=',').replace(' ','').replace('[','').replace(']','')
    c=', \n'
    lines[10]=a+b+c
    
    a='  ZL='
    b=np.array2string(ZL,separator=',').replace(' ','').replace('[','').replace(']','')
    c=', \n'
    lines[11]=a+b+c
    
    a='  S='
    b=np.array2string(S,separator=',').replace(' ','').replace('[','').replace(']','')
    c=', \n'
    lines[12]=a+b+c
    
    a='  P='
    b=np.array2string(P,separator=',').replace(' ','').replace('[','').replace(']','')
    c=', \n'
    lines[13]=a+b+c
    
    a='  R='
    b=np.array2string(R,separator=',').replace(' ','').replace('[','').replace(']','')
    c='$ \n'
    lines[14]=a+b+c
    
    #printer(16)
    a=lines[16].split(',')[0].split('=')[0]+'='+str(CHRDR_WG)+','
    b=lines[16].split(',')[1].split('=')[0]+'='+str(CHRDTP_WG)+','
    c=lines[16].split(',')[2].split('=')[0]+'='+str(SSPN_WG)+','
    d=lines[16].split(',')[3].split('=')[0]+'='+str(SSPNE_WG)+',\n'
    lines[16]=a+b+c+d
    #printer(16)
    
    #printer(17)
    a=lines[17].split(',')[0].split('=')[0]+'='+str(SAVSI_WG)+','
    b=lines[17].split(',')[1].split('=')[0]+'='+str(CHSTAT_WG)+','
    c=lines[17].split(',')[2].split('=')[0]+'='+str(TWISTA_WG)+','
    d=lines[17].split(',')[3].split('=')[0]+'='+str(DHDADI_WG)+','
    e=lines[17].split(',')[4]
    lines[17]=a+b+c+d+e
    #printer(17)
    
    #printer(19)
    a=lines[19].split(',')[0].split('=')[0]+'='+str(CHRDR_HT)+','
    b=lines[19].split(',')[1].split('=')[0]+'='+str(CHRDTP_HT)+','
    c=lines[19].split(',')[2].split('=')[0]+'='+str(SSPN_HT)+','
    d=lines[19].split(',')[3].split('=')[0]+'='+str(SSPNE_HT)+',\n'
    lines[19]=a+b+c+d
    #printer(19)
    
    
    
    #printer(20)
    a=lines[20].split(',')[0].split('=')[0]+'='+str(SAVSI_HT)+','
    b=lines[20].split(',')[1].split('=')[0]+'='+str(CHSTAT_HT)+','
    c=lines[20].split(',')[2].split('=')[0]+'='+str(TWISTA_HT)+','
    d=lines[20].split(',')[3].split('=')[0]+'='+str(DHDADI_HT)+','
    e=lines[20].split(',')[4]
    lines[20]=a+b+c+d+e
    #printer(20)
    
    
    
    #printer(22)
    a=lines[22].split(',')[0].split('=')[0]+'='+str(CHRDR_VT)+','
    b=lines[22].split(',')[1].split('=')[0]+'='+str(CHRDTP_VT)+','
    c=lines[22].split(',')[2].split('=')[0]+'='+str(SSPN_VT)+','
    d=lines[22].split(',')[3].split('=')[0]+'='+str(SSPNE_VT)+',\n'
    lines[22]=a+b+c+d
    #printer(22)
    
    
    
    #printer(23)
    a=lines[23].split(',')[0].split('=')[0]+'='+str(SAVSI_VT)+','
    b=lines[23].split(',')[1].split('=')[0]+'='+str(CHSTAT_VT)+','
    c=lines[23].split(',')[2]
    lines[23]=a+b+c
    #printer(23)
    
    file.close()
    
    file=open('A22DSE\Models\DATCOM\Current\Airfoiltools.txt','r')
    
    alines=file.readlines()
    
    file.close()
    
    import numpy as np
    
    Xcs=np.array([0,0.002,0.005,0.01,0.02,0.03,0.04])
    for i in range(24):
        Xcs=np.append(Xcs,Xcs[-1]+0.04)
    upper=alines[3:10]+alines[13:106:4]
    lower=alines[107:114]+alines[117::4]
    
    
    uppers=np.array([])
    for line in upper:
        uppers=np.append(uppers,float(line.split(' ')[-1].replace('\n','')))
    
    
    lowers=np.array([])
    for line in lower:
        lowers=np.append(lowers,float(line.split(' ')[-1].replace('\n','')))
    a=' $WGSCHR TYPEIN=1.0, NPTS='+str(float(len(Xcs)))+',\n'
    b=' XCORD= 0.0, '+np.array2string(Xcs[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
    c=' YUPPER= 0.0, '+np.array2string(uppers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
    d=' YLOWER= 0.0, '+np.array2string(lowers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+'$\n'
    liness=[a,b,c,d]
    linesss=lines[:15]+liness+lines[16:]
    file=open('A22DSE\Models\DATCOM\Current\CERES.dat','w')
    for line in linesss:
        file.write(line)
    file.close()
    
    

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