# solver/montecarlo.py
import numpy as np
from montecarlo_utils import generate_random_orbital_elements, orbital_elements_to_rv
from solver.config import ATTRACTOR, T0_STR


def sample_candidates(N, a_range, e_range, i_range, rng=None):
    """Génère N candidats (r0, v0) via Monte-Carlo. Retourne liste de tuples (r0,v0,elems)."""
    if rng is None:
        rng = np.random.default_rng()

    candidates = []
    for _ in range(N):
        a, e, inc, raan, argp, nu = generate_random_orbital_elements(
        a_range, e_range, i_range, rng=rng
        )
        r0, v0 = orbital_elements_to_rv(ATTRACTOR, T0_STR, a, e, inc, raan, argp, nu)
        candidates.append((r0, v0, (a,e,inc,raan,argp,nu)))
    return candidates