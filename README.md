# SJWP 2026 — Chromium Bioremediation Genetic Circuit Project

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11.x](https://img.shields.io/badge/python-3.11.x-blue.svg)](.python-version)

A computational synthetic biology project modeling a tri-modular genetic circuit for hexavalent chromium (Cr(VI)) bioremediation in closed-system microcosms.

**Status:** Computational design and validation only. No experimental or wet-lab data were generated; all results are derived from the simulation models in `simulations/`.

## Code and Data Availability

All simulation code is contained in this repository. No experimental or wet-lab data were generated in this project — all results are derived from computational modeling. Parameter sources (literature-derived vs. assumed/estimated) are documented in `simulations/parameters.py`, which is the single source of truth for every constant in the project. This repository is archived at Zenodo: [DOI to be inserted after first Zenodo release — see top of README for badge].

## Parameters

All model constants (literature-sourced and assumed) are centralized and individually cited/labeled in [`simulations/parameters.py`](simulations/parameters.py). Every constant is tagged with one of:

- `source: [N]` — taken from a numbered reference in the manuscript bibliography
- `ASSUMED` — not from a specific literature value; estimated/chosen for this model, with justification given inline
- `PREDICTED` — an output of this project's own simulation, not an input parameter
- `None` — a required value with no supporting literature source; must be resolved before peer-reviewed claims are made

If you are reviewing the manuscript: opening `parameters.py` is the fastest way to verify the provenance of every number in the body text.

## Project Structure

```
SJWP/
├── .python-version               # Pinned interpreter (3.11.x)
├── .gitignore                    # Keeps .venv/, __pycache__/, generated *.png out of git
├── LICENSE                       # CC BY 4.0
├── requirements.txt              # All project dependencies (pinned versions)
├── README.md                     # This file
├── Journal_Manuscript_2026.md    # Full research manuscript (Markdown source)
├── Journal_Manuscript_2026.pdf   # Final journal-submission PDF (regenerated from .md)
└── simulations/
    ├── parameters.py             # Centralized, cited parameter set (READ THIS FIRST)
    ├── circuit_ode_model.py      # Pillar 1: ODE systems biology simulation (96h)
    ├── nemA_mutant_kinetics.py   # Pillar 2: Wild-type vs. hypothesized NemA*2+ kinetics
    ├── metabolic_burden_model.py # Pillar 3: Ribosome allocation / GSMM (Scott et al. 2010)
    ├── biosafety_mutation_model.py # Pillar 4: Luria-Delbrück mutation modeling
    ├── biosafety_sensitivity.py  # Pillar 4b: Sensitivity sweep over mutation rate and volume
    ├── generate_pdf.py           # Renders Journal_Manuscript_2026.md to PDF
    ├── generate_circuit_diagrams.py # Renders plasmid module diagrams
    └── results/                  # Generated figures (PNG, 300 DPI) and CSV outputs
        ├── integrated_96h_simulation.png
        ├── nemA_mutant_kinetics.png
        ├── metabolic_burden_model.png
        ├── biosafety_mutation_model.png         # 365-day long-run view
        ├── biosafety_mutation_30day.png         # 30-day deployment-window view (Sec 4.4)
        ├── sensitivity_analysis.png             # Pillar 4b sweep results
        ├── sensitivity_analysis.csv             # Underlying numbers
        └── plasmid_module{1,2,3}.png
```

`generate_pdf.py` renders `Journal_Manuscript_2026.md` to submission-formatted PDF via reportlab and fpdf2; it is the only script in the simulations folder that does not produce a model figure.

## Quick Start

```powershell
# Activate the virtual environment (Windows)
.venv\Scripts\activate

# (First time only) Install all dependencies
pip install -r requirements.txt

# Run all simulations to regenerate figures
python simulations/circuit_ode_model.py
python simulations/nemA_mutant_kinetics.py
python simulations/metabolic_burden_model.py
python simulations/biosafety_mutation_model.py
python simulations/biosafety_sensitivity.py

# Generate the final PDF
python simulations/generate_pdf.py
```

## Computational Pillars

| Pillar | Script | Method |
|---|---|---|
| 1. Circuit Dynamics | `circuit_ode_model.py` | ODE (Hill + Michaelis-Menten, Radau solver, rtol=1e-6 / atol=1e-9) |
| 2. Protein Engineering | `nemA_mutant_kinetics.py` | Comparative Michaelis-Menten kinetics; NemA*2+ is a hypothesis-by-analogy to OYE precedent [15], not a designed variant |
| 3. Metabolic Burden | `metabolic_burden_model.py` | Ribosome allocation (Scott et al. 2010 framework) |
| 4. BMO Biosafety | `biosafety_mutation_model.py` | Luria-Delbrück fluctuation analysis with Poisson approximation |
| 4b. Biosafety Sensitivity | `biosafety_sensitivity.py` | Sweep over mutation rate (×0.01 – ×100) and reactor volume (10 L – 10,000 L) |

## Dependencies

All managed via the `.venv` virtual environment. See `requirements.txt` for pinned versions.
Core packages: `numpy`, `scipy`, `matplotlib`, `fpdf2`, `reportlab`, `Pillow`.

Python version is pinned in `.python-version` (3.11.x). The project should run on any 3.11+ interpreter; the pin exists so reviewers and Zenodo archivists get a reproducible environment.

## Authors

- **Zubayer Hasan Shaad** — Govt. Tolaram College, Narayanganj, Bangladesh
- **Humayra Afia** — British Standard School, Bangladesh
- **Mentor:** Zabeer Zareef
