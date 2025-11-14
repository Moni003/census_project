from singleshooting_utils import single_shooting, write_docks_file, parse_isot
from predefined_bodies import known_bodies
import numpy as np

print("\n=== SingleShootingMaker ===\n")

# 1. Date initiale
t1_str = input("Enter the initial date and time in ISOT format [default: 2025-01-01T12:00:00]: ") or "2025-01-01T12:00:00"
t1_dt = parse_isot(t1_str)

# 2. Choix du corps central
bodies_names = list(known_bodies.keys())
print("\nSelect the central body:")
for i, b in enumerate(bodies_names):
    print(f"{i}: {b}")
body_index = int(input("Choose a body by its number : "))
body_selected = bodies_names[body_index]
mu = known_bodies[body_selected][0]
print(f"Body selected: {body_selected}\n")

# 3. Paramètres d'estimation et cible
r0_guess = np.array([float(x) for x in input("Enter initial guess position r0 [m] (x y z): ").split()])
v0_guess = np.array([float(x) for x in input("Enter initial guess velocity v0 [m/s] (vx vy vz): ").split()])
rf_target = np.array([float(x) for x in input("Enter target position rf [m] (x y z): ").split()])
t_final_hours = float(input("Enter time of flight [hours]: "))
t_span = [0, t_final_hours * 3600]

# 4. Single Shooting
r0_sol, v0_sol = single_shooting(r0_guess, v0_guess, rf_target, t_span, mu)

print("\nSolution found:")
print("r0 (m):", r0_sol)
print("v0 (m/s):", v0_sol)

# 5. Génération fichier DOCKS
write_docks_file(f"InitCond_SingleShooting_{body_selected}.txt", t1_str, r0_sol, v0_sol)
print("\n=== End of script ===")
