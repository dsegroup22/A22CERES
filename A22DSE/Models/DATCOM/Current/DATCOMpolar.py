# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:55:47 2019

@author: menno
"""
import scipy
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
def polyfitter2(x1,y1):
    
    def func(x, a, c):
        return a+c*x**2

    outlierchecks=5
    coeff,cov=curve_fit(func,x1,y1)
    y=0
    i=0
    step=(max(x1)-min(x1))/2/len(x1)
    x=np.arange(min(x1),max(x1)+step,step)
    y=func(x,coeff[0],coeff[1])


    for j in range(outlierchecks):
        ycheck=func(x1,coeff[0],coeff[1])
        i=0
        e=y1-ycheck
        threshold=3.
        deleters=np.array([])
        #print ('maxzscore=', max(abs(scipy.stats.zscore(e))))
        for i in range(len(e)):
            if abs(scipy.stats.zscore(e)[i])>threshold:
                x1=np.delete(x1,i)
                y1=np.delete(y1,i)
                print ('oulier:',i)
                break
    
    coeff,cov=curve_fit(func,x1,y1)
    y=0
    i=0
    step=(max(x1)-min(x1))/2/len(x1)
    x=np.arange(min(x1),max(x1)+step,step)
    y=func(x,coeff[0],coeff[1])
    #print ('correlation=', np.corrcoef(ycheck,y1)[0,1])
    return x1,y1,x,y,coeff


from pathlib import Path
os.chdir(Path(__file__).parents[4])
from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Models.DATCOM.Current.datcomconvertermatlab import GetDerivatives


C_L,C_D=GetDerivatives(Conv,'polar')
polyfits=polyfitter2(C_L,C_D)
emeas=1/polyfits[4][1]/np.pi/Conv.ParAnFP.A
plt.clf()
plt.figure(figsize=(7,6))
plt.plot(polyfits[1],polyfits[0],'o',label='Data points')
plt.plot(polyfits[3],polyfits[2],label='Polynomial approximation\n$C_{D_{0}}$= '+str(round(polyfits[4][0],4))+' [-], e = '+str(round(emeas,3))+' [-]')
plt.legend(loc='center', fontsize=14)
plt.title('Drag Polar',fontsize=18)
plt.tick_params(labelsize=14)
plt.xlabel(r'$C_D$ [-]',fontsize=14)
plt.ylabel(r'$C_L$ [-]',fontsize=14)
plt.savefig(r'A22DSE\Models\DATCOM\Current\Plots\polar.png')


plt.show()