"""Corrected 6-panel confusion-matrix figure (manuscript Fig. 5) — replaces the
stale figure, which additionally mislabeled all three PAANDA-EA panels as
"stat+EN" (only N=50 actually uses that pool+reducer; N=35 uses fst_stat+EN,
N=70 uses FST+EN) and used the wrong classifier/accuracy throughout.

Top row: PAANDA-EA N=35/50/70 (leak-free out-of-fold, Best Fixed Configuration
— matching Table 2/3). Bottom row: Cai 2024, Cao 2022, Shi 2019 (best classifier
per Table 3), from the cached external out-of-fold predictions.

Writes: reports/figures/manuscript_fig5_confusion_grid.png / .svg
"""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from confusion_matrices import COMMITTED, confusion, out_of_fold_predictions
from nested_cv_sweep import Data

OOFPRED_PKL = (
    REPO
    / "results_archive/baseline_leaky_v1/self_evaluation/09_published_panel_comparison"
    / "panel_oofpreds.pkl"
)
OUT = REPO / "reports/figures"

LABELS = ["Han", "JPT", "SEA"]
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"


def load_pub_confusion(pkl_key: str, classifier: str, class_order: list[str]) -> tuple[np.ndarray, float]:
    with open(OOFPRED_PKL, "rb") as fh:
        d = pickle.load(fh)
    pkl_classes = [str(c) for c in d["classes"]]
    assert pkl_classes == class_order
    y_true, y_pred = d["oofpreds"][pkl_key][classifier]
    cm = confusion(y_true, y_pred, len(class_order))
    acc = np.trace(cm) / cm.sum()
    return cm, acc


def plot_cm(ax, cm: np.ndarray, title1: str, title2: str) -> None:
    row_pct = cm / cm.sum(axis=1, keepdims=True)
    ax.imshow(row_pct, cmap="Blues", vmin=0, vmax=1)
    n = cm.shape[0]
    for i in range(n):
        for j in range(n):
            frac = row_pct[i, j]
            color = "white" if frac > 0.55 else INK
            ax.text(j, i - 0.12, f"{cm[i, j]}", ha="center", va="center",
                     fontsize=11, fontweight="bold", color=color)
            ax.text(j, i + 0.18, f"{frac*100:.1f}%", ha="center", va="center",
                     fontsize=8, color=color)
    ax.set_xticks(range(n)); ax.set_xticklabels(LABELS, fontsize=9)
    ax.set_yticks(range(n)); ax.set_yticklabels(LABELS, fontsize=9)
    ax.set_xlabel("Predicted", fontsize=8.5, color=INK_SECONDARY)
    ax.set_ylabel("True", fontsize=8.5, color=INK_SECONDARY)
    ax.set_title(f"{title1}\n{title2}", fontsize=9.3, color=INK, pad=6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)


def main() -> None:
    data = Data()
    class_order = list(data.le.classes_)

    fig, axes = plt.subplots(2, 3, figsize=(11.5, 8), dpi=200)

    for ax, (label, n, pool, reductor, clf) in zip(axes[0], COMMITTED):
        y_true, y_pred = out_of_fold_predictions(data, pool, reductor, clf, n)
        cm = confusion(y_true, y_pred, len(class_order))
        acc = np.trace(cm) / cm.sum()
        plot_cm(ax, cm, f"PAANDA-EA N={n} ({pool}+{reductor})", f"{clf}, acc={acc*100:.1f}%")

    bottom = [
        ("Cai et al. 2024 (N=34)", "cai_eas34", "SVM_RBF"),
        ("Cao et al. 2022 (N=14 matched)", "cao_19", "LR"),
        ("Shi et al. 2019 (N=116 matched)", "shi_142", "SVM_RBF"),
    ]
    for ax, (label, key, clf) in zip(axes[1], bottom):
        cm, acc = load_pub_confusion(key, clf, class_order)
        plot_cm(ax, cm, label, f"{clf}, acc={acc*100:.1f}%")

    fig.text(0.06, 0.72, "PAANDA-EA committed panels", rotation=90, va="center",
              fontsize=10.5, color=INK)
    fig.text(0.06, 0.28, "Published panels", rotation=90, va="center",
              fontsize=10.5, color=INK)
    fig.suptitle("Fig. 5 — Confusion matrices: PAANDA-EA vs. published panels (5-fold OOF)",
                 fontsize=12.5, y=0.98)
    fig.tight_layout(rect=[0.07, 0, 1, 0.96])

    fig.savefig(OUT / "manuscript_fig5_confusion_grid.png", bbox_inches="tight")
    fig.savefig(OUT / "manuscript_fig5_confusion_grid.svg", bbox_inches="tight")
    print(f"Wrote {OUT / 'manuscript_fig5_confusion_grid.png'}")


if __name__ == "__main__":
    main()
