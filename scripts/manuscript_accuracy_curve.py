"""Corrected accuracy-vs-panel-size curve (manuscript Fig. 2/3) — replaces the
stale figure built around "Stage 2 CV" vs "Stage 3 hold-out," a distinction
that no longer exists in the leak-free nested CV design (no 80/20 hold-out
anywhere). Replaced with Blind Selection (bias-free) vs Best Fixed
Configuration (named winner), matching the already-corrected paragraph text.

Reads: results_archive/nested_leakfree_v1/08b_nested_cv_sweep/{nested_tierA_results,winner_per_N}.csv
Writes: reports/figures/manuscript_fig_accuracy_curve.png / .svg
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "results_archive/nested_leakfree_v1/08b_nested_cv_sweep"
OUT = REPO / "reports/figures"

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID_COLOR = "#e1e0d9"
SURFACE = "#fcfcfb"
BFC_COLOR = "#1c5083"
BS_COLOR = "#8fc1e3"
CAI_COLOR = "#c0392b"
CAO_COLOR = "#e0a458"

bs = pd.read_csv(ARCHIVE / "nested_tierA_results.csv")
bfc = pd.read_csv(ARCHIVE / "winner_per_N.csv")

plt.rcParams.update({
    "font.family": "sans-serif", "axes.edgecolor": INK_SECONDARY,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "font.size": 10,
})

fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200)
ax.grid(True, axis="y", color=GRID_COLOR, linewidth=0.8, zorder=0)

ax.plot(bfc.n_snps, bfc.best_acc, color=BFC_COLOR, linewidth=2, marker="o",
        markersize=6, markerfacecolor=BFC_COLOR, markeredgecolor=SURFACE,
        label="PAANDA-EA (Best Fixed Configuration)", zorder=4)
ax.plot(bs.n_snps, bs.acc_mean * 100, color=BS_COLOR, linewidth=2, linestyle="--",
        marker="s", markersize=5.5, markerfacecolor=BS_COLOR, markeredgecolor=SURFACE,
        label="PAANDA-EA (Blind Selection)", zorder=4)

ax.axhline(94.64, color=CAI_COLOR, linestyle=":", linewidth=1.3, zorder=2,
           label="Cai et al. 2024 (N=34, best clf 94.6%)")
ax.axhline(81.94, color=CAO_COLOR, linestyle=":", linewidth=1.3, zorder=2,
           label="Cao et al. 2022 (N=14 matched, best clf 81.9%)")

ax.set_xlabel("Panel size (N SNPs)")
ax.set_ylabel("Accuracy (%)")
ax.set_ylim(60, 100)
ax.set_yticks(range(60, 101, 5))
ax.set_yticklabels([f"{v}%" for v in range(60, 101, 5)])
ax.set_title("Classification accuracy vs panel size\n(Han / JPT / SEA, 504 samples, 5-fold nested CV)", fontsize=11.5)
ax.legend(frameon=True, loc="lower right", fontsize=8.3)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
fig.tight_layout()

fig.savefig(OUT / "manuscript_fig_accuracy_curve.png")
fig.savefig(OUT / "manuscript_fig_accuracy_curve.svg")
print(f"Wrote {OUT / 'manuscript_fig_accuracy_curve.png'}")
