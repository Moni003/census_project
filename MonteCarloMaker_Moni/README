# MonteCarloMaker

MonteCarloMaker est un ensemble de scripts Python permettant de générer des conditions initiales orbitales aléatoires pour des trajectoires autour d’un astre. Ces fichiers peuvent ensuite être utilisés dans DOCKS Trajectories pour simuler des trajectoires balistiques (sans propulsion continue).

---

Structure du projet

MonteCarloMaker/
│
├── montecarlo_utils.py   # Fonctions principales : génération Monte Carlo, conversion éléments → position, écriture fichiers DOCKS
├── main.py               # Script principal interactif
├── predefined_bodies.py  # Liste des corps célestes connus et leurs paramètres (μ, rayon)
└── tests/                # Scripts de test et génération automatique de fichiers de conditions initiales
    └── test_mc_generation.py

---


---

## Description des fichiers principaux

### `montecarlo_utils.py`
- `generate_random_orbital_elements(a_range, e_range, i_range)` : génère des paramètres orbitaux aléatoires dans les plages spécifiées.
- `orbital_elements_to_r(attractor, a, e, inc, Omega, omega, nu)` : convertit les éléments orbitaux en vecteur position 3D.
- `write_docks_file(filename, date_str, r, v)` : écrit un fichier de conditions initiales compatible DOCKS.

### `main.py`
- Script interactif permettant de générer **N échantillons aléatoires** de conditions initiales autour d’un corps central.
- L’utilisateur fournit :
  - le corps central (astre),
  - les plages de demi-grand axe, excentricité et inclinaison,
  - le nombre d’échantillons Monte Carlo,
  - la date initiale.
- Pour chaque échantillon généré :
  - vecteur position 3D
  - vecteur vitesse initiale (approximation circulaire Keplerienne)
  - fichier DOCKS compatible

### `predefined_bodies.py`
- Contient un dictionnaire `known_bodies` avec les paramètres des corps célestes (μ, rayon)
- Utilisé pour calculer les vitesses orbitales approximatives

### `tests/test_mc_generation.py`
- Génère automatiquement plusieurs fichiers de conditions initiales Monte Carlo pour un corps choisi
- Permet de tester la robustesse et la variété des échantillons générés

---

## Ordre recommandé d’utilisation

1. **Préparer vos paramètres**
   - Choisir le corps central (ex : Terre, Mars)
   - Définir les plages de paramètres orbitaux (a, e, i)
   - Choisir le nombre d’échantillons Monte Carlo

2. **Lancer la génération**
```bash
python main.py
