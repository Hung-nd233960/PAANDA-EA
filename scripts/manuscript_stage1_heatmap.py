"""Corrected Stage-1-style (pool, reductor) x panel-size accuracy heatmap
(manuscript Fig. 1) — replaces the stale figure, which was built from the
pre-fix sweep and includes N=85/95, neither of which exist in the leak-free
grid (18 sizes: 5-80 step 5, plus 90 and 100).

Accuracy is the fixed-Random-Forest-probe classifier's mean CV accuracy per
(pool, reductor, N) — the same comparison basis Stage 1 originally used, and
the same one behind the "fst_stat+EN peaks at 93.05% (N=90)" / "FST+LR never
exceeds 83.73% (N=100)" claims already corrected in the Results text.

Writes: reports/figures/manuscript_fig1_stage1_heatmap.png / .svg
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
GRID = REPO / "results_archive/nested_leakfree_v1/08b_nested_cv_sweep/grid_results.csv"
OUT = REPO / "reports/figures"

ROW_ORDER = [
    ("stat", "EN"), ("stat", "LR"), ("stat", "RF"),
    ("FST", "EN"), ("FST", "LR"), ("FST", "RF"),
    ("fst_stat", "EN"), ("fst_stat", "LR"), ("fst_stat", "RF"),
]
ROW_LABELS = [f"{p} + {r}" for p, r in ROW_ORDER]

grid = pd.read_csv(GRID)
rf_only = grid[grid.classifier == "RF"]
agg = rf_only.groupby(["n_snps", "panel", "reductor"]).acc.mean().reset_index()
agg["acc"] *= 100

ns = sorted(agg.n_snps.unique())
mat = np.zeros((len(ROW_ORDER), len(ns)))
for i, (pool, red) in enumerate(ROW_ORDER):
    for j, N in enumerate(ns):
        v = agg[(agg.panel == pool) & (agg.reductor == red) & (agg.n_snps == N)].acc
        mat[i, j] = v.iloc[0] if len(v) else np.nan

fig, ax = plt.subplots(figsize=(11.5, 4.2), dpi=200)
im = ax.imshow(mat, cmap="RdYlGn", vmin=60, vmax=97, aspect="auto")

ax.set_xticks(range(len(ns)))
ax.set_xticklabels(ns, fontsize=8.5)
ax.set_yticks(range(len(ROW_ORDER)))
ax.set_yticklabels(ROW_LABELS, fontsize=9)
ax.set_xlabel("Panel size (N SNPs)")
ax.set_title("Stage 1: CV accuracy by (candidate pool, reductor) × panel size", fontsize=11.5, pad=10)

vmid = 78
for i in range(len(ROW_ORDER)):
    for j in range(len(ns)):
        val = mat[i, j]
        color = "white" if val < 68 or val > 92 else "black"
        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=6.6, color=color)

cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.015)
cbar.set_label("CV Accuracy (%)", fontsize=9)
cbar.ax.tick_params(labelsize=8)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(length=0)
fig.tight_layout()

fig.savefig(OUT / "manuscript_fig1_stage1_heatmap.png")
fig.savefig(OUT / "manuscript_fig1_stage1_heatmap.svg")
print(f"Wrote {OUT / 'manuscript_fig1_stage1_heatmap.png'}")

peak_row = agg.loc[agg.acc.idxmax()]
print(f"Overall peak (RF-probe): {peak_row.panel}+{peak_row.reductor} @ N={peak_row.n_snps}: {peak_row.acc:.2f}%")
fst_lr = agg[(agg.panel == "FST") & (agg.reductor == "LR")]
print(f"FST+LR max: {fst_lr.acc.max():.2f}% at N={fst_lr.loc[fst_lr.acc.idxmax(), 'n_snps']}")
