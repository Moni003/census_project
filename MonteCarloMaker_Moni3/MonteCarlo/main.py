# main.py - Solveur de trajectoire satellite avec méthode Monte Carlo
import numpy as np
import os
from datetime import datetime
from predefined_bodies import known_bodies

def write_initial_conditions_file(filename, date_str, r, v):
    """Écrit un fichier de conditions initiales"""
    with open(filename, 'w') as f:
        line = f"{date_str}\t{r[0]:.6e}\t{r[1]:.6e}\t{r[2]:.6e}\t{v[0]:.6e}\t{v[1]:.6e}\t{v[2]:.6e}\n"
        f.write(line)
    print(f"    [OK] Fichier écrit: {filename}")

def write_parameters_file(filename, parameters):
    """Écrit un fichier avec tous les paramètres"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=== PARAMÈTRES DE SIMULATION MONTE CARLO ===\n")
        f.write(f"Timestamp: {parameters['timestamp']}\n\n")
        
        f.write("=== POSITIONS ET VITESSES ===\n")
        f.write(f"r1 (km): [{parameters['r1'][0]:.6e}, {parameters['r1'][1]:.6e}, {parameters['r1'][2]:.6e}]\n")
        f.write(f"r2 (km): [{parameters['r2'][0]:.6e}, {parameters['r2'][1]:.6e}, {parameters['r2'][2]:.6e}]\n")
        f.write(f"v1 (km/s): [{parameters['v1'][0]:.6e}, {parameters['v1'][1]:.6e}, {parameters['v1'][2]:.6e}]\n\n")
        
        f.write("=== PARAMÈTRES TEMPORELS ===\n")
        f.write(f"Date initiale: {parameters['date_initiale']}\n\n")
        
        f.write("=== CORPS GRAVITATIONNELS ===\n")
        f.write(f"Corps central: {parameters['corps_central']}\n")
        f.write(f"Autres corps: {', '.join(parameters['autres_corps'])}\n\n")
        
        f.write("=== PARAMÈTRES MONTE CARLO ===\n")
        f.write(f"Nombre d'itérations: {parameters['nombre_iterations']}\n")
        f.write(f"Domaine delta_v1_y: [-2.9, 2.9] km/s (perturbations très petites sur v1_y seulement)\n\n")
        
        f.write("=== DELTAV TIRÉS ===\n")
        if 'deltav_list' in parameters:
            for i, deltav in enumerate(parameters['deltav_list']):
                f.write(f"  Itération {i+1:03d}: [{deltav[0]:.12e}, {deltav[1]:.12e}, {deltav[2]:.12e}] km/s\n")
        f.write("\n")
        
        f.write("=== FICHIERS GÉNÉRÉS ===\n")
        for i in range(parameters['nombre_iterations']):
            f.write(f"  initial_conditions_iter_{i+1:03d}.txt\n")
        
        f.write(f"\n=== FORMAT DES FICHIERS DE CONDITIONS INITIALES ===\n")
        f.write(f"Colonnes: date rx ry rz vx vy vz\n")
        f.write(f"Unités: - km km km km/s km/s km/s\n")
        f.write(f"Séparateur: tabulation\n")
    
    print(f"    [OK] Fichier de paramètres écrit: {filename}")

print("\n=== Solveur de Trajectoire Satellite - Méthode Monte Carlo ===\n")

# 1. Demander les paramètres à l'utilisateur
print("=== Paramètres de la trajectoire ===")

# Position initiale r1
print("\nPosition initiale r1 (km):")
r1 = np.array([
    float(input("  r1_x [défaut 1.49e8]: ") or 1.496e8),
    float(input("  r1_y [défaut 0]: ") or 0.0),
    float(input("  r1_z [défaut 0]: ") or 0.0)
])

# Position finale r2
print("\nPosition finale r2 (km):")
r2 = np.array([
    float(input("  r2_x [défaut -2.27e8]: ") or -2.27e8),
    float(input("  r2_y [défaut 0]: ") or 0.0),
    float(input("  r2_z [défaut 0]: ") or 0.0)
])

# Vitesse initiale v1
print("\nVitesse initiale v1 (km/s):")
v1 = np.array([
    float(input("  v1_x [défaut 0]: ") or 0),
    float(input("  v1_y [défaut 32.7]: ") or 32.7),
    float(input("  v1_z [défaut 0]: ") or 0.0)
])

# Date initiale
t0_str = input("\nDate initiale [YYYY-MM-DDTHH:MM:SS] [défaut 1996-12-30T00:00:00]: ") or "1996-12-30T00:00:00"

# Corps gravitationnel central
print("\nCorps gravitationnels disponibles:")
bodies_names = list(known_bodies.keys())
for i, body in enumerate(bodies_names):
    print(f"  {i}: {body}")

central_body_idx = int(input("Corps central [défaut 0 = sun]: ") or "0")
central_body = bodies_names[central_body_idx]

# Deux autres corps gravitationnels
print(f"\nAutres corps gravitationnels (indices séparés par des virgules):")
print("Corps disponibles (hors corps central):")
for i, body in enumerate(bodies_names):
    if body != central_body:
        print(f"  {i}: {body}")

other_bodies_input = input("Indices des autres corps [défaut 3,4,5 = earth,moon,mars]: ") or "3,4,5"
other_bodies_indices = [int(i.strip()) for i in other_bodies_input.split(",")]
other_bodies = [bodies_names[i] for i in other_bodies_indices if bodies_names[i] != central_body]

print(f"\nCorps sélectionnés: {central_body} (central) + {other_bodies}")

# Nombre d'itérations Monte Carlo
N = int(input(f"\nNombre d'itérations Monte Carlo [défaut 1]: ") or "1")

print(f"\n=== Configuration ===")
print(f"r1: {r1}")
print(f"r2: {r2}")
print(f"v1: {v1}")
print(f"Date: {t0_str}")
print(f"Corps central: {central_body}")
print(f"Autres corps: {other_bodies}")
print(f"Nombre d'itérations: {N}")

# Créer un dossier unique pour cette exécution dans le dossier MonteCarlo
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
run_folder = f"run_{timestamp}"
os.makedirs(run_folder, exist_ok=True)
print(f"\n=== Dossier de résultats créé: MonteCarlo/{run_folder} ===")

# Sauvegarder les paramètres dans un fichier (sera réécrit après la boucle avec les deltav)
parameters = {
    'r1': r1,
    'r2': r2, 
    'v1': v1,
    'date_initiale': t0_str,
    'corps_central': central_body,
    'autres_corps': other_bodies,
    'nombre_iterations': N,
    'timestamp': timestamp
}

# Boucle Monte Carlo
print(f"\n=== Exécution Monte Carlo ===")
rng = np.random.default_rng(42)

# Liste pour stocker tous les deltav tirés
deltav_list = []

for i in range(N):
    print(f"\nItération {i+1}/{N}")
    
    # Tirage aléatoire d'une perturbation sur la deuxième composante de v1 (v1_y)
    #delta_v1_y = rng.uniform(-2.9, 2.9)  # Perturbation aléatoire sur v1_y    (delta=1.2 c bcp)
    delta_v1_y = 1e-3  # Perturbation très petite en km/s
    
    # Appliquer la perturbation seulement sur v1_y
    v1_prime = v1.copy()  # Copier v1 original
    v1_prime[1] = v1[1] + delta_v1_y  # Modifier seulement la composante y
    
    # Stocker le delta pour les paramètres
    deltav1 = np.array([0.0, delta_v1_y, 0.0])  # Perturbation seulement sur y
    deltav_list.append(deltav1)
    
    print(f"  delta_v1_y tiré: {delta_v1_y:.12e} km/s")
    print(f"  v1 original: [{v1[0]:.12e}, {v1[1]:.12e}, {v1[2]:.12e}] km/s")
    print(f"  v1' modifié: [{v1_prime[0]:.12e}, {v1_prime[1]:.12e}, {v1_prime[2]:.12e}] km/s")
    print(f"  v1' = {v1_prime}")
    
    # Génération du fichier de conditions initiales
    filename = os.path.join(run_folder, f"initial_conditions_iter_{i+1:03d}.txt")
    write_initial_conditions_file(filename, t0_str, r1, v1_prime)
    print(f"  [OK] Fichier généré: {filename}")

# Ajouter les deltav à la liste des paramètres et réécrire le fichier
parameters['deltav_list'] = deltav_list
write_parameters_file(os.path.join(run_folder, "parametres.txt"), parameters)

print(f"\n=== Fin du programme ===")
print(f"Tous les fichiers ont été générés dans le dossier: {run_folder}")
print(f"  - parametres.txt : paramètres de simulation")
print(f"  - initial_conditions_iter_XXX.txt : conditions initiales ({N} fichiers)")