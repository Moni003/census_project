# run_solver.py
import sys
import os
sys.path.append(os.path.dirname(__file__))  # ajoute la racine
from solver.solver import run_solver


if __name__ == "__main__":
    r0, v0, score = run_solver()
    print("Best score:", score)
    print("Best r0 (m):", r0)
    print("Best v0 (m/s):", v0)