# main_mc.py
import numpy as np
from datetime import datetime
from mc_utils import propagate, f1_cost, write_docks_file
from predefined_bodies import known_bodies
from tqdm import trange


print("\n=== MonteCarloSolverMultiCorps ===\n")


# 1. Date initiale
t0_str = input("Enter the initial date and time [YYYY-MM-DDTHH:MM:SS] [default 2025-01-01T12:00:00]: ") \
         or "2025-01-01T12:00:00"
t0_dt = datetime.fromisoformat(t0_str)


# 2. Corps central
bodies_names = list(known_bodies.keys())
print("\nSelect the central body:")
for i, b in enumerate(bodies_names):
    print(f"{i}: {b}")
body_index = input(f"Choose a body by number [default 3 = earth]: ") or "3"
body_index = int(body_index)
central_body = bodies_names[body_index]


# 3. Deux autres corps
print("\nSelect two additional bodies for gravity (comma-separated indices) [default 0,4 = sun, moon]:")
for i, b in enumerate(bodies_names):
    if b != central_body:
        print(f"{i}: {b}")
other_input = input("Enter indices: ") or "0,4"  # par défaut Soleil et Lune
other_indices = [int(i) for i in other_input.split(",")]
other_bodies = [bodies_names[i] for i in other_indices if bodies_names[i] != central_body]


print(f"Bodies included: {central_body} + {other_bodies}\n")


# 4. Paramètres initiaux
r1 = np.array([
    float(input("R1 x (m) [default 7e6]: ") or 7e6),
    float(input("R1 y (m) [default 0]: ") or 0.0),
    float(input("R1 z (m) [default 0]: ") or 0.0)
])

r2 = np.array([
    float(input("R2 x (m) [default 4.2e7]: ") or 4.2e7),
    float(input("R2 y (m) [default 0]: ") or 0.0),
    float(input("R2 z (m) [default 0]: ") or 0.0)
])

v2 = np.array([   
    float(input("V2 x (m/s) [default 0]: ") or 0.0),
    float(input("V2 y (m/s) [default 3e3]: ") or 3e3),
    float(input("V2 z (m/s) [default 0]: ") or 0.0)
]) # à quoi il sert vu qu'on ne l'utilise pas ?

# 4b. V1 fourni par Lambert
v1_guess = np.array([
    float(input("V1 x (m/s) [default 1e3]: ") or 1e3),
    float(input("V1 y (m/s) [default 1e3]: ") or 1e3),
    float(input("V1 z (m/s) [default 0]: ") or 0.0)
])


# 5. Paramètres Monte Carlo
N_samples = int(input("Number of Monte Carlo samples [default 500]: ") or 500)
tolerance_percent = float(input("Tolerance (percent) [default 1]: ") or 1.0)
tof = float(input("Time of flight Δt (s) [default 86400 = 1 day]: ") or 86400)

# --- Préparer les corps pour gravité ---
bodies_mu = []
for name in [central_body] + other_bodies:
    mu = known_bodies[name][0]
    r_body = np.array([0.0, 0.0, 0.0])  # approximation simple
    bodies_mu.append((r_body, mu))

tol = tolerance_percent / 100 * np.linalg.norm(r2 - r1)


# --- Préparer pour stocker tous les f1 ---
all_f1 = []       # liste pour stocker tous les f1
all_v1 = []       # liste pour stocker les v1 correspondants
all_r2i = []      # liste pour stocker les r2i correspondants


# --- Boucle Monte Carlo ---
best_f1 = np.inf
best_r2i = None
best_v1 = None
rng = np.random.default_rng(42)

for i in trange(N_samples, desc="Monte Carlo Progress"):
    # Tirage uniforme ±1% autour de v1_guess
    delta_v = rng.uniform(-0.01*np.linalg.norm(v1_guess), 0.01*np.linalg.norm(v1_guess), 3)   # ?????
    v1_trial = v1_guess + delta_v

    # Propagation
    prop = propagate(r1, v1_trial, bodies_mu)
    r2i = prop[:3]
    print(" r2i(t):", r2i)
    print(" r2(t):", r2)


    # Fonction de coût f1
    f1i = f1_cost(r2, r2i)
    print(f" f1:", f1i)
    #print(f"Trial {i+1}: v1 = {v1_trial}, r2i = {r2i}, f1 = {f1}\n")

    """if f1i <= tol:
        if f1i < best_f1:
            print(f"✅New best f1: {f1i} with v1: {v1_trial} and r2i: {r2i}\n")
            best_f1 = f1i
            best_r2i = r2i
            best_v1 = v1_trial

    print(f"✅New best f1: {f1i} with v1: {v1_trial} and r2i: {r2i}\n")
    best_f1 = f1i
    best_r2i = r2i
    best_v1 = v1_trial"""

    # Stocker les résultats
    all_f1.append(f1i)
    all_v1.append(v1_trial)
    all_r2i.append(r2i)

    # Affichage pour suivi
    print(f"Trial {i+1}: f1 = {f1i}, v1 = {v1_trial}, r2i = {r2i}")



# Fonction de coût f2
#f2 = best_f1

# --- Calcul du minimum final ---
best_index = np.argmin(all_f1)        # index de la plus petite f1
f2 = all_f1[best_index]               # valeur minimale
best_v1 = all_v1[best_index]          # v1 correspondant
best_r2i = all_r2i[best_index]        # r2i correspondant


# --- Résultats ---
print("\n=== Résultat Monte Carlo ===")
print(f"Vitesse initiale optimale v1 : {best_v1}")
print(f"Position finale r2i : {best_r2i}")
print(f"Fonction de coût f2: {f2}")


# Générer fichier DOCKS
write_docks_file(f"best_solution_mc_{central_body}.txt", t0_str, r1, best_v1)

print("\n=== End of Monte Carlo Script ===")
