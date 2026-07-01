"""
biosafety_sensitivity.py — Pillar 4b: Sensitivity analysis for the
Luria-Delbrück containment claim.

The headline biosafety result (P_escape ~ 1.11e-16 over 30 days) is
sensitive to several input parameters. This script sweeps the two most
uncertain:

  1. MUTATION_RATE_PER_BP_PER_GEN — swept over x0.01, x0.1, x1, x10,
     x100 of the baseline value from parameters.py. The literature
     range for spontaneous E. coli per-bp mutation rate spans roughly
     1e-10 to 1e-9, and the baseline (1e-9) sits at the conservative
     (higher) end; the sweep shows what happens if the true rate is
     even higher than assumed.

  2. POPULATION_VOLUME_L — swept over a few plausible closed-system
     deployment scales (10 L benchtop, 100 L pilot, 1000 L default,
     10000 L industrial).

Outputs:
  - results/sensitivity_analysis.png    (two-panel figure: top =
    P_escape vs. mutation-rate scaling at the 30-day headline; bottom
    = P_escape vs. reactor volume)
  - results/sensitivity_analysis.csv    (the underlying numbers, for
    inclusion in the manuscript's supplementary table)

The script answers the question the manuscript MUST address:
does the P_escape < 1e-15 headline claim survive a 10x or 100x error
in the mutation rate assumption? See Section 4.4.1 of the manuscript.

All numerical constants are imported from parameters.py.
"""

import csv
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parameters import (
    MUTATION_RATE_PER_BP_PER_GEN, TARGET_SIZE_BP,
    HGT_P_REVERT_THYA_PER_DIV, HGT_P_REVERT_DAPA_PER_DIV,
    MAX_CELL_DENSITY_PER_L, GENERATIONS_PER_DAY, DEPLOYMENT_WINDOW_DAYS,
    POPULATION_VOLUME_L, DE_MINIMIS_RISK_THRESHOLD,
)

MUTATION_SCALING_FACTORS = [0.01, 0.1, 1.0, 10.0, 100.0]
VOLUME_SCALING_FACTORS = [0.01, 0.1, 1.0, 10.0]  # relative to POPULATION_VOLUME_L


def _prob_escape(N, G, p):
    """Poisson approximation: P(at least 1) = 1 - e^(-N*G*p).

    For very small N*G*p (typical of the 30-day full-containment
    scenario, where N*G*p ~ 6e-17), direct evaluation of 1 - exp(-x)
    suffers from catastrophic cancellation in IEEE-754 floating point
    and returns ~1.11e-16 instead of the analytically correct 6e-17.
    We use the first-order Taylor expansion 1 - exp(-x) ~ x for x
    below a threshold, which is the physics-correct answer and matches
    biosafety_mutation_model.py.
    """
    x = np.asarray(N * G * p, dtype=float)
    return np.where(x < 1e-10, x, 1.0 - np.exp(-x))


def run_sensitivity():
    # -----------------------------------------------------------------
    # Per-division probabilities (do not depend on N or G)
    # -----------------------------------------------------------------
    p_ks_fail = MUTATION_RATE_PER_BP_PER_GEN * TARGET_SIZE_BP
    p_double_revert = HGT_P_REVERT_THYA_PER_DIV * HGT_P_REVERT_DAPA_PER_DIV
    p_combined_base = p_ks_fail * p_double_revert
    G = GENERATIONS_PER_DAY * DEPLOYMENT_WINDOW_DAYS  # total generations in window

    # -----------------------------------------------------------------
    # Sweep 1: mutation-rate scaling (default volume = 1000 L)
    # -----------------------------------------------------------------
    N_default = POPULATION_VOLUME_L * MAX_CELL_DENSITY_PER_L
    rows = []
    p_esc_by_scale = []
    for s in MUTATION_SCALING_FACTORS:
        p_ks_s = p_ks_fail * s
        p_combined_s = p_ks_s * p_double_revert
        p_esc = _prob_escape(N_default, G, p_combined_s)
        p_esc_by_scale.append(p_esc)
        rows.append({
            'axis': 'mutation_rate_scaling',
            'value': s,
            'p_combined_per_div': p_combined_s,
            'N_total_cells': N_default,
            'G_total': G,
            'p_escape_30d': p_esc,
            'passes_1e-15_threshold': p_esc < DE_MINIMIS_RISK_THRESHOLD,
        })

    # -----------------------------------------------------------------
    # Sweep 2: reactor volume (default mutation rate)
    # -----------------------------------------------------------------
    p_esc_by_volume = []
    for s in VOLUME_SCALING_FACTORS:
        V = POPULATION_VOLUME_L * s
        N = V * MAX_CELL_DENSITY_PER_L
        p_esc = _prob_escape(N, G, p_combined_base)
        p_esc_by_volume.append(p_esc)
        rows.append({
            'axis': 'reactor_volume_L',
            'value': V,
            'p_combined_per_div': p_combined_base,
            'N_total_cells': N,
            'G_total': G,
            'p_escape_30d': p_esc,
            'passes_1e-15_threshold': p_esc < DE_MINIMIS_RISK_THRESHOLD,
        })

    # -----------------------------------------------------------------
    # Print summary table
    # -----------------------------------------------------------------
    print("=" * 78)
    print("BIOSAFETY SENSITIVITY ANALYSIS (Pillar 4b)")
    print(f"Baseline: V={POPULATION_VOLUME_L} L, N={N_default:.2e}, "
          f"G={G} gens, mu_bp={MUTATION_RATE_PER_BP_PER_GEN:.0e}")
    print(f"Acceptable risk threshold: P_escape < {DE_MINIMIS_RISK_THRESHOLD:.0e}")
    print("-" * 78)
    print(f"{'axis':<24}{'value':>14}{'N_total':>14}{'P_escape (30d)':>22}")
    print("-" * 78)
    for r in rows:
        v = r['value']
        if r['axis'] == 'mutation_rate_scaling':
            vstr = f"x{v:g}"
        else:
            vstr = f"{v:.0f} L"
        print(f"{r['axis']:<24}{vstr:>14}{r['N_total_cells']:>14.2e}"
              f"{r['p_escape_30d']:>22.3e}")
    print("=" * 78)

    # -----------------------------------------------------------------
    # Write CSV
    # -----------------------------------------------------------------
    os.makedirs('results', exist_ok=True)
    csv_path = 'results/sensitivity_analysis.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {csv_path}")

    # -----------------------------------------------------------------
    # Plot
    # -----------------------------------------------------------------
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Panel 1: P_escape vs mutation-rate scaling
    axs[0].plot(MUTATION_SCALING_FACTORS, p_esc_by_scale, 'o-', color='C0',
                linewidth=2.5, markersize=10)
    axs[0].set_xscale('log')
    axs[0].set_yscale('log')
    axs[0].axhline(y=DE_MINIMIS_RISK_THRESHOLD, color='orange', linestyle=':',
                   label=f'Acceptable risk ({DE_MINIMIS_RISK_THRESHOLD:.0e})')
    axs[0].axhline(y=1.0, color='red', linestyle=':', label='P_escape = 1 (certain failure)')
    axs[0].set_xlabel('Mutation-rate scaling factor (relative to baseline '
                      f'{MUTATION_RATE_PER_BP_PER_GEN:.0e} per bp/gen)')
    axs[0].set_ylabel('P_escape over 30 days')
    axs[0].set_title(f'Effect of Mutation-Rate Assumption\n'
                     f'(V={POPULATION_VOLUME_L} L, 1e12 cells, '
                     f'{DEPLOYMENT_WINDOW_DAYS} d)')
    axs[0].grid(True, which='both', ls='-', alpha=0.3)
    axs[0].legend()

    # Panel 2: P_escape vs reactor volume
    volumes = [POPULATION_VOLUME_L * s for s in VOLUME_SCALING_FACTORS]
    axs[1].plot(volumes, p_esc_by_volume, 's-', color='C2',
                linewidth=2.5, markersize=10)
    axs[1].set_xscale('log')
    axs[1].set_yscale('log')
    axs[1].axhline(y=DE_MINIMIS_RISK_THRESHOLD, color='orange', linestyle=':',
                   label=f'Acceptable risk ({DE_MINIMIS_RISK_THRESHOLD:.0e})')
    axs[1].axhline(y=1.0, color='red', linestyle=':', label='P_escape = 1 (certain failure)')
    axs[1].set_xlabel('Reactor volume (L)')
    axs[1].set_ylabel('P_escape over 30 days')
    axs[1].set_title(f'Effect of Deployment Scale\n'
                     f'(baseline mu_bp={MUTATION_RATE_PER_BP_PER_GEN:.0e} per bp/gen)')
    axs[1].grid(True, which='both', ls='-', alpha=0.3)
    axs[1].legend()

    plt.tight_layout()
    fig_path = 'results/sensitivity_analysis.png'
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Wrote {fig_path}")


if __name__ == "__main__":
    run_sensitivity()
