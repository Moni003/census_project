#!/usr/bin/env python3
"""
main2.py - Calculateur de fonction de coût pour trajectoires DOCKS
Calcule f_i = min_t ||r2 - r2_i(t)|| à partir des fichiers de trajectoire DOCKS
"""

import numpy as np
import os
import sys
from datetime import datetime, timedelta

def read_docks_trajectory(filename):
    """
    Lit un fichier de trajectoire DOCKS et extrait les données de position.
    
    Format DOCKS:
    - Colonnes 1-2: Time (MJD)
    - Colonnes 3-5: Position (KM) 
    - Colonnes 6-8: Velocity (KM/S)
    - Colonnes 9-11: Acceleration (KM/S^2)
    
    Retourne:
    - times: array des temps (MJD)
    - positions: array des positions [N, 3] en km
    """
    print(f"[LECTURE] Lecture du fichier: {filename}")
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Fichier non trouvé: {filename}")
    
    times = []
    positions = []
    
    with open(filename, 'r') as f:
        # Ignorer l'en-tête jusqu'à META_STOP
        in_header = True
        line_count = 0
        
        for line in f:
            line = line.strip()
            line_count += 1
            
            # Détecter la fin de l'en-tête
            if line == "META_STOP":
                in_header = False
                continue
            
            # Ignorer les lignes d'en-tête et les lignes vides
            if in_header or not line or line.startswith('COMMENT'):
                continue
            
            # Parser les données
            try:
                parts = line.split()
                if len(parts) >= 5:  # Au minimum MJD + temps + 3 positions
                    # Colonnes: MJD, temps, rx, ry, rz, vx, vy, vz, ax, ay, az
                    mjd = float(parts[0])
                    time_sec = float(parts[1])
                    rx = float(parts[2])
                    ry = float(parts[3]) 
                    rz = float(parts[4])
                    
                    # Temps total en MJD (MJD + secondes/86400)
                    total_time = mjd + time_sec / 86400.0
                    
                    times.append(total_time)
                    positions.append([rx, ry, rz])
                    
            except (ValueError, IndexError) as e:
                print(f"[WARN] Erreur ligne {line_count}: {e}")
                continue
    
    times = np.array(times)
    positions = np.array(positions)
    
    print(f"[OK] Données lues: {len(times)} points de trajectoire")
    print(f"   Temps: {times[0]:.6f} -> {times[-1]:.6f} MJD")
    print(f"   Position initiale: [{positions[0,0]:.0f}, {positions[0,1]:.0f}, {positions[0,2]:.0f}] km")
    print(f"   Position finale: [{positions[-1,0]:.0f}, {positions[-1,1]:.0f}, {positions[-1,2]:.0f}] km")
    
    return times, positions

def mjd_to_date(mjd):
    """
    Convertit un Modified Julian Day (MJD) en date calendaire
    
    MJD = JD - 2400000.5
    JD 0 = 1er janvier -4712 à 12h00 UTC
    MJD 0 = 17 novembre 1858 à 00h00 UTC
    """
    # MJD 0 correspond au 17 novembre 1858
    mjd_epoch = datetime(1858, 11, 17)
    
    # Ajouter le nombre de jours
    date = mjd_epoch + timedelta(days=mjd)
    
    return date

def calculate_cost_function(r2_target, trajectory_positions):
    """
    Calcule la fonction de coût f_i = min_t ||r2 - r2_i(t)||
    
    Paramètres:
    - r2_target: position cible [3] en km
    - trajectory_positions: positions de la trajectoire [N, 3] en km
    
    Retourne:
    - f_i: valeur minimale de la distance
    - min_index: index du point le plus proche
    - min_distance_vector: vecteur de distance au point le plus proche
    """
    print(f"\nCalcul de la fonction de coût")
    print(f"   Position cible r2: [{r2_target[0]:.0f}, {r2_target[1]:.0f}, {r2_target[2]:.0f}] km")
    
    # Calculer les distances à chaque point de la trajectoire
    distances = []
    for i, r2_i in enumerate(trajectory_positions):
        distance = np.linalg.norm(r2_target - r2_i)
        distances.append(distance)
    
    distances = np.array(distances)
    
    # Trouver le minimum
    min_index = np.argmin(distances)
    f_i = distances[min_index]
    min_distance_vector = r2_target - trajectory_positions[min_index]
    
    print(f"   Distance minimale f_i: {f_i:.3f} km")
    print(f"   Trouvée au point {min_index}/{len(distances)} de la trajectoire")
    print(f"   Position la plus proche: [{trajectory_positions[min_index,0]:.0f}, {trajectory_positions[min_index,1]:.0f}, {trajectory_positions[min_index,2]:.0f}] km")
    print(f"   Vecteur d'erreur: [{min_distance_vector[0]:.0f}, {min_distance_vector[1]:.0f}, {min_distance_vector[2]:.0f}] km")
    
    return f_i, min_index, min_distance_vector

def get_user_input(prompt, default_value):
    """Helper function to get user input with default value"""
    try:
        user_input = input(prompt)
        if not user_input.strip():
            return default_value
        return float(user_input)
    except (ValueError, EOFError):
        return default_value
def main():
    """Programme principal"""
    
    # 1. Demander le fichier de trajectoire
    if len(sys.argv) > 1:
        trajectory_file = sys.argv[1]
    else:
        default_file = "MonteCarlo/run_20260104_131519/traj_1.txt"
        trajectory_file = input(f"Chemin vers le fichier de trajectoire DOCKS [défaut: {default_file}]: ")
        if not trajectory_file:
            trajectory_file = default_file
        
        # Nettoyer les guillemets si présents
        trajectory_file = trajectory_file.strip('"\'')
        
        # Si le chemin est relatif, le construire depuis le répertoire courant
        if not os.path.isabs(trajectory_file) and not os.path.exists(trajectory_file):
            # Essayer depuis le répertoire courant
            alt_path = os.path.join(".", trajectory_file)
            if os.path.exists(alt_path):
                trajectory_file = alt_path
    
    print("=== Calculateur de fonction de coût DOCKS ===\n")
    
    # 2. Demander la position cible r2
    print(f"\nPosition cible r2 (km):")
    r2_target = np.array([
        get_user_input("  r2_x [défaut -2.27e8]: ", -2.27e8),
        get_user_input("  r2_y [défaut 0]: ", 0.0),
        get_user_input("  r2_z [défaut 0]: ", 0.0)
    ])
    
    try:
        # 3. Lire la trajectoire DOCKS
        times, positions = read_docks_trajectory(trajectory_file)
        
        # 4. Calculer la fonction de coût
        f_i, min_index, error_vector = calculate_cost_function(r2_target, positions)
        
        # 5. Résultats détaillés
        print(f"\n" + "="*60)
        print(f"RÉSULTATS")
        print(f"="*60)
        print(f"Fichier analysé: {trajectory_file}")
        print(f"Position cible r2: [{r2_target[0]:.0f}, {r2_target[1]:.0f}, {r2_target[2]:.0f}] km")
        print(f"Position finale du fichier: [{positions[-1,0]:.0f}, {positions[-1,1]:.0f}, {positions[-1,2]:.0f}] km")
        print(f"Norme position cible: {np.linalg.norm(r2_target):.0f} km")
        print(f"Norme position finale: {np.linalg.norm(positions[-1]):.0f} km")
        print(f"")
        print(f"[CIBLE] FONCTION DE COÛT:")
        print(f"   f_i = min_t ||r2 - r2_i(t)|| = {f_i:.6f} km")
        print(f"")
        print(f"DÉTAILS:")
        print(f"   Point le plus proche: {min_index}/{len(positions)} ({min_index/len(positions)*100:.1f}% de la trajectoire)")
        print(f"   Temps correspondant: {times[min_index]:.6f} MJD ({mjd_to_date(times[min_index]).strftime('%Y-%m-%d %H:%M:%S')} UTC)")
        print(f"   Position atteinte: [{positions[min_index,0]:.0f}, {positions[min_index,1]:.0f}, {positions[min_index,2]:.0f}] km")
        print(f"   Erreur vectorielle: [{error_vector[0]:.0f}, {error_vector[1]:.0f}, {error_vector[2]:.0f}] km")
        print(f"   Norme de l'erreur: {np.linalg.norm(error_vector):.6f} km")
        
        # 6. Calculs des différences demandées
        # Position finale de la trajectoire
        r2_final = positions[-1]
        final_error_vector = r2_target - r2_final
        final_distance = np.linalg.norm(final_error_vector)
        
        print(f"")
        print(f"[POSITION] ANALYSES COMPARATIVES:")
        print(f"   Position finale atteinte: [{r2_final[0]:.0f}, {r2_final[1]:.0f}, {r2_final[2]:.0f}] km")
        print(f"   Temps final: {times[-1]:.6f} MJD ({mjd_to_date(times[-1]).strftime('%Y-%m-%d %H:%M:%S')} UTC)")
        print(f"   Distance finale vs cible: {final_distance:.6f} km")
        print(f"   Erreur vectorielle finale: [{final_error_vector[0]:.0f}, {final_error_vector[1]:.0f}, {final_error_vector[2]:.0f}] km")
        print(f"")
        print(f"   [COMPARAISON]:")
        print(f"   Distance optimale (point le plus proche): {f_i:.6f} km")
        print(f"   Distance finale (dernier point): {final_distance:.6f} km")
        print(f"   Amélioration optimale vs finale: {final_distance - f_i:.6f} km ({((final_distance - f_i)/final_distance)*100:.1f}%)")
        
        # 8. Sauvegarder les résultats
        output_dir = os.path.dirname(trajectory_file)
        if not output_dir:
            output_dir = "."
        
        results_file = os.path.join(output_dir, "cost_function_results.txt")
        with open(results_file, 'w') as f:
            f.write(f"=== RÉSULTATS FONCTION DE COÛT ===\n")
            f.write(f"Date de calcul: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Fichier trajectoire: {trajectory_file}\n")
            f.write(f"Position cible r2: [{r2_target[0]:.6e}, {r2_target[1]:.6e}, {r2_target[2]:.6e}] km\n")
            f.write(f"\n")
            f.write(f"FONCTION DE COÛT:\n")
            f.write(f"f_i = {f_i:.6f} km\n")
            f.write(f"\n")
            f.write(f"DÉTAILS:\n")
            f.write(f"Point optimal: {min_index}/{len(positions)}\n")
            f.write(f"Temps optimal: {times[min_index]:.6f} MJD ({mjd_to_date(times[min_index]).strftime('%Y-%m-%d %H:%M:%S')} UTC)\n")
            f.write(f"Position atteinte: [{positions[min_index,0]:.6e}, {positions[min_index,1]:.6e}, {positions[min_index,2]:.6e}] km\n")
            f.write(f"Erreur vectorielle: [{error_vector[0]:.6e}, {error_vector[1]:.6e}, {error_vector[2]:.6e}] km\n")
            f.write(f"\n")
            f.write(f"ANALYSES COMPARATIVES:\n")
            f.write(f"Position finale: [{r2_final[0]:.6e}, {r2_final[1]:.6e}, {r2_final[2]:.6e}] km\n")
            f.write(f"Temps final: {times[-1]:.6f} MJD ({mjd_to_date(times[-1]).strftime('%Y-%m-%d %H:%M:%S')} UTC)\n")
            f.write(f"Distance finale vs cible: {final_distance:.6f} km\n")
            f.write(f"Erreur vectorielle finale: [{final_error_vector[0]:.6e}, {final_error_vector[1]:.6e}, {final_error_vector[2]:.6e}] km\n")
            f.write(f"Amélioration optimale vs finale: {final_distance - f_i:.6f} km\n")
        
        print(f"\n[SAUVEGARDE] Résultats sauvegardés dans: {results_file}")
        
    except Exception as e:
        print(f"[ERREUR] Erreur: {e}")
        return 1
    
    print(f"\n[FIN] Calcul terminé avec succès!")
    return 0

if __name__ == "__main__":
    exit(main())