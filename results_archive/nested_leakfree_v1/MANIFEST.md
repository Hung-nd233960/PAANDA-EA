# Archive — leak-free nested-CV results (`nested_leakfree_v1`)

Results backing [`reports/REPORT.md`](../../reports/REPORT.md). Every file here was
produced with the full supervised selection chain rebuilt inside each outer CV fold
(candidate pools, reducer ranking, classifier), and **after** the combined-block
(`fst_stat`) fix — so the `fst_stat` pool is 965 SNPs throughout, not the 1,003 of
earlier drafts. Generated with `make nested` / `make compare-nested`; 5-fold
stratified outer CV, seed 42.

## `08b_nested_cv_sweep/`

| File | Contents | Used by |
|---|---|---|
| `grid_results.csv` | Full grid: 18 panel sizes × 3 pools × 3 reducers × 6 classifiers × 5 folds (4,860 fits) | Report §IV-D, Tables V–VIII, Figs. 3–4 |
| `nested_tierA_results.csv` | Blind Selection per-N summary (fully nested, inner-CV config selection) | Report §V-A, Table XI, Fig. 6 |
| `nested_tierA_folds.csv` | Blind Selection's per-fold configuration choice and accuracy | Report §V-B, Table IX |
| `winner_per_N.csv` | Best fixed configuration at each panel size | Report Table VII |
| `winner_per_fold.csv` | Fold-level component winners | Report Table V |
| `winner_config_leaderboard.csv` | Configurations ranked across the grid | Report Table X |
| `winner_stats_fragment.md` | Generated summary fragment of the winner analysis | — |
| `comparison_accuracy_vs_n.png` | Accuracy-vs-N comparison plot | — |
| `comparison_leaky_vs_nested.csv`, `comparison_summary.md` | Pre-fix leaky baseline vs leak-free, per N | Development record only; this comparison is deliberately absent from the final report |

## Stale file — do not use

**`nested_tierB_results.csv` is stale.** "Tier B" was the intermediate design that
rebuilt pools per fold while holding the baseline-committed configuration fixed, used
to isolate the magnitude of the original leak. This file still reflects the **pre-fix**
`fst_stat` pool (the old cascading χ²/mutual-information/KL-divergence filter), so its
numbers are not comparable with anything else in this directory. It was not rerun
after the fix, and nothing in the final report depends on it. The Tier A/Tier B
terminology was itself retired: the report uses **Blind Selection** (fully nested) and
**Best Fixed Configuration** instead.

## Related

- Frozen pre-fix baseline: [`../baseline_leaky_v1/`](../baseline_leaky_v1/) (read-only)
- Input data needed to regenerate: see the manifest inside
  `PAANDA-EA_v1.0_final_outputs.tar.gz` (archived separately; the raw 1000 Genomes
  working directory was deleted after release)
