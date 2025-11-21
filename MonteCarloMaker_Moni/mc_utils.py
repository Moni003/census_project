# mc_utils.py
import numpy as np
from scipy.integrate import solve_ivp

def nbody_accel(r, mu_central, perturbers):
    """
    Calcul de l'accélération multi-corps.
    
    r : position actuelle du corps (np.array 3D)
    mu_central : paramètre gravitationnel du corps central
    perturbers : liste de tuples (r_perturber, mu_perturber)
    """
    # Accélération centrale
    acc = -mu_central * r / np.linalg.norm(r)**3
    
    # Accélérations des perturbateurs
    for r_p, mu_p in perturbers:
        diff = r_p - r
        acc += mu_p * diff / np.linalg.norm(diff)**3
    
    return acc

def propagate(r0, v0, tof_seconds, mu_central, perturbers):
    """
    Propagation N-body simple par integration temporelle.
    
    r0 : position initiale (m)
    v0 : vitesse initiale (m/s)
    tof_seconds : durée du transfert (s)
    mu_central : paramètre gravitationnel du corps central
    perturbers : liste de tuples (r_perturber, mu_perturber)
    
    Retourne l'état final [x,y,z,vx,vy,vz]
    """
    def ode(t, y):
        r = y[:3]
        v = y[3:]
        a = nbody_accel(r, mu_central, perturbers)
        return np.hstack((v, a))
    
    y0 = np.hstack((r0, v0))
    sol = solve_ivp(ode, [0, tof_seconds], y0, rtol=1e-8, atol=1e-8)
    return sol.y[:, -1]

def score_final_state(state_f, target):
    """
    Calcul du score d'une trajectoire.
    Ici : distance euclidienne à la cible.
    
    state_f : état final [x,y,z,vx,vy,vz]
    target : position cible [x,y,z]
    """
    rf = state_f[:3]
    return np.linalg.norm(rf - target)

def write_docks_file(filename, t0_str, r0, v0):
    """
    Écriture d'un fichier DOCKS simple.
    t0_str : date de départ
    r0 : position initiale [m]
    v0 : vitesse initiale [m/s]
    """
    r_km = r0 / 1000.0
    v_kms = v0 / 1000.0
    line = f"{t0_str}\t" + "\t".join(f"{x:.15e}" for x in r_km) + "\t" + "\t".join(f"{x:.15e}" for x in v_kms)
    with open(filename, "w") as f:
        f.write(line)
    print(f"✅ Fichier DOCKS généré : {filename}")
