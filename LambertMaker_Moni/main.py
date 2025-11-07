from lambert_utils import orbital_elements_to_r_poliastro, solve_lambert, write_docks_file, parse_isot
from predefined_bodies import known_bodies
from poliastro.bodies import Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune
from datetime import timedelta
import numpy as np

# Mapping nom -> objet poliastro
body_dict = {
    "sun": Sun, "mercury": Mercury, "venus": Venus, "earth": Earth,
    "moon": Moon, "mars": Mars, "jupiter": Jupiter, "saturn": Saturn,
    "uranus": Uranus, "neptune": Neptune
}

print("\n=== LambertMakerSimple (modulaire) ===\n")

# 1. Date initiale
t1_str = input("Enter the initial date and time in ISOT format [default: 2025-01-01T12:00:00]: ") or "2025-01-01T12:00:00"
t1_dt = parse_isot(t1_str)

# 2. Choix du corps central
bodies_names = list(known_bodies.keys())
print("\nSelect the central body:")
for i, b in enumerate(bodies_names):
    print(f"{i}: {b}")
body_index = int(input("Choose a body by its number : "))
body_selected = bodies_names[body_index]
mu = known_bodies[body_selected][0]
attractor = body_dict[body_selected]
print(f"Body selected: {body_selected}\n")

# 3. Paramètres orbitaux pour les deux points
print("--- Point 1 ---")
a1 = float(input("Demi-grand axe a1 (m) : "))
e1 = float(input("Excentricité e1 : "))
inc1 = float(input("Inclinaison i1 (°) : "))

print("--- Point 2 ---")
a2 = float(input("Demi-grand axe a2 (m) : "))
e2 = float(input("Excentricité e2 : "))
inc2 = float(input("Inclinaison i2 (°) : "))

# 4. Calcul des positions r1 et r2
r1 = orbital_elements_to_r_poliastro(a1, e1, inc1, attractor=attractor)

# Try to compute r2 but avoid the degenerate case where r1 and r2 are collinear (which breaks Izzo's lambert)
# If the default angles produce collinear vectors, vary the true anomaly of point 2 until we get a non-collinear pair.
nu_candidates_deg = [0, 10, 30, 45, 90, 135, 180]
r2 = None
for nu_try in nu_candidates_deg:
    r2_try = orbital_elements_to_r_poliastro(a2, e2, inc2, nu_deg=nu_try, attractor=attractor)
    cross_norm = np.linalg.norm(np.cross(r1, r2_try))
    if cross_norm > 1e-6:  # not collinear
        r2 = r2_try
        if nu_try != 0:
            print(f"Note: adjusted true anomaly for point 2 to {nu_try}° to avoid collinear positions.")
        break

if r2 is None:
    # fallback: use the last candidate even if collinear (should be rare)
    r2 = orbital_elements_to_r_poliastro(a2, e2, inc2, nu_deg=nu_candidates_deg[-1], attractor=attractor)

print("\nr1 (m) =", r1)
print("r2 (m) =", r2)

# 5. Durée du transfert
deltaT_hours = float(input("\nDurée du transfert ΔT (heures) : "))
deltaT_days = deltaT_hours / 24
t2_dt = t1_dt + timedelta(hours=deltaT_hours)

# 6. Solveur Lambert
v1, v2 = solve_lambert(r1, r2, deltaT_days, mu)
print("\nv1 (m/s) =", v1)
print("v2 (m/s) =", v2)
print("Date point 2 :", t2_dt.isoformat())

# 7. Génération fichier DOCKS
write_docks_file(f"InitCond_Lambert_{body_selected}.txt", t1_str, r1, v1)

print("\n=== Fin du script ===")

