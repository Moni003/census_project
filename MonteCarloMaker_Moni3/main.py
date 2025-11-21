
# main_mc.py
import numpy as np
from datetime import datetime
from mc_utils import propagate, score_final_state, write_docks_file
from predefined_bodies import known_bodies

print("\n=== MonteCarloSolverMultiCorps ===\n")

# 1. Date initiale
t0_str = input("Enter the initial date and time [YYYY-MM-DDTHH:MM:SS] [default 2025-01-01T12:00:00]: ") \
         or "2025-01-01T12:00:00"
t0_dt = datetime.fromisoformat(t0_str)

# 2. Choix du corps central
bodies_names = list(known_bodies.keys())
print("\nSelect the central body:")
for i, b in enumerate(bodies_names):
    print(f"{i}: {b}")
body_index = int(input("Choose a body by number: "))
body_selected = bodies_names[body_index]
mu_central = known_bodies[body_selected][0]  # μ du corps central
print(f"Body selected: {body_selected}\n")

# 3. Paramètres initiaux (position et vitesse moyennes)
r_mean = np.array([float(input("R0 x (m) [default 1e11]: ") or 1e11),
                   float(input("R0 y (m) [default 0]: ") or 0.0),
                   float(input("R0 z (m) [default 0]: ") or 0.0)])
v_mean = np.array([float(input("V0 x (m/s) [default 0]: ") or 0.0),
                   float(input("V0 y (m/s) [default sqrt(mu/r)]: ") or np.sqrt(mu_central/np.linalg.norm(r_mean))),
                   float(input("V0 z (m/s) [default 0]: ") or 0.0)])

# 4. Durée du transfert
tof_hours = float(input("\nEnter transfer duration ΔT (hours) [default 720]: ") or 720)
tof_seconds = tof_hours * 3600

# 5. Cible finale
target_str = input("Enter target coordinates x,y,z (m) [default 1.5e11,0,0]: ") or "1.5e11,0,0"
TARGET_B = np.array([float(x) for x in target_str.split(",")])

# 6. Monte Carlo
N_SAMPLES = int(input("Number of Monte Carlo samples [default 500]: ") or 500)
R_SPREAD = float(input("Position spread (m) [default 1e10]: ") or 1e10)
V_SPREAD = float(input("Velocity spread (m/s) [default 1e3]: ") or 1e3)

# Création de la liste des perturbateurs (position et μ)
perturbers = [(np.array([1.496e11, 0, 0]), known_bodies["earth"][0]),
              (np.array([2.279e11, 0, 0]), known_bodies["mars"][0])]
# On peut filtrer le corps central
perturbers = [(r, mu) for r, mu in perturbers if mu != mu_central]

best_score = np.inf
best_r0 = None
best_v0 = None
rng = np.random.default_rng(42)

for i in range(N_SAMPLES):
    # Génération aléatoire autour de r_mean et v_mean
    r0 = r_mean + rng.uniform(-R_SPREAD, R_SPREAD, size=3)
    v0 = v_mean + rng.uniform(-V_SPREAD, V_SPREAD, size=3)

    # Propagation multi-corps
    state_f = propagate(r0, v0, tof_seconds, mu_central, perturbers)
    sc = score_final_state(state_f, TARGET_B)

    if sc < best_score:
        best_score = sc
        best_r0 = r0
        best_v0 = v0

# 7. Résultats
print(f"\nBest final distance to target: {best_score:.3e} m")
write_docks_file(f"best_solution_mc_{body_selected}.txt", t0_str, best_r0, best_v0)
print("\n=== End of Monte Carlo Script ===")
