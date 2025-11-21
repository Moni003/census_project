# solver.py
import numpy as np
from astropy.time import Time
from astropy import units as u

from poliastro.bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter
from poliastro.twobody.numerical import propagate
from poliastro.core.perturbations import third_body

from montecarlo_utils import generate_random_orbital_elements, orbital_elements_to_rv, write_docks_file
from predefined_bodies import known_bodies


############################
# PARAMÈTRES DU PROBLÈME
############################

# Point A = conditions initiales aléatoires via Monte-Carlo
# Point B = position cible (vecteur 3D)
target_B = np.array([1.2e11, 0.0, 0.0])  # exemple : point quelconque dans le référentiel solaire

t0_str = "2025-01-01T12:00:00"
epoch = Time(t0_str, scale="tdb")

N = 200  # nombre d'échantillons
TOF = 80 * u.day  # durée de propagation

attractor = Sun
mu = attractor.k.to_value(u.m**3/u.s**2)


############################
# PROPAGATION MULTI-CORPS
############################

planets = [Mercury, Venus, Earth, Mars, Jupiter]

def acceleration_nbody(t, state):
    """Accélération multi-corps : attraction du Soleil + planètes."""
    r = state[:3]
    v = state[3:]

    # accélération centrale du corps attracteur
    acc = -mu * r / np.linalg.norm(r)**3

    # troisième corps (planètes)
    for p in planets:
        rp = p.ephem.compute(epoch + t * u.s)[0].to_value(u.m)
        acc += third_body(r, rp, p.k.to_value(u.m**3/u.s**2))

    return np.hstack((v, acc))


############################
# BOUCLE MONTE-CARLO
############################

best_score = np.inf
best_r0 = None
best_v0 = None

for k in range(N):

    # 1) Échantillon random
    a, e, inc, raan, argp, nu = generate_random_orbital_elements(
        (0.5e11, 3e11),   # range demi-grand axe (ex.)
        (0, 0.6),
        (0, 40)
    )
    r0, v0 = orbital_elements_to_rv(attractor, t0_str, a, e, inc, raan, argp, nu)

    # État initial
    state0 = np.hstack((r0, v0))

    # 2) Propagation n-corps
    try:
        state_f = propagate(
            state0,
            TOF.to_value(u.s),
            acceleration_nbody,
            rtol=1e-9,
            atol=1e-9
        )
    except:
        continue  # ignore l’échantillon instable

    rf = state_f[:3]

    # 3) Score = distance finale au point B
    score = np.linalg.norm(rf - target_B)

    # 4) Minimisation
    if score < best_score:
        best_score = score
        best_r0 = r0
        best_v0 = v0

        print(f"New best score {best_score:.3e} at sample {k+1}")

############################
# SAUVEGARDE FINALE
############################

print("\n=== BEST SOLUTION FOUND ===")
print("Score:", best_score)
write_docks_file("best_solution.txt", t0_str, best_r0, best_v0)

print("\nFichier DOCKS généré : best_solution.txt")
