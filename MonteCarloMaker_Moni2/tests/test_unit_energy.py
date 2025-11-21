# tests/test_unit_energy.py
import numpy as np
from montecarlo_utils import orbital_elements_to_rv
from solver.config import ATTRACTOR, T0_STR


def test_energy_consistency():
# test : a calculé à partir de r,v doit retrouve