"""
parameters.py — Centralized, cited parameter set for the tri-modular
Cr(VI) bioremediation circuit model.

Every constant below is tagged with its provenance:
  - "source: [N]" = taken from a numbered reference in the manuscript bibliography
  - "ASSUMED"     = not from a specific literature value; estimated/chosen for
                     this model, with justification given
  - "PREDICTED"   = an output of this project's own simulation, not an input
                     parameter (kept here for reference/reporting only)
  - "None"        = gap: a value is required for the model to run but is not
                     currently supported by a literature source. These must
                     be resolved (with a real citation) or explicitly labeled
                     as ASSUMED in the manuscript's Limitations section
                     before any peer-reviewed claim is made.

Units are specified per-constant. Do not modify without updating the
corresponding value/citation in Journal_Manuscript_2026.md.

This file is the single source of truth for every constant used by:
  - circuit_ode_model.py            (Pillar 1)
  - nemA_mutant_kinetics.py         (Pillar 2)
  - metabolic_burden_model.py       (Pillar 3)
  - biosafety_mutation_model.py     (Pillar 4)
  - biosafety_sensitivity.py        (Pillar 4b)
"""

import math


# =====================================================================
# MODULE 1 — ChrB-sfGFP Biosensor
# =====================================================================

CHRB_OPERATOR_LENGTH_BP = 23   # bp, source: [14] iGEM BBa_K1149051 part
                                # documentation (Edinburgh 2013) — palindromic
                                # PchrB operator sequence

# The three values below are PREDICTED outputs of circuit_ode_model.py,
# not independent input parameters. Kept here only for transparent
# reporting in the manuscript.
LOD_CR6_NM = 80                 # nM, PREDICTED by this study's model (Sec 4.1)
FOLD_INDUCTION_100uM = 8.2      # x, PREDICTED by this study's model (Sec 4.1)
RESPONSE_TIME_90PCT_HR = 3      # hours, PREDICTED by this study's model (Sec 4.1)

# Hill-function parameters used by circuit_ode_model.py
HILL_KD_CHRB_uM = 0.1           # uM (== 100 nM), source: [14] iGEM BBa_K1149051
                                # dose-response EC50 characterisation
HILL_N_CHRB = 2                 # dimensionless, source: [14] iGEM BBa_K1149051
                                # published Hill coefficient for ChrB

# Pillar 1: circuit_ode_model.py
KCIRCUIT_K_NEMA_PROD = 5.0      # au/h, ASSUMED — production rate constant for
                                # NemA under PchrB de-repression; not
                                # independently fit; tuned to yield the
                                # observed 96h dynamics
KCIRCUIT_K_GFP_PROD = 10.0      # au/h, ASSUMED — production rate constant for
                                # sfGFP under PchrB; tuned for the predicted
                                # ~80 nM LOD
KCIRCUIT_DEG_NEMA = 0.05        # 1/h, ASSUMED — NemA degradation rate;
                                # corresponds to half-life ~13.9 h
KCIRCUIT_DEG_GFP = 0.02         # 1/h, ASSUMED — sfGFP degradation rate;
                                # corresponds to half-life ~34.7 h
KCIRCUIT_K_HOLIN_PROD = 2.0     # au/h, ASSUMED — Holin production rate
KCIRCUIT_KD_CI434 = 1.0         # au, ASSUMED — CI434 repression Kd for PC1
KCIRCUIT_HOLIN_THRESHOLD = 5.0  # au, ASSUMED — Holin lysis threshold
KCIRCUIT_MU_MAX = 0.5           # 1/h, ASSUMED — maximum specific growth rate
KCIRCUIT_K_CARRY = 1e9          # cells/mL, ASSUMED — logistic carrying capacity
KCIRCUIT_K_LYSIS = 0.15         # 1/h, ASSUMED — lysis rate constant after
                                # Holin crosses threshold


# =====================================================================
# MODULE 2 — NemA Chromate Reductase (Wild-Type)
# =====================================================================

NEMA_KM_WT_uM = 48              # uM, source: [12] Williams et al. 2003,
                                # published measured value on Cr(VI) substrate
NEMA_KCAT_WT_per_s = 0.39       # s^-1, source: [12] Williams et al. 2003
NEMA_KCAT_WT_per_hr = 1404      # h^-1, derived: NEMA_KCAT_WT_per_s * 3600
NEMA_KCAT_WT_per_h_circuit = 18.6  # h^-1, ASSUMED — used by circuit_ode_model.py;
                                # this value is ~75x lower than the published
                                # 1404 h^-1; treat the circuit model as a
                                # reduced/operational rate that captures the
                                # dynamics, not a direct physical measurement
E_TOTAL_uM = 5.0                # uM, ASSUMED — total NemA enzyme
                                # concentration in the kinetic model
CR_INITIAL_uM = 100.0           # uM, source: Sec 1.4 hypothesis (100 uM start)


# =====================================================================
# MODULE 2b — NemA*2+ Hypothesized Mutant
# =====================================================================
# IMPORTANT: These are ASSUMED values extrapolated from active-site mutation
# precedent in the OYE family [15] (Mowafy et al. 2010). They are NOT the
# result of any structural modeling pipeline, AlphaFold2 prediction,
# FoldX ddG scan, or molecular docking performed in this study — no such
# pipeline exists in this repository. The manuscript's discussion of
# NemA*2+ is framed as a hypothesis-by-analogy, not as a designed variant.

NEMA_KM_MUT_uM = 16             # uM, ASSUMED — extrapolated from active-site
                                # pocket mutation precedent in [15] Mowafy
                                # et al. 2010 (OYE-family enzyme). 3-fold
                                # improvement over NEMA_KM_WT_uM. NOT
                                # independently structurally modeled in this
                                # study.
NEMA_KCAT_MUT_per_hr = 37.2     # h^-1, ASSUMED — same basis as above.
                                # Reported as 2-fold improvement; note this
                                # is not directly comparable to the
                                # 1404 h^-1 published WT figure on a
                                # per-enzyme-molecule basis (the nemA script
                                # uses 18.6 h^-1 as the operational WT
                                # rate, against which 37.2 h^-1 is ~2x).
NEMA_KCAT_MUT_CIRCUIT_per_h = 37.2  # h^-1, ASSUMED — used in
                                # circuit_ode_model.py; see note above

# Auto-derived helper used by nemA_mutant_kinetics.py: assumes WT in
# script units is 18.6 h^-1, mutant is 2x.
KCIRCUIT_KCAT_NEMA = 18.6       # h^-1, ASSUMED — see NEMA_KCAT_WT_per_h_circuit
KCIRCUIT_KM_NEMA = 48.0         # uM, ASSUMED — operational Km in circuit model
KCIRCUIT_KCAT_NEMA_MUT = 37.2   # h^-1, ASSUMED — see NEMA_KCAT_MUT_CIRCUIT_per_h
KCIRCUIT_KM_NEMA_MUT = 16.0     # uM, ASSUMED — see NEMA_KM_MUT_uM


# =====================================================================
# MODULE 3 — Kill Switch (Holin-Endolysin, Dual-Trigger)
# =====================================================================

CI434_SSRA_HALFLIFE_HR = 24     # hours, source: manuscript Sec 2.4.3;
                                # cited from SsrA degron tag literature
                                # (Keiler et al. 1996, Gottesman et al. 1998).
                                # 24 h is a commonly reported value for
                                # the SsrA(DAS+4) tag family in E. coli.
LAMBDA_CI434_PER_HR = math.log(2) / CI434_SSRA_HALFLIFE_HR  # 1/h, derived

KILL_SWITCH_TRIGGER_TIME_HR = 72  # hours, PREDICTED — this is the ODE model's
                                  # OUTPUT (AND-gate fires at t=72h per
                                  # Sec 4.1), not an input parameter.
TARGET_SIZE_BP = 500             # bp, ASSUMED — combined target size of the
                                 # holin + endolysin + regulatory region
                                 # where a loss-of-function mutation could
                                 # silence the kill switch. Approximate;
                                 # justified by [13] Chan et al. 2016's
                                 # typical kill-switch architecture.


# =====================================================================
# CHASSIS — E. coli DH5a delta-thyA delta-dapA
# =====================================================================

# No quantitative kinetic parameters for auxotrophy reversion are
# independently cited; they are handled in the Luria-Delbruck block
# below. HGT reversion probability is the only mode of escape for
# chromosomal deletions.


# =====================================================================
# PLASMID COPY NUMBERS
# =====================================================================

COPY_NUMBER_PUC19 = 500         # approx copies/cell, source: standard
                                # pUC19 literature (e.g., Lin-Chao et al.
                                # 1992, Plasmid 28:58-65). The exact value
                                # depends on growth conditions; 500-700 is
                                # the commonly cited range. Used in Sec 2.1.
COPY_NUMBER_PET28A = 40         # approx copies/cell, source: standard
                                # pET-28a literature (Novagen/EMD Millipore
                                # documentation, pBR322-derived origin).
                                # Note: pET-28a is typically used with T7
                                # polymerase; in this design the PchrB
                                # promoter replaces T7, so the copy number
                                # is the un-induced pBR322-origin baseline.
COPY_NUMBER_PACYC184 = 15       # approx copies/cell, source: standard
                                # pACYC184 literature (Chang & Cohen 1978,
                                # J Bacteriol 134:1141-1156). p15A origin
                                # commonly cited as 10-18 copies/cell.


# =====================================================================
# METABOLIC BURDEN MODEL (Scott et al. 2010 framework)
# =====================================================================

# These are PREDICTED outputs of metabolic_burden_model.py, not inputs.
PROTEOME_BURDEN_PCT = 4.5       # %, PREDICTED — this study's model output
                                # (Sec 4.3), not an input
GROWTH_RATE_REDUCTION_MAX_PCT = 33  # %, PREDICTED — at maximum induction

# Scott et al. 2010 framework parameters (input to the model)
SCOTT_PHI_MAX = 0.55            # max mass fraction of proteome that can
                                # be ribosomes, source: Scott et al. 2010
                                # Science 330:1099-1102, Table 1 / Eq. 1
SCOTT_PHI_Q_HOUSEKEEPING = 0.40  # housekeeping protein mass fraction,
                                  # ASSUMED — adjusted from Scott et al.
                                  # 2010's typical ~0.27 value to reflect
                                  # a closed-pond / nutrient-poor environment
                                  # where a larger share of proteome is
                                  # needed for maintenance
SCOTT_KAPPA_T = 3.5             # 1/h, ASSUMED — translational elongation
                                # efficiency; lower than Scott et al. 2010's
                                # standard ~6-8 h^-1 to model nutrient-poor
                                # pond conditions
CR_TOXICITY_SATURATION_uM = 250  # uM, ASSUMED — Cr(VI) concentration at
                                 # which translational efficiency goes to
                                 # zero in the linear toxicity model.
                                 # No specific citation; conservative
                                 # order-of-magnitude estimate from
                                 # Cr(VI) growth-inhibition literature.


# =====================================================================
# LURIA-DELBRUCK EVOLUTIONARY BIOSAFETY MODEL
# =====================================================================

# The strongest claim in the manuscript (Pescape = 1.11e-16) is most
# sensitive to these constants. All require real citations before
# peer review.

MUTATION_RATE_PER_BP_PER_GEN = 1e-9  # mutations/bp/generation, ASSUMED —
                                      # commonly cited order-of-magnitude
                                      # for spontaneous E. coli mutation
                                      # rate per base pair per generation.
                                      # Source candidates: Drake et al.
                                      # 1998 (Genetics 148:1667-1686) for
                                      # the per-bp rate; Lee et al. 2012
                                      # (PNAS) for E. coli-specific context.
                                      # Range in literature: 1e-10 to 1e-9.
                                      # The 1e-9 used here is the more
                                      # conservative (higher) end; see
                                      # biosafety_sensitivity.py for the
                                      # sensitivity sweep across this range.
MUTATION_RATE_PER_GENE_PER_GEN = None  # CONFIRM — not directly stated in
                                      # the current manuscript. Derivable
                                      # from MUTATION_RATE_PER_BP_PER_GEN *
                                      # gene length if a specific gene length
                                      # is fixed; for kill-switch analysis
                                      # the script uses per-bp rate * target
                                      # size directly (TARGET_SIZE_BP).

GENERATION_TIME_MIN = 20        # minutes, ASSUMED — standard E. coli
                                # doubling time under lab conditions.
                                # For bioreactor/pond conditions with
                                # 33% growth reduction (GROWTH_RATE_REDUCTION_MAX_PCT),
                                # the effective generation time would be
                                # longer; biosafety_mutation_model.py
                                # uses generations_per_day = 4 (15 min/division
                                # spread) as a direct input, see below.
GENERATIONS_PER_DAY = 4         # generations/day, ASSUMED — slow growth
                                # in nutrient-poor closed pond; corresponds
                                # to effective generation time of 6 h (i.e.,
                                # growth is already burden-adjusted in the
                                # biosafety script).

POPULATION_VOLUME_L = 1000      # L, source: manuscript Sec 4.4 / Fig 4
                                # — assumed closed-system deployment scale
MAX_CELL_DENSITY_PER_L = 1e9    # cells/L, source: manuscript Sec 4.4.1
TOTAL_CELL_COUNT = POPULATION_VOLUME_L * MAX_CELL_DENSITY_PER_L  # 1e12, derived
DEPLOYMENT_WINDOW_DAYS = 30     # days, source: manuscript hypothesis
                                # (Sec 1.4) — 30-day deployment window
                                # explicitly stated.

# Auxotrophy reversion / HGT probabilities — order-of-magnitude estimates
# from environmental microbiology literature; no single citation supports
# the exact value used.
HGT_P_REVERT_THYA_PER_DIV = 1e-12  # per cell per division, ASSUMED —
                                    # conjugal HGT probability of an
                                    # intact functional thyA gene from
                                    # an environmental donor. Order-of-
                                    # magnitude estimate; no single
                                    # primary citation identified.
HGT_P_REVERT_DAPA_PER_DIV = 1e-12  # per cell per division, ASSUMED —
                                    # as above for dapA.

# PREDICTED outputs
PESCAPE_KILLSWITCH_ONLY = None  # PREDICTED — this study's output, kill switch
                                # layer alone (Fig 4, red dashed line)
PESCAPE_FULL_CONTAINMENT = 6.0e-17  # PREDICTED — this study's headline
                                     # output, full 5-layer containment over
                                     # 30 days (Sec 4.4). The value is
                                     # 1 - exp(-N*G*p) with N=1e12, G=120,
                                     # p=5e-31, giving N*G*p = 6e-17. For
                                     # such small arguments the Taylor
                                     # expansion 1 - exp(-x) ~ x is used
                                     # in biosafety_mutation_model.py to
                                     # avoid IEEE-754 catastrophic
                                     # cancellation, which would otherwise
                                     # return ~1.11e-16 (incorrect by
                                     # a factor of ~1.85).
COMBINED_FAILURE_PROBABILITY = 1e-30  # PREDICTED — stated in Abstract as
                                      # "theoretical combined failure
                                      # probability < 10^-30". This is the
                                      # per-division per-cell product
                                      # (p_KS * p_thyA * p_dapA); it is NOT
                                      # the same quantity as PESCAPE_FULL_CONTAINMENT
                                      # (which integrates over N*G).
DE_MINIMIS_RISK_THRESHOLD = 1e-15  # source: Sec 4.4.2 / Fig 4 — adopted
                                   # "acceptable risk" reference line for
                                   # the biosafety plot
