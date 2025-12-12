"""
predefined_bodies.py
Contient les données des corps célestes utilisés par LambertMaker
"""
import numpy as np

# Constante gravitationnelle
G = 6.67430e-11  # m^3/kg/s^2

# Données simplifiées des corps du système solaire : [mu (m^3/s²), rayon (m)]
known_bodies = {
    "sun":     [1.3271244004194e20, 696000000],
    "mercury": [2.2032080493345e13, 2440530],
    "venus":   [3.248586068371049e14, 6051800],
    "earth":   [3.98659293629478e14, 6378136.3],
    "moon":    [4.843941639988467e12, 1738000],
    "mars":    [4.28283132893115e13, 3396190],
    "jupiter": [1.26686536751784e17, 71492000],
    "saturn":  [3.79312396775046e16, 60268000],
    "uranus":  [5.79393921281797e15, 25559000],
    "neptune": [6.83509920358736e15, 24764000]
}

# Position du satellite : altitude de 10 000 km au-dessus de la surface de la Terre
r_satellite = np.array([6378136.3 + 10000e3, 0, 0])  # m

# Position approximative des autres corps (simplifiée sur l'axe X)
positions_bodies = {
    "sun": np.array([1.5e11, 0, 0]),
    "mercury": np.array([5.8e10, 0, 0]),
    "venus": np.array([1.08e11, 0, 0]),
    "earth": np.array([0, 0, 0]),
    "moon": np.array([3.84e8, 0, 0]),
    "mars": np.array([2.28e11, 0, 0]),
    "jupiter": np.array([7.78e11, 0, 0]),
    "saturn": np.array([1.43e12, 0, 0]),
    "uranus": np.array([2.87e12, 0, 0]),
    "neptune": np.array([4.5e12, 0, 0])
}
# Calculer les accélérations
accelerations = []
for name, (mu, radius) in known_bodies.items():
    r_body = positions_bodies[name]
    distance = np.linalg.norm(r_body - r_satellite)
    a = mu / distance**2
    accelerations.append((name, distance, a))

# Trier par accélération décroissante (du plus grand au plus petit)
accelerations_sorted = sorted(accelerations, key=lambda x: x[2], reverse=True)

# Afficher
print("Accélérations gravitationnelles par rapport au satellite (m/s²), triées du plus grand au plus petit :\n")
for name, distance, a in accelerations_sorted:
    print(f"{name:8s} -> distance = {distance:.3e} m, a = {a:.5e} m/s²")