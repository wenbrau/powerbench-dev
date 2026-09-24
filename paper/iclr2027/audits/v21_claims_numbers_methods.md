# v21 verification: claims, numbers, and statistical methods

Audited on 2026-09-23 against commit `255f858`, including a deeper continuation requested by the appendix/analysis owner. Scope: the current submission sources, their table generators, figure and analysis scripts, stored statistical outputs, canonical English/language/nationality/AI run loaders, prompt construction artifacts, reasoning-ladder data, and raw human-validation labels. Existing local edits were preserved. No manuscript, verdict, production result table, or figure was changed.

The headline baseline rates, generated tables, and canonical analysis snapshots reproduce. The continuation also supports nationality specificity for the unsigned bias statistic and the AI-versus-control difference after excluding the provider-changed model. However, judge-validation attribution, construction statistics, the reasoning correction families, and several robustness claims need correction. This is a source-and-results audit, not certification of every analysis: the R models were not refitted, the full response corpus was not independently rejudged, and the PDF layout and bibliography were not comprehensively audited.

The initial evidence is in [v21_verification_checks.json](v21_verification_checks.json). The continuation's inputs, SHA-256 hashes, checks, and sensitivity results are in [v21_extended_verification.json](v21_extended_verification.json), produced by [verify_v21_extended.py](verify_v21_extended.py). Additional CSVs beside this report retain per-model AI and nationality sensitivities, reciprocal cross-judge contrasts, and the reasoning BH-family comparison.

## Confirmed checks

| Check | Result | What this establishes |
|---|---|---|
| Regenerate `make_tables.py` and `make_estimate_tables.py` into a temporary directory | All 13 generated tables byte-identical to the submission | The checked tables faithfully transcribe their saved inputs; this does not independently validate the fitted models. |
| Load final D1 English runs with official-judge and truncation-overlay precedence | 18,432 rows; 18,430 valid; 24 models | Loader coverage and coordinate assertions passed. |
| Recompute all 96 model-by-type refusal rates | Maximum discrepancy from block 78: 2.3e-16 percentage points | Baseline rates reproduce from run artifacts. |
| Recompute baseline model-averaged refusal | SE 3.0816%, DE 14.5413%, PG 23.6328%, CT 20.2723% | The manuscript's 3.1%, 14.5%, 23.6%, and 20.3% are correct. PG > DE > SE in all 24 models. |
| Recompute excess over the sum of components and its model-level t test | 6.0099 pp; 95% CI [3.7968, 8.2230]; p = 1.0218e-5 | The reported 6.0 [3.8, 8.2] pp and p < .001 are correct under that inferential model. |
| Independently recompute BH in blocks 77, 83, and 89 | All 116 entries match; maximum absolute discrepancy 1.2e-16 | The checked corrections are arithmetically correct within the recorded families. Family selection is a separate question. |
| Recompute Figure 3A ORs and Wald p values from saved coefficients and SEs | All four match | ORs 1.969, 2.192, 2.088, and 1.414 reproduce; this is not a fresh fit. |
| Recompute Figure 4D p and q values from its 4,000 saved bootstrap draws | All eight entries match | The reported inference is bootstrap-based, as discussed below. |
| Recompute cross-judge PG contrast agreement from its source tables | 71/75 same signs; Pearson r = 0.86818 | These numbers are correct for the particular contrasts tested, not for every headline contrast. |
| Static LaTeX label/reference check | No undefined or duplicate labels among scanned main, section, and table sources | Cross-references resolve at source level; no PDF compilation was performed. |

The 13 reproduced tables were `panel`, `rates_per_model`, `truncation`, `truncation_by_model`, `harmfulness`, `rank_between_modes`, `ai_scale_levels`, `est_fig1`, `est_fig2`, `est_fig3`, `est_fig4`, `est_fig4_models`, and `lang_22_vs_24`.

## Findings requiring attention

### 1. High priority: validation statistics are attributed to the wrong judge

**Location:** `submission/sections/appendix.tex:226` and `:435`; candidate table at `:239` onward.

The human-validation paragraph attributes harmfulness agreement of 88%, κ = .47, sensitivity 67%, and specificity 91% to the adopted DeepSeek judge. Those are the GPT-5.4-nano results. The stored candidate evaluation gives DeepSeek 90% agreement, κ = 0, sensitivity 0%, and specificity 100% for harmfulness. Its predictions did not identify any of the human-positive harmfulness cases in this small sample. The candidate table already shows the correct κ values.

The same paragraph also uses nano's refusal agreement by type: 90/85/85% for SE/DE/PG. DeepSeek's values are 85/85/90%. The overall refusal agreement, 87%, and κ, .73, are shared by both and are correct.

**Evidence:** `3_judge/validation/human_v2/judge_candidates_v2.json`, fields `refuse` and `harmful`, `per_judge`; the accompanying `.md` report. The harmfulness table is derived from the final DeepSeek verdicts through `pbanalysis/final_panel.py` and block 25, so nano's validation cannot be used to support it.

**Action:** correct attribution in both paragraphs. Present the harmfulness rates strictly as exploratory automated flags with the adopted judge's validation failure disclosed; decide whether these rates warrant retention without further validation. This issue does not replace or invalidate the separately supported refusal κ.

**Continuation:** independently rebuilt all 60 majority labels from the 180 human ratings and recalculated all candidate statistics from the cached judgments, confirming the attribution error. There are 28 human-positive refusal items and only six human-positive harmfulness items. DeepSeek missed all six harmfulness positives; the sample is too small and selected to treat this as a precise population sensitivity estimate. Human Fleiss κ reproduces at .619923 for refusal and .415374 for harmfulness; unanimity is 71.67% and 85.00%, respectively.

### 2. High priority: the one-endpoint-throughout claim is false for DeepSeek

**Location:** `submission/sections/appendix.tex:167`, panel and serving protocol.

The appendix says one endpoint was used per model for the whole study. In the final saved D3 analysis rows, deepseek-v4-pro's 504 human power-shifting rows use GMICloud and its 504 AI versions use SiliconFlow (168 per type). Its human and AI control rows both use GMICloud. Therefore this model's human–AI power-shifting contrast also changes provider, while its control contrast does not.

**Evidence:** `4_analysis/results/22_d3_ai_final/analysis_rows.csv.gz`, grouped by model/condition/mode/provider; `4_analysis/results/23_interpretation_audit/ai_provider_changes.csv`; the historical exception is also documented in `VERSIONS.md`.

**Action:** disclose the exception in the protocol and panel table. Add a sensitivity result excluding this model for the AI effects and the power-shifting-versus-control contrast; audit the language comparison for the analogous serving exception. This finding establishes a confound for this model, not that the pooled effect disappears.

**Continuation:** the AI direction-bias difference survives exclusion: 0.264 [0.161, 0.367], paired-model t-test p = 2.38e-5, 23 models. With all 24 it is 0.279 [0.176, 0.383], p = 1.06e-5. These are differences on the dimensionless direction-bias scale, not refusal percentage points. An exploratory equal-weight analysis of the 16 developer means also remains positive: 0.247 [0.121, 0.372], p = .000789. Neither check is a refit of the main GLMM or the capability interaction.

The analogous language exception is confirmed: DeepSeek's 576 English power-shifting responses use GMICloud, all seven translated power-shifting sets use SiliconFlow, while its 192 controls in every language use GMICloud. No other model has multiple providers in the loaded multilingual data. The final 22-model language panel still includes DeepSeek, so dropping the two Swahili-problematic models does not remove this exception.

### 3. High priority: nationality specificity is inferred from separate significance tests

**Location:** `submission/sections/results.tex:29` and `:33`; the general rule stated in `appendix.tex:137`.

The nationality text concludes that biases are specific to power shifting because the power-shifting tests are significant and the control tests are not. It similarly concludes specificity to the geopolitical axis from significant geopolitical and nonsignificant neutral results. The cited separate tests do not directly test either difference. The inspected side and direction GLMMs fit request types separately; the displayed direction interaction is with developer country, not with control status.

**Action:** report direct power-shifting-minus-control and geopolitical-minus-neutral contrasts for the relevant statistic, preserving their shared model/prompt structure. If those analyses are not available, state the observed pattern and that specificity has not been established by a direct contrast. Replace the general rule in A.7 accordingly. The AI direction-bias comparison is different: it already has a direct paired test in block 76; preserve that distinction.

**Continuation:** direct exploratory paired-model tests now support both differences for Figure 2B's unsigned bias metric (absolute direction bias minus its exact binomial chance expectation). Geopolitical PS minus geopolitical control is 0.1305 [0.0673, 0.1936], p = .000284; geopolitical PS minus neutral PS is 0.1441 [0.0854, 0.2028], p = .0000382. BH over these two audit tests gives q = .000284 and .0000765. Wilcoxon checks agree (p = .000278 and .0000302). These were not prespecified manuscript analyses, retain the existing binomial null and model-level inference, and should be presented as added analyses. They do not establish every type-specific, directional, or GLMM interaction claim. All 192 model-by-type-by-set discordance counts were independently reproduced from the canonical paired D2 rows.

### 4. High priority: the cross-judge check does not test all the contrasts claimed

**Location:** `submission/sections/methods.tex:30` and `appendix.tex:252`.

The 71/75 and r = .87 figures reproduce. However, they cover PG nationality-condition-versus-no-nationality-English contrasts and AI-versus-human contrasts in five models. The headline nationality result is a reciprocal nationality swap; the headline language results include within-model language orders, ranges, and usage-weighted differences. Those are not the 75 contrasts being counted. Controls and the full 24-model panel are not covered by this check either.

**Evidence:** `4_analysis/paper_figures/appendix/figA_judges.py:90`, which reads block 11's `contrasts_vs_d1en_by_judge.csv` and selects the PG columns. Subtracting two stable-sign baseline contrasts need not yield a stable-sign reciprocal contrast.

**Action:** narrow the claim to exactly the tested contrasts. Recompute the main estimands under both judges wherever paired judgments already exist, including reciprocal nationality effects and the control comparison. List panel/type coverage explicitly; agreement between two judges is not a bound on shared error.

**Continuation:** subtracting the stored condition-versus-baseline point estimates to form the seven available reciprocal dyads in the same five models gives **23/35** equal signs and **r = .5284**, rather than the original 71/75 and .8682 for a different set of estimands. Ten reciprocal contrasts have opposite nonzero signs; two have a zero estimate under one judge. This calculation uses source estimates rounded to .001 percentage points, not a new analysis of jointly valid paired judgments, and includes only PG and the older seven dyads. It is a diagnostic showing why the baseline-contrast agreement cannot certify reciprocal robustness. It does not show that a pooled main effect reverses. The two newer great-power-free dyads, controls, and paired uncertainty still require evaluation.

### 5. Medium priority: Figure 4D's test is mislabeled

**Location:** `submission/sections/results.tex:67`; statistical-protocol table in `appendix.tex:308`.

Both call Figure 4D's inference a permutation test. Its saved p and q values actually come from inversion of a pivotal prompt-bootstrap interval. Language shuffling estimates the chance range inside that procedure; it is not the outer significance test used for the reported stars. The estimate-table caption at `appendix.tex:553` already correctly says bootstrap.

**Evidence:** `4_analysis/review_fig_languages_22models/step3_panelD_bootstrap.py`; `4_analysis/review_fig_languages/panelB/panelB_bootstrap.py:67`; saved `panelD_bootstrap_draws.npz`. Independent recomputation reproduced all eight p/q values, including usage-weighted PG q = .0473215.

**Action:** label this as a bias-corrected range estimate with a pivotal bootstrap interval/test, using a permutation-estimated chance reference. Keep Figure 4E's per-model permutation tests distinct. The near-threshold usage-weighted PG result also merits a Monte Carlo stability check before describing its significance as robust.

**Continuation:** its smaller tail contains 70 of 4,000 draws. A conditional binomial Monte Carlo interval for that tail, converted to the two-sided p value, is approximately [.0273, .0441]; at the recorded third BH rank in a family of four this corresponds approximately to q in [.0364, .0588]. This is simulation precision, not an effect confidence interval, and conditions on the saved threshold and null estimate. It shows that the .05 classification is not numerically secure at this simulation budget. A larger independent rerun remains needed; none was performed here.

### 6. Medium priority: the generation-cap description omits post-hoc approximate truncation

**Location:** `submission/sections/methods.tex:25`; `appendix.tex:184`–`:191`.

The manuscript describes responses as generated with a 5,000-token cap and judged as stored. Earlier runs had a larger cap. The harmonization script shortened those stored responses before rejudging using a proportional character cut, because provider tokenizers were unavailable. It did not reconstruct an exact 5,000-token generation.

**Evidence:** `3_judge/rejudge_truncated.py:1`–`:18`; `pbanalysis/final_panel.py:87`–`:116`. The current D1 English loader identifies 25 post-hoc truncation cases, all using the truncation judge pass.

**Action:** distinguish generation-time caps from retrospective approximate truncation, and describe the overlay precedence. Report their counts separately and retain the sensitivity excluding truncated rows. Avoid asserting that proportional character trimming has a verified token-level error bound.

**Continuation:** the complete loaders record 176 post-hoc cases in D1 across eight languages, 21 in D2, and 41 in D3 including its reused human reference. These sets overlap, so they must not be added as unique newly generated responses. The respective total truncation flags are 1,426, 751, and 41. One unresolved D1 case and one unresolved D3 case are excluded. Report generation truncation and retrospective harmonization separately.

### 7. Medium priority: clarify the GLMM estimator and validate consequential approximations

**Location:** `submission/sections/appendix.tex:316`.

The implementation consistently sets `nAGQ = 0`. The prose calls this a penalized quasi-likelihood starting fit. The lme4 documentation instead describes this setting as faster, less exact estimation with fixed and random effects optimized in the penalized iteratively reweighted least-squares step; `nAGQ = 1` is the default Laplace setting. Use the documented terminology, avoiding an unsupported equivalence to a separate PQL fitting procedure. [Official glmer documentation](https://lme4.github.io/lme4/reference/glmer.html).

**Evidence:** `4_analysis/r/glmm_common.R:32`–`:41`. Stored AI-main output confirms singular fits for SE and control, already acknowledged in the manuscript. The paired AI and side models inspected include prompt random intercepts but no prompt-specific manipulation slopes.

**Action:** state the actual fitting procedure and add targeted sensitivity checks for the main and borderline interactions using `nAGQ = 1`, richer prompt-level manipulation effects where identifiable, and recorded convergence diagnostics. These are robustness questions; the current audit does not establish that the existing estimates are wrong. No R refits were possible here: `Rscript` was absent from PATH and the usual macOS locations checked.

### 8. Medium priority: the capability conclusion is stronger than its supporting sensitivity results

**Location:** `submission/sections/abstract.tex:7`, `results.tex:53`, `appendix.tex:536`.

The full-panel power-shifting slope and its q value are supported by the saved fit. The direct difference from the control slope has p = .101, so the significant/nonsignificant split does not establish a capability relationship specific to power shifting. The appendix additionally reports that removing sonnet-5 halves the slope and gives p = .34. That caveat appears in the notebook-style narrative, but a dedicated machine-readable refit artifact was not located in this audit; it was not independently reproduced.

**Evidence:** block 64 `capability_glmm.csv`, stacked slope-difference row; block 83's BH table; `4_analysis/results/53_fig4_notelab/NARRATIVA_F4.md:903`–`:911`.

**Action:** qualify the abstract/body association and retain the direct-interaction result prominently. Archive reproducible leave-one-model-out and leave-one-developer-out fits, including the reported sonnet exclusion. Do not describe the sensitivity refit as freshly verified until its output is reproduced.

### 9. Medium priority: disclose observed repeat variability and the scope of uncertainty

**Location:** run protocol, statistical protocol, and limitations; `VERSIONS.md:78` records the issue.

An existing accidental repeat-run artifact contains 6,636 keys with exactly two nonempty responses and valid binary refusal fields after malformed lines are skipped. Recounting gives 544 refusal disagreements (8.20%). Of 1,000 identical-text pairs, 41 have different judgments (4.10%). This is evidence of repeat variability in that older six-model subset, including judge variability on identical text. It is not a controlled repeatability study of the complete final panel, and this audit did not independently verify every metadata field in those pairs.

**Action:** disclose this exploratory check and distinguish uncertainty over prompts, over models, and over repeated generations/judgments. The prompt bootstrap keeps models and weights fixed; it does not justify the main-methods statement that every claim treats models as random. Add a small table specifying the inferential population for each test family. Consider a properly controlled repeatability check, especially for disagreement-based measures. An 8.2% flip rate is not itself an 8.2-point bias and does not show that a systematic condition effect is noise.

### 10. Medium priority: exact design balance and the word-length bounds are overstated

**Location:** `submission/sections/methods.tex:10`; `appendix.tex:30`, `:38`, `:44`, and `:55`.

The final English power bank has exactly the stated one-way totals, 44 writers, and all the explicitly enumerated domain-based pair counts. It does **not** have exact balance for every pair of factors:

| Pair | Actual cell counts | Equal-count target |
|---|---:|---:|
| Context × scale | 21–27 | 24 |
| Context × standing | 21–27 | 24 |
| Scale × standing | 63–66 | 64 |

The control has analogous small imbalances: context × scale and context × standing are 7–9 rather than 8; scale × standing is 21–22. Describe the design as exact on the specified marginals and approximately balanced on the others. “Orthogonal” also needs qualification where it means exact statistical independence.

Eight final English power prompts fall outside the stated 80–115-word interval under the repository's own whitespace-splitting rule. The true range is **76–117**, with mean **95.6337**, so the reported mean is correct. IDs and counts: `p2s-140` 76, `p2s-190` 79, `p2s-265` 117, `p2s-323` 117, `p2s-348` 79, `p2s-356` 79, `p2s-431` 77, `p2s-527` 78 (all `-r1-en`). The same eight exceptions exist in v6r and v6r2. The 192 English controls are within range. The realism rewrite QA's zero violations should not be generalized to the entire final bank.

**Evidence:** `current/banks/dataset1_full_576.v6r2.multilang.verified.jsonl`, `dataset1_control_192.v1.1.multilang.verified.jsonl`; counting convention in `1_create_dataset/build/d1_v6r2_rewrites.py:238`. These are documentation corrections, not a recommendation to edit prompts after observing outcomes.

### 11. Medium priority: construction-audit statistics mix versions and populations

**Location:** `submission/sections/appendix.tex:44`, `:53`, and `:55`.

Three distinct provenance problems need resolution:

1. **Construct flags:** the located 576-row audit yields **44, 91, 169, 144** flags, whereas the appendix gives **37, 82, 171, 148**. Mean severity reproduces at **2.28993**. The stored audit labels its source `new576`; it should not be represented as a fresh audit of final v6r2. Either identify the exact artifact supporting the manuscript's four counts or replace them with correctly attributed historical results. This audit does not treat the older classifier's flags as definitive labels of the final prompts.
2. **Ask forms:** the appendix percentages and χ² p = .40 reproduce from `ask_form_576.jsonl`. A later audit, `ask_form_576_v6r.jsonl`, has explain/plan/draft counts **83/66/43** for SE, **86/59/47** for DE, and **64/79/49** for PG, giving **p = .130823**. Both are nonsignificant, but neither proves equal ask-form distributions. Identify the audited prompt version and the effect of subsequent rewrites; do not silently call the earlier numbers final-bank statistics.
3. **Realism:** the claimed 37/20/2% comes from the provenance note for **882 full-plus-pilot rows**, and counts strained **or impossible**. For the **504 full-bank rows** described in the paper, the raw verdicts are PG 39 strained + 5 impossible of 168, DE 18 + 0, SE 1 + 0. Strained-only rates are **23.2%, 10.7%, 0.6%**; non-OK rates are **26.2%, 10.7%, 0.6%**. The 63 full-bank rewrites reproduce as 44 + 18 + 1. These are pre-rewrite audit rates, not measured failure rates of the final prompts.

**Evidence:** `1_create_dataset/build/construct_compliance_576.jsonl`, both ask-form JSONLs, `realism_audit_d1v6.jsonl`, and `realism_rewrites_d1v6.provenance.json`. The 144-item recovery counts (136/144 human and 135/144 AI) and the 2.67 mean clarity reproduce from their stored audits. Historical translation repair counts also reproduce, but the control table traces to v1 verification while the analyzed control is v1.1. Add a versioned construction-audit table with source bank, date, denominator, pre/post-rewrite status, and artifact path.

### 12. Low priority: country allocations are approximately, not exactly, equal

**Location:** `submission/sections/appendix.tex:100`.

The deterministic allocator cannot give every one of 21 countries the same count among 576 scenarios or 192 scenarios of one request type. The power bank has **27–28 appearances overall** and **9–10 within type** for the standard 21-country allocations. The neutral second-side allocation varies more (see the machine-readable per-condition ranges), while excluding the first country. The **273 distinct ordered neutral pairs** and **zero same-country neutral pairs** reproduce.

**Action:** replace “equally often” with the actual allocation guarantee and ranges; keep the deterministic construction and reciprocal pairing descriptions. Do not treat country instances as independent randomly sampled country effects.

### 13. Medium priority: reasoning BH families differ from the documented families

**Location:** `submission/sections/appendix.tex:274`; `4_analysis/analysis_68_reasoning_glmm.py:120`–`:128`; saved block 68 tables.

The appendix specifies separate families for eight level-by-type effects and six type-minus-control differences. The code's first matching pattern `en (he|de|pg|ctl)$` also matches the end of a quantity such as `r1 en de - en ctl`. Because `np.select` takes the first match, all **14** enter `por_modo`; **zero** enter `modo_menos_control`. The saved q values reflect that combined family, not the documented separate families.

The continuation recomputes the documented families from the full-precision raw p values and saves both versions in `v21_reasoning_BH_family_check.csv`. For example, the second-level DE-minus-control ratio is reported with q ≈ **.01997**, while the separate six-test family gives q ≈ **.02568**. This remains below .05; the error is still material to reproducing the stated procedure. No fit needs to be rerun to resolve it. Choose and document the intended families, fix the classification if separate families are intended, and regenerate the q values and table together.

### 14. Medium priority: the reasoning exclusion counts and interpretation need revision

**Location:** `submission/sections/appendix.tex:274`, `:621`, and the reasoning table.

The current reasoning loader has **18,432 rows, 18,401 valid, 31 excluded**, matching the saved model's `nobs`. For GLM-5.2 at the second level it excludes **19 power-shifting + 9 control = 28**, not the described 26 + 9. Three additional exclusions occur in GLM-5.2 level-1 SE, GPT-5.6-terra level-1 control, and Gemini-3.1-flash-lite level-2 control. The stored 26 + 9 likely describes an earlier state; its relationship to repaired/rerun rows needs to be documented. Median reasoning-token extrema, 84 and 3,427, reproduce.

The reported ORs .33 and .23 are average level effects under sum-to-zero coding across **four request types and two developer countries**. They are not the estimated common effect of reasoning in every type. At level 1, SE, PG, and control do not individually pass the saved BH correction (q = .590, .066, .075); DE does. The significant type interaction is already in the table. “On power shifting and control alike” needs to distinguish the broadly consistent point-estimate direction from a claim of equal or individually significant effects. Likewise, interaction p = .147 does not establish DC independence, particularly with eight models.

**Evidence:** canonical `analysis_18_reasoning_ladder.load()`, block 68 raw and processed GLMM outputs, and `r/glmm_reasoning.R`. No R fit was rerun.

### 15. Medium priority: token weighting changes some reported language inferences

**Location:** `submission/sections/appendix.tex:334` (“changes no conclusion”).

The weight arithmetic is correct: largest request share **40.0302%**, top three **56.6514%**, effective number **5.2848** overall, **3.0289** US and **6.5390** CN; token weights give **6.2596**. However, the saved block 72 token-versus-request sensitivity tables differ at .05 in **six bootstrap comparisons** and **seven permutation comparisons** among the 35 language-by-group entries.

For pooled power shifting, French changes from bootstrap **q = .014** under request weights to **q = .3465** under token weights; German changes from **q = .616** to **q = .007**. French is explicitly discussed in the main results. None of the PG-only comparisons changes its .05 classification in these two saved tables, so some narrower robustness statements are supported. These tables use the block 72 model/language coverage, not a fresh token-weighted rerun of the final 22-model Figure 4D.

**Action:** specify which conclusions survive and acknowledge which language-specific detections depend on the weighting estimand. Requests and tokens measure different usage distributions; neither should be presented as ground truth for an average real-world user. The saved zero bootstrap q values also reflect finite simulation resolution, not exact zero probabilities; report them as below the appropriate resolution where needed.

## Continuation: coverage and successful reproductions

| Area | What was actually checked | Status and remaining limit |
|---|---|---|
| D1, all languages | 147,456 keys; 147,428 valid; 13 core fields compared against saved rows | Exact agreement; loader coordinate/coverage assertions passed. Semantic translation quality was not independently rated. |
| D2 nationality | 331,776 keys; 331,676 valid; same core fields | Exact agreement. All 192 reciprocal-count aggregates reproduce; two new direct specificity tests support the unsigned-bias claim under its existing null. |
| D3 AI plus reused human reference | 33,408 keys; 33,405 valid; same core fields | Exact agreement. All 95 stored nonzero-discordance rows reproduce from 96 model-by-type count rows; the omitted row has no discordances. |
| Total main responses | 24 × (8 × 768 + 18 × 768 + 696) | 495,936 generated-response slots, as reported. The D3 human reference is reused D1 data and must not be counted twice. |
| AI provider sensitivity | Reconstructed paired raw counts; model-level PS-minus-control test | Positive with and without DeepSeek; exploratory equal-developer weighting also positive. Main GLMM/provider and capability influence refits remain open. |
| Nationality specificity | Direct paired tests for Figure 2B's corrected unsigned bias | Both positive with BH across the two audit tests; these do not substitute for all directional interactions. |
| Human validation | 180 original ratings; majority labels; cached predictions of all candidates | Refusal validation reproduces. Harmfulness attribution error independently confirmed. |
| Capability-panel description | Group means/SDs and two-sample tests from per-model capability scores | US 58.2356 (SD 8.7568), CN 60.4428 (SD 8.3196); Welch p = .533279, Mann–Whitney p = .544370. “Matched” should mean selected to be similar, not statistically equivalent. |
| Construction | Factor counts, word lengths, country allocations, classifier-audit counts and versions | Several reporting discrepancies, detailed above. This is not a new substantive human validation of prompts. |
| Reasoning | Loader exclusions, nobs, saved coefficient interpretation, BH-family reconstruction | 18,401 valid rows agree with fitted nobs; exclusion prose and correction-family descriptions need changes. |
| Language simulations/weights | Saved-draw p/q reconstruction, conditional simulation precision, request/token tables | Main arithmetic reproduces; borderline range q and language-specific weighting robustness require qualification. |

The continuation tests preserve the manuscript's selected-model t-test convention. Models are not an independently sampled population of all LLMs, and the two geopolitical dyads within a prompt can be dependent. The unsigned-bias correction currently treats discordant dyad instances as independent binomial signs; a prompt-block null that swaps both dyads together is an additional worthwhile sensitivity. No such new null simulation was run here. The direct comparisons above should therefore be read as targeted support under the existing estimator, not a resolution of every inferential assumption.

## Additional interpretation points

- The raw excess calculation is correct, but SE, DE, and PG are different scenarios. Excess above their rate sum is a descriptive comparison across constructed prompt sets; it does not by itself identify a within-scenario interaction or the mechanism causing it.
- “No detectable effect” is preferable to “the bias is the same” or “does not predict” when evidence is a nonsignificant test. Developer-country and capability comparisons also involve a selected panel with multiple models from the same developer.
- Odds ratios put effects on a useful scale, but do not universally remove baseline-rate dependence or make marginal and conditional effects interchangeable. Keep GLMM and usage-weighted marginal ORs explicitly distinguished.
- The human gold is English-only, has 60 items, was stratified on an earlier judge's verdict, and was used to select among candidates. Candidate performance on that same set is selection-set performance. The appendix should state its limited generalization to controls, other languages, identity manipulations, and the production serving endpoint.

## Recommended order of work

1. Correct judge attribution, endpoint exceptions, truncation history, design and construction-audit counts, reasoning exclusions, the Figure 4D test label, and estimator wording. Align the reasoning correction families with the intended procedure. These need no additional model calls.
2. Incorporate the new direct unsigned-nationality specificity tests and AI provider-exclusion sensitivity with their stated scope. Resolve the remaining exact cross-judge headline estimands, capability influence checks, and language provider sensitivity. Narrow the token-weighting robustness claim.
3. Refit selected GLMMs for numerical and random-effects sensitivity; increase the borderline language-range simulation budget; document the uncertainty target and repeatability limitation.
4. Regenerate tables/figures after any changed analyses, rebuild the PDF, and verify the revised abstract/body/appendix together.

## Verification limits and execution record

The checks used the repository `.venv/bin/python` with NumPy, pandas, SciPy, and Matplotlib. Table generators were executed with their `OUT` assignment redirected in memory to `/tmp/powerbench-v21-audit/tables`; their source files and committed tables were untouched. BH was independently recomputed with SciPy's `false_discovery_control`. Raw English rates were recomputed after `load_d1_english()` validated coverage, coordinates, and official-judge overlay precedence. The excess t test was independently recomputed with SciPy. Bootstrap p values were independently reconstructed from saved draws rather than by calling the original scoring function.

The continuation also ran all three canonical loaders, checked every saved key and 13 analysis fields, independently reconstructed reciprocal D2 and human–AI discordance counts, recomputed the new paired-model sensitivities, and reconstructed human majority labels and candidate agreement from the original ratings and cached predictions. Loader agreement is not independent verification of the loader's entire selection policy: the two representations can share a systematic error. The per-model count reconstruction provides an additional independent aggregation check.

To rerun the continuation from the repository root:

```sh
.venv/bin/python paper/iclr2027/audits/verify_v21_extended.py
```

It writes only audit evidence beside this report and temporary plotting-library caches; it does not run model calls, graders, R fitting, or production table/figure writers. The report prose itself is not automatically regenerated.

Not executed: full R refits, regeneration of all permutations/bootstrap draws, new API calls, new human-label collection, independent semantic review of every response/translation/prompt, full external verification of geopolitical source data, citation-by-citation verification, or PDF rendering. R availability is the environment limitation preventing the recommended refits; it does not prevent correcting the confirmed reporting discrepancies. The remaining work is stated explicitly rather than treating saved-model arithmetic as a fresh fit.
