#input numpy array with altitudes you want to know ISA of (can also be only one altitude) in meters
#export Temperature, pressure, density SI units
class Atmos(object):
    
    def __init__(self):
        self.g0 = 9.80665
        self.rho0 = 1.225
        self.p0 = 101325.
        self.T0 = 273.15        
        self.h_cruise = 20000. #[m]
        self.R = 287            # unit
        self.gamma  = 1.4       # unit
        
    def ISAFunc(self, h):
        import numpy as np
        
        output=np.array([0,0,0])
            
        for alt in h:
            h=alt
            Menu = 2
            #standard values
            g_0 = 9.80665
            R = 287.058
            #lists
            lsthtop =np.array([11000., 20000., 32000., 47000., 51000., 71000., 84852., 100000.])
            lsth = np.array([0., 11000., 20000., 32000., 47000., 51000., 71000., 84852.])
            lsta = np.array([-0.0065, 0, 0.001,0.0028, 0, -0.0028, -0.002, 0.])
            lstT = np.array([ ])
            lstp = np.array([ ])
            lstrho = np.array([ ])
            #sea level values
            pbase = 101325.
            Tbase = 288.15
            rhobase = 1.225
            i = 0
            for i in range(len(lsth)) :
                htop = lsthtop[i]
                hbase = lsth[i]
                a = lsta[i]    
                if lsta[i] == 0 :
                    T1 = Tbase + a*(htop - hbase)
                    p1  = pbase * np.exp(-(g_0/(R*Tbase))*(htop-hbase))
                    rho1 = rhobase * np.exp(-(g_0/(R*Tbase))*(htop-hbase))
                    
                else :
                    T1 = Tbase + a*(htop - hbase)
                    p1 = pbase*(T1/Tbase)**-(g_0/(a*R))
                    rho1 = p1/(R*T1)
    
                lstp=np.append(lstp,pbase)
                lstT=np.append(lstT,Tbase)
                lstrho=np.append(lstrho,rhobase)
                
                
                Tbase = T1
                pbase = p1
                rhobase = rho1
    
            hbase = 0
            nrh = 0
            
            #print (lstp)
            #print (lstT)
            #print (lstrho)
            #actual calculations        
            if Menu == 2 :
                if h >= 0 :
                    for n in lsthtop:
                        if h < n:
                            break
                    nrh= np.where(lsthtop==n)[0][0]
                    hbase = lsth[nrh]
                    Tbase= lstT[nrh]
                    a = lsta[nrh]                     
                    if a == 0 :                     
                        T = lstT[nrh]
                        p = lstp[nrh]* np.exp(-(g_0/(R*Tbase))*(h-hbase))
                        rho = p/(R*T)
    
                    else :
                        T = lstT[nrh] + a*(h - hbase)
    
                        p = lstp[nrh]*(T/lstT[nrh])**-(g_0/(a*R))
    
                        rho = p/(R*T)
            output= np.array([T,p,rho])
            
        return output


