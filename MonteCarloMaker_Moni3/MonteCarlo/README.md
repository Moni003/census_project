# Solveur de Trajectoire Satellite - Méthode Monte Carlo

## Description

...

## Algorithme

### Vue d'ensemble
1. **Saisie des paramètres** : L'utilisateur fournit les conditions initiales et les paramètres de simulation
2. **Perturbation Monte Carlo** : Pour chaque itération, un vecteur de perturbation aléatoire est appliqué à la vitesse initiale
3. **Génération des fichiers** : Les conditions initiales perturbées sont sauvegardées pour la propagation externe

### Étapes détaillées

#### 1. Paramètres d'entrée
- **r1** : Position initiale du satellite [rx, ry, rz] en km
- **r2** : Position finale cible [rx, ry, rz] en km
- **v1** : Vitesse initiale nominale [vx, vy, vz] en km/s
- **Date initiale** : Date de départ au format YYYY-MM-DDTHH:MM:SS
- **Corps central** : Corps gravitationnel principal (défaut : Terre)
- **Autres corps** : Deux corps gravitationnels additionnels (défaut : Soleil, Lune)
- **N** : Nombre d'itérations Monte Carlo (défaut : 1)

#### 2. Boucle Monte Carlo
Pour chaque itération i = 1 à N :

1. **Tirage aléatoire** :
   ```
   deltav1 = [0, uniform_random(-2.8, 2.8), 0]  # Perturbation uniquement sur v1_y
   ```

2. **Calcul de la vitesse perturbée** :
   ```
   v1' = v1 + deltav1
   ```

3. **Sauvegarde** :
   - Fichier de conditions initiales : `initial_conditions_iter_XXX.txt`
   - Format : `date rx ry rz v1x v1y v1z` (positions en km, vitesses en km/s)

#### 3. Organisation des résultats
Chaque exécution crée un dossier unique avec :
- **parameters.txt** : Tous les paramètres de simulation
- **initial_conditions_iter_XXX.txt** : Fichiers de conditions initiales pour chaque itération

## Structure des fichiers

```
MonteCarlo/
├── main.py                    # Programme principal
├── mc_utils.py               # Fonctions utilitaires
├── predefined_bodies.py      # Données des corps célestes
├── README.md                 # Cette documentation
└── run_YYYYMMDD_HHMMSS/     # Dossier de résultats (créé à chaque exécution)
    ├── parametres.txt        # Paramètres de simulation
    └── initial_conditions_iter_XXX.txt  # Conditions initiales
```

## Utilisation

1. **Lancer le programme** :
   ```bash
   python main.py
   ```

2. **Saisir les paramètres** (ou utiliser les valeurs par défaut) :
   - Positions r1 et r2
   - Vitesse initiale v1
   - Date initiale
   - Corps gravitationnels
   - Nombre d'itérations N

3. **Résultats** :
   - Un nouveau dossier `run_YYYYMMDD_HHMMSS` est créé
   - Les fichiers de conditions initiales sont prêts pour DOCKS

## Paramètres par défaut

- **r1** : [7e3, 0, 0] km
- **r2** : [4.2e4, 0, 0] km  
- **v1** : [1, 1, 0] km/s
- **Date** : 2025-01-01T12:00:00
- **Corps central** : Terre
- **Autres corps** : Soleil, Lune
- **N** : 1 itération

## Corps célestes disponibles

- Soleil (sun)
- Mercure (mercury)
- Vénus (venus)
- Terre (earth) - défaut
- Lune (moon)
- Mars (mars)
- Jupiter (jupiter)
- Saturne (saturn)
- Uranus (uranus)
- Neptune (neptune)

## Notes techniques

- **Domaine de perturbation** : [-2.8, 2.8] km/s appliqué uniquement sur la composante v1_y
- **Format de sortie** : Compatible avec le propagateur DOCKS (positions en km, vitesses en km/s)
- **Générateur aléatoire** : numpy.random avec seed fixe (42) pour la reproductibilité
- **Pas de propagation** : Les fichiers sont destinés à être propagés sur DOCKS

## Exemple de fichier de conditions initiales

```
2025-01-01T12:00:00	7.000000e+03	0.000000e+00	0.000000e+00	1.001234e+00	9.987654e-01	-1.234567e-03
```

Format : `date rx ry rz vx vy vz` (positions en km, vitesses en km/s)