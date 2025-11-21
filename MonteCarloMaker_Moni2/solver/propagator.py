# solver/propagator.py
import numpy as np
from astropy.time import Time
from scipy.integrate import solve_ivp
from poliastro.core.perturbations import third_body
from solver.config import MU, PERTURBERS, T0_STR


epoch = Time(T0_STR, scale="tdb")



def nbody_accel(t, state):
    r = state[:3]
    v = state[3:]

    # central
    acc = -MU * r / np.linalg.norm(r)**3


    # third bodies
    for p in PERTURBERS:
        try:
            rp = p.ephem.compute(epoch + t * 1.0).to_value()[0]
            acc += third_body(r, rp, p.k.to_value())
        except Exception:
            # en cas d'erreur d'éphéméride, on ignore ce perturbeur
            continue

    return np.hstack((v, acc))




def propagate_kepler(r0, v0, tof_seconds):
    """Propagation Keplerienne rapide via un solveur simple (approximation)."""
    # Ici on utilise un solveur simple en N-body désactivé — placeholder
    state0 = np.hstack((r0, v0))
    sol = solve_ivp(lambda t,y: nbody_accel(t,y), [0, tof_seconds], state0, rtol=1e-8, atol=1e-8)
    return sol.y[:, -1]




def propagate_nbody(r0, v0, tof_seconds):
    state0 = np.hstack((r0, v0))
    try:
        sol = solve_ivp(lambda t,y: nbody_accel(t,y), [0, tof_seconds], state0, rtol=1e-9, atol=1e-9)
        return sol.y[:, -1]
    except Exception:
        return None