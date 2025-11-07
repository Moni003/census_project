import sys
import os
import csv
from datetime import timedelta

import numpy as np

# Ajouter le dossier parent pour trouver lambert_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lambert_utils import orbital_elements_to_r_poliastro, solve_lambert, write_docks_file, parse_isot
from predefined_bodies import known_bodies
from poliastro.bodies import Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune

# Mapping nom -> objet poliastro
body_dict = {
    "sun": Sun, "mercury": Mercury, "venus": Venus, "earth": Earth,
    "moon": Moon, "mars": Mars, "jupiter": Jupiter, "saturn": Saturn,
    "uranus": Uranus, "neptune": Neptune
}

# Chemin vers le CSV
csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "convert_tle_params", "orbital_params.csv"))

# Dossier de sortie (tests/)
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
os.makedirs(output_folder, exist_ok=True)

# Demander combien de lignes traiter
num_lines = int(input("Combien de lignes du fichier tle.txt voulez-vous utiliser ? "))

# Lire le CSV
with open(csv_file, newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)[:num_lines]

# Boucle sur chaque ligne du CSV
for i, row in enumerate(rows, start=1):
    print(f"\n=== Ligne {i} : {row['nom']} ===")
    
    # Corps central
    body_name = "earth"  # par défaut, à adapter selon le satellite si tu veux
    mu = known_bodies[body_name][0]
    attractor = body_dict[body_name]
    
    # Extraction des paramètres orbitaux
    a = float(row["demi_grand_axe_km"]) * 1000  # km → m
    e = float(row["excentricite"])
    inc = float(row["inclinaison_deg"])
    Omega = float(row["noeud_ascendant_deg"])
    omega = float(row["argument_perigee_deg"])
    nu = float(row["anomalie_vraie_deg"])
    
    # Conversion éléments → position
    r = orbital_elements_to_r_poliastro(a, e, inc, Omega_deg=Omega, omega_deg=omega, nu_deg=nu, attractor=attractor)
    
    # Exemple : trajectoire simple de Lambert pour un petit transfert (ΔT arbitraire)
    deltaT_hours = 2.0  # tu peux adapter
    deltaT_days = deltaT_hours / 24
    t1_dt = parse_isot(row["epoque_utc"])
    t2_dt = t1_dt + timedelta(hours=deltaT_hours)
    
    # Pour un test, on fait un petit déplacement fictif de 100 km sur x
    r2 = r + np.array([1e5, 0, 0])
    
    # Solveur Lambert
    v1, v2 = solve_lambert(r, r2, deltaT_days, mu)
    
    # Affichage
    print("r (m) =", r)
    print("r2 (m) =", r2)
    print("v1 (m/s) =", v1)
    print("v2 (m/s) =", v2)
    print("Date point 2 :", t2_dt.isoformat())
    
    # Génération fichier DOCKS dans le dossier tests/
    output_file = os.path.join(output_folder, f"InitCond_Lambert_test_{i}.txt")
    write_docks_file(output_file, row["epoque_utc"], r, v1)
