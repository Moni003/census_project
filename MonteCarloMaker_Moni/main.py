# main.py
from montecarlo_utils import generate_random_orbital_elements, orbital_elements_to_r, write_docks_file
from predefined_bodies import known_bodies
from poliastro.bodies import Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune
from datetime import datetime
import numpy as np

# Mapping nom -> objet poliastro
body_dict = {
    "sun": Sun, "mercury": Mercury, "venus": Venus, "earth": Earth,
    "moon": Moon, "mars": Mars, "jupiter": Jupiter, "saturn": Saturn,
    "uranus": Uranus, "neptune": Neptune
}

print("\n=== MonteCarloMaker ===\n")

# 1. Date initiale
t0_str = input("Enter the initial date in ISOT format [default: 2025-01-01T12:00:00]: ") or "2025-01-01T12:00:00"

# 2. Choix du corps central
bodies_names = list(known_bodies.keys())
print("\nSelect the central body:")
for i, b in enumerate(bodies_names):
    print(f"{i}: {b}")
body_index = int(input("Choose a body by its number : "))
body_selected = bodies_names[body_index]
attractor = body_dict[body_selected]
mu = known_bodies[body_selected][0]

# 3. Définir les ranges pour le Monte Carlo
a_min = float(input("Demi-grand axe min (m) : "))
a_max = float(input("Demi-grand axe max (m) : "))
e_min = float(input("Excentricité min : "))
e_max = float(input("Excentricité max : "))
i_min = float(input("Inclinaison min (°) : "))
i_max = float(input("Inclinaison max (°) : "))
N = int(input("Nombre d'échantillons Monte Carlo : "))

# 4. Génération Monte Carlo
for k in range(N):
    a, e, i = generate_random_orbital_elements([a_min, a_max], [e_min, e_max], [i_min, i_max])
    r = orbital_elements_to_r(attractor, a, e, i)
    # vitesse initiale Keplérienne circulaire approximative
    v_mag = np.sqrt(mu / np.linalg.norm(r))
    v = np.array([v_mag, 0, 0])
    write_docks_file(f"InitCond_MC_{body_selected}_{k+1}.txt", t0_str, r, v)

print(f"\n✅ Monte Carlo terminé : {N} fichiers générés pour {body_selected}.")
