#!/usr/bin/env python3

import numpy as np
from math import *

def scatter(tau_c, omega, theta_0, n_total, return_array=False, track_max_depth=False):
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

    if(track_max_depth):
        max_depths = []

    #Non command line vars
    block_size = 1

    #Debugging
    verbose = False

    #Seed randomizer
    np.random.seed()

    #Main loop
    for i in range(n_total):
        #Set up variables for this photon
        tau = 0.0
        theta = theta_0
        absorbed = False
        max_depth = 0.0

        if(verbose):
            print("New photon")

        #Move Photon 
        # first move done before checking for being outside:
        # for very thin clouds or weird angles this is important
        zeta = np.random.random(block_size)
        L = -log(1 - zeta)
        tau += L*cos(theta)
        if(track_max_depth and max_depth < tau):
            max_depth = tau

        while(0.0 < tau and tau < tau_c and not absorbed):

            #Check for max_depth
            if(track_max_depth and max_depth < tau):
                max_depth = tau

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

        #Check for max_depth one last time if not absorbed 
        if(track_max_depth and max_depth < tau and not absorbed):
            max_depth = tau

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
                if(track_max_depth):
                    max_depths += [max_depth]
            elif(tau >= tau_c):
                n_tra[-1] += 1
            else:
                print("error--should be one of those three")
        else:
            if(absorbed): #Keep first
                n_abs += 1
            elif(tau <= 0.0):
                n_ref += 1
                if(track_max_depth):
                    max_depths += [max_depth]
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
    
    if(not track_max_depth):
        return (n_ref, n_abs, n_tra)
    else:
        return (n_ref, n_abs, n_tra, max_depths)

#Testing
if (__name__ == "__main__"):

    #Parameters
    tau_c = 3.0
    omega = 0.9
    theta_0 = pi/4
    #n_total = 10000
    n_total = 10
    return_array = True
    track_max_depth = True

    ##Run code
    #A = scatter(tau_c, omega, theta_0, n_total, return_array = return_array, track_max_depth=track_max_depth)

    ##Unpack
    #if(not track_max_depth):
    #    (n_ref, n_abs, n_tra) = A
    #else:
    #    (n_ref, n_abs, n_tra, max_depths) = A

    ##Friendly output either way
    #if(return_array):
    #    for i in range(n_total):
    #        print(" ".join([str(s) for s in [i, n_ref[i], n_abs[i], n_tra[i]]]))
    #else:
    #    print("ref:", n_ref)
    #    print("abs:", n_abs)
    #    print("tra:", n_tra)

    #if(track_max_depth):
    #    print("max depth of reflected", max(max_depths))


    #Question 1: Relationship of Reflectance to tau_c and omega
    print(" - - - Question 1 using theta_0 of pi/4, n_total = 1000 - - - ")
    omega_vals = [1.0, 0.9, 0.8]
    #tau_c_vals = [0.1*x for x in range(1,201)] #For final run use this
    tau_c_vals = [2.0*x for x in range(1,11)]
    theta_0 = pi/4
    n_total = 1000
    reflectance = [[0.0 for _ in range(1,201)] for __ in range(3)]
    for i in range(len(omega_vals)):
        omega = omega_vals[i]
        for j in range(len(tau_c_vals)):
            tau_c = tau_c_vals[j]
            print("Checking omega =", omega, "tau_c =", tau_c)
            (n_ref, n_abs, n_tra) = scatter(tau_c, omega, theta_0, n_total)
            reflectance[i][j] = n_ref/n_total

    outputFile = open("question_1.dat", "w")
    for i in range(len(omega_vals)):
        outputFile.write("".join([str(s) for s in ["Omega=", str(omega_vals[i]), "\n"]]))
        for j in range(len(tau_c_vals)):
            outputFile.write(" ".join([str(s) for s in [tau_c_vals[j], reflectance[i][j], "\n"]]))
        outputFile.write("\n\n")

    outputFile.close()



    #Question 2: Max Depth of Reflected Photons
    print(" - - - Question 2 - - - ")
    tau_c = 10.0
    theta_0 = 0.0
    n_total = 10000
    for omega in [1.0, 0.96, 0.92, 0.88]:
        print("Checking omega =", omega)
        outputFile = open("question_2_omega_"+str(omega)+".dat", "w")
        (n_ref, n_abs, n_tra, max_depths) = scatter(tau_c, omega, theta_0, n_total, track_max_depth=True)

        #Write output
        for depth in max_depths:
            outputFile.write(str(depth))
            outputFile.write("\n")
        outputFile.close()
        
    #Question 3:
    print(" - - - Question 3 - - - ")
