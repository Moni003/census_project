import numpy as np
from scipy.integrate import solve_ivp
from datetime import datetime
from astropy import units as u

def two_body_equations(t, y, mu):
    """Équations du mouvement à deux corps"""
    r = y[:3]
    v = y[3:]
    r_norm = np.linalg.norm(r)
    a = -mu * r / r_norm**3
    dydt = np.concatenate((v, a))
    return dydt

def single_shooting(r0_guess, v0_guess, rf_target, t_span, mu, tol=1e-3, max_iter=50):
    """
    Méthode de single shooting pour trouver v0 (et r0 si nécessaire) qui atteint rf_target
    r0_guess, v0_guess : estimation initiale
    rf_target : position finale désirée
    t_span : [t0, tf]
    mu : paramètre gravitationnel
    """
    r0 = np.array(r0_guess)
    v0 = np.array(v0_guess)
    
    for i in range(max_iter):
        y0 = np.concatenate((r0, v0))
        sol = solve_ivp(two_body_equations, t_span, y0, args=(mu,), rtol=1e-9, atol=1e-12)
        rf_calc = sol.y[:3, -1]
        error = rf_target - rf_calc
        if np.linalg.norm(error) < tol:
            print(f"Converged in {i+1} iterations.")
            return r0, v0
        # Ajustement simple : gradient approximé par différence finie
        v0 += 0.1 * error / (t_span[1]-t_span[0])
    
    print("Warning: maximum iterations reached, solution may be inaccurate.")
    return r0, v0

def write_docks_file(filename, date_str, r, v):
    """
    Écrit un fichier de conditions initiales compatible DOCKS
    """
    r_km = r / 1000
    v_kms = v / 1000
    line = f"{date_str}\t" + "\t".join(f"{x:.15e}" for x in r_km) + "\t" + "\t".join(f"{x:.15e}" for x in v_kms)
    with open(filename, "w") as f:
        f.write(line)
    print(f"✅ Fichier DOCKS généré : {filename}")

def parse_isot(date_str):
    """Conversion ISO8601 → datetime"""
    return datetime.fromisoformat(date_str)
