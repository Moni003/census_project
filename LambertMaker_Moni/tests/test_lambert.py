import numpy as np
from lambert_utils import solve_lambert
from predefined_bodies import known_bodies

def test_solve_lambert():
    # Exemple simple autour de la Terre
    mu = known_bodies["earth"][0]
    r1 = np.array([7000e3, 0, 0])
    r2 = np.array([8000e3, 5000e3, 0])
    tof_days = 0.01  # ~14,4 minutes

    v1, v2 = solve_lambert(r1, r2, tof_days, mu)

    # Vérifier que les vecteurs vitesse ont la bonne dimension
    assert v1.shape == (3,), f"v1 dimension incorrecte : {v1.shape}"
    assert v2.shape == (3,), f"v2 dimension incorrecte : {v2.shape}"

    # Vérifier que les vitesses ne contiennent pas de nan
    assert not np.any(np.isnan(v1)), f"v1 contient NaN : {v1}"
    assert not np.any(np.isnan(v2)), f"v2 contient NaN : {v2}"

    print("✅ test_solve_lambert passed")
