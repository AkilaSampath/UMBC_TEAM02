import scatter as s

"""
This program outputs the reflectivity, absorbance and transmittance so that
we can judge how best to set n_total 
"""

tau_c = 5.0
omega = 0.9
theta_0 = 3.1415/4
n_total = 100000

(n_ref, n_abs, n_tra) = s.scatter(tau_c, omega, theta_0, n_total, return_array=True)

refle = [n_ref[i]/i for i in range(1, n_total)]
absor = [n_abs[i]/i for i in range(1, n_total)]
trans = [n_tra[i]/i for i in range(1, n_total)]

for i in range(len(refle)):
    print(" ".join([str(s) for s in [refle[i], absor[i], trans[i]]]))

