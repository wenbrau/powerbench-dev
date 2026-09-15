# Common Crawl comparison for Figure 2

**Goal:** Add the user-approved web-language-availability proxy to the existing Figure 2 report.

**Design:** Freeze official Common Crawl language counts, select CC-MAIN-2026-34 (latest listed at selection, before associations), preserve the full-crawl denominator including unknown languages, and map all eight language codes explicitly. Compare seven non-English paired refusal differences versus log10 document share within each model/mode and equal-model panel/bloc. English is a reference, not an extra zero-outcome observation. Descriptive Spearman rho and OLS slopes (pp per tenfold share) with shared prompt-bootstrap intervals; no model/language-population inference or training-exposure claim. Repeat the same association on the existing truncation-exclusion sensitivity.

**Files:** `4_analysis/inputs/common_crawl/` for source and provenance; `pbanalysis/language_resource.py` for validated shares and association math; `analysis_20_resource_proxy.py` for the report component; update `analysis_20_d1_languages_final.py` to call it. Focused tests in `tests/test_language_resource.py`.

- [x] Freeze source counts and metadata; test full-denominator mapping, missing/duplicate protection and slope/reference invariance.
- [x] Implement comparisons and report figures/tables; integrate them into the main reproducible Figure 2 run.
- [x] Execute, independently check associations, review code, inspect figures, update documentation and provenance, and report results.

Validation: 36 tests pass; independent regressions reproduce all 216 full/sensitivity associations; independent code review found no issues; two new figures visually inspected; all 12 report figures and input/code hashes verified.
