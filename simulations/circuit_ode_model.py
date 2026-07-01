"""
circuit_ode_model.py — Pillar 1: ODE systems biology simulation of the
tri-modular Cr(VI) bioremediation circuit (96h horizon).

All numerical constants are imported from parameters.py so the source
vs. assumed status of every value is auditable in one place. See
simulations/parameters.py for the provenance of each constant.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os
import sys

# Allow imports whether run from repo root or from simulations/ dir.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parameters import (
    HILL_KD_CHRB_uM, HILL_N_CHRB,
    KCIRCUIT_K_NEMA_PROD, KCIRCUIT_K_GFP_PROD,
    KCIRCUIT_DEG_NEMA, KCIRCUIT_DEG_GFP,
    KCIRCUIT_K_HOLIN_PROD, KCIRCUIT_KD_CI434,
    KCIRCUIT_HOLIN_THRESHOLD, KCIRCUIT_MU_MAX, KCIRCUIT_K_CARRY, KCIRCUIT_K_LYSIS,
    KCIRCUIT_KCAT_NEMA, KCIRCUIT_KM_NEMA,
    LAMBDA_CI434_PER_HR,
)

# Note: the circuit model uses an "operational" kcat (KCIRCUIT_KCAT_NEMA,
# 18.6 h^-1) that is lower than the published literature value
# (NEMA_KCAT_WT_per_hr = 1404 h^-1 in parameters.py). This is intentional
# and is documented in parameters.py — the circuit model captures
# qualitative 96h dynamics; the literature value drives Pillar 2's
# comparative kinetics. See parameters.py for the full discussion.

def hill_activation(S, Kd, n):
    return (S**n) / (Kd**n + S**n)

def circuit_dynamics(t, y, params):
    Cr_ext, NemA, GFP, CI434, Holin, Cells = y

    Kd_ChrB = params['Kd_ChrB']
    n = params['n']
    k_NemA_prod = params['k_NemA_prod']
    k_GFP_prod = params['k_GFP_prod']
    deg_NemA = params['deg_NemA']
    deg_GFP = params['deg_GFP']
    kcat_NemA = params['kcat_NemA']
    Km_NemA = params['Km_NemA']

    k_CI434_prod = params['k_CI434_prod']
    deg_CI434 = params['deg_CI434']

    k_Holin_prod = params['k_Holin_prod']
    Kd_CI434 = params['Kd_CI434']

    mu_max = params['mu_max']
    K_carry = params['K_carry']
    k_lysis = params['k_lysis']

    v_reduction = (kcat_NemA * NemA * Cr_ext) / (Km_NemA + Cr_ext)
    dCr_ext_dt = -v_reduction

    act_ChrB = hill_activation(Cr_ext, Kd_ChrB, n)

    dNemA_dt = k_NemA_prod * act_ChrB - deg_NemA * NemA
    dGFP_dt = k_GFP_prod * act_ChrB - deg_GFP * GFP

    dCI434_dt = -deg_CI434 * CI434

    rep_CI434 = (Kd_CI434**2) / (Kd_CI434**2 + CI434**2)
    rep_Cr = (Kd_ChrB**n) / (Kd_ChrB**n + Cr_ext**n)

    dHolin_dt = k_Holin_prod * rep_Cr * rep_CI434

    lysis_rate = k_lysis if Holin > params['Holin_threshold'] else 0.0
    dCells_dt = mu_max * Cells * (1 - Cells / K_carry) - lysis_rate * Cells

    if Cells < 1 and dCells_dt < 0:
        dCells_dt = -Cells

    return [dCr_ext_dt, dNemA_dt, dGFP_dt, dCI434_dt, dHolin_dt, dCells_dt]

def run_simulation():
    # All constants sourced from parameters.py
    params = {
        'Kd_ChrB': HILL_KD_CHRB_uM,
        'n': HILL_N_CHRB,
        'k_NemA_prod': KCIRCUIT_K_NEMA_PROD,
        'k_GFP_prod': KCIRCUIT_K_GFP_PROD,
        'deg_NemA': KCIRCUIT_DEG_NEMA,
        'deg_GFP': KCIRCUIT_DEG_GFP,
        'kcat_NemA': KCIRCUIT_KCAT_NEMA,
        'Km_NemA': KCIRCUIT_KM_NEMA,
        'k_CI434_prod': 0.0,
        'deg_CI434': LAMBDA_CI434_PER_HR,
        'k_Holin_prod': KCIRCUIT_K_HOLIN_PROD,
        'Kd_CI434': KCIRCUIT_KD_CI434,
        'Holin_threshold': KCIRCUIT_HOLIN_THRESHOLD,
        'mu_max': KCIRCUIT_MU_MAX,
        'K_carry': KCIRCUIT_K_CARRY,
        'k_lysis': KCIRCUIT_K_LYSIS
    }

    Cr0 = 100.0
    CI434_0 = 10.0
    Cells_0 = 1e7
    y0 = [Cr0, 0.0, 0.0, CI434_0, 0.0, Cells_0]

    t_span = (0, 96)
    t_eval = np.linspace(0, 96, 500)

    sol = solve_ivp(circuit_dynamics, t_span, y0, args=(params,),
                    t_eval=t_eval, method='Radau',
                    rtol=1e-6, atol=1e-9)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].plot(sol.t, sol.y[0], 'r-', label='Cr(VI) (uM)')
    axs[0, 0].set_title('Chromate Reduction (NemA Activity)')
    axs[0, 0].set_xlabel('Time (h)')
    axs[0, 0].set_ylabel('Concentration (uM)')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    axs[0, 1].plot(sol.t, sol.y[2], 'g-', label='GFP (RFU)')
    axs[0, 1].set_title('Biosensor Activation')
    axs[0, 1].set_xlabel('Time (h)')
    axs[0, 1].set_ylabel('Fluorescence')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    axs[1, 0].plot(sol.t, sol.y[3], 'b--', label='CI434 (Timer)')
    axs[1, 0].plot(sol.t, sol.y[4], 'k-', label='Holin (Toxin)')
    axs[1, 0].axhline(y=params['Holin_threshold'], color='r', linestyle=':', label='Threshold')
    axs[1, 0].set_title('Kill Switch Dynamics')
    axs[1, 0].set_xlabel('Time (h)')
    axs[1, 0].set_ylabel('Protein Level')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    axs[1, 1].semilogy(sol.t, np.maximum(sol.y[5], 1), 'm-', label='Live Cells (CFU/mL)')
    axs[1, 1].axhline(y=1e2, color='r', linestyle=':', label='Detection Limit')
    axs[1, 1].set_title('Cell Population / Biosafety Containment')
    axs[1, 1].set_xlabel('Time (h)')
    axs[1, 1].set_ylabel('CFU / mL (log scale)')
    axs[1, 1].set_ylim([1, 1e10])
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/integrated_96h_simulation.png', dpi=300)
    print("Simulation complete. Results saved to results/integrated_96h_simulation.png")

if __name__ == "__main__":
    run_simulation()
