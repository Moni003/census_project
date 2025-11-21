# README.md

## Objectif du programme

Ce programme est un solveur de trajectoires spatiales basé sur la méthode Monte-Carlo pour des systèmes multi-corps. Il permet de générer automatiquement **la meilleure condition initiale** pour qu'un satellite passe d'un point A à un point B, en utilisant une propagation N-corps et en produisant un fichier compatible DOCKS.

## Architecture du projet

```
docks_montecarlo_solver/
├── solver/               # Contient le cœur du solveur
│   ├── __init__.py       # Import du solver pour utilisation en package
│   ├── config.py         # Paramètres et configuration par défaut
│   ├── montecarlo.py     # Génération des candidats Monte-Carlo
│   ├── propagator.py     # Propagation Kepler et N-corps des trajectoires
│   ├── scorer.py         # Calcul du score pour chaque trajectoire
│   └── solver.py         # Algorithme principal de sélection de la meilleure trajectoire
├── docks_utils.py        # Fonctions pour lire et vérifier les fichiers DOCKS
├── montecarlo_utils.py   # Fonctions utilitaires pour Monte-Carlo et écriture DOCKS
├── predefined_bodies.py  # Paramètres physiques des corps du système solaire
├── run_solver.py         # Script principal pour lancer le solver
├── requirements.txt      # Dépendances Python
├── README.md             # Documentation et instructions
└── tests/                # Tests unitaires et de validation
    ├── test_unit_energy.py
    ├── test_consistency_seed.py
    └── test_docks_file_format.py
```

## But de chaque fichier

* **solver/**init**.py** : Permet d'importer le solver comme module Python.
* **solver/config.py** : Définit les paramètres par défaut du solver, corps centraux, perturbateurs, TOF, cible, nombre d'échantillons, options multi-fidélité et seed.
* **solver/montecarlo.py** : Génère des conditions initiales aléatoires (r,v) pour chaque candidat via Monte-Carlo.
* **solver/propagator.py** : Contient les fonctions de propagation rapide Kepler et N-corps.
* **solver/scorer.py** : Évalue la distance finale au point cible et calcule un score pour chaque candidat.
* **solver/solver.py** : Coordonne l'algorithme complet : génération des candidats, propagation rapide, sélection des meilleurs, raffinement N-corps et écriture du fichier DOCKS final.
* **montecarlo_utils.py** : Fonctions utilitaires pour la conversion éléments orbitaux <-> vecteur r/v et pour écrire les fichiers DOCKS.
* **predefined_bodies.py** : Contient les valeurs de μ et rayon pour les corps célestes utilisés.
* **docks_utils.py** : Fonctions pour lire et valider les fichiers DOCKS.
* **run_solver.py** : Script principal pour lancer le solver et générer le fichier DOCKS final.
* **tests/** : Contient les tests unitaires et de validation pour s'assurer que le solver est correct et reproductible.

## Comment lancer le programme

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Lancer le solver pour générer la meilleure trajectoire et le fichier DOCKS :

```bash
python run_solver.py
```

3. Vérifier le fichier DOCKS généré et, si nécessaire, l'utiliser avec DOCKS Trajectories.
4. Exécuter les tests pour valider la robustesse et la reproductibilité :

```bash
pytest -q
```

**Ordre recommandé d'exécution** :

1. `run_solver.py` pour générer la solution.
2. Vérification du fichier DOCKS dans DOCKS Trajectories.
3. `pytest` pour s'assurer de la fiabilité du solver.
