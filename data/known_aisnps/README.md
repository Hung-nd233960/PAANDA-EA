# Known AISNP panels — reference collection

Marker lists for published ancestry-informative SNP panels, collected during this
project as background reference material. Each file is a plain list of dbSNP rsIDs,
one per line, with no genotype or sample data.

**These panels were not benchmarked in the report.** The three panels actually
re-genotyped and evaluated on this study's cohort (Cai, Cao, Shi) live separately in
[`../published_panels/`](../published_panels/) — see `reports/REPORT.md` §V-D. The
files here are a wider survey of panels that exist in the literature, kept for
orientation and for any future overlap analysis. No pipeline code reads this
directory.

| File | Unique rsIDs | Notes |
|---|---|---|
| `seldin_128.csv` | 128 | Count matches the filename's nominal panel size. |
| `hsiao_lin_hwa_2017.csv` | 130 | No trailing newline on the final line. |
| `cal_2016.csv` | 74 | See provenance caveat below. |
| `cal_et_al_2025.csv` | 58 | See provenance caveat below. |
| `forenseq_ancestry.csv` | 56 | **Has a `rsID` header row** — the only file here that does. Ancestry markers from the ForenSeq panel. |
| `kiddlab_.csv` | 55 | Kidd lab panel; the trailing underscore in the filename is an artifact, not meaningful. |

## Provenance caveat

The filenames were assigned during collection and were **not** re-verified against
their source publications when this directory was archived. Two in particular should
be checked before being cited:

- `cal_2016.csv` and `cal_et_al_2025.csv` — the `cal_` prefix may be a transcription
  of "Cai". If so, these could relate to the same author group as the `cai_*` files in
  [`../published_panels/`](../published_panels/), but the marker counts (74 and 58) do
  not match the Cai-34 or Cai-58 panels used in the report, so they are more likely
  different panels or different papers. Resolve against the source before treating
  either as a specific published panel.

Anyone reusing these lists should confirm each file's source publication
independently rather than relying on its filename.
