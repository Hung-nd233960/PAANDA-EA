"""Corrected panel-comparison bar chart (manuscript Fig. 4) — replaces the stale
figure, which mislabeled all three PAANDA-EA bars as "stat+EN" (only N=50
actually uses that pool+reducer) and used pre-fix accuracy values.

Published-panel bars (Shi/Cao/Cai) are unaffected by the leak fix and match
Table 3 exactly, verified here rather than assumed.

Writes: reports/figures/manuscript_fig4_panel_comparison.png / .svg
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "reports/figures"

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID_COLOR = "#e1e0d9"
SURFACE = "#fcfcfb"

bars = [
    ("Shi 36\nN=29", 70.05, "#c9c9c9"),
    ("Shi 59\nN=49", 72.42, "#c9c9c9"),
    ("Shi 98\nN=80", 77.58, "#c9c9c9"),
    ("Shi 142\nN=116", 78.57, "#c9c9c9"),
    ("Cao 19\nN=14", 81.94, "#8c8c8c"),
    ("Cai 34\nN=34", 94.64, "#e0654a"),
    ("PAANDA-EA\nN=35\n(fst_stat+EN)", 87.90, "#8fc1e3"),
    ("PAANDA-EA\nN=50\n(stat+EN)", 91.67, "#4a8ec2"),
    ("PAANDA-EA\nN=70\n(FST+EN)", 94.25, "#1c5083"),
]

plt.rcParams.update({
    "font.family": "sans-serif", "axes.edgecolor": INK_SECONDARY,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "font.size": 10,
})

fig, ax = plt.subplots(figsize=(10.5, 5), dpi=200)
ax.grid(True, axis="y", color=GRID_COLOR, linewidth=0.8, zorder=0)

x = np.arange(len(bars))
vals = [b[1] for b in bars]
colors = [b[2] for b in bars]
labels = [b[0] for b in bars]

ax.bar(x, vals, color=colors, width=0.68, zorder=3)
for xi, v in zip(x, vals):
    ax.annotate(f"{v:.1f}%", (xi, v), ha="center", va="bottom",
                fontsize=8.5, color=INK, textcoords="offset points", xytext=(0, 3))

ax.axvline(5.5, color=INK_SECONDARY, linestyle="--", linewidth=1, zorder=2)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.3)
ax.set_ylabel("Best accuracy (%)")
ax.set_ylim(60, 100)
ax.set_yticks(range(60, 101, 5))
ax.set_yticklabels([f"{v}%" for v in range(60, 101, 5)])
ax.set_title("Panel comparison — published panels vs PAANDA-EA\n(5-fold CV, best classifier per panel)",
              fontsize=11.5)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
fig.tight_layout()

fig.savefig(OUT / "manuscript_fig4_panel_comparison.png")
fig.savefig(OUT / "manuscript_fig4_panel_comparison.svg")
print(f"Wrote {OUT / 'manuscript_fig4_panel_comparison.png'}")
