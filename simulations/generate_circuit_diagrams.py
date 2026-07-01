import os
import matplotlib.pyplot as plt
from dna_features_viewer import GraphicFeature, GraphicRecord

# Ensure output directory exists
out_dir = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(out_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. pChrB-sfGFP (Biosensor)
# ---------------------------------------------------------------------------
features_1 = [
    GraphicFeature(start=100, end=900, strand=1, color="#ffcccc", label="AmpR (pUC19)"),
    GraphicFeature(start=1000, end=1100, strand=1, color="#ffff99", label="PchrB (BBa_K1149051)"),
    GraphicFeature(start=1120, end=1140, strand=1, color="#cccccc", label="RBS (BBa_B0034)"),
    GraphicFeature(start=1140, end=1850, strand=1, color="#99ff99", label="sfGFP (BBa_I746916)"),
    GraphicFeature(start=1870, end=1970, strand=1, color="#ff9999", label="Double Terminator (BBa_B0015)"),
]
record_1 = GraphicRecord(sequence_length=2200, features=features_1)
ax1, _ = record_1.plot(figure_width=10)
ax1.set_title("Module 1: pChrB-sfGFP Biosensor (pUC19 Backbone)", fontweight="bold")
plt.savefig(os.path.join(out_dir, "plasmid_module1.png"), dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 2. pNemA-His (Bioremediator)
# ---------------------------------------------------------------------------
features_2 = [
    GraphicFeature(start=100, end=900, strand=1, color="#ccccff", label="KanR (pET-28a)"),
    GraphicFeature(start=1000, end=1100, strand=1, color="#ffff99", label="PchrB (BBa_K1149051)"),
    GraphicFeature(start=1120, end=1140, strand=1, color="#cccccc", label="RBS (BBa_B0032)"),
    GraphicFeature(start=1140, end=2240, strand=1, color="#ffcc99", label="nemA-6xHis"),
    GraphicFeature(start=2260, end=2360, strand=1, color="#ff9999", label="Double Terminator (BBa_B0015)"),
]
record_2 = GraphicRecord(sequence_length=2500, features=features_2)
ax2, _ = record_2.plot(figure_width=10)
ax2.set_title("Module 2: pNemA-His Chromate Reductase (pET-28a Backbone)", fontweight="bold")
plt.savefig(os.path.join(out_dir, "plasmid_module2.png"), dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 3. pKillSwitch-DT (Kill Switch)
# ---------------------------------------------------------------------------
features_3 = [
    GraphicFeature(start=100, end=900, strand=1, color="#e6ccff", label="CmR (pACYC184)"),
    GraphicFeature(start=1000, end=1050, strand=1, color="#ffff99", label="J23119 (Constitutive)"),
    GraphicFeature(start=1060, end=1080, strand=1, color="#cccccc", label="RBS (BBa_B0032)"),
    GraphicFeature(start=1080, end=1700, strand=1, color="#99ccff", label="CI434-SsrA Timer"),
    GraphicFeature(start=1720, end=1820, strand=1, color="#ff9999", label="Terminator (BBa_B0015)"),
    
    GraphicFeature(start=2000, end=2050, strand=1, color="#ffd699", label="PC1 (CI434 repressed)"),
    GraphicFeature(start=2060, end=2160, strand=1, color="#ffff99", label="PchrB-inv (ChrB repressed)"),
    GraphicFeature(start=2180, end=2200, strand=1, color="#cccccc", label="RBS (BBa_B0034)"),
    GraphicFeature(start=2200, end=2500, strand=1, color="#ff6666", label="holin (S105)"),
    GraphicFeature(start=2520, end=2540, strand=1, color="#cccccc", label="RBS (BBa_B0034)"),
    GraphicFeature(start=2540, end=3000, strand=1, color="#cc0000", label="endolysin (R)"),
    GraphicFeature(start=3020, end=3120, strand=1, color="#ff9999", label="Terminator (BBa_B0015)"),
]
record_3 = GraphicRecord(sequence_length=3300, features=features_3)
ax3, _ = record_3.plot(figure_width=12)
ax3.set_title("Module 3: pKillSwitch-DT Dual-Trigger Kill Switch (pACYC184 Backbone)", fontweight="bold")
plt.savefig(os.path.join(out_dir, "plasmid_module3.png"), dpi=300, bbox_inches="tight")
plt.close()

print("Plasmid diagrams generated successfully.")
