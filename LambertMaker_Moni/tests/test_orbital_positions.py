import numpy as np
from lambert_utils import orbital_elements_to_r

def test_orbital_elements_to_r():
    a = 7000e3     # demi-grand axe en m
    e = 0.1        # excentricité
    inc = 30       # degrés

    r = orbital_elements_to_r(a, e, inc)
    rp = a * (1 - e)

    # Vérification : la norme de r doit être proche de rp
    assert np.isclose(np.linalg.norm(r), rp), f"Norme de r {np.linalg.norm(r)} != rp {rp}"

    # Vérification de la dimension
    assert r.shape == (3,), f"r n'a pas la bonne dimension : {r.shape}"

    print("✅ test_orbital_positions passed")
