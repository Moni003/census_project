# mc_utils.py
import numpy as np
from scipy.integrate import solve_ivp

def nbody_accel(r, bodies_mu):
    """
    Calcul de l'accélération multi-corps.
    
    r : position actuelle du satellite (np.array 3D)
    bodies_mu : liste de tuples (r_body, mu)
    """
    acc = np.zeros(3)
    for r_body, mu in bodies_mu:
        diff = r - r_body
        acc += -mu * diff / np.linalg.norm(diff)**3
    return acc

def propagate(r0, v0, bodies_mu):
    """
    Propagation multi-corps simplifiée.
    
    r0 : position initiale (m)
    v0 : vitesse initiale (m/s)
    bodies_mu : liste de tuples (r_body, mu)
    
    Retourne l'état final [x,y,z,vx,vy,vz]
    """
    def ode(t, y):
        r = y[:3]
        v = y[3:]
        a = nbody_accel(r, bodies_mu)
        return np.hstack((v, a))
    
    y0 = np.hstack((r0, v0))
    
    # Temps d'intégration arbitraire : on peut prendre une grande valeur pour atteindre t2 mais ça va prendre du temps
    t_final =1e9  # tof ?????????
    sol = solve_ivp(ode, [0, t_final], y0, rtol=1e-8, atol=1e-8)
    
    return sol.y[:, -1]

def f1_cost(r_target, r_final):
    """
    Fonction de coût f1 : norme de la distance finale par rapport à la cible
    """
    return np.linalg.norm(r_target - r_final)

def write_docks_file(filename, t0_str, r0, v0):
    """
    Écriture simple d'un fichier DOCKS.
    """
    r_km = r0 / 1000.0
    v_kms = v0 / 1000.0
    line = f"{t0_str}\t" + "\t".join(f"{x:.15e}" for x in r_km) + "\t" + "\t".join(f"{x:.15e}" for x in v_kms)
    with open(filename, "w") as f:
        f.write(line)
    print(f"✅ Fichier DOCKS généré : {filename}")
