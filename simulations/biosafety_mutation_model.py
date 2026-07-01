"""
biosafety_mutation_model.py — Pillar 4: Luria-Delbrück evolutionary
biosafety modeling for the layered containment architecture.

Outputs TWO figures:
  - results/biosafety_mutation_model.png         (the 365-day long-run view,
                                                  used in main text as the
                                                  full-timescale
                                                  supplementary-style plot)
  - results/biosafety_mutation_30day.png         (cropped to the 30-day
                                                  deployment window that the
                                                  hypothesis explicitly
                                                  targets; this is the
                                                  figure referenced in
                                                  Section 4.4 of the
                                                  manuscript main text)

Both figures share the same model — only the x-axis window differs.
The 30-day view is produced to resolve the previous mismatch where
the script plotted to 350+ days while the manuscript's stated
deployment window and hypothesis are 30 days.

All numerical constants are imported from parameters.py.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parameters import (
    MUTATION_RATE_PER_BP_PER_GEN,
    TARGET_SIZE_BP,
    HGT_P_REVERT_THYA_PER_DIV,
    HGT_P_REVERT_DAPA_PER_DIV,
    POPULATION_VOLUME_L, MAX_CELL_DENSITY_PER_L, TOTAL_CELL_COUNT,
    GENERATIONS_PER_DAY, DEPLOYMENT_WINDOW_DAYS,
    DE_MINIMIS_RISK_THRESHOLD,
)

def _prob_escape(N, G, p):
    """Poisson approximation: P(at least 1) = 1 - e^(-N*G*p).

    For very small N*G*p (typical of the 30-day full-containment
    scenario, where N*G*p ~ 6e-17), direct evaluation of 1 - exp(-x)
    suffers from catastrophic cancellation in IEEE-754 floating point
    and returns ~1.11e-16 instead of the analytically correct 6e-17.
    We use the first-order Taylor expansion 1 - exp(-x) ~ x for x
    below a threshold, which is the physics-correct answer and matches
    the algebraic walkthrough shown in the manuscript.

    Accepts scalar or numpy-array G; N and p are broadcast.
    """
    x = np.asarray(N * G * p, dtype=float)
    return np.where(x < 1e-10, x, 1.0 - np.exp(-x))

def calculate_probabilities():
    # -----------------------------------------------------------------
    # 1. Per-cell-per-generation failure probabilities
    # -----------------------------------------------------------------
    P_ks_fail_per_gen = MUTATION_RATE_PER_BP_PER_GEN * TARGET_SIZE_BP
    P_revert_thyA = HGT_P_REVERT_THYA_PER_DIV
    P_revert_dapA = HGT_P_REVERT_DAPA_PER_DIV
    P_double_revert = P_revert_thyA * P_revert_dapA

    # Combined: cell must (escape kill switch) AND (escape both auxotrophies)
    P_total_escape_per_gen = P_ks_fail_per_gen * P_double_revert

    total_generations = GENERATIONS_PER_DAY * DEPLOYMENT_WINDOW_DAYS

    print("=" * 70)
    print("LURIA-DELBRUCK CONTAINMENT ANALYSIS")
    print("=" * 70)
    print(f"Kill switch failure rate:        {P_ks_fail_per_gen:.2e} per division")
    print(f"  (mu_bp={MUTATION_RATE_PER_BP_PER_GEN:.0e} x target {TARGET_SIZE_BP} bp)")
    print(f"Auxotrophy HGT reversion:        thyA={P_revert_thyA:.0e}, "
          f"dapA={P_revert_dapA:.0e}")
    print(f"Double auxotrophy escape:        {P_double_revert:.2e} per division")
    print(f"Combined per-division escape:    {P_total_escape_per_gen:.2e}")
    print(f"Deployment scale:                {POPULATION_VOLUME_L} L x "
          f"{MAX_CELL_DENSITY_PER_L:.0e} cells/L = {TOTAL_CELL_COUNT:.0e} cells")
    print(f"Deployment window:               {DEPLOYMENT_WINDOW_DAYS} days "
          f"@ {GENERATIONS_PER_DAY} gen/day = {total_generations} generations")
    print("-" * 70)

    # -----------------------------------------------------------------
    # 2. Probabilities over time for two containment layers
    # -----------------------------------------------------------------
    days_long = np.arange(1, 366)
    gens_long = days_long * GENERATIONS_PER_DAY
    p_fail_ks_only_long = _prob_escape(TOTAL_CELL_COUNT, gens_long, P_ks_fail_per_gen)
    p_fail_all_long = _prob_escape(TOTAL_CELL_COUNT, gens_long, P_total_escape_per_gen)
    p_fail_all_long_plot = np.maximum(p_fail_all_long, 1e-35)

    days_30 = np.arange(1, DEPLOYMENT_WINDOW_DAYS + 1)
    gens_30 = days_30 * GENERATIONS_PER_DAY
    p_fail_ks_only_30 = _prob_escape(TOTAL_CELL_COUNT, gens_30, P_ks_fail_per_gen)
    p_fail_all_30 = _prob_escape(TOTAL_CELL_COUNT, gens_30, P_total_escape_per_gen)
    p_fail_all_30_plot = np.maximum(p_fail_all_30, 1e-35)

    # Headline numbers (over the 30-day window)
    prob_escape_30 = float(_prob_escape(
        TOTAL_CELL_COUNT,
        GENERATIONS_PER_DAY * DEPLOYMENT_WINDOW_DAYS,
        P_total_escape_per_gen
    ))
    print(f"Headline (30-day) P_escape:      {prob_escape_30:.2e}")
    print("=" * 70)

    # -----------------------------------------------------------------
    # 3. Plot the 365-day long-run view
    # -----------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(days_long, p_fail_ks_only_long, 'r--',
            label='Kill Switch Only (Layer 1)')
    ax.plot(days_long, p_fail_all_long_plot, 'g-',
            label='Full 5-Layer Containment (inc. Auxotrophy)')
    ax.set_yscale('log')
    ax.set_ylim([1e-35, 1.5])
    ax.set_xlim([1, 365])
    ax.set_xlabel('Days in Closed Pond (1000L, 1e12 total cells)')
    ax.set_ylabel('Probability of Containment Failure')
    ax.set_title('Evolutionary Stability & BMO Biosafety Risk Assessment\n'
                 '(365-day long-run view; see biosafety_mutation_30day.png '
                 'for the deployment-window view referenced in main text)')
    ax.axhline(y=DE_MINIMIS_RISK_THRESHOLD, color='orange', linestyle=':',
               label=f'Acceptable Risk Threshold ({DE_MINIMIS_RISK_THRESHOLD:.0e})')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend()
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/biosafety_mutation_model.png', dpi=300)
    plt.close()
    print("Saved 365-day view to results/biosafety_mutation_model.png")

    # -----------------------------------------------------------------
    # 4. Plot the 30-day deployment-window view (referenced in Sec 4.4)
    # -----------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(days_30, p_fail_ks_only_30, 'r--',
            label='Kill Switch Only (Layer 1)')
    ax.plot(days_30, p_fail_all_30_plot, 'g-',
            label='Full 5-Layer Containment (inc. Auxotrophy)')
    ax.set_yscale('log')
    ax.set_ylim([1e-35, 1.5])
    ax.set_xlim([1, DEPLOYMENT_WINDOW_DAYS])
    ax.set_xlabel('Days in Closed Pond (deployment window)')
    ax.set_ylabel('Probability of Containment Failure')
    ax.set_title(f'Evolutionary Stability over the {DEPLOYMENT_WINDOW_DAYS}-Day '
                 'Deployment Window\n(closed system, 1000 L, 1e12 cells)')
    ax.axhline(y=DE_MINIMIS_RISK_THRESHOLD, color='orange', linestyle=':',
               label=f'Acceptable Risk Threshold ({DE_MINIMIS_RISK_THRESHOLD:.0e})')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend()
    plt.savefig('results/biosafety_mutation_30day.png', dpi=300)
    plt.close()
    print(f"Saved {DEPLOYMENT_WINDOW_DAYS}-day deployment-window view to "
          "results/biosafety_mutation_30day.png")

if __name__ == "__main__":
    calculate_probabilities()
