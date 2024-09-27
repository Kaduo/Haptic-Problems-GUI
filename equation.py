import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, log
from itertools import product

# F_N = 1 # Force normale du doigt
# mu_b_b = 0.4 # Coefficient de frottement bois/bois
# mu_d_v = 1.2 # Coefficient de frottement doigt/verre
g = 9.8 # Constante gravitationnelle
# tau = 1.3 # micromètres

# K = mu_b_b * g / (mu_d_v * F_N)

# unit_mass = 0.0014

def amplitude(m, tau, mu_b_b, mu_d_v, F_N):
    return sqrt(-2*tau**2*log(m*mu_b_b * g / (mu_d_v * F_N)))



# for l in range(1, 10):
#     print(f"longueur : {l}, amplitude : {amplitude(l*unit_mass)}")


# m = np.linspace(unit_mass, 10*unit_mass)
# for t in np.linspace(0.5, 2, 10):
#     plt.plot(m, amplitude(m, t))
# plt.show()

n = 10

tau_range = np.linspace(0.8, 2, n)
F_N_range = np.linspace(0.5, 1.5, n)
mu_b_b_range = np.linspace(0.2, 1.5, n)
mu_d_v_range = np.linspace(0.8, 1.5, n)
unit_mass_range = np.linspace(0.001, 0.002, n)

amplitude_range = [0.1, 2]

best_params = []
best_min_amp = None
best_max_amp = None
min = np.inf

for tau, F_N, mu_b_b, mu_d_v, unit_mass in product(tau_range, F_N_range, mu_b_b_range, mu_d_v_range, unit_mass_range):
    candidate = (amplitude(unit_mass, tau, mu_b_b, mu_d_v, F_N) - 0.1)**2 # + (amplitude(unit_mass*10, tau, mu_b_b, g, mu_d_v, F_N) - 2)**2
    if candidate < min:
        min = candidate
        best_params = [tau, F_N, mu_b_b, mu_d_v, unit_mass]
        best_min_amp = amplitude(unit_mass, tau, mu_b_b, mu_d_v, F_N)
        best_max_amp = amplitude(unit_mass*10, tau, mu_b_b, mu_d_v, F_N)

print(f"{min}, {best_params}, {best_min_amp}, {best_max_amp}")

best_tau = best_params[0]
best_F_N = best_params[1]
best_mu_b_b = best_params[2]
best_mu_d_v = best_params[3]
best_unit_mass = best_params[4]

def lateral_force(m, tau, F_N, mu_b_b, mu_d_v):
    return mu_d_v * np.exp(-amplitude(m, tau, mu_b_b, mu_d_v, F_N))*F_N


masses = np.linspace(best_unit_mass, 10*best_unit_mass)

plt.plot(masses, lateral_force(masses, best_tau, best_F_N, best_mu_b_b, best_mu_d_v))
plt.show()