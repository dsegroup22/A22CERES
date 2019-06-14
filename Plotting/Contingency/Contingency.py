# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:02:45 2019

@author: Nout
"""
import matplotlib.pyplot as plt
import numpy as np
def TPMplotter(Plot):
    MTOWact = [62500,22380,41655]
    MTOWcur = [75000,25737,47589]
    MTOWspef = [75000,63250,60500]  
    MTOWtar = [62500,55000,55000]
    
    OEWact = [26600,9064,20761]
    OEWcur = [31250,10423,25882]
    OEWspef =  [31250,31625,30250]
    OEWtar = [26600,27500,27500]
    
    phase = ['Preliminary design','Class I design', 'Detailed design']
    x_values = np.arange(1, len(phase) + 1, 1)
    
    if Plot ==1:
        plt.plot(x_values,MTOWact,x_values,MTOWcur,x_values,MTOWspef,x_values,MTOWtar)
        plt.xticks(x_values, phase)
        plt.ylabel('MTOW [kg]')
        plt.legend(['actual','current','specification','target'])
        plt.show()
        
    if Plot ==2:
        plt.plot(x_values,OEWact,x_values,OEWcur,x_values,OEWspef,x_values,OEWtar)
        plt.xticks(x_values, phase)
        plt.ylabel('OEW [kg]')
        plt.legend(['actual','current','specification','target'])
        plt.show()
    