"""Corrected classifier-robustness bar chart (manuscript Fig. 6) — replaces the
stale figure built from the pre-leak-fix PAANDA-EA N=35/N=50 panels.

Cai-34's per-classifier accuracy is external and unaffected by the leak fix
(pulled as-is from the cached out-of-fold predictions, verified against the
original figure's readings). PAANDA-EA N=35/N=50 per-classifier accuracy comes
from the leak-free grid (results_archive/nested_leakfree_v1/08b_nested_cv_sweep/
grid_results.csv), matching Table 2.

Writes: reports/figures/manuscript_fig6_classifier_robustness.png / .svg
"""

from __future__ import annotations

import pickle
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
GRID = REPO / "results_archive/nested_leakfree_v1/08b_nested_cv_sweep/grid_results.csv"
OOFPRED_PKL = (
    REPO
    / "results_archive/baseline_leaky_v1/self_evaluation/09_published_panel_comparison"
    / "panel_oofpreds.pkl"
)
OUT = REPO / "reports/figures"

CLASSIFIERS = ["RF", "XGB", "LR", "SVM_RBF", "SVM_Lin", "GBM"]
DISPLAY = {"RF": "RF", "XGB": "XGB", "LR": "LR", "SVM_RBF": "SVM_RBF",
           "SVM_Lin": "SVM_Lin", "GBM": "GBM"}

with open(OOFPRED_PKL, "rb") as fh:
    d = pickle.load(fh)
cai = {c: (yt == yp).mean() * 100 for c, (yt, yp) in d["oofpreds"]["cai_eas34"].items()}

grid = pd.read_csv(GRID)
combos = {35: ("fst_stat", "EN"), 50: ("stat", "EN"), 70: ("FST", "EN")}
paanda = {}
for N, (pool, red) in combos.items():
    sub = grid[(grid.n_snps == N) & (grid.panel == pool) & (grid.reductor == red)]
    paanda[N] = sub.groupby("classifier").acc.mean() * 100

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID_COLOR = "#e1e0d9"
SURFACE = "#fcfcfb"
CAI_COLOR = "#e8836a"
N35_COLOR = "#aed4ec"
N50_COLOR = "#5a9bc9"
N70_COLOR = "#1c5083"

plt.rcParams.update({
    "font.family": "sans-serif", "axes.edgecolor": INK_SECONDARY,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "font.size": 10,
})

fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200)
ax.grid(True, axis="y", color=GRID_COLOR, linewidth=0.8, zorder=0)

x = np.arange(len(CLASSIFIERS))
width = 0.20
cai_vals = [cai[c] for c in CLASSIFIERS]
n35_vals = [paanda[35][c] for c in CLASSIFIERS]
n50_vals = [paanda[50][c] for c in CLASSIFIERS]
n70_vals = [paanda[70][c] for c in CLASSIFIERS]

ax.bar(x - 1.5 * width, cai_vals, width=width * 0.92, color=CAI_COLOR, label="Cai N=34", zorder=3)
ax.bar(x - 0.5 * width, n35_vals, width=width * 0.92, color=N35_COLOR, label="PAANDA-EA N=35", zorder=3)
ax.bar(x + 0.5 * width, n50_vals, width=width * 0.92, color=N50_COLOR, label="PAANDA-EA N=50", zorder=3)
ax.bar(x + 1.5 * width, n70_vals, width=width * 0.92, color=N70_COLOR, label="PAANDA-EA N=70", zorder=3)

ax.set_xticks(x)
ax.set_xticklabels([DISPLAY[c] for c in CLASSIFIERS])
ax.set_ylabel("Accuracy (%)")
ax.set_ylim(80, 100)
ax.set_yticks(range(80, 101, 2))
ax.set_yticklabels([f"{v}%" for v in range(80, 101, 2)])
ax.set_title("Classifier robustness: Cai expert panel vs PAANDA-EA N=35/50/70 panels", fontsize=11)
ax.legend(frameon=True, loc="upper right", fontsize=9)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
fig.tight_layout()

fig.savefig(OUT / "manuscript_fig6_classifier_robustness.png")
fig.savefig(OUT / "manuscript_fig6_classifier_robustness.svg")
print(f"Wrote {OUT / 'manuscript_fig6_classifier_robustness.png'}")
for c in CLASSIFIERS:
    print(f"{c}: Cai={cai[c]:.2f} N35={paanda[35][c]:.2f} N50={paanda[50][c]:.2f} N70={paanda[70][c]:.2f}")
