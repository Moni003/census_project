# predefined_bodies.py - Corps célestes prédéfinis pour le solveur Monte Carlo
"""
Contient les données des corps célestes utilisés par le solveur de trajectoire Monte Carlo.
Données: paramètre gravitationnel standard μ (m³/s²) et rayon (m)
"""
import numpy as np

# Constante gravitationnelle universelle
G = 6.67430e-11  # m³/kg/s²

# Données des corps du système solaire : [μ (m³/s²), rayon (m)]
# μ = GM où M est la masse du corps
known_bodies = {
    "sun":     [1.3271244004194e20, 696000000],      # Soleil
    "mercury": [2.2032080493345e13, 2440530],        # Mercure
    "venus":   [3.248586068371049e14, 6051800],      # Vénus
    "earth":   [3.98659293629478e14, 6378136.3],     # Terre
    "moon":    [4.843941639988467e12, 1738000],      # Lune
    "mars":    [4.28283132893115e13, 3396190],       # Mars
    "jupiter": [1.26686536751784e17, 71492000],      # Jupiter
    "saturn":  [3.79312396775046e16, 60268000],      # Saturne
    "uranus":  [5.79393921281797e15, 25559000],      # Uranus
    "neptune": [6.83509920358736e15, 24764000]       # Neptune
}

def get_body_mu(body_name):
    """
    Retourne le paramètre gravitationnel μ d'un corps céleste.
    
    Paramètres:
    - body_name: nom du corps (string)
    
    Retourne:
    - μ: paramètre gravitationnel en m³/s²
    """
    if body_name.lower() in known_bodies:
        return known_bodies[body_name.lower()][0]
    else:
        raise ValueError(f"Corps '{body_name}' non reconnu. Corps disponibles: {list(known_bodies.keys())}")

def get_body_radius(body_name):
    """
    Retourne le rayon d'un corps céleste.
    
    Paramètres:
    - body_name: nom du corps (string)
    
    Retourne:
    - rayon: rayon en mètres
    """
    if body_name.lower() in known_bodies:
        return known_bodies[body_name.lower()][1]
    else:
        raise ValueError(f"Corps '{body_name}' non reconnu. Corps disponibles: {list(known_bodies.keys())}")

def get_body_info(body_name):
    """
    Retourne toutes les informations d'un corps céleste.
    
    Paramètres:
    - body_name: nom du corps (string)
    
    Retourne:
    - tuple: (μ, rayon)
    """
    if body_name.lower() in known_bodies:
        return known_bodies[body_name.lower()]
    else:
        raise ValueError(f"Corps '{body_name}' non reconnu. Corps disponibles: {list(known_bodies.keys())}")

def list_available_bodies():
    """
    Affiche la liste des corps célestes disponibles avec leurs caractéristiques.
    """
    print("Corps célestes disponibles:")
    print("-" * 60)
    print(f"{'Nom':<10} {'μ (m³/s²)':<20} {'Rayon (m)':<15}")
    print("-" * 60)
    
    for name, (mu, radius) in known_bodies.items():
        print(f"{name:<10} {mu:<20.3e} {radius:<15.0f}")
    
    print("-" * 60)

def get_bodies_for_simulation(central_body, other_bodies):
    """
    Prépare les données des corps pour la simulation.
    
    Paramètres:
    - central_body: nom du corps central (string)
    - other_bodies: liste des noms des autres corps (list of strings)
    
    Retourne:
    - dict: dictionnaire avec les informations de tous les corps
    """
    simulation_bodies = {}
    
    # Ajouter le corps central
    simulation_bodies[central_body] = get_body_info(central_body)
    
    # Ajouter les autres corps
    for body in other_bodies:
        if body != central_body:  # Éviter les doublons
            simulation_bodies[body] = get_body_info(body)
    
    return simulation_bodies

# Affichage des informations au chargement du module (optionnel)
if __name__ == "__main__":
    print("=== Module predefined_bodies.py ===")
    list_available_bodies()