"""
Professional Journal PDF Generator
Generates a two-column, academic journal-style PDF from the manuscript content.
Uses fpdf2 for PDF generation with professional typography.
"""
import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ─── CONFIGURATION ───────────────────────────────────────────────
TITLE = "In Silico Design and Computational Validation of a Tri-Modular Genetic Circuit for Autonomous Detection and Bioremediation of Hexavalent Chromium in Closed-System Microcosms"
AUTHORS = "Zubayer Hasan Shaad¹, Humayra Afia²"
AFFILIATIONS = "¹ Govt. Tolaram College, Narayanganj, Bangladesh\n² British Standard School, Bangladesh"
MENTOR = "Mentor: Zabeer Zareef"
CORRESPONDING = "Corresponding author: Zubayer Hasan Shaad"

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "Journal_Manuscript_2026.pdf")

# ─── CUSTOM PDF CLASS ────────────────────────────────────────────
class JournalPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=20)
        self.col_width = 82  # mm per column
        self.col_gap = 6     # mm between columns
        self.left_margin_val = 15
        self.current_col = 0 # 0 = left, 1 = right
        self.y_col = [0, 0]  # track y position per column
        self._in_two_col = False
        self._header_printed = False

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, "Shaad & Afia (2026) - Tri-Modular Genetic Circuit for Cr(VI) Bioremediation", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            self.line(self.left_margin_val, 12, 210 - self.left_margin_val, 12)
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def title_block(self):
        """Render the first-page title block (single column)."""
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6.5, TITLE, align="C")
        self.ln(4)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, AUTHORS, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(1)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 4, AFFILIATIONS, align="C")
        self.ln(1)
        self.multi_cell(0, 4, MENTOR + "  |  " + CORRESPONDING, align="C")
        self.ln(2)
        # Horizontal rule
        self.set_draw_color(0, 0, 0)
        self.line(self.left_margin_val, self.get_y(), 210 - self.left_margin_val, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def section_heading(self, number, title):
        """Major section heading spanning full width."""
        self._end_two_col()
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(20, 60, 120)
        self.cell(0, 7, f"{number}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(20, 60, 120)
        self.line(self.left_margin_val, self.get_y(), 210 - self.left_margin_val, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)
        self._start_two_col()

    def subsection_heading(self, number, title):
        """Subsection heading within current column."""
        self._check_col_break(12)
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(20, 60, 120)
        x = self._col_x()
        self.set_x(x)
        self.multi_cell(self.col_width, 5, f"{number} {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def subsubsection_heading(self, number, title):
        self._check_col_break(10)
        self.ln(1)
        self.set_font("Helvetica", "BI", 9)
        self.set_text_color(40, 80, 140)
        x = self._col_x()
        self.set_x(x)
        self.multi_cell(self.col_width, 4.5, f"{number} {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        """Body paragraph in the current column."""
        self.set_font("Helvetica", "", 9)
        x = self._col_x()
        self.set_x(x)
        self.multi_cell(self.col_width, 4.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.5)

    def bold_text(self, text):
        self.set_font("Helvetica", "B", 9)
        x = self._col_x()
        self.set_x(x)
        self.multi_cell(self.col_width, 4.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def italic_text(self, text):
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(60,60,60)
        x = self._col_x()
        self.set_x(x)
        self.multi_cell(self.col_width, 3.8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_text_color(0,0,0)

    def equation_block(self, eq_text):
        """Render an equation as centered monospace text."""
        self._check_col_break(10)
        self.set_font("Courier", "", 8)
        self.set_text_color(40, 40, 40)
        x = self._col_x()
        self.set_x(x)
        self.multi_cell(self.col_width, 4, eq_text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.5)
        self.set_text_color(0, 0, 0)

    def bullet_point(self, text):
        self._check_col_break(8)
        self.set_font("Helvetica", "", 9)
        x = self._col_x()
        self.set_x(x + 3)
        self.cell(4, 4.2, chr(8226), new_x=XPos.END)
        self.multi_cell(self.col_width - 7, 4.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def numbered_item(self, num, text):
        self._check_col_break(8)
        self.set_font("Helvetica", "", 9)
        x = self._col_x()
        self.set_x(x + 2)
        self.set_font("Helvetica", "B", 9)
        self.cell(6, 4.2, f"{num}.", new_x=XPos.END)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(self.col_width - 8, 4.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def insert_figure(self, img_path, caption, fig_num):
        """Insert a full-width figure with caption."""
        self._end_two_col()
        self.ln(3)
        if os.path.exists(img_path):
            img_w = 170
            self.image(img_path, x=(210 - img_w)/2, w=img_w)
        else:
            self.set_font("Helvetica", "I", 9)
            self.cell(0, 6, f"[Figure {fig_num}: Image not found at {img_path}]", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(2)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 3.8, f"Figure {fig_num}. {caption}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(3)
        self._start_two_col()

    def insert_table(self, headers, rows, caption=None, table_num=None):
        """Insert a full-width table."""
        self._end_two_col()
        self.ln(2)
        if caption and table_num:
            self.set_font("Helvetica", "BI", 8)
            self.set_text_color(40, 40, 40)
            self.multi_cell(0, 4, f"Table {table_num}. {caption}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(1)
            self.set_text_color(0,0,0)
        
        n_cols = len(headers)
        total_w = 180
        col_w = total_w / n_cols
        x_start = self.left_margin_val
        
        # Header row
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(20, 60, 120)
        self.set_text_color(255, 255, 255)
        self.set_x(x_start)
        for h in headers:
            self.cell(col_w, 6, h, border=1, fill=True, align="C", new_x=XPos.END)
        self.ln()
        
        # Data rows
        self.set_font("Helvetica", "", 8)
        self.set_text_color(0, 0, 0)
        for i, row in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(240, 245, 255)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_x(x_start)
            for val in row:
                self.cell(col_w, 5.5, str(val), border=1, fill=True, align="C", new_x=XPos.END)
            self.ln()
        self.ln(3)
        self._start_two_col()

    def reference_item(self, num, text):
        self.set_font("Helvetica", "", 7.5)
        x = self._col_x()
        self.set_x(x)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(6, 3.5, f"[{num}]", new_x=XPos.END)
        self.set_font("Helvetica", "", 7.5)
        self.multi_cell(self.col_width - 6, 3.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    # ─── TWO-COLUMN LAYOUT ENGINE ────────────────────────────────
    def _col_x(self):
        if not self._in_two_col:
            return self.left_margin_val
        if self.current_col == 0:
            return self.left_margin_val
        else:
            return self.left_margin_val + self.col_width + self.col_gap

    def _start_two_col(self):
        self._in_two_col = True
        self.current_col = 0
        self.y_col = [self.get_y(), self.get_y()]

    def _end_two_col(self):
        if self._in_two_col:
            self.set_y(max(self.y_col[0], self.y_col[1]))
        self._in_two_col = False
        self.current_col = 0

    def _check_col_break(self, needed_h=10):
        """Check if we need to switch columns or add a page."""
        if not self._in_two_col:
            if self.get_y() + needed_h > 280:
                self.add_page()
            return
        
        if self.get_y() + needed_h > 280:
            if self.current_col == 0:
                self.y_col[0] = self.get_y()
                self.current_col = 1
                self.set_y(self.y_col[1])
            else:
                self.y_col[1] = self.get_y()
                self.add_page()
                self.current_col = 0
                self.y_col = [self.get_y(), self.get_y()]

    def _after_write(self):
        """Call after each write to track column y."""
        if self._in_two_col:
            self.y_col[self.current_col] = self.get_y()


# ─── BUILD THE DOCUMENT ─────────────────────────────────────────
def build_pdf():
    pdf = JournalPDF()
    pdf.set_left_margin(pdf.left_margin_val)
    pdf.set_right_margin(pdf.left_margin_val)
    pdf.add_page()

    # ═══════════════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════════════
    pdf.title_block()

    # ─── ABSTRACT ─────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(20, 60, 120)
    pdf.cell(0, 6, "Abstract", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

    abstract = (
        "Hexavalent chromium [Cr(VI)], a Group 1 IARC carcinogen, has been measured at concentrations up to 3.54 mg/L "
        "in Bangladesh's Buriganga River -- approximately 70-fold above the US EPA surface water limit -- primarily as a "
        "consequence of unregulated leather tannery effluent discharge. While existing remediation technologies address "
        "contamination passively, none integrate real-time sensing, dose-responsive enzymatic treatment, and autonomous "
        "post-treatment self-termination. Here, we present a fully computational design and validation of a tri-modular "
        "synthetic genetic circuit expressed in a double-auxotrophic Escherichia coli chassis, exclusively deployed within "
        "a closed-system microcosm. The three modules function as follows: (1) a ChrB-sfGFP biosensor module (pChrB-sfGFP, "
        "pUC19) provides Cr(VI) detection at nanomolar sensitivity; (2) a NemA chromate reductase module (pNemA-His, pET-28a) "
        "ensures dose-responsive Cr(VI) to Cr(III) reduction; (3) a dual-trigger holin-endolysin 'Deadman' kill switch "
        "(pKillSwitch-DT, pACYC184) enforces programmed cell death via AND-gate logic. The computational validation spans "
        "ODE systems modeling, protein kinetic modeling of a hypothesized NemA catalytic mutant, ribosome-allocation metabolic "
        "burden analysis, and Luria-Delbruck fluctuation analysis proving the layered containment architecture reduces the "
        "probability of a viable escapee to P_escape = 1.11 x 10^-16 over 30 days in a 1,000-liter closed system. This "
        "framework establishes the first rigorous in silico biosafety validation standard for BMO-based heavy metal remediation."
    )
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 4.2, abstract)
    pdf.ln(2)

    # Keywords
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(18, 4, "Keywords:", new_x=XPos.END)
    pdf.set_font("Helvetica", "I", 8)
    pdf.multi_cell(0, 4, "synthetic biology, hexavalent chromium, genetic kill switch, ChrB biosensor, NemA reductase, bioremediation, Luria-Delbruck mutation model, plasmid architecture, BMO biosafety, Bangladesh tannery pollution")
    pdf.ln(3)
    pdf.line(pdf.left_margin_val, pdf.get_y(), 210 - pdf.left_margin_val, pdf.get_y())
    pdf.ln(3)

    # ═══════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("1", "Introduction")

    pdf.subsection_heading("1.1", "The Hexavalent Chromium Crisis in Bangladesh")
    pdf.body_text(
        "Hexavalent chromium [Cr(VI)] is a highly soluble, mobile, and persistent environmental contaminant "
        "classified by the International Agency for Research on Cancer (IARC) as a definitive Group 1 human "
        "carcinogen [1]. At the molecular level, Cr(VI) enters cells through nonspecific anion transport channels "
        "(sharing uptake pathways with sulfate and phosphate), where it undergoes intracellular reduction to Cr(III) "
        "and Cr(V) intermediates. These intermediates generate reactive oxygen species (ROS) that form DNA adducts, "
        "strand breaks, and protein-DNA crosslinks -- mechanisms directly linked to lung carcinoma, nasal septal "
        "perforation, and renal tubular necrosis upon chronic exposure [2]."
    )
    pdf.body_text(
        "In Bangladesh, the leather tanning industry -- historically centred in Hazaribagh, Dhaka, and partially "
        "relocated to the Savar Tannery Industrial Estate following the 2017 relocation mandate -- has for decades "
        "discharged chromium-laden wastewater into the Buriganga and Shitalakshya rivers with demonstrably inadequate "
        "treatment infrastructure. A systematic survey of Buriganga river water (dry season, 2021-2023) recorded "
        "Cr(VI) concentrations spanning 0.01-3.54 mg/L (mean: 0.48 mg/L), with total dissolved chromium at "
        "industrial outfall points reaching 8.42 mg/L [3,4]. For context, the US EPA maximum contaminant level for "
        "total chromium in surface water is 0.1 mg/L; the WHO guideline for drinking water is 0.05 mg/L. In the "
        "Shitalakshya River (Narayanganj), Cr(VI) concentrations range from 0.037 to 0.102 mg/L, with bioaccumulation "
        "in local fish tissue measured at 0.5-2 mg/kg dry weight [5,6]."
    )

    pdf.subsection_heading("1.2", "Limitations of Existing Remediation Approaches")
    pdf.body_text(
        "Conventional Cr(VI) remediation methodologies each carry fundamental limitations. Chemical precipitation "
        "(reduction to Cr(III) using sodium bisulfite at pH 2-3, followed by Cr(OH)3 precipitation) generates large "
        "volumes of hazardous sludge and operates in narrow pH windows incompatible with river conditions [7]. "
        "Electrocoagulation requires continuous electrical input (30-50 W/m3), is economically prohibitive for "
        "low-resource deployment, and applies equal treatment intensity regardless of Cr(VI) concentration [8]. "
        "Phytoremediation operates on timescales of months to years [9]. Conventional unmodified bioremediation "
        "cannot report chromium presence, cannot self-terminate after remediation, and lacks containment guarantees [10]."
    )
    pdf.body_text(
        "Most critically: none of these approaches operate as integrated sensing-acting-self-terminating systems. "
        "They cannot distinguish between a heavily polluted site and a recovered one, they cannot scale their "
        "response proportionally, and they provide no mechanism to prevent long-term biological persistence."
    )

    pdf.subsection_heading("1.3", "Synthetic Biology as a Remediation Paradigm")
    pdf.body_text(
        "Synthetic biology offers a categorically different framework. By encoding programmable genetic logic "
        "directly into a bacterial chassis, it is possible to engineer organisms that act as autonomous "
        "bio-computers: sensing a specific signal (Cr(VI) concentration), computing a proportional response "
        "(NemA expression level), executing that response (enzymatic reduction), and self-terminating upon task "
        "completion (kill switch activation). This 'sense-respond-terminate' architecture -- all governed by the "
        "same regulatory protein (ChrB) -- is the conceptual core of the present design."
    )
    pdf.body_text(
        "However, prior synthetic biology approaches to bioremediation have consistently underestimated the risks "
        "of deploying Biologically Modified Organisms (BMOs) in open environments. Engineered bacteria are living "
        "organisms subject to Darwinian selection. Any kill switch can fail through mutation; any auxotrophy can "
        "theoretically revert through horizontal gene transfer. A single escaped, reproductively competent BMO "
        "in the Buriganga River could represent an ecological catastrophe. The first and most important design "
        "decision of this project is therefore absolute: we do not propose open-water deployment. The platform "
        "operates exclusively within a physically sealed, closed-system microcosm."
    )

    pdf.subsection_heading("1.4", "Novelty and Research Hypothesis")
    pdf.body_text(
        "The novelty of this work is not the individual components -- ChrB biosensors [11], NemA reductases [12], "
        "and holin-endolysin kill switches [13] have each been independently described -- but rather: (i) their "
        "integration into a single, three-plasmid, tri-modular system governed by a unified regulatory signal; "
        "(ii) the deployment of a computationally hypothesized NemA catalytic mutant with substantially improved "
        "kinetics; and (iii) the first application of Luria-Delbruck fluctuation theory to rigorously quantify "
        "the evolutionary failure probability of a layered BMO containment architecture."
    )
    pdf.body_text(
        "Central hypothesis: A tri-modular platform integrating ChrB-sfGFP biosensor, NemA chromate reductase, "
        "and dual-trigger kill switch -- expressed in a double-auxotrophic E. coli DH5a dthyA ddapA chassis "
        "within a closed-system microcosm -- can achieve: (1) >=99% Cr(VI) removal within 48 hours; "
        "(2) >=99% programmed cell death within 72 hours of chromate depletion; and (3) a containment breach "
        "probability < 10^-15 over a 30-day deployment."
    )

    # ═══════════════════════════════════════════════════════════════
    # 2. GENETIC CIRCUIT ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("2", "Genetic Circuit Architecture and Plasmid Design")

    pdf.subsection_heading("2.1", "System Overview: Tri-Modular Design Philosophy")
    pdf.body_text(
        "The central engineering challenge of whole-cell bioremediation is achieving coherent signal integration "
        "across functional modules. In many prior designs, sensing, effector expression, and kill switch elements "
        "are independently regulated, creating temporal desynchronization risks. Our design resolves this by making "
        "the ChrB regulatory protein the single master regulator of all three modules simultaneously."
    )
    pdf.body_text(
        "The ChrB protein -- a transcriptional repressor from Pseudomonas aeruginosa -- binds the PchrB operator "
        "in the apo (chromate-free) state and releases it upon Cr(VI) binding. This governs: Module 1: De-repression "
        "of PchrB -> sfGFP (biosensor); Module 2: De-repression of PchrB -> NemA (remediation); Module 3: "
        "Repression of inverted PchrB -> holin/endolysin (kill switch suppression during active sensing)."
    )

    # Plasmid compatibility table
    pdf.insert_table(
        ["Plasmid", "Module", "Backbone", "Origin", "Marker", "Copy #"],
        [
            ["pChrB-sfGFP", "Biosensor", "pUC19", "pMB1", "AmpR", "~500"],
            ["pNemA-His", "Reductase", "pET-28a", "pBR322", "KanR", "~40"],
            ["pKillSwitch-DT", "Kill Switch", "pACYC184", "p15A", "CmR", "~15"],
        ],
        caption="Three-plasmid architecture with orthogonal origins and selectable markers.",
        table_num=1
    )

    pdf.body_text(
        "The three backbones belong to orthogonal incompatibility groups: pMB1 and pBR322 are ColE1-derived "
        "but differ in copy control; p15A (pACYC184) is IncFII, fully compatible with both. The three antibiotic "
        "markers (AmpR, KanR, CmR) enable three-way selective plating after co-transformation [17]. The copy "
        "number differential is intentional: high-copy biosensor ensures robust signal; medium-copy reductase "
        "balances production vs. burden; low-copy kill switch prevents constitutive Holin leakage."
    )

    pdf.subsection_heading("2.2", "Module 1: ChrB-sfGFP Chromium Biosensor")
    pdf.subsubsection_heading("2.2.1", "Molecular Mechanism of ChrB-Based Sensing")
    pdf.body_text(
        "ChrB is a LysR-type transcriptional regulator (LTTR) from P. aeruginosa PAO1 [11]. In the absence "
        "of chromate, the ChrB dimer binds a 23-bp palindromic PchrB operator upstream of the chrBCA operon, "
        "sterically blocking RNA polymerase. Upon chromate (CrO4 2-) binding to the co-inducer domain, ChrB "
        "undergoes an allosteric conformational shift reducing its operator affinity, releasing PchrB and "
        "permitting transcriptional read-through. Published characterization of BBa_K1149051 indicates a Hill "
        "coefficient n = 2.0-2.2 (cooperative dimeric binding) and Kd = 100 nM [14]."
    )
    pdf.body_text(
        "ChrB specificity is determined by anion geometry: chromate (CrO4 2-, tetrahedral) triggers conformational "
        "release, while divalent cation metals (Pb2+, Cd2+, Cu2+, Zn2+) acting through cation-binding proteins "
        "(MerR, CadC, CusS-CusR) do not interact with the ChrB binding pocket."
    )

    pdf.subsubsection_heading("2.2.2", "Genetic Parts and Construct Architecture")
    pdf.body_text(
        "pChrB-sfGFP [pUC19 | AmpR | pMB1 ori]: PchrB promoter (BBa_K1149051, including 23-bp operator and "
        "sigma70-compatible -35/-10 core promoter), RBS BBa_B0034 (medium strength, ~1000 au), sfGFP BBa_I746916 "
        "(superfolder GFP; maturation t1/2 ~8 min vs. ~30 min for eGFP; oxidative stress resistant), and double "
        "terminator BBa_B0015. Predicted LOD: ~80 nM Cr(VI); fold-induction at 100 uM: 8.2x; response time: ~3 h."
    )

    pdf.subsection_heading("2.3", "Module 2: NemA Chromate Reductase")
    pdf.subsubsection_heading("2.3.1", "Structure and Catalytic Mechanism")
    pdf.body_text(
        "NemA (N-ethylmaleimide reductase; EC 1.6.99.1) is a native E. coli NADH-dependent flavoprotein of the "
        "Old Yellow Enzyme (OYE) superfamily [12]. The catalytic mechanism is ping-pong bi-bi: (1) NADH reduces "
        "the FMN prosthetic group (FMN_ox -> FMN_red); (2) FMN_red transfers electrons to Cr(VI), reducing it to "
        "Cr(III) and regenerating FMN_ox. Published kinetic parameters: Km = 48 uM, kcat = 0.39 s^-1 "
        "(1,404 h^-1), kcat/Km = 1.1 x 10^5 M^-1 s^-1 [12]. Stable at pH 6.5-8.5 and 28-37 C."
    )
    pdf.body_text(
        "NemA is placed under the identical PchrB promoter as sfGFP in pET-28a (KanR), achieving stoichiometric "
        "co-regulation: both biosensor signal and enzymatic reduction increase proportionally with Cr(VI) concentration."
    )

    pdf.subsubsection_heading("2.3.2", "Computationally Hypothesized 'Super-NemA' Mutant")
    pdf.body_text(
        "The OYE superfamily active site features a conserved Tyr-His catalytic pair (equivalent to Tyr-196 and "
        "His-191 in PETNR) that anchors the FMN isoalloxazine ring. A second shell of hydrophobic residues (Trp, "
        "Phe, Ile) flanks the substrate pocket and governs substrate approach geometry. Mutagenesis studies in "
        "PETNR and morphinone reductase have shown that substituting these second-shell residues with smaller "
        "side chains (Trp->Ala, Phe->Gly) expands the binding pocket and reduces steric hindrance for non-canonical "
        "electron acceptors [15]. We hypothesize NemA*2+: Km* = 16 uM (3-fold improvement), kcat* = 2,808 h^-1 "
        "(2-fold improvement), yielding kcat/Km = 6.5 x 10^5 M^-1 s^-1 -- a 6-fold catalytic efficiency gain."
    )

    pdf.subsection_heading("2.4", "Module 3: Dual-Trigger Kill Switch")
    pdf.subsubsection_heading("2.4.1", "Why Single-Trigger Kill Switches Fail")
    pdf.body_text(
        "A single toxin gene repressed by a single repressor can be silenced by any mutation that: (i) disrupts "
        "the toxin promoter, (ii) introduces a premature stop codon, (iii) amplifies the repressor, or (iv) mutates "
        "the repressor binding site [13]. In a population of 10^12 cells, such mutations occur with near-certainty "
        "(Section 4.4). Our design addresses this through AND-gate logic requiring two simultaneous triggers."
    )

    pdf.subsubsection_heading("2.4.2", "Trigger 1: ChrB-Inverted Promoter Logic Gate")
    pdf.body_text(
        "The kill switch inverts the ChrB logic: the holin-endolysin operon is placed downstream of PchrB in "
        "reverse orientation. High Cr(VI) -> ChrB released -> Holin repressed. Low Cr(VI) -> ChrB bound -> "
        "Holin de-repressed and accumulates. This ensures any BMO in a Cr(VI)-free environment (pristine water) "
        "immediately begins Holin accumulation and lyses."
    )

    pdf.subsubsection_heading("2.4.3", "Trigger 2: CI434-SsrA Temporal Timer")
    pdf.body_text(
        "CI434 (phage 434 repressor) is expressed from a constitutive J23119 promoter and represses the PC1 "
        "promoter upstream of the holin operon. The SsrA degradation tag (AANDENYALAA) targets CI434 for "
        "ClpXP/ClpAP protease degradation, giving it a 24-hour half-life (decay constant lambda = ln2/24 = "
        "0.0289 h^-1). By t = 72 h, CI434-SsrA decays to 12.5% of initial -- below the repression threshold. "
        "Combined with Cr(VI) depletion (Trigger 1), Holin accumulates and crosses the lysis threshold at 72-96 h."
    )

    pdf.subsubsection_heading("2.4.4", "The Executioners: Holin and Endolysin")
    pdf.body_text(
        "Terminal effectors are lambda phage holin (S105) and endolysin (R). Holin oligomerizes in the inner "
        "membrane forming >2 nm pores, collapsing the proton-motive force and allowing endolysin (an N-acetyl"
        "muramidase) to access and degrade the peptidoglycan layer. Together they achieve >=99.9% cell death "
        "within 60 minutes of Holin crossing the lysis threshold [13]. The pKillSwitch-DT construct uses the "
        "pACYC184 backbone (p15A origin, CmR) at low copy number (~15) to prevent constitutive Holin leakage."
    )

    pdf.subsection_heading("2.5", "The Chassis: E. coli DH5a dthyA ddapA Double Auxotroph")
    pdf.body_text(
        "The chassis carries two complete chromosomal gene deletions (full coding sequence removals, not point "
        "mutations). dthyA (thymidylate synthase): eliminates the sole biosynthetic route to dTMP; bacteria "
        "require exogenous thymine (50 ug/mL) for DNA replication. ddapA (4-hydroxy-tetrahydrodipicolinate "
        "synthase): eliminates the sole route to diaminopimelic acid (DAP) and L-lysine; bacteria cannot "
        "synthesize peptidoglycan and lyse without exogenous DAP (100 uM). Both thymine and DAP are absent "
        "from natural aquatic environments. Reversion of full gene deletions by point mutation is biologically "
        "impossible. Compensatory HGT-based reversion is quantified in Section 4.4."
    )

    # ═══════════════════════════════════════════════════════════════
    # 3. COMPUTATIONAL METHODS
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("3", "Computational Methods")

    pdf.subsection_heading("3.1", "ODE Systems Biology Model")
    pdf.body_text(
        "The circuit was modeled as a coupled ODE system using Python scipy.integrate.solve_ivp (Radau solver). "
        "Six state variables were tracked over 96 h: [Cr_ext, NemA, sfGFP, CI434, Holin, Cells]. The equations are:"
    )
    pdf.equation_block("d[Cr]/dt = -kcat * [NemA] * [Cr] / (Km + [Cr])")
    pdf.equation_block("d[NemA]/dt = k_NemA * [Cr]^n/(Kd^n+[Cr]^n) - d_NemA*[NemA]")
    pdf.equation_block("d[CI434]/dt = -lambda_CI434 * [CI434]")
    pdf.equation_block("d[Holin]/dt = k_H * Kd^n/(Kd^n+[Cr]^n) * Kci^2/(Kci^2+[CI434]^2)")
    pdf.equation_block("d[Cells]/dt = mu*Cells*(1-Cells/K) - k_lysis*Cells*I(Holin>theta)")
    pdf.body_text("Parameters were derived from published experimental values [11,12,13,14].")

    pdf.subsection_heading("3.2", "NemA Kinetic Mutant Modeling")
    pdf.body_text(
        "WT and NemA*2+ kinetics were modeled via Michaelis-Menten: d[Cr]/dt = -kcat*E*[Cr]/(Km+[Cr]). "
        "WT parameters: kcat = 1,404 h^-1, Km = 48 uM. Mutant: kcat* = 2,808 h^-1, Km* = 16 uM."
    )

    pdf.subsection_heading("3.3", "Ribosome Allocation Metabolic Burden Model")
    pdf.body_text(
        "Growth rate was computed using the Scott et al. (2010) framework [16]: mu = (phi_max - phi_q - phi_s) "
        "* kappa_t, where phi_max = 0.55, phi_q = 0.40, phi_s ~ 0.045, and kappa_t is adjusted for Cr(VI) "
        "oxidative stress: kappa_t_stressed = kappa_t * (1 - [Cr]/[Cr]_max)."
    )

    pdf.subsection_heading("3.4", "Luria-Delbruck Evolutionary Biosafety Modeling")
    pdf.body_text(
        "Containment failure probability was computed using a Poisson approximation: P_escape = 1 - exp(-N*G*p). "
        "For combined containment: p_combined = p_KS_fail * p_dthyA_HGT * p_ddapA_HGT."
    )

    # ═══════════════════════════════════════════════════════════════
    # 4. RESULTS
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("4", "Results")

    pdf.subsection_heading("4.1", "Circuit Systems Dynamics: 96-Hour Simulation")
    pdf.body_text(
        "The 96-hour ODE simulation reveals precise temporal coordination (Figure 1). Upon 100 uM Cr(VI) "
        "exposure, ChrB de-represses PchrB within 2-3 h. NemA plateaus at ~80 protein units by t = 12 h, "
        "driving Cr(VI) below detection by t ~ 44 h. During the 0-72 h treatment window, CI434-SsrA represses "
        "Holin. By t = 72 h, CI434 decays to 12.5%, both AND-gate triggers fire, and Holin crosses the lysis "
        "threshold by t ~ 80 h. Cell viability drops by >4 orders of magnitude by t = 96 h."
    )

    fig1 = os.path.join(FIGURE_DIR, "integrated_96h_simulation.png")
    pdf.insert_figure(fig1,
        "96-hour ODE simulation of tri-modular circuit dynamics. Top: Cr(VI) depletion (left), sfGFP biosensor "
        "signal (right). Bottom: CI434/Holin kill switch dynamics (left), cell viability on log scale (right).",
        "1")

    pdf.subsection_heading("4.2", "NemA vs. NemA*2+ Kinetic Comparison")
    pdf.body_text(
        "Wild-type NemA reduces 100 uM Cr(VI) below the EPA limit (~1.9 uM) in ~43 hours. NemA*2+, with "
        "3-fold lower Km and doubled kcat, achieves the same endpoint in ~11 hours -- a 4-fold reduction in "
        "treatment time (Figure 2). At low substrate concentrations (<20 uM), the mutant maintains near-maximal "
        "velocity while WT is strongly limited -- critical for 'tail-end' cleanup to regulatory thresholds."
    )

    fig2 = os.path.join(FIGURE_DIR, "nemA_mutant_kinetics.png")
    pdf.insert_figure(fig2,
        "Comparative kinetics of wild-type NemA vs. NemA*2+ mutant. Left: Cr(VI) time-course depletion. "
        "Right: Michaelis-Menten velocity curves.",
        "2")

    pdf.subsection_heading("4.3", "Metabolic Feasibility: Circuit Burden Analysis")
    pdf.body_text(
        "The ribosome-allocation model confirms the synthetic circuit (~4.5% of total proteome at full "
        "induction) is metabolically sustainable (Figure 3). At 100 uM Cr(VI), growth rate reduces from "
        "0.525 h^-1 (uninduced) to 0.349 h^-1 -- a 33% reduction, but still positive. Bacteria maintain "
        "viability throughout the remediation window. At >150 uM Cr(VI), oxidative stress becomes "
        "bacteriostatic -- an intrinsic safety feature."
    )

    fig3 = os.path.join(FIGURE_DIR, "metabolic_burden_model.png")
    pdf.insert_figure(fig3,
        "Ribosome-allocation metabolic model. Growth rate (mu) vs. circuit expression (% proteome) under "
        "four Cr(VI) stress conditions. Dashed vertical: predicted circuit burden at full induction.",
        "3")

    pdf.subsection_heading("4.4", "Evolutionary Biosafety: Containment Failure Analysis")
    pdf.subsubsection_heading("4.4.1", "Kill Switch Failure Rate in Isolation")
    pdf.body_text(
        "The kill switch targets a ~500 bp coding region. At mu_bp = 10^-9 mutations/base/generation: "
        "p_KS_fail = 10^-9 * 500 = 5 x 10^-7 per cell per generation. In a 1,000 L system (10^12 cells, "
        "4 gen/day, 30 days = 120 generations): P_KS = 1 - exp(-10^12 * 120 * 5*10^-7) ~ 1.0. "
        "The kill switch alone will fail with near-certainty. This is an inevitable consequence of bacterial "
        "population genetics at scale."
    )

    pdf.subsubsection_heading("4.4.2", "Double Auxotrophy as the Essential Failsafe")
    pdf.body_text(
        "For a kill-switch escapee to survive in the closed pond: it must escape the kill switch "
        "(p = 5 x 10^-7) AND simultaneously acquire functional thyA via HGT (p = 10^-12) AND acquire "
        "functional dapA via HGT (p = 10^-12). These are full gene deletions -- point-mutation reversion "
        "is impossible. Combined per-division probability:"
    )
    pdf.equation_block("p_combined = 5e-7 * 1e-12 * 1e-12 = 5 x 10^-31")
    pdf.body_text(
        "Poisson probability of one escapee in 1000 L over 30 days:"
    )
    pdf.equation_block("P_escape = 1-exp(-1.2e14 * 5e-31) = 1.11 x 10^-16")
    pdf.body_text(
        "For comparison, the annual probability of a meteorite striking a specific square meter of Earth's "
        "surface is ~10^-15. The containment architecture is safer by two orders of magnitude."
    )

    fig4 = os.path.join(FIGURE_DIR, "biosafety_mutation_model.png")
    pdf.insert_figure(fig4,
        "Evolutionary containment failure probability over 365 days. Red dashed: kill switch alone "
        "(approaches P=1). Green solid: full 5-layer containment (remains < 10^-20). "
        "Orange dotted: acceptable risk threshold (10^-15).",
        "4")

    # ═══════════════════════════════════════════════════════════════
    # 5. DISCUSSION
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("5", "Discussion")

    pdf.subsection_heading("5.1", "Engineering Elegance of Unified ChrB Regulation")
    pdf.body_text(
        "By coupling biosensing, remediation, and kill switch suppression to the same ChrB protein-DNA "
        "interaction, the system achieves inherent temporal synchronization. Remediation is active iff the "
        "biosensor is active. A cell that silences NemA also loses ChrB-driven kill switch suppression. The "
        "kill switch fires when, and only when, the remediation task is complete. This self-computing "
        "architecture minimizes independent failure modes and creates compensatory failure consequences."
    )

    pdf.subsection_heading("5.2", "Why Closed-System Deployment Is Non-Negotiable")
    pdf.body_text(
        "The Luria-Delbruck analysis provides quantitative confirmation: in an open-river system, the "
        "bacterium would encounter unlimited HGT donors (Buriganga microbiome: >10,000 species), unlimited "
        "space for population expansion, and no physical containment. The combined effect is that N*G is "
        "unbounded -- and any finite p_combined yields P_escape -> 1 over sufficient time. The closed "
        "system bounds N by reactor volume, limits HGT by restricting microbial diversity, and allows "
        "physical collection and sterilization of all biomass post-treatment."
    )

    pdf.subsection_heading("5.3", "Limitations")
    pdf.body_text(
        "This study is entirely computational. Kinetic parameters were drawn from published literature, not "
        "from the specific constructs described. The NemA*2+ mutant remains a hypothesis. HGT probability "
        "estimates carry large uncertainty bounds. Physical validation in BSL-1 -- co-transforming all three "
        "plasmids into the dthyA ddapA chassis, confirming compatibility, measuring kill switch kinetics, and "
        "demonstrating auxotrophic non-survival in pond water -- is required before real-world claims."
    )

    # ═══════════════════════════════════════════════════════════════
    # 6. CONCLUSIONS
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("6", "Conclusions")
    pdf.body_text(
        "We present the first fully computational, multi-methodology biosafety-validated design of a "
        "tri-modular genetic circuit for Cr(VI) bioremediation in closed-system microcosms. Key contributions:"
    )
    pdf.numbered_item(1, "A unified ChrB regulatory architecture coupling biosensing, enzymatic remediation, "
        "and kill switch suppression through a single regulatory protein.")
    pdf.numbered_item(2, "A computationally hypothesized NemA*2+ catalytic mutant with projected 6-fold "
        "improvement in kcat/Km, reducing treatment time from ~43 to ~11 hours.")
    pdf.numbered_item(3, "A ribosome-allocation metabolic model proving ~4.5% proteome burden does not "
        "impair cell viability during the remediation window.")
    pdf.numbered_item(4, "A Luria-Delbruck evolutionary biosafety analysis demonstrating combined kill switch "
        "+ double auxotrophy reduces viable escapee probability to 1.11 x 10^-16 over 30 days.")
    pdf.ln(2)
    pdf.body_text(
        "This computational framework does not merely describe what the system should do -- it provides "
        "the mathematical foundation to prove that it is safe to attempt."
    )

    # ═══════════════════════════════════════════════════════════════
    # REFERENCES
    # ═══════════════════════════════════════════════════════════════
    pdf.section_heading("", "References")
    refs = [
        "IARC Working Group. Chromium, Nickel and Welding. IARC Monographs Vol. 49. Lyon: IARC; 1990.",
        "Eastmond DA et al. Mutagenicity of hexavalent chromium in mammalian cells. Mutat Res. 2008;650(2):107-122.",
        "Rahman MM et al. Chromium speciation in Buriganga River water. Environ Monit Assess. 2021;193(7):420.",
        "Ahmed MF et al. Heavy metal contamination in Buriganga River. J Environ Sci. 2022;115:112-123.",
        "Islam MS et al. Shitalakshya river water quality: heavy metals in fish. J Hazard Mater. 2020;399:123074.",
        "DOEM (Bangladesh). Annual Water Quality Monitoring Report: Narayanganj. 2022.",
        "Sharma SK et al. Chromium removal: a critical review. Desalin Water Treat. 2017;59:1-12.",
        "Heidmann I, Calmano W. Removal of Cr(VI) by electrocoagulation. J Hazard Mater. 2008;152(3):934-941.",
        "Ali H et al. Phytoremediation of heavy metals. Chemosphere. 2013;91(7):869-881.",
        "Viti C et al. Chromate-resistant bacteria. Environ Microbiol. 2003;5(5):348-356.",
        "Branco R et al. chrBACF operon from TnOtChr. J Bacteriol. 2013;195(10):2054-2065.",
        "Williams RE et al. N-ethylmaleimide reductase characterisation. Biochem Biophys Res Commun. 2003;290(1):249-254.",
        "Chan CTY et al. Deadman and Passcode microbial kill switches. Nat Chem Biol. 2016;12(2):82-86.",
        "iGEM Edinburgh 2013. BBa_K1149051: ChrB biosensor characterisation. iGEM Parts Registry. 2013.",
        "Mowafy AM et al. Old Yellow Enzyme from Thermus scotoductus SA-01. Protein Sci. 2010;19(7):1283-1296.",
        "Scott M et al. Interdependence of cell growth and gene expression. Science. 2010;330(6007):1099-1102.",
        "Chang ACY, Cohen SN. Construction and characterization of amplifiable multicopy DNA cloning vehicles derived from the P15A cryptic miniplasmid. J Bacteriol. 1978;134(3):1141-1156.",
    ]
    for i, ref in enumerate(refs, 1):
        pdf.reference_item(i, ref)

    # ─── OUTPUT ──────────────────────────────────────────────────
    out = os.path.abspath(OUTPUT_FILE)
    pdf.output(out)
    print(f"PDF generated successfully: {out}")
    print(f"Total pages: {pdf.page_no()}")

if __name__ == "__main__":
    build_pdf()
