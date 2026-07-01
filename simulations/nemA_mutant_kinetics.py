"""
nemA_mutant_kinetics.py — Pillar 2: Wild-type vs. hypothesized NemA*2+
mutant Michaelis-Menten kinetics.

PROVENANCE NOTE (read before citing NemA*2+ claims in the manuscript):
The NemA*2+ variant in this script is a HYPOTHESIZED variant whose
kinetic parameters (Km = 16 uM, kcat = 37.2 h^-1) are ASSUMED, not
derived from a structural modeling pipeline. There is no AlphaFold2
model, FoldX ddG scan, Rosetta design run, or molecular docking output
in this repository that produced these values. They are extrapolated
by analogy from active-site pocket mutagenesis precedent in the OYE
enzyme family, as reported in Mowafy et al. 2010 [15]. The manuscript's
discussion of NemA*2+ must be framed as a hypothesis-by-analogy, not
as a designed variant with structural justification.

All numerical constants are imported from parameters.py.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parameters import (
    KCIRCUIT_KCAT_NEMA, KCIRCUIT_KM_NEMA,          # WT operational values
    KCIRCUIT_KCAT_NEMA_MUT, KCIRCUIT_KM_NEMA_MUT,  # NemA*2+ hypothesized
    E_TOTAL_uM, CR_INITIAL_uM,
)

def michaelis_menten(t, y, kcat, Km, E_total):
    S = y[0]
    dS_dt = -(kcat * E_total * S) / (Km + S)
    return [dS_dt]

def run_mutant_simulation():
    # All kinetic constants now sourced from parameters.py
    kcat_wt = KCIRCUIT_KCAT_NEMA      # h^-1, operational WT (see parameters.py)
    Km_wt = KCIRCUIT_KM_NEMA          # uM

    # NemA*2+ (hypothesized): parameters are ASSUMED, extrapolated from
    # OYE-family active-site mutagenesis precedent [15]. See file header.
    kcat_mut = KCIRCUIT_KCAT_NEMA_MUT  # h^-1
    Km_mut = KCIRCUIT_KM_NEMA_MUT      # uM

    E_total = E_TOTAL_uM               # uM
    S0 = CR_INITIAL_uM                 # uM starting Cr(VI)

    t_span = (0, 24)
    t_eval = np.linspace(0, 24, 200)

    sol_wt = solve_ivp(michaelis_menten, t_span, [S0],
                       args=(kcat_wt, Km_wt, E_total),
                       t_eval=t_eval, method='Radau',
                       rtol=1e-6, atol=1e-9)
    sol_mut = solve_ivp(michaelis_menten, t_span, [S0],
                        args=(kcat_mut, Km_mut, E_total),
                        t_eval=t_eval, method='Radau',
                        rtol=1e-6, atol=1e-9)

    # Calculate reaction velocities vs Substrate concentration for Lineweaver-Burk
    S_range = np.linspace(1, 100, 100)
    V_wt = (kcat_wt * E_total * S_range) / (Km_wt + S_range)
    V_mut = (kcat_mut * E_total * S_range) / (Km_mut + S_range)

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Time-course depletion
    axs[0].plot(sol_wt.t, sol_wt.y[0], 'b--', label='Wild-Type NemA')
    axs[0].plot(sol_mut.t, sol_mut.y[0], 'r-',
                label='Hypothesized NemA*2+ (extrapolated, [15])')
    axs[0].set_title('Cr(VI) Depletion Over Time')
    axs[0].set_xlabel('Time (h)')
    axs[0].set_ylabel('Cr(VI) Concentration (uM)')
    axs[0].grid(True)
    axs[0].legend()

    # Michaelis-Menten Curve
    axs[1].plot(S_range, V_wt, 'b--', label=f'Wild-Type (Km={Km_wt} uM)')
    axs[1].plot(S_range, V_mut, 'r-', label=f'NemA*2+ (Km={Km_mut} uM, ASSUMED)')
    axs[1].set_title('Enzyme Kinetics (V vs [S])')
    axs[1].set_xlabel('Substrate [Cr(VI)] (uM)')
    axs[1].set_ylabel('Velocity (uM/h)')
    axs[1].grid(True)
    axs[1].legend()

    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/nemA_mutant_kinetics.png', dpi=300)
    print("Saved mutant kinetics model to results/nemA_mutant_kinetics.png")

if __name__ == "__main__":
    run_mutant_simulation()
