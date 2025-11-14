# montecarlo_utils.py
import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.twobody import Orbit

def generate_random_orbital_elements(a_range, e_range, i_range):
    """
    Génère un ensemble aléatoire de paramètres orbitaux (Monte Carlo)
    """
    a = np.random.uniform(a_range[0], a_range[1])
    e = np.random.uniform(e_range[0], e_range[1])
    i = np.random.uniform(i_range[0], i_range[1])
    return a, e, i

def orbital_elements_to_r(attractor, a, e, inc, Omega=0, omega=0, nu=0):
    """
    Convertit les éléments orbitaux en vecteur position 3D (m)
    """
    a_q = a * u.m
    ecc = e * u.one
    inc_q = inc * u.deg
    raan_q = Omega * u.deg
    argp_q = omega * u.deg
    nu_q = nu * u.deg
    epoch = Time("2025-01-01 12:00:00", scale="tdb")
    orb = Orbit.from_classical(attractor, a_q, ecc, inc_q, raan_q, argp_q, nu_q, epoch)
    return orb.r.to_value(u.m)

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
