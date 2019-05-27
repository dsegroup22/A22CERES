import sys
sys.path.append('../../')

from A22DSE.Models.POPS.Current.payloadcalculations import *
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, ISA_model

import numpy as np
import matplotlib.pyplot as plt

M_cruise_org = Conv.ParAnFP.M_cruise
Ms=np.linspace(0.3,3,50)
As=np.array([])

for M in Ms:
    Conv.ParAnFP.M_cruise = M
    As=np.append(As,InletArea(Conv,ISA_model))


plt.title('Payload Combustor Inlet Area',fontsize=16)
plt.plot(Ms,As)
plt.plot([M_cruise_org,M_cruise_org],[min(As),max(As)],'k--',label='Current Design Point')
plt.xlabel('Cruise Mach Number [-]',fontsize=12)
plt.ylabel('Required Inlet Area [$m^2$]',fontsize=12)
plt.legend(fontsize=12)
plt.tick_params(axis='both',labelsize=12)
plt.show()
    
