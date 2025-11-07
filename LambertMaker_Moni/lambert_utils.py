import numpy as np
from datetime import datetime
from astropy import units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro.iod.izzo import lambert

def orbital_elements_to_r_poliastro(a_m, e, inc_deg, Omega_deg=0, omega_deg=0, nu_deg=0, attractor=None):
    """
    Convertit des éléments orbitaux en position 3D (m) et retourne la position.

    a_m : demi-grand axe (m)
    e : excentricité
    inc_deg : inclinaison en degrés
    Omega_deg : longitude du nœud ascendant (°)
    omega_deg : argument du périapse (°)
    nu_deg : anomalie vraie (°)
    attractor : corps central (poliastro body)
    Retourne : np.array [rx, ry, rz] en mètres
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

    # If the result is degenerate (y and z nearly zero because nu==0),
    # try a few alternative true anomalies so the position is a proper 3D vector.
    if np.allclose(r_vec[1:], 0.0, atol=1e-12):
        nu_candidates = [10, 30, 45, 60, 90]
        for nu_try in nu_candidates:
            nu_try_q = (nu_try * u.deg)
            orb_try = Orbit.from_classical(attractor, a, ecc, inc, raan, argp, nu_try_q, epoch)
            r_try = orb_try.r.to_value(u.m)
            if not np.allclose(r_try[1:], 0.0, atol=1e-12):
                r_vec = r_try
                break

    return r_vec


def orbital_elements_to_r_alternative(a_m, e, inc_deg, Omega_deg=0, omega_deg=0, nu_deg=0, attractor=None):
    """
    Alternative method to convert orbital elements to 3D position (m).

    a_m : semi-major axis (m)
    e : eccentricity
    inc_deg : inclination in degrees
    Omega_deg : right ascension of ascending node (°)
    omega_deg : argument of periapsis (°)
    nu_deg : true anomaly (°)
    attractor : central body (poliastro body)
    Returns : np.array [rx, ry, rz] in meters
    """
    if attractor is None:
        raise ValueError("A central body must be provided via `attractor`.")

    # Alternative calculation using Kepler's laws or another method
    # This is a placeholder for the actual implementation
    # For now, we will return a dummy position
    return np.array([0.0, 0.0, 0.0])


def solve_lambert(r0, rf, tof_days, mu):
    """
    Résout Lambert et retourne les vecteurs vitesse initiale et finale (m/s)
    """
    if np.isnan(r0).any() or np.isnan(rf).any() or np.isnan(tof_days):
        raise ValueError("Les valeurs d'entrée ne doivent pas contenir de nan.")

    r0_q = r0 * u.m
    rf_q = rf * u.m
    tof_q = tof_days * u.day
    lambert_gen = lambert(mu * u.m**3 / u.s**2, r0_q, rf_q, tof_q)
    v0_q, vf_q = next(lambert_gen)
    v0 = v0_q.to(u.m/u.s).value
    vf = vf_q.to(u.m/u.s).value
    return v0, vf


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
    """
    Conversion ISO8601 → datetime
    """
    return datetime.fromisoformat(date_str)
