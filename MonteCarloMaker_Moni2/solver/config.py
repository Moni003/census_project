# solver/config.py
from poliastro.bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter
from astropy import units as u
import numpy as np


# Attracteur principal (modifiable)
ATTRACTOR = Sun
MU = ATTRACTOR.k.to_value(u.m**3 / u.s**2)


# Corps perturbateurs (multi-corps)
PERTURBERS = [Mercury, Venus, Earth, Mars, Jupiter]


# Horizon de propagation par défaut
TOF = 80 * u.day


# Point cible (à remplacer par le vrai point B en m)
TARGET_B = np.array([1.2e11, 0.0, 0.0])


# Nombre d'échantillons standard
N_SAMPLES = 1000


# Epoch par défaut
T0_STR = "2025-01-01T12:00:00"


# Option multi-fidélité : première passe en Kepler rapide (True) puis N-body refine
USE_MULTIFIDELITY = True
# Fraction des meilleurs candidats à raffiner en N-body (0.0-1.0)
REFINE_FRACTION = 0.05


# RNG seed par défaut pour reproductibilité
DEFAULT_SEED = 42