import numpy as np
from datetime import datetime
from astropy import units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro.iod.izzo import lambert

def orbital_elements_to_r_poliastro(a_m, e, inc_deg, Omega_deg=0, omega_deg=0, nu_deg=0, attractor=None):
    """
    Convertit des éléments orbitaux en position 3D (m) et retourne la position.
    """
    if attractor is None:
        raise ValueError("Un corps central doit être fourni via `attractor`.")

    a = a_m * u.m
    ecc = e * u.one
    inc = inc_deg * u.deg
    raan = Omega_deg * u.deg
    argp = omega_deg * u.deg
    nu = nu_deg * u.deg

    epoch = Time("2000-01-01 12:00:00", scale="tdb")
    orb = Orbit.from_classical(attractor, a, ecc, inc, raan, argp, nu, epoch)
    r_vec = orb.r.to_value(u.m)

    # Eviter positions collinéaires (y=z≈0)
    if np.allclose(r_vec[1:], 0.0, atol=1e-12):
        nu_candidates = [10, 30, 45, 60, 90]
        for nu_try in nu_candidates:
            orb_try = Orbit.from_classical(attractor, a, ecc, inc, raan, argp, nu_try * u.deg, epoch)
            r_try = orb_try.r.to_value(u.m)
            if not np.allclose(r_try[1:], 0.0, atol=1e-12):
                r_vec = r_try
                break

    return r_vec

def solve_lambert(r0, rf, tof_days, mu):
    """
    Résout Lambert et retourne les vecteurs vitesse initiale et finale (m/s)
    """
    r0_q = r0 * u.m
    rf_q = rf * u.m
    tof_q = tof_days * u.day
    lambert_gen = lambert(mu * u.m**3 / u.s**2, r0_q, rf_q, tof_q)
    v0_q, vf_q = next(lambert_gen)
    return v0_q.to(u.m/u.s).value, vf_q.to(u.m/u.s).value

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
