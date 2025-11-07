# LambertMaker_Moni

LambertMaker_Moni est un ensemble de scripts Python permettant de générer des **conditions initiales pour des trajectoires$s** à partir de paramètres orbitaux (récupéré depuis des TLE). Ces conditions peuvent ensuite être utilisées dans **DOCKS Trajectories** pour simuler des trajectoires transitoires entre deux points autour d’un astre.

---



## Structure du projet
LambertMaker_Moni/
│
├── lambert_utils.py # Fonctions principales : conversion éléments orbitaux → position, solveur Lambert, écriture fichiers DOCKS
├── main.py # Script principal interactif (similaire à OrbitMakerSimple)
├── predefined_bodies.py # Liste des corps célestes connus et leurs paramètres (μ, rayon)
├── convert_tle_params/ # CSV contenant les paramètres orbitaux extraits de TLE
│ └── orbital_params.csv
└── tests/ # Scripts de test et génération automatique de fichiers de conditions initiales
└── test_lambert_from_csv.py





---

## Description des fichiers principaux

### `lambert_utils.py`
- **orbital_elements_to_r_poliastro** : convertit les éléments orbitaux classiques (a, e, i, Ω, ω, ν) en vecteur position 3D.
- **solve_lambert** : résout le problème de Lambert entre deux points `r1` et `r2` pour une durée `ΔT`.
- **write_docks_file** : écrit un fichier de conditions initiales compatible DOCKS.
- **parse_isot** : convertit une date ISO8601 en objet `datetime`.

### `main.py`
- Script interactif permettant de générer des fichiers de conditions initiales pour une **trajectoire transitoire** entre deux points autour d’un astre.
- L’utilisateur fournit :  
  - le corps central (astre),  
  - les paramètres orbitaux des deux points,  
  - la durée du transfert.
- Le script calcule `r1`, `r2` et les vitesses `v1`, `v2` via Lambert, puis génère un fichier de conditions initiales.

### `predefined_bodies.py`
- Contient un dictionnaire `known_bodies` avec les paramètres des corps célestes (mu, rayon).  (est-ce utile ?)

### `convert_tle_params/orbital_params.csv`
- Fichier CSV avec des données orbitales (nom, époques, a, e, i, Ω, ω, ν) provenant de TLE ou d’autres sources.
- Utilisé dans les tests pour générer automatiquement des fichiers de conditions initiales.

### `tests/test_lambert_from_csv.py`
- Lit un CSV et génère un fichier de conditions initiales pour chaque ligne (une ligne = un TLE qu'on a convertie en paramètres orbitaux).
- Permet de tester plusieurs satellites ou époques en même temps.

---

## Ordre recommandé d’utilisation

1. **Préparer vos données**  
   - Pour une trajectoire personnalisée : utiliser `main.py` et saisir les paramètres orbitaux manuellement.  
   - Pour tester plusieurs satellites : préparer `orbital_params.csv` dans `convert_tle_params/`.

2. **Générer des conditions initiales**  
   - Pour une entrée manuelle : lancer `main.py`.  
   - Pour les tests automatiques : lancer `tests/test_lambert_from_csv.py`.

3. **Vérifier vos fichiers générés**  
   - Les fichiers générés se trouvent dans le dossier `tests/`.  

4. **Utiliser DOCKS Trajectories**  
   - Importer les fichiers DOCKS générés pour simuler et visualiser les trajectoires.  
   - Les positions et vitesses générées peuvent être utilisées pour reproduire ou tester des transferts orbitaux.

---

## Remarques

- **Robustesse** : `main.py` et `lambert_utils.py` gèrent les cas colinéaires pour éviter les `NaN` dans Lambert.  
- **Unités** : toutes les positions sont en **mètres**, toutes les vitesses en **m/s**.  
- **Astres pris en charge** : Soleil, Mercure, Vénus, Terre, Lune, Mars, Jupiter, Saturne, Uranus, Neptune.

---

## Exemple rapide

```bash
# Générer un fichier DOCKS pour un satellite à partir d'un CSV
python tests/test_lambert_from_csv.py

