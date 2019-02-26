#!/usr/bin/env python3

import numpy as np
from math import *

def scatter(tau_c, omega, theta_0, n_total, return_array=False):
    """
    This program uses a 1 dimensional Monte-Carlo method to simulate photon scattering 
    through a cloud.

    The inputs, all required, are as follows

    tau_c, the cloud optical thickness

    omega, the cloud single-scattering albedo

    theta_0, the solar zenith angle

    n_total, the total number of incoming photons

    - - - - - - 

    The optional parameters are as follows:

    return_array (= False), this returns the results as arrays n_ref[i], n_abs[i], n_tra[i]. 
                            the ith entry contains the state after i photons have been processed.
                            this way, information can be obtained about the success of the Monte-
                            Carlo method. 

    - - - - - - 

    The outputs are returned as a tuple. These are as follows:

    n_ref, the number of photons reflected

    n_abs, the number of photons absorbed

    n_tra, the number of photons transmitted

    From these, the reflectance, absorbance, and transmittance can be easily calculated.
    """


    #Set up counters
    if(return_array):
        n_ref = [0]
        n_abs = [0]
        n_tra = [0]
    else:
        n_ref = 0
        n_abs = 0
        n_tra = 0

    #Non command line vars
    block_size = 1

    #Debugging
    verbose = False

    #Main loop
    for i in range(n_total):
        #Set up variables for this photon
        tau = 0.0
        theta = theta_0
        absorbed = False

        if(verbose):
            print("New photon")

        #Move Photon 
        # first move done before checking for being outside:
        # for very thin clouds or weird angles this is important
        zeta = np.random.random(block_size)
        L = -log(1 - zeta)
        tau += L*cos(theta)

        while(0.0 < tau and tau < tau_c and not absorbed):

            #If here, then inside
            zeta = np.random.random(block_size)
            absorbed = (zeta > omega)
        
            #Move Photon (assume scattered)
            #Direction
            zeta = np.random.random(block_size)
            mu = 2.0*zeta - 1.0
            theta = acos(mu)

            #Move
            zeta = np.random.random(block_size)
            L = -log(1 - zeta)
            tau += L*cos(theta)

            if(verbose):
                if(not absorbed):
                    print(tau)

        #Note: due to loop order, there is a final movement regardless of absorption.
        #Thus, absorbed *must* be checked first. Sometimes the photon may be absorbed and
        #move outside the cloud in the same loop. Don't rearrange!
        
        if(return_array):
            n_abs += [n_abs[-1]]
            n_ref += [n_ref[-1]]
            n_tra += [n_tra[-1]]
            if(absorbed): #Keep first
                n_abs[-1] += 1
            elif(tau <= 0.0):
                n_ref[-1] += 1
            elif(tau >= tau_c):
                n_tra[-1] += 1
            else:
                print("error--should be one of those three")
        else:
            if(absorbed): #Keep first
                n_abs += 1
            elif(tau <= 0.0):
                n_ref += 1
            elif(tau >= tau_c):
                n_tra += 1
            else:
                print("error--should be one of those three")

        if(verbose):
            if(absorbed): #Keep first
                print("abs")
            elif(tau <= 0.0):
                print("ref")
            elif(tau >= tau_c):
                print("tra")
            else:
                print("error--should be one of those three")
    
    return (n_ref, n_abs, n_tra)

#Testing
if (__name__ == "__main__"):

    #Parameters
    tau_c = 3.0
    omega = 0.9
    theta_0 = pi/4
    n_total = 10000
    return_array = True

    #Run code
    (n_ref, n_abs, n_tra) = scatter(tau_c, omega, theta_0, n_total, return_array = return_array)

    #Friendly output either way
    if(return_array):
        for i in range(n_total+1):
            print(" ".join([str(s) for s in [i, n_ref[i], n_abs[i], n_tra[i]]]))
    else:
        print("ref:", n_ref)
        print("abs:", n_abs)
        print("tra:", n_tra)
