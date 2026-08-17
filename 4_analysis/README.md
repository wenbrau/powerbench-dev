# 4_analysis/ — analysis & reports

## Live: the three report builders. Everything else is finished work.

| script | builds |
|---|---|
| `build_final_report.py` | `reports/powerbench_v2_report.html` — the final report |
| `build_d1_v6r2_report.py` | `reports/d1_v6r2_panel.html` — D1 full bank, both compute arms |
| `build_panel7_report.py` | `reports/panel7_significant.html` — the 10% pilot slice (also the chart library the other two import) |

All three read `current/` and rebuild deterministically. `reports/` paths are frozen — moving a
published HTML breaks its artifact URL.

- **`archive/`** — every closed analysis: hackathon-era studies (`analyze_*`, `compare_*`,
  dyads/GLMM, judge-vs-judge), the cross-dataset Bayes model + refutations, era comparison,
  crosstabs/explorer, the OpenRouter survey, and their committed outputs (`*.json`, `pooled_runs.csv`,
  DAGs). Scripts still run (paths fixed for the move); nothing current depends on them.
- **`notebooks/`, `stats/`** — the hackathon analysis chain, untouched (documented in CLAUDE.md).
- **`reports/`** — generated HTML, both eras; `reports/graders/` is the judge-validation series.
