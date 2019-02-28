
# coding: utf-8

# In[150]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import reshape
def MC_rad_transfer(minz,maxz,stepz,w0,theta):
    #w0 = 0.8; # single-scattering albedo
    N = 1; # number of photons to trace
    ns = 1; # max number of scatters per photon #zeta control
    E = np.zeros(N*maxz); # initialize detector
    Eabs=np.zeros(N*maxz)
    Et=np.zeros(N*maxz)
#minz=0.1
#maxz=3
#stepz=1
#%how far does it go?
#l=-(1/c)*log(1-rand); %total path length Tow C
    for i in range(0,N):
        #z = np.arange(0.1,3,1) #initial position of the photon
        z = np.arange(minz,maxz,stepz)
        for k in range (0, maxz):
    #z = 0.1; # initial position depth
          w = 1; # initial photon weight
          #theta=(np.pi)/4 #default pi/2
          muz = np.cos(theta); # incident light direction (collimated)
          for j in range(ns):
            zeta=np.random.rand() 
#    s = 1*(np.log(np.random.rand))/c; # geometric path length
            s= -1*np.log(1-zeta)
#     s=0.8147
# print(s)
            z = z + muz*s; # move photon
# print(z)
            if np.any(z<0): 
              E+=1; 
              break #count photons leaving out top
            w=w*w0; # absorb fraction of photon packet   
            muz= 2*zeta-1; # isotopic scattering
            if np.any(z>s): 
              Et+=1; #photons transmitted 
              break
            if (np.any(z>0) and np.any(z<s)): 
#         w=w*w0
              if (zeta>w0):
                Eabs+=1
                break
              if np.any(zeta<=w0):   
                muz= 2*zeta-1; #scattering angle
 
 #print(muz)
#print(Eabs)
#print(Et)
#print(E)
        Ref=E/N;
        Abs=Eabs/N;
        Transm=Et/N;
      #print((Ref))
      #print((Abs))
        Ref=Ref
 #       Abs=Abs
 #       Transm=Transm
    
 #       return Ref,Abs,Transm
        return Ref


# In[109]:


MC = MC_rad_transfer(0,25,1,1,np.pi/4)# [minz,maxz,stepz,N,ns,w,theta]
print(MC)


# In[141]:


def gamma(wl,c0=0.04,k=0.2):
    alpha = [c0*tau*np.exp(-k*tau)for l in wl]
    return alpha


# In[142]:


import numpy as np
import pandas as pd
import scipy
from math import pi
tau =np.arange(minz,maxz,stepz)
print(tau)


# In[149]:


import numpy as np
import pandas as pd
import scipy
from math import pi
minz=0.1
maxz=50
stepz=1

#tau =np.arange(minz,maxz,stepz)
tau =np.arange(minz,maxz,stepz)
#print(tau)
RT=np.asarray(gamma(tau,c0=0.04,k=0.2))
print((RT))
VT=np.asarray(MC_rad_transfer(minz,maxz,stepz,1,np.pi/4))
#print(VT)
#OT=RT*VT
OT=RT.dot(VT)
#print(OT)
#numerical value
dy1 = np.trapz(OT,tau)
#print(dy1)

