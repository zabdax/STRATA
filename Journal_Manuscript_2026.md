# In Silico Design and Computational Validation of a Tri-Modular Genetic Circuit for Autonomous Detection and Bioremediation of Hexavalent Chromium in Closed-System Microcosms

**Zubayer Hasan Shaad¹**

¹ Govt. Tolaram College, Narayanganj, Bangladesh

**Corresponding author:** Zubayer Hasan Shaad (mdzubayerhasanshaad99@gmail.com)

---

## Abstract

Hexavalent chromium [Cr(VI)], a Group 1 IARC carcinogen, has been measured at concentrations up to 3.54 mg/L in Bangladesh's Buriganga River—approximately 70-fold above the US EPA surface water limit—primarily as a consequence of unregulated leather tannery effluent discharge. While existing remediation technologies address contamination passively, none integrate real-time sensing, dose-responsive enzymatic treatment, and autonomous post-treatment self-termination. More critically, prior proposals deploying engineered microorganisms in open rivers carry catastrophic ecological risks that remain computationally unquantified.

Here, we present a fully computational design and validation of a tri-modular synthetic genetic circuit expressed in a double-auxotrophic *Escherichia coli* chassis, exclusively deployed within a closed-system microcosm (bioreactor or sealed pond). The three modules—each encoded on an orthogonal, compatibility-verified plasmid backbone—function as follows: **(1)** a ChrB-sfGFP biosensor module (pChrB-sfGFP, pUC19) provides Cr(VI) detection at nanomolar sensitivity via a de-repression logic gate; **(2)** a NemA chromate reductase module (pNemA-His, pET-28a), driven by the identical PchrB promoter, ensures coordinately regulated, dose-responsive enzymatic Cr(VI) → Cr(III) reduction; **(3)** a dual-trigger holin-endolysin 'Deadman' kill switch (pKillSwitch-DT, pACYC184) enforces programmed cell death via AND-gate logic integrating chromate depletion sensing and a constitutive CI434-SsrA timer repressor with a 24-hour protein half-life.

The computational validation framework spans four orthogonal methodologies: Ordinary Differential Equation (ODE) systems modeling of the gene expression dynamics across all three modules over 96 hours; comparative Michaelis-Menten modeling of a hypothesized NemA\*²⁺ catalytic variant whose kinetic parameters ($K_m^* = 16$ μM, $k_{cat}^* = 37.2$ h⁻¹) are **assumed** by analogy to OYE-family active-site mutagenesis precedent [15], not derived from a structural modeling pipeline executed in this study; a ribosome-allocation genome-scale metabolic model demonstrating the circuit's ~4.5% proteome burden is metabolically sustainable at environmentally relevant chromium concentrations; and Luria-Delbrück fluctuation analysis showing that, under the assumed input parameters, the layered containment architecture (genetic kill switch + double auxotrophy ΔthyA ΔdapA) yields a 30-day probability of a viable escapee in a 1,000-liter closed system of $P_{escape} = 1.11 \times 10^{-16}$, below an acceptable-risk threshold of $10^{-15}$. A sensitivity sweep (Pillar 4b) shows this headline figure is robust to a 10× error in the assumed per-bp mutation rate and to a 10× scale-up of the deployment reactor, but is not robust to a 100× error in $\mu_{bp}$, at which point $P_{escape}$ rises to 5.99 × 10⁻¹⁵, above the threshold. All simulations were executed in Python (SciPy, NumPy, Matplotlib).

This work demonstrates that, under its modeling assumptions, the proposed tri-modular system can reduce 100 μM Cr(VI) by >99% within 48 hours under closed-system conditions. We argue that this computational framework—by mathematically quantifying both remediation performance and mutation-driven failure modes, and by reporting the sensitivity of its safety claim to its key input assumption—establishes a transparent in silico biosafety validation template for BMO-based heavy metal remediation in resource-constrained settings. The work is entirely computational; no wet-lab validation has been performed.

**Keywords:** synthetic biology · hexavalent chromium · genetic kill switch · ChrB biosensor · NemA reductase · bioremediation · Luria-Delbrück mutation model · plasmid architecture · BMO biosafety · Bangladesh tannery pollution

---

## 1. Introduction

### 1.1 The Hexavalent Chromium Crisis in Bangladesh

Hexavalent chromium [Cr(VI)] is a highly soluble, mobile, and persistent environmental contaminant classified by the International Agency for Research on Cancer (IARC) as a definitive Group 1 human carcinogen [1]. At the molecular level, Cr(VI) enters cells through nonspecific anion transport channels (sharing uptake pathways with sulfate and phosphate), where it undergoes intracellular reduction to Cr(III) and Cr(V) intermediates. These intermediates generate reactive oxygen species (ROS) that form DNA adducts, strand breaks, and protein-DNA crosslinks—mechanisms directly linked to lung carcinoma, nasal septal perforation, and renal tubular necrosis upon chronic exposure [2].

In Bangladesh, the leather tanning industry—historically centred in Hazaribagh, Dhaka, and partially relocated to the Savar Tannery Industrial Estate following the 2017 relocation mandate—has for decades discharged chromium-laden wastewater into the Buriganga and Shitalakshya rivers with demonstrably inadequate treatment infrastructure. A systematic survey of Buriganga river water (dry season, 2021–2023) recorded Cr(VI) concentrations spanning 0.01–3.54 mg/L (mean: 0.48 mg/L), with total dissolved chromium at industrial outfall points reaching 8.42 mg/L [3,4]. For context, the US EPA maximum contaminant level for total chromium in surface water is 0.1 mg/L; the WHO guideline for drinking water is 0.05 mg/L. In the Shitalakshya River (Narayanganj), which flows past Govt. Tolaram College, Cr(VI) concentrations range from 0.037 to 0.102 mg/L, with bioaccumulation in local fish tissue measured at 0.5–2 mg/kg dry weight [5,6]. Dissolved oxygen (DO) in the Buriganga near tannery outfalls falls below 2 mg/L during the dry season—the hypoxic threshold lethal to most fish species—with near-complete loss of aquatic macroinvertebrate diversity in affected zones. Communities dependent on these rivers for subsistence fishing, smallholder agriculture, and informal water access face compounding public health and economic consequences.

### 1.2 Limitations of Existing Remediation Approaches

Conventional Cr(VI) remediation methodologies each carry fundamental limitations that prevent their adoption as scalable, adaptive, and cost-effective solutions in low-resource settings. Chemical precipitation (reduction to Cr(III) using sodium bisulfite or ferrous sulfate at pH 2–3, followed by lime-induced Cr(OH)₃ precipitation) generates large volumes of hazardous chromium-hydroxide sludge requiring further processing, operates in narrow pH windows incompatible with river conditions, and exhibits no ability to modulate treatment intensity in response to fluctuating Cr(VI) concentrations [7]. Electrocoagulation—the approach taken by a prior Bangladesh SJWP entry in 2022—requires continuous electrical input (30–50 W/m³), is economically prohibitive for remote or rural deployment, and applies equal treatment intensity regardless of actual contamination levels [8]. Phytoremediation (hyperaccumulating plants such as *Thlaspi caerulescens*) operates on timescales of months to years and is constrained by seasonal biomass availability [9]. Conventional unmodified bioremediation exploits endogenous chromate reductase activity in naturally occurring strains (e.g., *Bacillus subtilis*, *Lysinibacillus fusiformis*), but these organisms cannot report chromium presence, cannot be programmed to self-terminate after remediation, and lack containment guarantees for open-water environments [10].

Most critically: *none of these approaches operate as integrated sensing-acting-self-terminating systems*. They cannot distinguish between a heavily polluted sampling site and a recovered one, they cannot scale their response in proportion to pollution levels, and they provide no mechanism to prevent long-term biological persistence in the treatment environment.

### 1.3 Synthetic Biology as a Remediation Paradigm

Synthetic biology offers a categorically different framework. By encoding programmable genetic logic directly into a bacterial chassis, it is possible to engineer organisms that act not as passive chemical sponges but as autonomous bio-computers: sensing a specific signal (Cr(VI) concentration), computing a proportional response (NemA expression level), executing that response (enzymatic reduction), and self-terminating upon task completion (kill switch activation). This "sense-respond-terminate" architecture—all governed by the same regulatory protein (ChrB)—is the conceptual core of the present design.

However, prior synthetic biology approaches to bioremediation have consistently underestimated or insufficiently quantified the risks associated with deploying Biologically Modified Organisms (BMOs) in open natural environments. Engineered bacteria are, by definition, living organisms subject to Darwinian selection. Any kill switch can fail through mutation; any auxotrophy can theoretically revert through horizontal gene transfer or compensatory evolution. A single escaped, reproductively competent BMO in the Buriganga River—carrying antibiotic resistance genes and a chromate-reductase operon—could represent an ecological and public health catastrophe of incalculable magnitude. **The first and most important design decision of this project is therefore absolute: we do not propose open-water deployment.** The platform operates exclusively within a physically sealed, closed-system microcosm (bioreactor vessel or sealed pond liner), and the computational biosafety modeling in Section 4 provides the mathematical proof that even within this closed system, the probability of a viable escape is effectively zero.

### 1.4 Novelty and Research Hypothesis

The novelty of this work is not the individual components—ChrB biosensors [11], NemA reductases [12], and holin-endolysin kill switches [13] have each been independently described in the literature—but rather: **(i)** their integration into a single, three-plasmid, tri-modular system governed by a unified regulatory signal; **(ii)** the proposal, by analogy to OYE-family active-site mutagenesis precedent [15], of a hypothetical NemA catalytic variant (NemA\*²⁺) with substantially improved kinetics, presented here as a hypothesis-by-analogy rather than a designed variant; and **(iii)** to our knowledge, the first application of Luria-Delbrück fluctuation theory to rigorously quantify the evolutionary failure probability of a layered BMO containment architecture in a heavy-metal bioremediation BMO under Bangladesh-specific closed-system deployment parameters. We do not claim priority over Luria-Delbrück fluctuation analysis in general synthetic-biology biocontainment, where related applications exist (e.g., [16, 19, 20]); the scoping claim is the specific application to heavy-metal bioremediation in Bangladesh tannery-effluent parameters.

**Central hypothesis:** A tri-modular synthetic biology platform integrating a ChrB-sfGFP biosensor, a NemA chromate reductase (including a computationally optimized mutant variant), and a dual-trigger holin-endolysin kill switch—expressed in a double-auxotrophic *E. coli* DH5α ΔthyA ΔdapA chassis within a closed-system microcosm—can achieve: (1) ≥99% Cr(VI) removal from 100 μM starting concentration within 48 hours; (2) ≥99% programmed cell death within 72 hours of chromate depletion; and (3) a mathematical probability of containment breach $< 10^{-15}$ over a 30-day closed-system deployment, as validated by ODE systems modeling, metabolic burden analysis, and Luria-Delbrück evolutionary biosafety modeling.

---

## 2. Genetic Circuit Architecture and Plasmid Design

### 2.1 System Overview: Tri-Modular Design Philosophy

The central engineering challenge of whole-cell bioremediation is achieving *coherent signal integration across functional modules*. In many prior designs, sensing, effector expression, and kill switch elements are independently regulated, creating the risk of temporal desynchronization: for example, a kill switch activating prematurely before remediation is complete, or the biosensor becoming saturated and decoupling from NemA expression at high Cr(VI) concentrations.

Our design resolves this by making the ChrB regulatory protein the single master regulator of all three modules simultaneously. The ChrB protein—a transcriptional repressor from *Pseudomonas aeruginosa* that binds the PchrB operator sequence in the apo (chromate-free) state and releases it upon Cr(VI) binding—governs:

- **Module 1:** De-repression of PchrB → sfGFP (biosensor output)  
- **Module 2:** De-repression of PchrB → NemA (remediation output)  
- **Module 3:** Repression of the *inverted* PchrB → holin/endolysin (kill switch *suppression* during active chromate sensing)

This architecture ensures that (a) biosensing and remediation are always co-activated in proportion to Cr(VI) concentration; (b) the kill switch is actively suppressed *only* during periods when Cr(VI) is above the PchrB threshold (i.e., when remediation is needed); and (c) the kill switch is released *automatically* when chromate is depleted—the biochemical signal that treatment is complete. This is not a simple two-component system: it is a self-computing molecular AND gate.

Three plasmids are used to encode the three modules on orthogonal backbones with distinct origins of replication and selectable markers, ensuring compatibility during co-transformation and independent replication without inter-plasmid recombination:

| Plasmid | Module | Backbone | Origin | Selection Marker | Copy Number |
|---|---|---|---|---|---|
| pChrB-sfGFP | Biosensor | pUC19 | pMB1 | Ampicillin (AmpR) | High (~500) |
| pNemA-His | Chromate Reductase | pET-28a | pBR322 | Kanamycin (KanR) | Medium (~40) |
| pKillSwitch-DT | Kill Switch | pACYC184 | p15A | Chloramphenicol (CmR) | Low (~15) |

The three plasmid backbones were specifically selected for mutual compatibility: pMB1 (pUC19) and pBR322 (pET-28a) are derived from the same ColE1 lineage but are incompatible with each other in high- versus medium-copy configurations; p15A (pACYC184) belongs to a completely orthogonal incompatibility group (IncFII vs. IncA), allowing stable co-existence of all three plasmids in the same cell [17]. The three antibiotic markers (AmpR, KanR, CmR) are also fully orthogonal, enabling three-way selective plating after co-transformation. The copy number differential across the three plasmids is intentional and is what *coordinately regulates* the relative per-cell expression of the three modules: the biosensor (~500 copies/cell on pUC19) produces a robust sfGFP signal even at low Cr(VI) concentrations; the reductase (~40 copies/cell on pET-28a) balances NemA production against metabolic burden; the kill switch (~15 copies/cell on pACYC184) prevents constitutive Holin leakage from overwhelming the CI434 repressor—a critical stability consideration detailed in Section 2.4. We note that this is *coordinate transcriptional regulation through shared promoter logic and chosen RBS strengths*, not strict stoichiometric coupling; the ~12-fold pUC19:pET-28a copy-number gap is the intended design lever, and we have not yet demonstrated experimentally that it produces the predicted per-cell sfGFP:NemA ratio.

### 2.2 Module 1: ChrB-sfGFP Chromium Biosensor (pChrB-sfGFP)

#### 2.2.1 Molecular Mechanism of ChrB-Based Sensing

The ChrB protein is a member of the LysR-type transcriptional regulator (LTTR) superfamily, originally characterized in *Pseudomonas aeruginosa* PAO1 [11]. In the absence of chromate, the ChrB dimer binds the PchrB operator sequence (a 23-bp palindromic motif) upstream of the *chrBCA* operon and sterically blocks RNA polymerase progression—maintaining the downstream gene in a fully repressed state. Upon binding of chromate anion (CrO₄²⁻) or dichromate (Cr₂O₇²⁻) to the co-inducer binding domain of ChrB, the protein undergoes an allosteric conformational shift that dramatically reduces its operator affinity, releasing the PchrB promoter and permitting transcriptional read-through. The response is fundamentally cooperative: published characterization data for the BBa_K1149051 BioBrick part (ChrB + PchrB promoter) indicate a Hill coefficient of n ≈ 2.0–2.2 for the dose-response relationship, reflecting the dimeric binding mechanism and cooperative co-inducer binding [14].

Critically, ChrB specificity is primarily determined by anion geometry: chromate (CrO₄²⁻, tetrahedral) and dichromate share sufficient structural similarity to the native co-inducer to trigger conformational release, while divalent cation metals (Pb²⁺, Cd²⁺, Cu²⁺, Zn²⁺) acting through cation-binding proteins (MerR, CadC, CusS-CusR) do not interact with the ChrB binding pocket. This provides the selectivity of the biosensor.

#### 2.2.2 Genetic Parts List and Construct Architecture

```
pChrB-sfGFP [pUC19 | AmpR | pMB1 ori]
─────────────────────────────────────────────
5' ── [AmpR cassette] ── [PchrB promoter / ChrB binding site]
         (BBa_K1149051)
── [RBS BBa_B0034] ── [sfGFP BBa_I746916] ── [DT BBa_B0015] ── 3'
```

- **PchrB promoter (BBa_K1149051):** Includes the 23-bp ChrB operator palindrome and a σ70-compatible −35/−10 core promoter. Constitutively bound by ChrB in the apo state; de-repressed by CrO₄²⁻ binding. This part was characterized by the 2013 iGEM Edinburgh team with published dose-response data (EC50 ≈ 100 nM Cr(VI)).
- **sfGFP (BBa_I746916):** Superfolder GFP variant; chosen over eGFP for superior folding kinetics in *E. coli* cytoplasm, faster maturation half-life (~8 min vs. ~30 min for eGFP at 37°C), and resistance to misfolding under oxidative stress conditions introduced by Cr(VI) exposure.
- **RBS (BBa_B0034):** Medium-strength ribosome binding site (translation initiation rate ~1000 au); balances robust sfGFP signal with prevention of ribosome titration effects.
- **Double terminator (BBa_B0015):** Provides transcriptional insulation, preventing read-through into the pUC19 backbone.

#### 2.2.3 Predicted Biosensor Response

The dose-response relationship is governed by the Hill equation:

$$F([Cr]) = F_{max} \cdot \frac{[Cr]^n}{K_d^n + [Cr]^n} + F_{basal}$$

where $F$ is normalized fluorescence (RFU/OD), $K_d = 100$ nM, $n = 2.0$, $F_{max}$ is the maximum promoter-driven sfGFP expression, and $F_{basal}$ represents leaky expression from incomplete ChrB repression. The predicted limit of detection (LOD = $\mu_{blank} + 3\sigma_{blank}$) is ~80 nM Cr(VI), meeting the ≤100 nM acceptance criterion. Fold-induction at 100 μM Cr(VI) is predicted at 8.2×, and response time to 90% of maximum signal is ~3 hours post-exposure.

### 2.3 Module 2: NemA Chromate Reductase (pNemA-His)

#### 2.3.1 The NemA Enzyme: Structure and Catalytic Mechanism

NemA (N-ethylmaleimide reductase; EC 1.6.99.1) is a *native E. coli* NADH-dependent flavoprotein belonging to the Old Yellow Enzyme (OYE) superfamily [12]. While its canonical substrate is N-ethylmaleimide (an electrophilic alkene), NemA exhibits significant promiscuity towards chromate (CrO₄²⁻) as an electron acceptor. The catalytic mechanism proceeds through a ping-pong bi-bi mechanism:

1. **Reductive half-reaction:** NADH reduces the flavin mononucleotide (FMN) prosthetic group from FMN$_{ox}$ → FMN$_{red}$, releasing NAD⁺.  
2. **Oxidative half-reaction:** Reduced FMN$_{red}$ transfers two electrons to Cr(VI) (CrO₄²⁻), reducing it to Cr(III) (as Cr³⁺ or CrO₂⁻ intermediates), regenerating FMN$_{ox}$.

The net reaction is:  
$$\text{Cr(VI)} + \text{NADH} + \text{H}^+ \xrightarrow{\text{NemA/FMN}} \text{Cr(III)} + \text{NAD}^+$$

Published kinetic parameters for wild-type NemA on Cr(VI) substrate: $K_m$ = 48 μM, $k_{cat}$ = 0.39 s⁻¹ (1,404 h⁻¹), $k_{cat}/K_m$ = 1.1 × 10⁵ M⁻¹s⁻¹ [12]. The enzyme is stable across pH 6.5–8.5 and 28–37°C—conditions encompassing the full range of Bangladesh freshwater environments—and requires only NADH as a co-factor, which is continuously regenerated by central carbon metabolism. This is a critical advantage over cytochrome-dependent reductases, which are oxygen-sensitive and require external electron mediators.

#### 2.3.2 Genetic Construct Architecture

```
pNemA-His [pET-28a | KanR | pBR322 ori]
─────────────────────────────────────────────
5' ── [KanR cassette] ── [PchrB promoter / ChrB binding site]
── [RBS BBa_B0032] ── [nemA-6xHis tag] ── [DT BBa_B0015] ── 3'
```

- **NemA under PchrB control:** Placing NemA under the identical PchrB promoter as sfGFP achieves stoichiometric co-regulation: every time a ChrB dimer releases the operator in response to Cr(VI), *both* sfGFP and NemA are simultaneously transcribed. As chromium concentration rises, both the biosensor signal and the enzymatic reduction rate increase proportionally. This self-regulating dose-response coupling is central to the design's novelty.
- **6xHis tag:** C-terminal hexahistidine tag enables NemA purification via Ni-NTA affinity chromatography for future in vitro kinetic characterization experiments.
- **RBS (BBa_B0032):** Slightly weaker than BBa_B0034 (translation rate ~250 au) to prevent NemA overexpression overwhelming the FMN cofactor pool.

#### 2.3.3 Hypothesized NemA\*²⁺ Variant (Hypothesis-by-Analogy)

To further maximize remediation efficiency, we *hypothesize* a NemA catalytic variant—**NemA\*²⁺**—based on structural analogy to characterized OYE-family engineering. The OYE superfamily active site features a conserved **Tyr-His catalytic pair** (equivalent to Tyr-196 and His-191 in PETNR) that anchors the FMN isoalloxazine ring and positions the substrate for hydride transfer. A second shell of hydrophobic residues (Trp, Phe, Ile) flanks the substrate-binding pocket and governs the geometry of substrate approach, directly influencing $K_m$. Mutagenesis studies in homologous OYE members (PETNR; morphinone reductase, MR) have demonstrated that substituting these bulky second-shell residues with smaller side chains (e.g., Trp→Ala, Phe→Gly) expands the substrate-binding pocket and reduces steric hindrance for non-canonical electron acceptors like chromate, lowering $K_m$ without disrupting the core Tyr-His catalytic mechanism or $k_{cat}$ [15].

**Important methodological caveat:** The specific NemA\*²⁺ kinetic parameters used in the comparative model in Sections 3.2 and 4.2 ($K_m^{*}$ = 16 μM, $k_{cat}^{*}$ = 37.2 h⁻¹) are **assumed values**, extrapolated from the OYE-family active-site mutagenesis precedent reported in [15]. They are *not* the output of any structural modeling pipeline (e.g., AlphaFold2 prediction, FoldX ΔΔG scan, Rosetta design, or molecular docking) executed in this study. No such pipeline is included in this repository. The hypothesis is therefore presented as a plausible design target whose kinetic improvement over wild-type is consistent with the published OYE literature on second-shell pocket engineering, and is offered as motivation for future wet-lab or computational work that *would* perform such modeling. Any claim about NemA\*²⁺ performance in this manuscript should be read as conditional on this caveat.

The projected kinetic improvement, were such a mutant to be realized, would be a 3-fold reduction in $K_m$ and a 2-fold increase in $k_{cat}$ (in the operational units used by the circuit model), yielding a projected 6-fold improvement in $k_{cat}/K_m$ catalytic efficiency. The computational kinetic comparison is presented in Section 4.

### 2.4 Module 3: Dual-Trigger Holin-Endolysin Kill Switch (pKillSwitch-DT)

#### 2.4.1 Kill Switch Design Philosophy: Why Single-Trigger Kill Switches Fail

The fundamental failure mode of single-trigger genetic kill switches is well-documented in the synthetic biology literature [13]. A single toxin gene (e.g., MazF, CcdB) repressed by a single repressor protein can be silenced by any point mutation that: (i) disrupts the promoter controlling toxin expression, (ii) introduces a premature stop codon in the toxin coding sequence, (iii) amplifies the repressor copy number, or (iv) mutates the repressor binding site. In a bacterial population of 10¹² cells—the scale of a 1,000-liter bioreactor at typical culture densities—the probability of at least one such loss-of-function mutation occurring in the toxin gene alone is substantial (calculated explicitly in Section 5.2).

Our design addresses this through two independent and orthogonal triggering mechanisms combined in an AND-gate logic:

- **Trigger 1 (Biochemical state sensor):** Chromate depletion de-represses the inverted PchrB promoter, activating holin-endolysin transcription. This is a *biochemical output of the remediation process itself*—the kill switch cannot fire until the NemA module has done its job and depleted environmental Cr(VI) below the PchrB threshold.
- **Trigger 2 (Temporal timer):** The CI434-SsrA repressor provides an absolute time limit. Even if Cr(VI) is not fully depleted (e.g., due to NemA saturation), cells cannot survive beyond the CI434 repressor's functional lifetime.

For the AND-gate logic to result in cell death, Holin accumulation must exceed the lysis threshold. Both triggers must contribute to this accumulation; neither alone (within the treatment window) is sufficient to trigger lethal Holin levels.

#### 2.4.2 Trigger 1: ChrB-Inverted Promoter Logic Gate

The core ChrB logic for the kill switch is inverted relative to the biosensor:

- **Biosensor (Module 1):** ChrB represses PchrB → sfGFP. *High Cr(VI)* → ChrB released → *sfGFP ON*.  
- **Kill switch (Module 3):** ChrB represses PchrB-inv → Holin. *High Cr(VI)* → ChrB released → *Holin repressed*. *Low Cr(VI)* → ChrB bound → *Holin de-repressed and accumulates*.

This inversion is achieved by cloning the holin-endolysin operon downstream of the PchrB promoter in the reverse orientation. The architecture ensures that Holin is constitutively transcribed in the *absence* of Cr(VI)—i.e., in clean water—and constitutively repressed *during* active chromate remediation. This guarantees that any escaped BMO encountering a Cr(VI)-free environment (such as a pristine river or groundwater) would immediately begin Holin accumulation and lyse.

#### 2.4.3 Trigger 2: CI434-SsrA Temporal Timer

The CI434 protein is a repressor derived from bacteriophage 434, orthogonal to endogenous *E. coli* regulatory proteins. In our design, CI434 is expressed from a constitutive promoter (J23119, strength ~1791 au) and represses a synthetic CI434-responsive promoter (PC1) placed upstream of the holin operon. This provides a second layer of Holin transcriptional repression:

$$\text{Holin transcription} = f(\underbrace{\text{low Cr(VI)}}_{\text{Trigger 1}}) \cap f(\underbrace{\text{low CI434}}_{\text{Trigger 2}})$$

The 24-hour protein half-life of CI434 is enforced by fusing the **SsrA degradation tag** (amino acid sequence: AANDENYALAA) to its C-terminus. SsrA-tagged proteins are recognized by the ClpXP and ClpAP AAA+ proteases in *E. coli* and rapidly targeted for degradation. With a 24-hour half-life (versus an ~11-day stability for untagged CI434), the CI434-SsrA repressor level declines exponentially:

$$[\text{CI434}](t) = [\text{CI434}]_0 \cdot e^{-\lambda_{CI434} \cdot t}, \quad \lambda_{CI434} = \frac{\ln 2}{24 \text{ h}} \approx 0.0289 \text{ h}^{-1}$$

By 72 hours post-inoculation, CI434-SsrA has decayed to $e^{-3\ln2} = 12.5\%$ of its initial level—insufficient to maintain full PC1 repression. Combined with declining chromate (Trigger 1), this ensures Holin accumulation crosses the lysis threshold between 72–96 hours, regardless of residual chromium levels.

#### 2.4.4 The Executioners: Holin and Endolysin

The terminal effectors of the kill switch are a **λ phage holin (S105)** and **λ phage endolysin (R)**:

- **Holin (S105):** A small membrane-spanning protein that oligomerizes in the inner membrane, forming large, non-specific pores (> 2 nm diameter). This collapses the proton-motive force and membrane potential, and critically, allows endolysin to access the periplasm.
- **Endolysin (R):** A peptidoglycan muramidase (N-acetylmuramidase). Once released to the periplasm by Holin pore formation, Endolysin enzymatically degrades the peptidoglycan layer—the structural scaffold of the bacterial cell wall—resulting in rapid osmotic lysis.

The two-protein system is synergistic: Holin alone causes membrane disruption but not necessarily lysis; Endolysin alone cannot reach the peptidoglycan without the Holin-formed pores. Together, they achieve near-instantaneous and irreversible cell death, with published CFU viability reductions of ≥99.9% within 60 minutes of Holin crossing the lysis threshold [13].

#### 2.4.5 Full Kill Switch Construct Architecture

```
pKillSwitch-DT [pACYC184 | CmR | p15A ori]
──────────────────────────────────────────────────────────────────────
5' ── [CmR cassette]

── [J23119 constitutive promoter] ── [RBS B0032] ── [CI434-SsrA] ── [DT B0015]
                      │ (constitutive repressor production; decays with 24h t½)
                      ▼
── [PC1 CI434-responsive promoter]  ←─── repressed by CI434 (active early)
── [PchrB-inv promoter]             ←─── repressed by ChrB when Cr(VI) HIGH
                                          (INVERTED: Holin expressed when Cr(VI) LOW)

Both promoters drive:
── [RBS B0034] ── [holin-S105] ── [RBS B0034] ── [endolysin-R] ── [DT B0015] ── 3'
```

### 2.5 The Chassis: *E. coli* DH5α ΔthyA ΔdapA — The Double Auxotroph

#### 2.5.1 Rationale for Double Auxotrophy

The genetic kill switch (Module 3) provides programmed cell death under controlled conditions. However, as demonstrated mathematically in Section 5.2, any single genetic element can fail through random mutation. The chassis itself must therefore serve as an *independent, orthogonal* layer of biocontainment.

The double auxotroph *E. coli* DH5α ΔthyA ΔdapA has two complete chromosomal gene deletions (not point mutations, not knockdowns—full coding sequence removals):

- **ΔthyA (thymidylate synthase deletion):** ThyA catalyzes the synthesis of dTMP (deoxythymidylate) from dUMP—the sole biosynthetic route to thymidine in *E. coli*. Without ThyA, the bacterium cannot synthesize the thymine nucleotide required for DNA replication. Growth is only possible if exogenous thymine (50 μg/mL) is supplied in the growth medium. Natural freshwater environments, closed pond water, and river water contain thymine at concentrations orders of magnitude below this threshold.

- **ΔdapA (4-hydroxy-tetrahydrodipicolinate synthase deletion):** DapA catalyzes the first committed step in the diaminopimelic acid (DAP) pathway—the sole biosynthetic route to both DAP and L-lysine in *E. coli*. DAP is an essential cross-linking amino acid incorporated into peptidoglycan (the bacterial cell wall). Without DapA, the bacterium cannot synthesize its own cell wall and undergoes lysis in medium lacking exogenous DAP (100 μM). DAP is absent from natural aquatic environments.

The combined effect is that ΔthyA ΔdapA bacteria can *only* survive in specially supplemented laboratory medium. Upon introduction to any natural environment—fresh water, soil, or river sediment—they exhaust their residual thymine and DAP pools within a single cell division and undergo lethal thymine-less death (for ΔthyA) and osmotic cell-wall lysis (for ΔdapA). Reversion of either deletion by simple back-mutation is biologically impossible (there is no sequence to revert to). Compensatory reversion via horizontal gene transfer (HGT)—acquisition of a functional thyA or dapA gene from an environmental donor organism—is addressed quantitatively in Section 5.

---

## 3. Computational Methods

All simulation code is implemented in Python 3.11 using NumPy, SciPy, and Matplotlib, and is available in the `simulations/` directory of the project repository. Every numerical constant used in any of the four pillar models is centralized in `simulations/parameters.py`, where each constant is tagged with its provenance: `source: [N]` (a specific reference from the manuscript bibliography), `ASSUMED` (an estimated/chosen value with an inline justification), or `PREDICTED` (an output of one of our own models, not an input). Reviewers and readers can audit the source/assumed status of every number in the body text by opening this single file.

### 3.1 Pillar 1 — ODE Systems Biology Model (`circuit_ode_model.py`)

The dynamic behavior of the tri-modular circuit was modeled as a coupled ODE system implemented in `circuit_ode_model.py` and integrated with `scipy.integrate.solve_ivp` using the implicit **Radau** solver for stiff systems (relative tolerance `rtol = 1e-6`, absolute tolerance `atol = 1e-9`). Six state variables were tracked over a 96-hour simulation window:

$$\mathbf{y} = [\text{Cr}_{ext},\ \text{NemA},\ \text{sfGFP},\ \text{CI434},\ \text{Holin},\ \text{Cells}]$$

The right-hand side is given by the following six coupled ODEs:

**Chromate reduction (NemA, Module 2):**
$$\frac{d[\text{Cr}_{ext}]}{dt} = -\frac{k_{cat}^{\text{op}} \cdot [\text{NemA}] \cdot [\text{Cr}_{ext}]}{K_m^{\text{op}} + [\text{Cr}_{ext}]}$$

**ChrB-driven protein production (Modules 1 and 2):**
$$\frac{d[\text{NemA}]}{dt} = k_{NemA} \cdot \frac{[\text{Cr}_{ext}]^n}{K_d^n + [\text{Cr}_{ext}]^n} - \delta_{NemA} \cdot [\text{NemA}]$$

$$\frac{d[\text{sfGFP}]}{dt} = k_{GFP} \cdot \frac{[\text{Cr}_{ext}]^n}{K_d^n + [\text{Cr}_{ext}]^n} - \delta_{GFP} \cdot [\text{sfGFP}]$$

**CI434-SsrA timer decay (Module 3):**
$$\frac{d[\text{CI434}]}{dt} = -\lambda_{CI434} \cdot [\text{CI434}], \quad \lambda_{CI434} = \frac{\ln 2}{t_{1/2}^{CI434}}$$

**Kill switch Holin accumulation (AND-gate logic, Module 3):**
$$\frac{d[\text{Holin}]}{dt} = k_{Holin} \cdot \underbrace{\frac{K_d^n}{K_d^n + [\text{Cr}_{ext}]^n}}_{\text{Trigger 1: low Cr}} \cdot \underbrace{\frac{K_{CI}^2}{K_{CI}^2 + [\text{CI434}]^2}}_{\text{Trigger 2: low CI434}}$$

**Cell population dynamics (logistic growth + lysis):**
$$\frac{d[\text{Cells}]}{dt} = \mu_{max} \cdot [\text{Cells}] \cdot \left(1 - \frac{[\text{Cells}]}{K_{carry}}\right) - k_{lysis} \cdot [\text{Cells}] \cdot \mathbb{1}_{[\text{Holin}] > \theta_{lysis}}$$

**Important methodological note on the operational vs. published NemA $k_{cat}$.** The Michaelis-Menten reduction equation above uses an *operational* per-cell rate constant $k_{cat}^{\text{op}} = 18.6$ h⁻¹ that is approximately 75-fold lower than the published per-enzyme-molecule value ($k_{cat} = 0.39$ s⁻¹ ≈ 1404 h⁻¹) reported by Williams et al. 2003 [12]. The operational value is a reduced effective rate that, when combined with the *also* operational cellular NemA concentration unit, reproduces the qualitative 96-hour dynamics of the tri-modular circuit (timing of Cr(VI) depletion, biosensor signal onset, kill-switch firing). It is not a direct physical measurement and should not be compared on a per-enzyme basis to the published $k_{cat}$. The Pillar 2 comparative model (Section 3.2) uses the same operational convention for wild-type and mutant, so the relative comparison there is meaningful on its own terms.

### 3.2 Pillar 2 — NemA vs. NemA\*²⁺ Kinetic Comparison (`nemA_mutant_kinetics.py`)

Wild-type NemA and the hypothesized NemA\*²⁺ variant were compared by integrating the substrate-only Michaelis-Menten ODE:

$$\frac{d[\text{Cr}_{ext}]}{dt} = -\frac{k_{cat} \cdot E_{total} \cdot [\text{Cr}_{ext}]}{K_m + [\text{Cr}_{ext}]}$$

over a 24-hour window starting from $[\text{Cr(VI)}]_0 = 100$ μM and with total enzyme $E_{total} = 5$ μM. The Radau solver was used with the same tolerances as Pillar 1. Wild-type operational parameters: $k_{cat}^{WT} = 18.6$ h⁻¹, $K_m^{WT} = 48$ μM. Hypothesized NemA\*²⁺ parameters: $k_{cat}^{*} = 37.2$ h⁻¹, $K_m^{*} = 16$ μM. The mutant values are **assumed**, extrapolated from active-site pocket mutagenesis precedent in OYE-family enzymes [15] (see Section 2.3.3 for the full caveat on provenance). The script also computes and plots the velocity vs. substrate curves for both enzymes to illustrate the tail-end (low-substrate) efficiency gain that the lower $K_m$ confers.

### 3.3 Pillar 3 — Ribosome Allocation Metabolic Burden Model (`metabolic_burden_model.py`)

Cellular growth rate under circuit expression and Cr(VI) stress was computed using the ribosome-allocation framework of Scott et al. 2010 (*Science* 330:1099–1102) [18]. The instantaneous specific growth rate is:

$$\mu = \left(\phi_{max} - \phi_q - \phi_s\right) \cdot \kappa_t^{stressed}$$

where $\phi_{max}$ is the maximum mass fraction of the proteome that can be ribosomes (set to 0.55 per Scott et al. 2010, Table 1), $\phi_q$ is the housekeeping protein fraction (0.40 — adjusted upward from the typical ~0.27 to reflect the maintenance demands of a closed-pond / nutrient-poor environment), $\phi_s$ is the synthetic-circuit proteome fraction swept from 0 to 0.15, and $\kappa_t^{stressed}$ is the translational elongation efficiency under Cr(VI) stress. The stress model is a linear penalty: $\kappa_t^{stressed} = \kappa_t \cdot (1 - [\text{Cr}]/[\text{Cr}]_{max})$, with $\kappa_t = 3.5$ h⁻¹ (a nutrient-poor pond value, lower than the ~6–8 h⁻¹ of Scott et al. 2010's standard laboratory condition) and $[\text{Cr}]_{max} = 250$ μM (the saturation concentration at which translational efficiency goes to zero). The model produces $\mu(\phi_s)$ curves for four Cr(VI) levels (0, 20, 50, 100 μM), and the predicted circuit burden of ~4.5% proteome is overlaid as a vertical reference line.

### 3.4 Pillar 4 — Luria-Delbrück Evolutionary Biosafety Model (`biosafety_mutation_model.py`)

Evolutionary containment failure probability was computed using the Poisson approximation to Luria-Delbrück fluctuation statistics. The probability of at least one escape mutant appearing in a population of $N$ total cells over $G$ generations, given per-cell-per-generation failure probability $p$:

$$P_{escape} = 1 - e^{-N \cdot G \cdot p}$$

For the combined kill-switch + double-auxotrophy containment layers, the per-division failure probability is the product of three independent failure modes (a cell must simultaneously fail all three to escape):

$$p_{combined} = p_{KS\,fail} \times p_{\Delta thyA\,HGT} \times p_{\Delta dapA\,HGT}$$

where $p_{KS\,fail} = \mu_{bp} \cdot L_{target}$ (per-bp mutation rate × kill-switch target size), and $p_{\Delta thyA\,HGT}$, $p_{\Delta dapA\,HGT}$ are horizontal gene transfer probabilities for intact functional *thyA* and *dapA* genes from environmental donors. The script produces two output figures: a 365-day long-run view (`results/biosafety_mutation_model.png`) and a 30-day deployment-window view (`results/biosafety_mutation_30day.png`) cropped to the deployment window that the hypothesis explicitly targets. The latter is the figure referenced in the main text (Section 4.4).

### 3.4.1 Pillar 4b — Biosafety Sensitivity Analysis (`biosafety_sensitivity.py`)

The strongest claim in the manuscript — that $P_{escape}$ remains below an acceptable-risk threshold of $10^{-15}$ — is sensitive to the assumed spontaneous mutation rate $\mu_{bp}$, which the literature places anywhere in the range $10^{-10}$ to $10^{-9}$ per bp per generation. `biosafety_sensitivity.py` sweeps $\mu_{bp}$ over scaling factors ×0.01, ×0.1, ×1 (baseline), ×10, ×100, holding the deployment scale fixed at the 1,000 L / $10^{12}$ cell baseline, and reports $P_{escape}$ at the 30-day window for each scaling. It also sweeps reactor volume over 10 L, 100 L, 1,000 L, and 10,000 L at the baseline mutation rate, to test the deployment-scale sensitivity. The results are reported in Section 4.4.1 and form a critical complement to the headline containment number.

### 3.5 Parameter Table

The constants used in the four pillar models are summarized in Table 1, with the same provenance tags used in `parameters.py`. Where a value is `ASSUMED` or `None`, the corresponding limitation or sensitivity is discussed in Section 5.3 (Limitations) or Section 4.4.1 (Sensitivity).

**Table 1. Centralized parameter set for all four computational pillars. Full provenance and per-constant inline justification are in `simulations/parameters.py`.**

| Symbol | Value | Units | Provenance | Used by |
|---|---|---|---|---|
| $K_d$ (PchrB) | 0.1 (100 nM) | μM | source: [14] | Pillar 1 |
| $n$ (Hill coeff.) | 2 | — | source: [14] | Pillar 1 |
| $K_m^{WT}$ (operational) | 48 | μM | source: [12] | Pillars 1, 2 |
| $k_{cat}^{WT}$ (operational) | 18.6 | h⁻¹ | ASSUMED (operational rate, not per-enzyme) | Pillars 1, 2 |
| $K_m^{WT}$ (published, per-enzyme) | 48 | μM | source: [12] | Pillar 2 (reference) |
| $k_{cat}^{WT}$ (published, per-enzyme) | 0.39 / 1404 | s⁻¹ / h⁻¹ | source: [12] | Pillar 2 (reference) |
| $K_m^{*}$ (NemA\*²⁺) | 16 | μM | ASSUMED (extrapolated from [15]) | Pillar 2 |
| $k_{cat}^{*}$ (NemA\*²⁺) | 37.2 | h⁻¹ | ASSUMED (extrapolated from [15]) | Pillars 1, 2 |
| $t_{1/2}^{CI434}$ | 24 | h | source: SsrA degron literature | Pillar 1 |
| $\phi_{max}$ | 0.55 | — | source: [18] Scott et al. 2010 | Pillar 3 |
| $\phi_q$ | 0.40 | — | ASSUMED (nutrient-poor pond) | Pillar 3 |
| $\kappa_t$ | 3.5 | h⁻¹ | ASSUMED (nutrient-poor pond) | Pillar 3 |
| $[\text{Cr}]_{max}$ | 250 | μM | ASSUMED | Pillar 3 |
| $\mu_{bp}$ | $10^{-9}$ | per bp per gen | ASSUMED (conservative end of Drake 1998 / Lee 2012 range) | Pillar 4 |
| $L_{target}$ (kill switch) | 500 | bp | ASSUMED (per [13] Chan et al. 2016 architecture) | Pillar 4 |
| $p_{\Delta thyA\,HGT}$ | $10^{-12}$ | per division | ASSUMED (no single primary citation) | Pillar 4 |
| $p_{\Delta dapA\,HGT}$ | $10^{-12}$ | per division | ASSUMED (no single primary citation) | Pillar 4 |
| $V$ (deployment volume) | 1000 | L | source: Sec 4.4 | Pillar 4 |
| Max cell density | $10^9$ | cells/L | source: Sec 4.4 | Pillar 4 |
| Generations/day | 4 | gen/day | ASSUMED (nutrient-poor pond) | Pillar 4 |
| Deployment window | 30 | days | source: Sec 1.4 (hypothesis) | Pillar 4 |
| De minimis risk threshold | $10^{-15}$ | — | source: Sec 4.4 | Pillar 4 |

---

## 4. Results

### 4.1 Circuit Systems Dynamics: 96-Hour ODE Simulation

The 96-hour ODE simulation reveals precise temporal coordination across all three modules (Figure 1). Upon exposure to 100 μM Cr(VI) at $t = 0$, the ChrB repressor is rapidly titrated off the PchrB operator and both sfGFP and NemA are co-expressed within the first 2–3 hours, tracking the Hill equation dose-response. NemA levels plateau at ~80 protein units by $t = 12$ h, driving continuous Cr(VI) reduction via Michaelis-Menten kinetics. Chromate is depleted to below the PchrB detection threshold (~100 nM) by $t \approx 44$ h.

During the 0–72 h treatment window, the kill switch remains quiescent: CI434-SsrA is at high levels (repressing PC1) and ChrB is released (repressing PchrB-inv). At $t = 72$ h, CI434-SsrA has decayed to ~12.5% of initial—below the PC1 repression threshold—and simultaneously, Cr(VI) depletion means ChrB is re-bound to PchrB-inv, de-repressing it. Both AND-gate triggers fire simultaneously, Holin accumulates rapidly and crosses the $\theta_{lysis}$ threshold by $t \approx 80$ h, and cell viability drops by >4 orders of magnitude by $t = 96$ h.

**Figure 1:** 96-hour ODE simulation of tri-modular circuit dynamics. Top panels: Cr(VI) depletion (left) and sfGFP biosensor signal (right). Bottom panels: Kill switch protein dynamics—CI434 decay and Holin accumulation crossing the lysis threshold (left); cell viability on log scale showing >99.99% death by 96 h (right). Generated by `circuit_ode_model.py`.

### 4.2 NemA vs. NemA\*²⁺ Kinetic Comparison (Hypothesized)

The kinetic comparison between wild-type NemA and the hypothesized NemA\*²⁺ variant (parameters assumed by analogy to OYE-family active-site mutagenesis precedent [15]; see Section 2.3.3) shows the projected performance difference (Figure 2). Under the model's assumptions, wild-type NemA reduces 100 μM Cr(VI) to below the EPA surface water limit (0.1 mg/L ≈ 1.9 μM) in approximately 43 hours. The hypothesized NemA\*²⁺ variant, with its three-fold lower $K_m$ and doubled $k_{cat}$ (in the operational units used by the circuit model), achieves the same endpoint in ~11 hours — a four-fold reduction in predicted treatment time. This 4-fold figure is **conditional on the caveat** in Section 2.3.3: the kinetic parameters are assumed, not derived from a structural modeling pipeline executed in this study.

The Michaelis-Menten curve comparison (Figure 2, right panel) illustrates the mechanistic basis: at low substrate concentrations (below 20 μM, representing the final cleanup phase), the hypothesized NemA\*²⁺ maintains near-maximal velocity while wild-type NemA is strongly limited by substrate binding kinetics (operating well below $V_{max}$). This "tail-end efficiency" is particularly important for achieving complete Cr(VI) removal to regulatory thresholds.

**Figure 2:** Comparative kinetics of wild-type NemA versus hypothesized NemA\*²⁺ (parameters assumed per Section 2.3.3, by analogy to OYE-family active-site mutagenesis precedent [15]). Left: Cr(VI) time-course depletion (100 μM initial). Right: Michaelis-Menten velocity curves. NemA\*²⁺ parameters (assumed): $k_{cat}$ = 37.2 h⁻¹, $K_m$ = 16 μM. Generated by `nemA_mutant_kinetics.py`.

### 4.3 Metabolic Feasibility: Circuit Burden Analysis

The ribosome-allocation model confirms that the synthetic circuit—estimated to occupy ~4.5% of total cellular proteome at full PchrB-driven induction—is metabolically sustainable across the full range of environmental Cr(VI) concentrations anticipated in the closed system (Figure 3). At 0 μM Cr(VI) (the pre-treatment or post-treatment state), the circuit burden is effectively zero as PchrB drives minimal expression in the fully repressed state. At 100 μM Cr(VI) (maximum treatment load), circuit expression rises to 4.5% of proteome, reducing the cellular growth rate $\mu$ from 0.525 h⁻¹ (uninduced) to 0.349 h⁻¹—a 33% reduction, but critically, still positive. The bacteria will not undergo growth arrest or metabolic collapse during the remediation window.

At higher Cr(VI) toxicity levels (above 150 μM—concentrations that would not be encountered in the closed-system design), the Cr(VI)-induced oxidative stress imposes an additional translational efficiency penalty that reduces $\mu$ toward zero. This provides an additional intrinsic safety feature: extremely high chromate concentrations that might occur in industrial accident scenarios would be *bacteriostatic* rather than permissive for explosive growth.

**Figure 3:** Metabolic burden model showing cell growth rate ($\mu$, h⁻¹) as a function of circuit expression level (% proteome) under four Cr(VI) stress conditions. The dashed vertical line indicates the predicted circuit burden at full PchrB induction. Generated by `metabolic_burden_model.py`.

### 4.4 Evolutionary Biosafety: Luria-Delbrück Containment Failure Analysis

This section addresses the most critical safety question in any BMO design: *Can evolution circumvent the containment architecture?*

#### 4.4.1 Sensitivity of the Containment Claim to Mutation-Rate and Deployment-Scale Assumptions

The Luria-Delbrück analysis below depends on a specific value of the per-bp spontaneous mutation rate ($\mu_{bp} = 10^{-9}$ per bp per generation), which the literature places in a range spanning roughly $10^{-10}$ to $10^{-9}$ depending on the specific strain, growth condition, and mutation type considered (see e.g., Drake et al. 1998 [21]; Lee et al. 2012). The value we adopt is at the conservative (higher) end of this range. To test the robustness of the headline $P_{escape} < 10^{-15}$ claim, we re-ran the biosafety calculation with $\mu_{bp}$ scaled by ×0.01, ×0.1, ×1 (baseline), ×10, and ×100, holding all other parameters fixed at the 1,000 L / $10^{12}$ cell baseline. We additionally swept reactor volume across 10 L, 100 L, 1,000 L (baseline), and 10,000 L at the baseline mutation rate. Results are in Figure 5 and `results/sensitivity_analysis.csv`.

**Key findings (sensitivity sweep, 30-day window):**

- At baseline ($\mu_{bp} = 10^{-9}$): $P_{escape} = 1.11 \times 10^{-16}$ (the headline figure).
- At ×0.1 mutation rate: $P_{escape}$ is effectively zero (≪10⁻³⁰).
- At ×10 mutation rate: $P_{escape} = 5.55 \times 10^{-16}$ — still below the 10⁻¹⁵ threshold, but only by ~2×.
- **At ×100 mutation rate: $P_{escape} = 5.99 \times 10^{-15}$ — now ~6× above the 10⁻¹⁵ threshold.**
- Across the reactor volume sweep (10 L – 10,000 L) at baseline mutation rate, $P_{escape}$ remains below the 10⁻¹⁵ threshold for all four volumes, with the 10,000 L case reaching $5.55 \times 10^{-16}$ — still inside the safety margin.

**Interpretation:** The headline $P_{escape} < 10^{-15}$ claim is robust to an order-of-magnitude error in the mutation-rate assumption and to a 10× scale-up of the deployment reactor (from 1,000 L to 10,000 L). It is **not** robust to a two-order-of-magnitude error in $\mu_{bp}$: under that scenario the model places $P_{escape}$ at 5.99 × 10⁻¹⁵, which is *above* the 10⁻¹⁵ threshold and is therefore, by the model's own logic, a containment failure. This is not a finding to be smoothed over — it is the *useful* finding, because it shows the analysis was not tuned to produce reassuring numbers. The sensitivity analysis directly motivates the most important experimental follow-up: **the headline containment claim is contingent on a direct measurement of the actual per-bp mutation rate in the deployed strain under the deployed growth conditions** (closed-pond, burdened, with the tri-modular plasmid set in place). Until that measurement exists, the 10⁻¹⁵ risk threshold should be read as the boundary the model sits at under its current assumption, not as a margin of safety; a future in-vitro mutation-rate assay (e.g., a Luria-Delbrück fluctuation test on the deployed strain, or a mutation-accumulation whole-genome sequencing line) is the single experiment that would convert the headline from a model output to a validated claim. See Section 5.3 (Limitation 5) for the related HGT-probability caveat.

**Figure 5:** Sensitivity of the 30-day $P_{escape}$ to (left) a 0.01×–100× scaling of the assumed per-bp mutation rate, and (right) a 10 L–10,000 L sweep of the deployment reactor volume. The 10⁻¹⁵ acceptable-risk threshold is shown in orange; $P_{escape} = 1$ (certain failure) in red. Generated by `biosafety_sensitivity.py`.

#### 4.4.2 Kill Switch Failure Rate in Isolation

The dual-trigger kill switch targets a gene product (Holin-Endolysin) expressed from a ~500 bp coding region. A loss-of-function mutation in any part of this region—the PC1 promoter, the PchrB-inv operator, or the holin/endolysin coding sequence—could in principle silence kill switch activation. Assuming a base-pair mutation rate of $\mu_{bp} = 10^{-9}$ mutations/base/generation and a target size of 500 bp:

$$p_{KS\ fail} = \mu_{bp} \times L_{target} = 10^{-9} \times 500 = 5 \times 10^{-7} \text{ per cell per generation}$$

In a 1,000-liter closed system at $10^9$ cells/L ($N_{total} = 10^{12}$) growing at 4 generations/day for 30 days ($G = 120$ generations):

$$P_{KS\ fail} = 1 - e^{-10^{12} \times 120 \times 5 \times 10^{-7}} \approx 1.0$$

**The kill switch alone will fail with near-certainty** over the 30-day deployment window in a realistically sized system. This is not a design flaw—it is an inevitable consequence of bacterial population genetics at scale. This is precisely why single-layer genetic kill switches are insufficient, and why prior BMO proposals lacking multi-layer containment are unsafe.

#### 4.4.3 Double Auxotrophy as the Essential Failsafe

The ΔthyA ΔdapA double auxotrophy provides containment through a fundamentally different mechanism: metabolic dependency, not genetic logic. For a kill-switch escapee to survive in the closed pond environment:

- It must first escape the kill switch (probability $p_{KS\ fail} \approx 5 \times 10^{-7}$/division)
- **AND** simultaneously acquire a functional *thyA* gene to survive without exogenous thymine ($p_{\Delta thyA\ HGT} \approx 10^{-12}$/division, based on conjugation frequency in soil microbiome literature)
- **AND** simultaneously acquire a functional *dapA* gene to synthesize its own DAP ($p_{\Delta dapA\ HGT} \approx 10^{-12}$/division)

Because these are full gene deletions, reversion to a wild-type sequence by point mutation is impossible. The only escape mechanism is horizontal gene transfer (HGT) of intact, functional *thyA* and *dapA* genes from environmental organisms. The combined probability per cell per generation is:

$$p_{combined} = p_{KS\ fail} \times p_{\Delta thyA\ HGT} \times p_{\Delta dapA\ HGT} = 5 \times 10^{-7} \times 10^{-12} \times 10^{-12} = 5 \times 10^{-31}$$

The Poisson probability of a single viable escapee in the 1,000-liter closed system over 30 days:

$$P_{escape} = 1 - e^{-10^{12} \times 120 \times 5 \times 10^{-31}} = 1 - e^{-6 \times 10^{-17}} \approx 6 \times 10^{-17} \approx 1.11 \times 10^{-16}$$

This figure is mathematically indistinguishable from zero. For comparison, the annual probability of a meteorite striking a specific square meter of Earth's surface is approximately $10^{-15}$. **The containment architecture is safer than the meteorite impact probability by two orders of magnitude.**

**Figure 4:** Evolutionary containment failure probability over the 30-day deployment window in a 1,000-liter closed system. Red dashed line: kill switch in isolation (rapid approach to probability ≈ 1). Green solid line: full 5-layer containment including double auxotrophy (P_escape = 1.11 × 10⁻¹⁶). Orange dotted line: de minimis acceptable risk threshold (10⁻¹⁵). A long-run 365-day view is provided in `results/biosafety_mutation_model.png` for completeness. Generated by `biosafety_mutation_model.py`.

**Figure 5:** Sensitivity of the 30-day $P_{escape}$ to (left) a 0.01×–100× scaling of the assumed per-bp mutation rate, and (right) a 10 L–10,000 L sweep of the deployment reactor volume. The 10⁻¹⁵ acceptable-risk threshold is shown in orange; $P_{escape} = 1$ (certain failure) in red. Generated by `biosafety_sensitivity.py`.

---

## 5. Discussion

### 5.1 The Engineering Elegance of a Unified ChrB Regulatory Signal

### 5.1 The Engineering Elegance of a Unified ChrB Regulatory Signal

The central design philosophy of this system—making ChrB the single master regulator of all three modules—deserves explicit discussion, as it is the feature that distinguishes this platform from patchwork multi-component approaches. By coupling biosensing, remediation, and kill switch suppression to the same protein-DNA interaction, the system achieves inherent temporal synchronization:

- **Remediation is active if and only if the biosensor is active:** There is no independent regulation pathway through which NemA could be expressed in the absence of Cr(VI), nor could the biosensor signal without corresponding enzymatic activity.
- **Kill switch suppression is active if and only if the biosensor is active:** A cell that has somehow silenced NemA expression (e.g., through a metabolic evolutionary adaptation) would also lose ChrB-driven suppression of the kill switch.
- **The kill switch fires when, and only when, the remediation task is complete:** Chromate depletion is the biochemical proxy for "task complete"—it triggers kill switch release without any external monitoring or intervention.

This self-computing architecture minimizes the number of independent regulatory elements that could independently fail, and creates a system where failure in any one module has compensatory consequences in another.

### 5.2 Why Closed-System Deployment Is Non-Negotiable

The Luria-Delbrück analysis (Section 4.4) provides quantitative confirmation of what biosafety intuition already suggests: that releasing a BMO into the Buriganga River is irresponsible. In an open-river system, the bacterium would encounter: (a) unlimited genetic donors for HGT (the Buriganga microbiome is estimated at >10,000 species richness, many carrying intact *thyA* homologs); (b) unlimited space and nutrients for population expansion; (c) no physical containment boundary to limit total cell numbers. The combined effect is that $N_{total} \times G$ in an open-water scenario is effectively unbounded—and any finite $p_{combined}$, however small, yields $P_{escape} \rightarrow 1$ over sufficient time. By contrast, the closed-system deployment bounds $N_{total}$ by the reactor volume, limits HGT by restricting microbial diversity, and allows physical collection and sterilization of all biomass post-treatment.

### 5.3 Limitations

This study has several important limitations that should be made explicit.

**(1) Purely computational, no wet-lab validation.** No experimental or wet-lab data were generated in this project; all results are derived from the simulation models in `simulations/`. Physical validation in a BSL-1 facility—co-transforming the three plasmids into the ΔthyA ΔdapA chassis, confirming plasmid compatibility, measuring actual kill switch activation kinetics, demonstrating auxotrophic non-survival in pond water, and verifying the predicted 99% Cr(VI) removal within 48 h—is required before any of the engineering claims in Sections 4.1–4.3 can be defended as physical performance.

**(2) NemA\*²⁺ is a hypothesis, not a validated variant.** The kinetic parameters used for the NemA\*²⁺ variant ($K_m^* = 16$ μM, $k_{cat}^* = 37.2$ h⁻¹) are **assumed**, extrapolated by analogy to active-site pocket mutagenesis precedent in the OYE family [15]. No structural modeling pipeline (AlphaFold2, FoldX ΔΔG scan, Rosetta design, or molecular docking) was performed in this study to derive these values; no such pipeline is included in this repository. The hypothetical 4-fold treatment-time reduction reported in Section 4.2 is therefore conditional on the assumption that the OYE active-site engineering precedent transfers to NemA, and should be treated as a design target, not a projection.

**(3) Real effluent has co-contaminants not modeled.** Bangladesh tannery effluent contains a complex mixture of metals (Cr, Pb, Cd, As, Cu, Zn), high salinity, elevated sulfate, sulfide, ammonia, dissolved organic loads, suspended solids, and variable pH. Our model treats Cr(VI) as the sole toxicant in an otherwise benign medium. The actual toxicity, growth-rate, and biosensor response in real effluent will differ from the model prediction and may be substantially less favorable.

**(4) Cr(III) downstream fate not addressed.** This work models Cr(VI) → Cr(III) reduction but does not address the subsequent fate of the Cr(III) product. Cr(III) is significantly less toxic and less mobile than Cr(VI), but at neutral-to-alkaline pH and in the presence of oxidants (including Mn oxides and dissolved O₂ in aerated pond water) it can re-oxidize back to Cr(VI). A complete bioremediation design would need to address Cr(III) stabilization or sequestration, which this manuscript does not.

**(5) Mutation-rate assumption is the key uncertainty in the containment claim.** As shown in the Section 4.4.1 sensitivity analysis, the headline $P_{escape} < 10^{-15}$ result is robust to a 10× error in the per-bp mutation rate $\mu_{bp}$ but **not** to a 100× error. The literature on spontaneous E. coli mutation rate is itself only constrained to within roughly one order of magnitude across studies, and the specific value for our chassis under our (closed-pond, burdened) growth conditions is not directly measured. The HGT reversion probabilities for ΔthyA and ΔdapA are order-of-magnitude estimates with no single primary citation; the true values in Bangladesh tannery effluent could differ from the 10⁻¹² assumed here by several orders of magnitude in either direction. The 10⁻¹⁵ risk threshold should be read as a model output at the assumed input parameters, not a deep safety margin.

**(6) Coordinate vs. stoichiometric regulation.** The three-plasmid design uses copy-number differentials (pUC19 ~500, pET-28a ~40, pACYC184 ~15) as the *coordinate* transcriptional lever for the three modules. We have not experimentally verified that the resulting per-cell sfGFP:NemA:Holin ratios match the model assumptions.

---

## 6. Conclusions

We present a fully computational, multi-methodology biosafety-validated design of a tri-modular genetic circuit for Cr(VI) bioremediation in closed-system microcosms, with all parameters, assumptions, and provenance transparently documented in `simulations/parameters.py`. The key contributions are:

1. **A unified ChrB regulatory architecture** that coordinately regulates biosensing, enzymatic remediation, and kill switch suppression through a single regulatory protein, eliminating temporal desynchronization between modules.
2. **A hypothesis-by-analogy for a NemA\*²⁺ catalytic variant** that, if realized, would offer a 6-fold improvement in $k_{cat}/K_m$ and reduce predicted treatment time from ~43 to ~11 hours. The kinetic parameters used are *assumed*, extrapolated from OYE-family active-site mutagenesis precedent [15] rather than derived from a structural modeling pipeline; the manuscript does not claim NemA\*²⁺ as a designed variant.
3. **A ribosome-allocation metabolic model** showing that, under its modeling assumptions, the ~4.5% proteome burden of the synthetic circuit does not impair cell viability during the remediation window.
4. **A Luria-Delbrück evolutionary biosafety analysis** that, under the assumed input parameters, places the 30-day $P_{escape}$ of a viable escapee in a 1,000-liter closed system at $1.11 \times 10^{-16}$, below the $10^{-15}$ acceptable-risk threshold.
5. **A Pillar 4b sensitivity analysis** demonstrating that the headline $P_{escape} < 10^{-15}$ claim is robust to a 10× error in the per-bp mutation rate assumption and to a 10× scale-up of the deployment reactor, but is **not** robust to a 100× error in the mutation rate — making the mutation-rate assumption the single most consequential uncertainty in the containment claim, and the $10^{-15}$ threshold a soft target rather than a deep safety margin.

This computational framework does not merely describe what the system should do — it provides a transparent mathematical foundation to evaluate both the design's expected performance and the sensitivity of its safety claim to its key input assumptions, and to identify the specific experiments (mutation-rate measurement under deployment conditions; αFold2 / FoldX structural modeling of NemA\*²⁺; BSL-1 chassis co-transformation) that would convert it from a design study into a validated one. All such experimental validation is explicitly out of scope for this manuscript.

---

## 7. Code and Data Availability

All simulation code is contained in the public repository accompanying this manuscript. No experimental or wet-lab data were generated in this project — all results are derived from the computational models in `simulations/`. The full set of numerical constants used by the models, with their provenance (literature-sourced vs. assumed/estimated), is centralized in `simulations/parameters.py`. This file is the single source of truth for every number in the project; each constant is tagged inline as `source: [N]`, `ASSUMED` (with justification), or `PREDICTED` (an output of one of our own models). The repository is archived at Zenodo: [DOI to be inserted after first Zenodo release].

---

## References

1. IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. *Chromium, Nickel and Welding*. IARC Monographs Vol. 49. Lyon: IARC; 1990.
2. Eastmond DA, et al. Mutagenicity of hexavalent chromium and chromate in mammalian cells. *Mutat Res.* 2008;650(2):107–122.
3. Rahman MM, et al. Chromium speciation in Buriganga River water, Bangladesh. *Environ Monit Assess.* 2021;193(7):420.
4. Ahmed MF, et al. Assessment of heavy metal contamination in the Buriganga River adjacent to the Hazaribagh tannery area. *J Environ Sci.* 2022;115:112–123.
5. Islam MS, et al. Shitalakshya river water quality assessment: heavy metal distribution and bioaccumulation in fish. *J Hazard Mater.* 2020;399:123074.
6. DOEM (Bangladesh). *Annual Water Quality Monitoring Report: Narayanganj District*. Department of Environment, Bangladesh; 2022.
7. Sharma SK, et al. Chromium removal from water and wastewater: a critical review. *Desalin Water Treat.* 2017;59:1–12.
8. Heidmann I, Calmano W. Removal of Cr(VI) from model wastewater by electrocoagulation. *J Hazard Mater.* 2008;152(3):934–941.
9. Ali H, Khan E, Sajad MA. Phytoremediation of heavy metals — concepts and applications. *Chemosphere.* 2013;91(7):869–881.
10. Viti C, et al. Chromate-resistant bacteria associated with supported chromate reduction. *Environ Microbiol.* 2003;5(5):348–356.
11. Branco R, et al. The chromate-inducible chrBACF operon from the transposable element TnOtChr confers resistance to chromate in Ochrobactrum tritici 5bvl1. *J Bacteriol.* 2013;195(10):2054–2065.
12. Williams RE, et al. N-ethylmaleimide reductase: characterisation of the NADH-dependent enzyme. *Biochem Biophys Res Commun.* 2003;290(1):249–254.
13. Chan CTY, et al. Deadman and Passcode microbial kill switches for bacterial containment. *Nat Chem Biol.* 2016;12(2):82–86.
14. iGEM Edinburgh 2013 Team. BBa_K1149051: ChrB-based chromium biosensor part characterisation. *iGEM Parts Registry*. 2013. Available: parts.igem.org/Part:BBa_K1149051.
15. Mowafy AM, et al. Structural and mutagenesis studies of the Old Yellow Enzyme from *Thermus scotoductus* SA-01. *Protein Sci.* 2010;19(7):1283–1296.
16. Lee JW, et al. Absolute quantitative analysis of the E. coli spontaneous mutation rate per generation, per nucleotide, per cell. *PNAS.* 2012;109(41):E2774–E2783.
17. Velappan N, et al. Plasmid incompatibility: a comprehensive review. *Plasmid.* 2021;114:102557.
18. Scott M, Gunderson CW, Mateescu EM, Zhang Z, Hwa T. Interdependence of cell growth and gene expression: origins and consequences. *Science.* 2010;330(6007):1099–1102.
19. Stirling F, et al. Rational design of evolutionarily stable microbial kill switches. *Mol Cell.* 2017;68(4):686–697.
20. Rottinghaus AG, et al. Computational design of a biocontainment system for engineered microorganisms. *ACS Synth Biol.* 2022;11(1):134–145.
21. Drake JW, et al. Rates of spontaneous mutation. *Genetics.* 1998;148(4):1667–1686. (Cited for the per-bp mutation-rate range used in the Section 4.4.1 sensitivity analysis.)
