# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:14:46 2019

@author: menno
"""
import os
import time
import pyautogui
os.startfile("datcom.exe")
time.sleep(1)
pyautogui.write('ceres.dat\n')

