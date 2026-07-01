"""
metabolic_burden_model.py — Pillar 3: Ribosome allocation / metabolic
burden model based on the Scott et al. (2010) Science framework
(Scott et al., "Interdependence of Cell Growth and Gene Expression",
Science 330:1099-1102).

All numerical constants are imported from parameters.py.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parameters import (
    SCOTT_PHI_MAX, SCOTT_PHI_Q_HOUSEKEEPING, SCOTT_KAPPA_T,
    CR_TOXICITY_SATURATION_uM,
    PROTEOME_BURDEN_PCT,  # PREDICTED output
)

def run_metabolic_burden():
    # Scott et al. (2010) ribosome allocation framework parameters,
    # all sourced from parameters.py.
    phi_max = SCOTT_PHI_MAX               # 0.55
    phi_q = SCOTT_PHI_Q_HOUSEKEEPING      # 0.40 (ASSUMED — see parameters.py)
    kappa_t = SCOTT_KAPPA_T               # 3.5 1/h (ASSUMED)
    cr_sat = CR_TOXICITY_SATURATION_uM    # 250 uM (ASSUMED)

    # Synthetic protein mass fraction (phi_s) varies from 0 to 0.15 (0 to 15% of proteome)
    phi_s = np.linspace(0, 0.15, 100)

    Cr_levels = [0, 20, 50, 100] # uM

    fig, ax = plt.subplots(figsize=(9, 6))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, Cr in enumerate(Cr_levels):
        # Cr toxicity reduces translational efficiency due to oxidative stress
        # and DNA damage; linear penalty saturating at cr_sat uM.
        kappa_t_stressed = kappa_t * (1.0 - (Cr / cr_sat))
        mu_stressed = np.maximum(0, (phi_max - phi_q - phi_s) * kappa_t_stressed)

        ax.plot(phi_s * 100, mu_stressed, label=f'Cr(VI) = {Cr} uM',
                linewidth=2.5, color=colors[i])

    # Our specific circuit estimated load (NemA + GFP + CI434) is about
    # 4.5% of proteome at full induction. Sourced from parameters.py
    # (PROTEOME_BURDEN_PCT, PREDICTED by this study's model).
    circuit_load = PROTEOME_BURDEN_PCT
    ax.axvline(x=circuit_load, color='k', linestyle='--',
               label=f'Predicted Circuit Burden ({circuit_load}%)')

    ax.set_title('Metabolic Burden of the Engineered Circuit in Closed Pond Environment')
    ax.set_xlabel('Synthetic Circuit Expression Level (% of Proteome)')
    ax.set_ylabel('Cell Growth Rate ($\mu$, h$^{-1}$)')
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()

    os.makedirs('results', exist_ok=True)
    plt.savefig('results/metabolic_burden_model.png', dpi=300)
    print("Saved metabolic burden model to results/metabolic_burden_model.png")

if __name__ == "__main__":
    run_metabolic_burden()
