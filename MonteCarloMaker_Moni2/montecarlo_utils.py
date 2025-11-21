# montecarlo_utils.py
import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.twobody import Orbit




def generate_random_orbital_elements(a_range, e_range, i_range, raan_range=(0,360), argp_range=(0,360), nu_range=(0,360), distribution_a="uniform", rng=None):
    """Génère un jeu aléatoire d'éléments orbitaux.
    - a_range en mètres
    - e_range dimensionless
    - i_range en degrés
    Retourne: a (m), e, i (deg), RAAN (deg), argp (deg), nu (deg)
    """
    if rng is None:
        rng = np.random

    if distribution_a == "log":
        a = 10**rng.uniform(np.log10(a_range[0]), np.log10(a_range[1]))

    else:
        a = rng.uniform(a_range[0], a_range[1])
    e = rng.uniform(e_range[0], e_range[1])
    i = rng.uniform(i_range[0], i_range[1])
    raan = rng.uniform(raan_range[0], raan_range[1])
    argp = rng.uniform(argp_range[0], argp_range[1])
    nu = rng.uniform(nu_range[0], nu_range[1])
    return a, e, i, raan, argp, nu




def orbital_elements_to_rv(attractor, t0_str, a, e, inc, Omega, omega, nu):
    """Convertit éléments classiques en r (m) et v (m/s) via poliastro.

    - attractor : classe poliastro.bodies (p.ex. poliastro.bodies.Sun)
    - t0_str : ISO time string
    """
    a_q = a * u.m
    ecc = e * u.one
    inc_q = inc * u.deg
    raan_q = Omega * u.deg
    argp_q = omega * u.deg
    nu_q = nu * u.deg
    epoch = Time(t0_str, scale="tdb")
    orb = Orbit.from_classical(attractor, a_q, ecc, inc_q, raan_q, argp_q, nu_q, epoch)
    return orb.r.to_value(u.m), orb.v.to_value(u.m / u.s)




def write_docks_file(filename, date_str, r_m, v_ms):
    """Écrit un fichier de conditions initiales compatible DOCKS.

    Format attendu : t0\trx\try\trz\tvx\tvy\tvz (r en km, v en km/s)
    """
    r_km = r_m / 1000.0
    v_kms = v_ms / 1000.0
    line = f"{date_str}\t" + "\t".join(f"{x:.15e}" for x in r_km) + "\t" + "\t".join(f"{x:.15e}" for x in v_kms)

    with open(filename, "w") as f:
        f.write(line)