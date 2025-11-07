"""tle_to_orbital_params.py

Lit un fichier TLE (trois lignes par objet: nom, line1, line2) et extrait
les paramètres orbitaux présents dans le TLE. Écrit le résultat dans
`orbital_params.csv` (CSV avec en-tête).

Ce script n'utilise aucune dépendance externe — il parse les champs fixes
du format TLE.
"""

from __future__ import annotations
import argparse
import csv
from datetime import datetime, timedelta
from typing import Tuple
import math


def parse_epoch_from_line1(line1: str) -> str:
    """Extrait l'époque du TLE (YYDDD.DDD...) et retourne ISO string UTC."""
    # Colonnes 19-20 -> année (YY), 21-32 -> jour de l'année et fraction (DDD.DDDDDDDD)
    yy = line1[18:20]
    ddd = line1[20:32]
    try:
        year = int(yy)
        year += 2000 if year < 57 else 1900  # convention TLE
        day_of_year = float(ddd)
        day_integer = int(day_of_year)
        fractional = day_of_year - day_integer
        epoch = datetime(year, 1, 1) + timedelta(days=day_integer - 1, seconds=fractional * 86400)
        return epoch.isoformat() + "Z"
    except Exception:
        return ""


def parse_line2(line2: str) -> Tuple[float, float, float, float, float, float]:
    """Parse line2 et renvoie (inc_deg, raan_deg, ecc, argp_deg, mean_anom_deg, mean_motion_rev_per_day).

    Les positions sont basées sur le format TLE standard (0-index dans les slices).
    """
    # Many TLE parsers use these slices (0-indexed):
    # inclination: cols 9-16 -> [8:16]
    # RAAN: cols 18-25 -> [17:25]
    # eccentricity (no decimal): cols 27-33 -> [26:33]
    # arg of perigee: cols 35-42 -> [34:42]
    # mean anomaly: cols 44-51 -> [43:51]
    # mean motion: cols 52-63 -> [52:63]
    try:
        inc = float(line2[8:16].strip())
    except Exception:
        inc = float('nan')
    try:
        raan = float(line2[17:25].strip())
    except Exception:
        raan = float('nan')
    try:
        ecc_str = line2[26:33].strip()
        ecc = float("0." + ecc_str) if ecc_str else float('nan')
    except Exception:
        ecc = float('nan')
    try:
        argp = float(line2[34:42].strip())
    except Exception:
        argp = float('nan')
    try:
        mean_anom = float(line2[43:51].strip())
    except Exception:
        mean_anom = float('nan')
    try:
        mean_motion = float(line2[52:63].strip())
    except Exception:
        mean_motion = float('nan')

    return inc, raan, ecc, argp, mean_anom, mean_motion


def mean_motion_to_sma(mean_motion_rev_per_day: float, mu: float = 398600.4418) -> float:
    """Convertit le mouvement moyen (rev/day) en demi-grand axe (km) via la loi de Kepler.

    a = (mu / n^2)^{1/3}, avec n en rad/s.
    mu par défaut = 398600.4418 km^3/s^2 (Terre)
    """
    try:
        if mean_motion_rev_per_day is None or math.isnan(mean_motion_rev_per_day):
            return float('nan')
        n = mean_motion_rev_per_day * 2.0 * math.pi / 86400.0  # rev/day -> rad/s
        a = (mu / (n * n)) ** (1.0 / 3.0)
        return a
    except Exception:
        return float('nan')


def mean_to_true_anomaly(mean_anom_deg: float, e: float) -> float:
    """Convertit anomalie moyenne (deg) en anomalie vraie (deg) pour orbite elliptique.

    Résolution numérique de l'équation de Kepler pour obtenir l'anomalie excentrique E,
    puis conversion en anomalie vraie v.
    """
    try:
        if mean_anom_deg is None or math.isnan(mean_anom_deg) or e is None or math.isnan(e):
            return float('nan')
        M = math.radians(mean_anom_deg) % (2.0 * math.pi)
        # cas quasi-circulaire
        if abs(e) < 1e-12:
            return math.degrees(M)

        # initial guess
        E = M if e < 0.8 else math.pi
        for _ in range(60):
            f = E - e * math.sin(E) - M
            fprime = 1 - e * math.cos(E)
            if abs(fprime) < 1e-16:
                break
            delta = f / fprime
            E -= delta
            if abs(delta) < 1e-12:
                break

        # calcul de l'anomalie vraie
        cosE = math.cos(E)
        sinE = math.sin(E)
        denom = 1 - e * cosE
        if abs(denom) < 1e-16:
            v = 0.0
        else:
            sin_v = math.sqrt(1 - e * e) * sinE / denom
            cos_v = (cosE - e) / denom
            v = math.atan2(sin_v, cos_v)

        return math.degrees(v) % 360.0
    except Exception:
        return float('nan')


def process_tle_file(input_path: str, output_csv: str) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [ln.rstrip('\n') for ln in f if ln.strip() != '']

    # Expect groups of 3 lines: name, line1, line2
    rows = []
    i = 0
    while i + 2 < len(lines):
        name = lines[i].strip()
        line1 = lines[i+1].rstrip() if i+1 < len(lines) else ''
        line2 = lines[i+2].rstrip() if i+2 < len(lines) else ''

        epoch_iso = parse_epoch_from_line1(line1) if line1 else ''
        inc, raan, ecc, argp, mean_anom, mean_motion = parse_line2(line2) if line2 else (None,)*6

        # Calculer demi-grand axe (km) à partir du mouvement moyen (rev/day)
        demi_grand_axe_km = mean_motion_to_sma(mean_motion)

        # Calculer l'anomalie vraie (deg) à partir de l'anomalie moyenne (deg) et excentricité
        anomalie_vraie_deg = mean_to_true_anomaly(mean_anom, ecc)

        rows.append({
            'nom': name,
            'epoque_utc': epoch_iso,
            'demi_grand_axe_km': demi_grand_axe_km,
            'excentricite': ecc,
            'inclinaison_deg': inc,
            'noeud_ascendant_deg': raan,
            'argument_perigee_deg': argp,
            'anomalie_vraie_deg': anomalie_vraie_deg,
        })

        i += 3

    # Écrire CSV
    fieldnames = ['nom', 'epoque_utc', 'demi_grand_axe_km', 'excentricite', 'inclinaison_deg',
                  'noeud_ascendant_deg', 'argument_perigee_deg', 'anomalie_vraie_deg']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"✅ {len(rows)} TLE(s) traités. Fichier de sortie : {output_csv}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Extraire paramètres orbitaux depuis un fichier TLE vers CSV')
    parser.add_argument('-i', '--input', default='tle.txt', help='Chemin vers le fichier TLE (par défaut: tle.txt)')
    parser.add_argument('-o', '--output', default='orbital_params.csv', help='Fichier CSV de sortie')
    args = parser.parse_args()

    process_tle_file(args.input, args.output)


if __name__ == '__main__':
    main()

