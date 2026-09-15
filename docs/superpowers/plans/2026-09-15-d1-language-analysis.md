# D1 final-panel language analysis implementation plan

**Goal:** Reproduce Figure 2's agreed language comparisons on all 24 models, eight languages and four modes.

**Spec:** `notebooks/PowerBench.md`, September 8/14; user instruction to continue after Figure 1.

**Architecture:** Extend the explicit final-panel loader to multilingual banks. Use a compact paired-prompt bootstrap over shared prompt draws, preserving per-model denominators. A new numbered script writes tables, figures, methods and provenance. Execute inline in the existing workspace, preserving the previous batch and unrelated local files.

**Stack:** Existing NumPy, pandas, SciPy, Matplotlib and pytest environment. No model API calls.

## Scope and constraints

- Exactly 24 models, 12 US / 12 CN; official DeepSeek judgments and mandatory truncation overlays.
- Compare each language to English on complete pairs; English denominators can differ by comparison. Report every exclusion. Raw levels use available rows; range uses prompts complete in all eight languages.
- Primary differences in percentage points, with a normalized companion: direction among discordant pairs, `(language-only refusal - English-only refusal) / discordant pairs`. Undefined when there are no discordances; no artificial pseudocount.
- Per-model exact McNemar tests (binomial over discordances), BH over 24 × 7 × 4 comparisons. Equal-model panel/bloc means use shared prompt draws, 5,000 iterations; no inference to a population of models.
- Controls displayed separately. Scale/standing language comparisons within each level. Language-pair matrices and language ranges are descriptive; avoid selecting extrema and then reporting unadjusted significance.
- Audit truncation by model/language; sensitivity removes both members when either response was truncated.
- The user subsequently approved Common Crawl; see the Common Crawl plan for its frozen source and descriptive comparison.

## Tasks

- [x] Add tests for multilingual loading, duplicate and cross-language metadata protection; implement `load_d1_multilingual()` in `pbanalysis/final_panel.py`, preserving English behavior.
- [x] Add and test `pbanalysis/paired_languages.py`: exact complete-pair estimates, discordance counts, symmetric reversals, shared resampling, and truncation exclusion.
- [x] Create `analysis_20_d1_languages_final.py`: raw rates, English contrasts, scale/standing summaries, descriptive pair matrices, complete-eight-language ranges and truncation sensitivity.
- [x] Produce `results/20_d1_languages_final/`: HTML, PNG/PDF, CSV, README, input/code hashes, tests and validation record. Update the analysis index.
- [x] Execute the real analysis, independently recount paired counts from source labels, review calculation code, inspect all figures, verify that English matches Figure 1, and summarize findings.

Completed core Figure 2 analysis: 32 tests pass; source recount matches 768 rates and 672 paired contrasts; independent review found no remaining issues; ten figures inspected and exports/hash records verified. The subsequently approved Common Crawl comparison is implemented; see the companion plan and current verification record.
