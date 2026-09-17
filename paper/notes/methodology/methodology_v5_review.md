# Methodology v5 — review and revision notes

## What changed and why

This revision uses the v2–v4 drafts as editorial starting points and checks substantive claims against repository artifacts and selected decision-log entries. It creates a new main section and supplement, preserving earlier drafts. It does not change benchmark data, runner code, analysis outputs, or the historical LaTeX paper. No external sources or fresh model calls were used.

The main section explains the construct, comparisons, construction, collection, judging, and inference in that order. Only the request-type and dataset-design tables remain there. Detailed rosters, country lists, provenance, schema, validation tables, and an exact prompt example move to the supplement. A reader can understand the study without first learning repository filenames; a reader auditing it can follow the source map below.

### Substantive corrections

| Issue in v4 | Revision and evidence |
|---|---|
| Official judge assigned harmfulness κ = 0.47 and said to over-flag harm | Those describe nano. The candidate report gives DeepSeek κ = 0, sensitivity 0%, specificity 100%. Harmfulness is explicitly exploratory; refusal validity cannot establish harmfulness validity. |
| Official judge's per-mode refusal κ copied from nano | Correct DeepSeek values: 0.694 he, 0.700 de, 0.798 pg. Same candidate report. |
| Candidate validation implicitly described the pinned production configuration | DeepSeek's candidate calls used multiple providers; Morph pinning came later. Validation does not directly certify the final endpoint. |
| “Our reading” of 99 disagreements implied independent human adjudication | The September 5 notebook attributes the 67-versus-9 adjudication to Fable. It is model-assisted selection evidence, separate from human gold. |
| Every two-way design margin described as balanced | Direct audit finds context×scale and context×standing counts 21/24/27, and scale×standing 63/66, across the 576 English prompts. Domain×context is exactly 9 per pair. |
| Pilot word counts placed in final-bank QA table | Recomputed means: he 96.07, de 94.21, pg 96.61; reference 100.82. Eight English power prompts exceed the 80–115 specification under whitespace counting. |
| D1 source file treated as 576 English-only rows | It has 1,152 English/Spanish rows and 576 scenario IDs; select English or use the 4,608-row verified multilingual bank. |
| Both nationalities said to be visible in the judge's request | User country is in the target system message; affected nationality is in the request. The judge omits the system message, although the response can repeat its contents. |
| Generation-funnel row implied 882 full-bank candidates | The realism audit combined full-bank and pilot rows. Its 63 full-bank replacements and 113 pilot replacements must remain distinct. |
| D3 uniformly claimed per-row recast classification / edit distance | The inspected power bank does not uniformly carry those fields. The reference bank has `recast`, with 110 identity-only and 82 counterpart rows. |
| Alignment voting component called ideal points | Code uses dyadic voting agreement; ideal-point distance is a separate check. |
| Country pools presented as free of hand selection | They include normative hand-coded layers, thresholds, and two demonym-based substitutions. |
| Historical 5,000-token regrading presented as exact truncation | The script cuts a character prefix in proportion to reported completion tokens. Stored full output and retrospectively judged text can differ. |
| All analyses said to use 3,000 bootstrap draws | Block 17 and the reasoning ladder use 1,000; block 16 uses 3,000. |
| Logit difference-in-differences presented as uniformly implemented | Expanded D3 blocks 16/18 compute percentage-point effects. The logit proposal is distinguished from existing results and needs a zero/one-rate policy. |
| Positive independence-based excess said to be positive under any dependence | This is mathematically false. The correct union bounds are max(a,b) and min(1,a+b); independence lies inside them. The three modes are also different stories. |
| Nationality significance threshold used non-overlap of intervals | Removed. Test the contrast itself using its sampling distribution. |
| Sequential IDs called content-derived | IDs preserve scenario identity; file hashes identify content. |
| Panel totals and valid counts mixed 6-, 19-, 24-, and 25-model populations | Main table now gives bank dimensions. Saved expanded D1 quality counts have their own labelled appendix table. Other final denominators require a consistent release manifest. |
| Minimum-detectable-effect table mixed illustrative assumptions and pooled/mode-specific n | Removed pending result-specific estimates. Sharing prompts does not imply pooled precision can never improve, and 504 D3 prompts is only 168 per mode. |

## Decisions and checks still needed before submission

These are publication/analysis tasks, not permission requests and not claims that the manuscript is ready to submit.

1. **Freeze the result set and grading policy.** Choose which expanded-panel blocks supply final figures, then reconcile old official sidecars and truncation sidecars in every selected loader. Some generic loaders and older result blocks still use legacy judgments. This revision does not silently replace their outputs.
2. **Finalize reference-adjusted estimands.** Decide whether the paper will report points, logits, or both. If logits are added, specify treatment of zero/one rates and implement the analysis before describing it as performed. Preserve both interpretations if both are scientifically useful.
3. **Harmfulness validation.** Determine whether a later production-pin validation exists; it was not established by the reviewed candidate report. Otherwise retain the explicit limitation and avoid safety conclusions from this label. New validation would be additional research, not an editorial repair.
4. **Consolidate response accounting.** Produce one versioned manifest per published result: panel, bank hash, run files, judgment precedence, collected rows, exclusions by reason, and common-valid pair counts. Saved block 17 gives a checked 24-model D1 table; it is not a manifest for all controls and families.
5. **Resolve generation/translation model provenance.** Reconcile the Sonnet workflow records with the notebook's Fable/Opus verification account at the pass level. Do not guess a single model name for the whole pipeline.
6. **Disclose outcome-dependent exclusion.** The Gemini 2.5 Flash Lite rationale includes zero refusal. Retain the explanation and examine a sensitivity analysis if it affects the final panel claim.
7. **Release packaging.** Confirm final licences and the release manifest for benchmark prompts, third-party probe material, model completions, and annotations. The user describes the benchmark as public; local file presence does not establish licence terms or the exact public snapshot. No licence was invented here.
8. **Optional final-bank semantic audit.** The current offline check measures structure and whitespace length. It does not certify no declarations, method cues, geographic leakage, or translation errors. Remove absolute zero-error wording unless a final-bank audit supports it.

## Reading guide

- `methodology_v5_main.md`: revised paper-body prose.
- `methodology_v5_appendixes.md`: full methodological supplement and repository source map.
- `methodology_draft_v5.md`: combined reading copy of the two files above.
- `methodology_v5_bank_audit.json`: measured bank counts, dimensions, hashes, and pairing checks.
- `audit_methodology_v5.py`: rerunnable, offline bank audit; reads only the eight named banks and writes the audit JSON.

The central intuitive distinction is between changing a version of the same story and comparing different stories. Translations and recasts support the former; request types, standing, and scale mostly support the latter. Likewise, a specification says what writers were asked to do, while the bank audit says what is actually in the files. Keeping both distinctions explicit makes the paper easier to understand and harder to overinterpret.
