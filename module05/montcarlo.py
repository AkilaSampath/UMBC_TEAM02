import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

w0 = 0.8; # single-scattering albedo
N = 10000; # number of photons to trace
ns = 100; # max number of scatters per photon #zeta control
E = 0; # initialize detector
Eabs=0
Et=0
#%how far does it go?
#l=-(1/c)*log(1-rand); %total path length Tow C
for i in range(0,N):
 z = 0; # initial position depth
 muz = 0.1; # incident light direction (collimated)
 w = 1; # initial photon weight
 w = 1; # initial photon weight
 theta=(np.pi)/4 #default pi/2
 muz = np.cos(theta); # incident light direction (collimated)
 for j in range(ns):
      zeta=np.random.rand() 
#    s = 1*(np.log(np.random.rand))/c; # geometric path length
      s= -1*np.log(1-zeta)/c
#     s=0.8147
# print(s)
      z = z + muz*s; # move photon
# print(z)
      if (z<0): 
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
         if (zeta<=w0):   
            muz= 2*zeta-1; #scattering angle
 
 #print(muz)
#print(Eabs)
#print(Et)
#print(E)
Ref=E/N;
Abs=Eabs/N;
Transm=Et/N;
print(Ref)
print(Abs)
print(Transm)
 
print(muz)
