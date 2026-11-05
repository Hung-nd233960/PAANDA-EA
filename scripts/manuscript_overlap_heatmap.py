"""Corrected SNP panel overlap heatmap (manuscript Fig. 7) — replaces the stale
figure built from the pre-leak-fix committed panels.

Uses the corrected committed panels' rsIDs (reports/figures/committed_panel_markers.csv,
built leak-free: N=35 from fst_stat, N=50 from stat, N=70 from FST — three
different candidate pools, so the self-overlap block is no longer fully nested)
against the published panel marker lists in data/published_panels/.

Writes: reports/figures/manuscript_fig7_overlap_heatmap.png / .svg
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
MARKERS = REPO / "reports/figures/committed_panel_markers.csv"
PUB_DIR = REPO / "data/published_panels"
OUT = REPO / "reports/figures"


def load_ids(fn: str) -> set[str]:
    return set(x.strip() for x in open(PUB_DIR / fn) if x.strip())


df = pd.read_csv(MARKERS)
ours = {N: set(df[df.N == N].rsID.dropna()) for N in [35, 50, 70]}

panels = {
    "Shi 36": load_ids("shi_36.txt"),
    "Shi 59": load_ids("shi_59.txt"),
    "Shi 98": load_ids("shi_98.txt"),
    "Shi 142": load_ids("shi_142.txt"),
    "Cao 19": load_ids("cao_19.txt"),
    "Cai 34": load_ids("cai_eas34.txt"),
    "PAANDA-EA N=35": ours[35],
    "PAANDA-EA N=50": ours[50],
    "PAANDA-EA N=70": ours[70],
}
names = list(panels.keys())
n = len(names)

count_mat = np.zeros((n, n), dtype=int)
jac_mat = np.zeros((n, n))
for i, a in enumerate(names):
    for j, b in enumerate(names):
        inter = len(panels[a] & panels[b])
        union = len(panels[a] | panels[b])
        count_mat[i, j] = inter
        jac_mat[i, j] = inter / union if union else 0.0

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), dpi=200)

for ax, mat, title, fmt, vmax in (
    (axes[0], count_mat, "Absolute SNP overlap (count)", "d", None),
    (axes[1], jac_mat, "Jaccard similarity (shared / union)", ".2f", 1.0),
):
    im = ax.imshow(mat, cmap="YlOrRd", aspect="auto", vmin=0, vmax=vmax)
    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8.5)
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=8.5)
    ax.set_title(title, fontsize=11, pad=10)
    thresh = mat.max() * 0.6
    for i in range(n):
        for j in range(n):
            val = mat[i, j]
            color = "white" if val > thresh else "black"
            label = f"{val:{fmt}}"
            ax.text(j, i, label, ha="center", va="center", fontsize=7.8, color=color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=8)
    if mat is count_mat:
        cbar.set_label("Shared SNPs (count)", fontsize=8.5)
    else:
        cbar.set_label("Jaccard similarity", fontsize=8.5)

fig.suptitle(
    "SNP panel overlap — published panels vs. PAANDA-EA committed panels",
    fontsize=12.5, y=1.02,
)
fig.tight_layout()
fig.savefig(OUT / "manuscript_fig7_overlap_heatmap.png", bbox_inches="tight")
fig.savefig(OUT / "manuscript_fig7_overlap_heatmap.svg", bbox_inches="tight")
print(f"Wrote {OUT / 'manuscript_fig7_overlap_heatmap.png'}")
