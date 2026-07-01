<div align="center">

# 🧬 SJWP 2026 — Chromium Bioremediation Genetic Circuit

**A computational synthetic biology project modeling a tri-modular genetic circuit for hexavalent chromium [Cr(VI)] biosensing, enzymatic remediation, and autonomous self-termination in closed-system microcosms.**

<br>

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=for-the-badge)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11](https://img.shields.io/badge/python-3.11.x-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](.python-version)
[![Status: Computational](https://img.shields.io/badge/status-computational%20only-orange?style=for-the-badge)](#-important-caveat)
[![Code: documented](https://img.shields.io/badge/code-documented-brightgreen?style=for-the-badge)](#-code-and-data-availability)
[![Repo: GitHub](https://img.shields.io/badge/repo-zabdax%2Fcr6--biocircuit--model-181717?style=for-the-badge&logo=github)](https://github.com/zabdax/cr6-biocircuit-model)

</div>

---

## 📌 Project at a glance

| | |
|---|---|
| **Chassis** | *E. coli* DH5α ΔthyA ΔdapA (double auxotroph) |
| **Modules** | 3 — ChrB-sfGFP biosensor · NemA chromate reductase · Holin-Endolysin kill switch |
| **Plasmids** | 3 — pUC19 (~500 cp) · pET-28a (~40 cp) · pACYC184 (~15 cp) |
| **Computational pillars** | 4 + 1 — ODE · Kinetics · Metabolic burden · Biosafety · Sensitivity sweep |
| **Headline result** | $P_\text{escape}(30\,\text{d}) \approx 6 \times 10^{-17}$ in 1,000 L closed system |
| **Sensitivity finding** | Robust to 10× error in mutation rate; fails at 100× (above 10⁻¹⁵ threshold) |
| **Status** | Computational design only — no wet-lab data generated |

---

## ⚠️ Important caveat

> **This work is entirely computational.** No experimental or wet-lab data were generated; all results are derived from the simulation models in `simulations/`. The deployment claim is contingent on a direct measurement of the per-bp mutation rate in the deployed strain under the deployed growth conditions, which has not yet been performed. See [`simulations/parameters.py`](simulations/parameters.py) for the provenance of every number in the manuscript.

---

## 📖 Code and Data Availability

All simulation code is contained in this repository. No experimental or wet-lab data were generated in this project — all results are derived from computational modeling. Parameter sources (literature-derived vs. assumed/estimated) are documented in [`simulations/parameters.py`](simulations/parameters.py), which is the single source of truth for every constant in the project.

This repository is archived at **Zenodo** *(DOI badge will be added after first Zenodo release)*.

---

## 🧪 Parameters

All model constants — literature-sourced, assumed, or predicted — are centralized and individually cited/labeled in [`simulations/parameters.py`](simulations/parameters.py). Each constant is tagged as one of:

| Tag | Meaning |
|---|---|
| `source: [N]` | taken from a numbered reference in the manuscript bibliography |
| `ASSUMED` | estimated/chosen for this model, with justification given inline |
| `PREDICTED` | an output of this project's own simulation, not an input parameter |
| `None` | a required value with no supporting literature source — must be resolved before peer-reviewed claims are made |

> **Reviewers:** opening `parameters.py` is the fastest way to verify the provenance of every number in the manuscript body.

---

## 🏗️ Project Structure

```
SJWP/
├── .python-version               # Pinned interpreter (3.11.x)
├── .gitignore                    # Keeps .venv/, __pycache__/, generated *.png, etc. out of git
├── LICENSE                       # CC BY 4.0
├── README.md                     # This file
├── requirements.txt              # All project dependencies (pinned versions)
├── Journal_Manuscript_2026.md    # Full research manuscript (Markdown source)
├── Journal_Manuscript_2026.tex   # LaTeX source for Overleaf/journal submission
└── simulations/
    ├── parameters.py             # ⭐ Centralized, cited parameter set — read this first
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
        ├── biosafety_mutation_30day.png         # 30-day deployment-window view
        ├── sensitivity_analysis.png             # Pillar 4b sweep results
        ├── sensitivity_analysis.csv             # Underlying numbers
        └── plasmid_module{1,2,3}.png
```

> `generate_pdf.py` renders `Journal_Manuscript_2026.md` to submission-formatted PDF via `reportlab` and `fpdf2`; it is the only script in the `simulations/` folder that does not produce a model figure.

---

## 🚀 Quick Start

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

---

## 🔬 Computational Pillars

| Pillar | Script | Method | Headline output |
|---|---|---|---|
| **1. Circuit Dynamics** | `circuit_ode_model.py` | ODE (Hill + Michaelis-Menten, Radau solver, rtol=1e-6 / atol=1e-9) | 96h tri-modular dynamics: 100 μM Cr(VI) depleted by t≈44h, kill switch fires at t≈72h |
| **2. Protein Engineering** | `nemA_mutant_kinetics.py` | Comparative Michaelis-Menten kinetics; NemA*2+ is a hypothesis-by-analogy to OYE precedent [15], not a designed variant | Hypothesized NemA\*²⁺: K_m 48→16 μM, k_cat ×2 |
| **3. Metabolic Burden** | `metabolic_burden_model.py` | Ribosome allocation (Scott et al. 2010 framework) | ~4.5% proteome burden; 33% growth reduction at full induction |
| **4. BMO Biosafety** | `biosafety_mutation_model.py` | Luria-Delbrück fluctuation analysis with Poisson approximation | $P_\text{escape}(30\,\text{d}) \approx 6 \times 10^{-17}$ |
| **4b. Biosafety Sensitivity** | `biosafety_sensitivity.py` | Sweep over mutation rate (×0.01 – ×100) and reactor volume (10 L – 10,000 L) | Robust to 10× rate error; fails at 100× (6×10⁻¹⁵, above 10⁻¹⁵ threshold) |

---

## 📦 Dependencies

All managed via the `.venv` virtual environment. See [`requirements.txt`](requirements.txt) for pinned versions.

**Core packages:** `numpy` · `scipy` · `matplotlib` · `fpdf2` · `reportlab` · `Pillow`

Python version is pinned in [`.python-version`](.python-version) (3.11.x). The project should run on any 3.11+ interpreter; the pin exists so reviewers and Zenodo archivists get a reproducible environment.

---

## 👤 Author

**Zubayer Hasan Shaad** — Govt. Tolaram College, Narayanganj, Bangladesh

📫 [mdzubayerhasanshaad99@gmail.com](mailto:mdzubayerhasanshaad99@gmail.com) · 🐙 [@zabdax](https://github.com/zabdax)

---

## 📄 License

This work is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to share (copy and redistribute in any medium or format) and adapt (remix, transform, and build upon) the material for any purpose, even commercially, provided that appropriate credit is given. See the [LICENSE](LICENSE) file for the full license text.

---

<div align="center">

<sub>Computational synthetic biology for resource-constrained bioremediation · SJWP 2026</sub>

</div>
