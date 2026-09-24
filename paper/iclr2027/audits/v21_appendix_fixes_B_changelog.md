# v21 section-B fixes: changelog for `v21_appendix_fixes_B.patch`

2026-09-24. This patch applies section B (rows B1–B17) of `v21_appendix_MASTER.md` to the v21 manuscript. It was built on a
scratch copy of `paper/iclr2027/submission/`. Nothing in `submission/` was modified; the patch and this file are the only
files written to the repository. No API, model or judge calls were made.

- **Apply:** from the repository root, `git apply paper/iclr2027/audits/v21_appendix_fixes_B.patch`
  (`git apply --check` passes against the current working tree). It changes 8 files: `make_tables.py`,
  `tables/ai_scale_levels.tex` and six files in `sections/` (appendix, discussion, introduction, methods, related, results).
  `main.pdf` is not in the patch; recompile after applying.
- **Section A** was not applied. Where a B fix shares a sentence with an A item, only the B part was changed (see
  "Choices" below).
- **Line numbers** in the table are v21 line numbers, before the patch. Each paragraph of the `.tex` sources is one line,
  so several rows can share a line.
- **Sources:** S = `v21_appendix_recheck_stats.md`, D = `v21_appendix_recheck_data.md`, M = `v21_appendix_methods_audit.md`,
  R = `v21_appendix_results_audit.md`, Report = a separate literature check of the cited works (not in the repository).
  "M34-Bn" is row Bn of the table in M §3, the pending related-work characterizations of `bibliography/AUDIT_SUMMARY.md` §B.

## 1. Changes

### Main text (rows 1–13; two of them add a line, see §5)

| # | B row | file:line | What changed | Source |
|---|---|---|---|---|
| 1 | B3 | methods.tex:10 | "every factor and every pair of factors is balanced" → "... every pair of factors involving the power domain is balanced (the other pairs approximately)" | D §10 |
| 2 | B3 | methods.tex:10 | "768 requests of 80 to 115 words" → "of 76 to 117 words" (actual range) | D §10 |
| 3 | B2 | methods.tex:25 | "capped at 5,000 output tokens (Appendix…)" → "(214 post hoc; Appendix…)" | D §6 |
| 4 | B11 | methods.tex:30 | Cross-judge sentence scoped: "in every language on five models' power-shifting responses, where 71 of 75 \pg{} contrasts with base English keep their sign"; drops "the contrasts on which our biases rest" | S #4, M18 |
| 5 | B10 | methods.tex:35 | "test every claim with the model as a random effect" → "test most claims …" (the per-family population is stated in the appendix, row 55) | S #9 |
| 6 | B16 | results.tex:7 | Excess reference `app:results` → `app:baseline` | R #27 |
| 7 | B16 | results.tex:27 | "at most 1.7 pp in the geopolitical pairings" → "in the pooled geopolitical set (2.5 in the ally pairing alone)" | R #20 |
| 8 | B16 | results.tex:53 | "almost every context and domain" → "most contexts and domains" | R #26 |
| 9 | B7 | results.tex:67 | Fig. 4D test "permutation test" → "bootstrap over prompts" | S #5 |
| 10 | B15 | introduction.tex:10 | AI-agent version: "and, outside the health domain, in a version in which …" | M31 |
| 11 | B17 | related.tex:4 | "can bypass refusal" → "can bypass some models' refusal" (model-specific; see §3 for the citations not added) | Report #15 |
| 12 | B17 | related.tex:4 | "an evaluation that \citet{davidson2025coups} call for" → "in the spirit of \citet{davidson2025coups}" | Report #5 |
| 13 | B11 | discussion.tex:12 | "agreement with an independent judge is as high …" → "… independent judge on five models is as high …" | S #4 |

### Appendix: extended methods

| # | B row | file:line | What changed | Source |
|---|---|---|---|---|
| 14 | B15 | appendix.tex:6 | "the definitions exactly as the writers … received them" → "the definitions the writers … received, in the terminology of this paper" | M21 |
| 15 | B15 | appendix.tex:19 | "never one member power standing in for it" → "never one member standing in for it" | M19 |
| 16 | B15 | appendix.tex:23 | Vocabulary list: "power standing" → "social standing" | M20 |
| 17 | B3 | appendix.tex:30 | Balance restated: exact on one-way marginals and on pairs involving domain or request type; context × scale and context × standing 21–27 (24), scale × standing 63–66 (64) | D §10 |
| 18 | B3 | appendix.tex:40 | "is orthogonal to scale" → "varies independently of scale" | D §10 |
| 19 | B3 | appendix.tex:44 | "Requests are 80 to 115 words (mean 95.6)" → written to be 80–115; range 76–117, mean 95.6, 8 of 576 outside | D §10 |
| 20 | B3 | appendix.tex:55 | "Deterministic checks afterwards found no row outside 80--115 words" → "checks of the rewritten requests found none outside …" | D §10 |
| 21 | B4 | appendix.tex:55 | Realism: 37/20/2% → pre-rewrite 26% (44 of 168) \pg, 11% (18) \de, 1% (1) \he | D §11c |
| 22 | B15 | appendix.tex:64 | "The control requests was" → "were" | M22 |
| 23 | B13 | appendix.tex:67 | Table `tab:translation` caption: two verifier passes with different models, Swahili repairs 130/288 vs 25/288, repair counts not comparable; 28 rows hand-corrected (16 hi, 11 sw, 1 pt) | M5 |
| 24 | B15 | appendix.tex:98 | Dominica and Samoa: demonyms shared with the Dominican Republic and American Samoa (a territory) | M23 |
| 25 | B5 | appendix.tex:100 | "equally often" → counts within one of each other; 27–28 per country overall, 9–10 per request type; control 9–10 and 1–2 per trigger family; 101 distinct control pairs | D §12 |
| 26 | B15 | appendix.tex:131 | "the final ask unchanged" → "unchanged except in nine requests, where its wording changed" | M24 |
| 27 | B3 | appendix.tex:139 | Control balance added: pairs with the trigger family exact; context × scale and context × standing 7–9 (8); scale × standing 21–22 | D §10 |
| 28 | B15 | appendix.tex:142 | Table `tab:triggers` caption: the domain–trigger pairing is alphabetical, fixes the design balance, and carries no meaning | M28 |
| 29 | B14 | appendix.tex:167 | Added: for six models the ranked endpoint was replaced by a declared one, in three cases because it did not serve reasoning, was rate-limited, or was unreachable from the account | M12 |
| 30 | B14 | appendix.tex:184 | "quantization fixed" → "fixed where the provider declares it"; rows record output tokens, from which truncation is determined (no per-row truncation flag) | M13, M16 |
| 31 | B14 | appendix.tex:184 | "re-sent up to three times" → "sent up to three times in all"; the 2% rule is a preflight projection that excludes an endpoint, not a post-run acceptance rule | M14, M15 |
| 32 | B2 | appendix.tex:184 | "almost all in Swahili" → 989 (45%) Swahili, 751 D2 (English), 240 Hindi; cap introduced mid-collection; 1,980 truncated at generation vs 214 (176 D1, 21 D2, 17 D3) cut post hoc to 5,000/t of characters and re-judged; one row excluded | D §6, M9 |
| 33 | B2 | appendix.tex:187 | "English (91% against 14%)" → "Among power-shifting requests, … English (59% against 14%, on 17 truncated responses)"; Swahili and Chinese figures kept (they are the power-shifting values); "far more often" → "more often" | M10; MASTER reconciliation |
| 34 | B2 | appendix.tex:190 | Table `tab:truncation` caption: "during generation or by the later cut" | D §6 |
| 35 | B2 | appendix.tex:199 | Table `tab:truncation-model` caption: same addition | D §6 |
| 36 | B11 | appendix.tex:211 | "agreement with an independent judge over the full data, which bounds …" → "… on the power-shifting responses of five models." | M18, S #4 |
| 37 | B14 | appendix.tex:224 | Judge call: "low reasoning effort" → "reasoning on (the endpoint accepts a low effort setting but does not honor effort levels)" | M17 |
| 38 | B1 | appendix.tex:226 | Gold balanced on gpt-5.4-nano's verdicts (the judge in use when the sample was drawn), soft quota of its harmful verdicts; "six models … (five of them in the final panel)" | D §1 (1a), M4 |
| 39 | B1 | appendix.tex:226 | "balanced on the judge's verdict" → "balanced on gpt-5.4-nano's verdict" | D §1 (1a), M4 |
| 40 | B1 | appendix.tex:226 | Per-type refusal agreement 90/85/85 (nano's) → 85/85/90 (adopted judge, candidate run) | D §1 (1b-i) |
| 41 | B1 | appendix.tex:226 | Harmfulness: 0.47 [0.04; 0.78] (nano's) → adopted judge flagged none of the 60 (κ 0.00; agreement 90%, sens. 0%, spec. 100%; 6 human positives), "so its harmfulness verdict is not validated" | D §1 (1c) |
| 42 | B1 | appendix.tex:228 | Added: in the candidate comparison deepseek-v4-flash-0731 was unpinned, served by nine providers, none the bf16 production endpoint; nano's verdicts are the stored inline ones | D §1, M3 |
| 43 | B11 | appendix.tex:252 | Heading "Agreement with an independent judge on the full data." → "Agreement with an independent judge." | M18 |
| 44 | B11 | appendix.tex:252 | Scope: power-shifting responses only; control and the four conditions without the US or China graded by the adopted judge only | S #4 |
| 45 | B11 | appendix.tex:252 | "those differences hold under either judge" removed; added that the 75 contrasts are not the paper's estimands and that two-judge agreement does not exclude shared errors | S #4 |
| 46 | B11 | appendix.tex:255 | Table `tab:judge-agreement` caption: power-shifting responses; refusal rate over the three power-shifting types (not four) | S #4, M18 |
| 47 | B15 | appendix.tex:274 | Reasoning levels: "first two offered" → "first two … above minimal"; qwen3.8-27b labelled CN; ON-arm output budget 65,536 (20,000 for gemini-3.1-flash-lite) | M25 |
| 48 | B6 | appendix.tex:274 | Exclusions: 26 + 9 → 29 glm-5.2 rows (19 PS + 9 control at extra-high, 1 PS at high) + 1 gpt-5.6-terra + 1 gemini-3.1-flash-lite control row; 18,401 of 18,432 enter the model | D §14 |
| 49 | B9 | appendix.tex:302 | Table `tab:tests`, Fig. 3C: "bootstrap" → "$t$ test" | S incidental 1, M8 |
| 50 | B7 | appendix.tex:308 | Table `tab:tests`, Fig. 4D: "permutation test" → observed over chance range; pivotal bootstrap over prompts, $p$ by inversion | S #5 |
| 51 | B8 | appendix.tex:316 | "Laplace approximation replaced by the penalized quasi-likelihood starting fit (nAGQ = 0)" → nAGQ = 0 per lme4 docs (fixed and random effects in the PIRLS step, variance parameters on the Laplace approximation) | S #7 |
| 52 | B8 | appendix.tex:316 | Singular-fit list completed from the saved `singular` flags (see §2) | S #7, M11 |
| 53 | B15 | appendix.tex:321 | Fig. 4A formula: language fits have no type term, one fit per request type | M27 |
| 54 | B15 | appendix.tex:328 | "which matters only in \he" → excludes one model in \he{} (Fig. 3B) and in \de{} of the neutral pairing (Fig. 2B), and several models in the per-level tests (Figs. 3C–E) | M26 (+ R25 evidence) |
| 55 | B7, B10 | appendix.tex:332 | $p$ by interval inversion also for the language range; added which analyses hold the 24 models fixed (usage-weighted Figs. 2D, A3B, A4B; Fig. 4D; per-model tests of Fig. 4E; Fig. 4F inset; spread test) and that Fig. A2 factor cells use fixed model effects with model-clustered SEs | S #5, S #9 |
| 56 | B12 | appendix.tex:334 | "changes no conclusion" → what token weighting changes: AI-agent and Fig. 2D geopolitical set unchanged; US–China \pg{} passes (q 0.022 vs 0.12); \pg{} language results unchanged; pooled-PS French q 0.35, German q 0.007; some \he{}/control languages differ; Fig. 4D not recomputed | S #15 |

### Appendix: extended related work (B17)

| # | B row | file:line | What changed | Source |
|---|---|---|---|---|
| 57 | B17 | appendix.tex:348 | SORRY-Bench: "organized into 44 categories and 20 linguistic variations" → "in 44 categories, rewrote each in 20 linguistic variations" | M34-B1 |
| 58 | B15, B17 | appendix.tex:348 | "This is the convention behind our 'significant help' threshold" (StrongREJECT) → the threshold follows SORRY-Bench's definition of fulfilment | M29, M34-B6 |
| 59 | B17 | appendix.tex:348 | XSTest/OR-Bench: "over-refusal separates models as much as refusal does" → models differ widely in over-refusal; those refusing more harmful requests refuse more safe ones | M34-B2 |
| 60 | B17 | appendix.tex:348 | Rao et al.: report raw agreement with κ and error rates (not κ "over" raw agreement); we report κ with raw agreement, sensitivity, specificity | M34-B3 |
| 61 | B17 | appendix.tex:350 | Yong 2023: tested GPT-4 | M34-B4 |
| 62 | B17 | appendix.tex:350 | Deng: unintentional and intentional multilingual jailbreaks | M34-B5 |
| 63 | B17 | appendix.tex:350 | Oppong: hidden states of four open models, four African languages, not routed to the refusal mechanism | M34-B7 |
| 64 | B17 | appendix.tex:350 | Marx: multi-turn jailbreaks, varies across commercial models from different developers | M34-B8 |
| 65 | B17 | appendix.tex:352 | Pan & Xu: non-circular wording (China-developed models refuse China-sensitive questions far more often) | M34-B9 |
| 66 | B17 | appendix.tex:352 | Bladon: "found it amplified by" → "the language of the prompt can amplify it" | M34-B10 |
| 67 | B17 | appendix.tex:352 | Williams: refusing models do so unevenly by political perspective and target (not "beneficiaries") | M34-B11 |
| 68 | B17 | appendix.tex:354 | Turner: "in most environments" → "in many environments (e.g., shutdown), … for most reward functions" | M34-B13 |
| 69 | B17 | appendix.tex:354 | MACHIAVELLI measures power-seeking, not power "accumulated" | M34-B14 |
| 70 | B17 | appendix.tex:354 | Davidson: "seize and entrench power" → "seize power" | Report #4, M34-B15 |
| 71 | B17 | appendix.tex:356 | El Yagoubi: "an interlocutor that presents as" → "the recipient … is described as" an AI agent | M34-B16 |
| 72 | B17 | appendix.tex:356 | "In all of these, the agent acts." → "In these three benchmarks, the agent acts." | M34-B17 |

### Appendix: additional results, and the generated table

| # | B row | file:line | What changed | Source |
|---|---|---|---|---|
| 73 | B16 | appendix.tex:363 | "estimate, interval, and adjusted $p$ behind every mark" → intervals except in Fig. 2E; for Figs. 3D–E the number of marked cells | R #23 |
| 74 | B16 | appendix.tex:373 | Table `tab:est-fig1` caption: first block is BH over the two request-type contrasts | R #24 |
| 75 | B16 | appendix.tex:417 | Context × (PS vs control): smallest q 0.77 (omnibus p 0.70) for pooled PS; 0.30 is per type against the control | R #12 |
| 76 | B16 | appendix.tex:435 | "with no difference between DCs" removed (no test exists) | R #7 |
| 77 | B1 | appendix.tex:435 | "harmfulness verdict agrees with human labels at κ=0.47" (nano's) → the judge's κ is 0.00; it marked none of the six human-positive responses | D §1, M4 |
| 78 | B1, B16 | appendix.tex:438 | Table `tab:harm` caption: "Responses flagged as harmful by the judge …, mean over models with …" | D §1, R #7 |
| 79 | B16 | appendix.tex:462 | Ally pairing \de: GLMM "q=0.001" → "q<0.001" (0.00098); usage-weighted "q<0.001" (permutation) → "q=0.003" (bootstrap) | R #11, S incidental 2 |
| 80 | B16 | appendix.tex:467 | Fig. A2-by-pairing caption (A): "(23 in \de{} of the neutral pairing)" | R #25 |
| 81 | B16 | appendix.tex:467 | Same caption (C): stars from the same bootstrap | R #11 |
| 82 | B16 | appendix.tex:501 | Table `tab:est-fig3` caption: GLMM column of C is BH over 12 contrasts; F over pooled PS and control | R #6 |
| 83 | B16 | appendix.tex:518 | `\ref{fig:a3-scale-power standing}` → `fig:a3-scale-standing` | R #17, M19 |
| 84 | B16 | appendix.tex:518 | "refused in 11.9% of cases" + "(health domain excluded)" | R #10 |
| 85 | B16 | appendix.tex:518 | "Refusal of both requesters rises with scale" → "is higher with a society than with an individual" (AI \pg{} 22.3 → 21.7 → 45.2) | R #22 |
| 86 | B16 | appendix.tex:524 | `\label{fig:a3-scale-power standing}` → `fig:a3-scale-standing` | R #17 |
| 87 | B16 | appendix.tex:528 | Table `tab:ai-scale` caption: D3 pairs, health excluded, so human rates differ from Fig. 1D; $t$ intervals over models | R #10 |
| 88 | B16 | appendix.tex:550 | nova-2-lite English refusal "19%" → "18%" | R #18 |
| 89 | B16 | appendix.tex:550 | "keep all 24 models": the level ranges and per-model concordances use the 22 models | R #8 |
| 90 | B16 | appendix.tex:579 | "Averaged over models" → "Averaged over the 22 models of Figure 4" | R #8 |
| 91 | B12 | appendix.tex:579 | "no language differs from English in \he{} or the control" → "with request weights …(token weights: Appendix A.12)" | S #15 |
| 92 | B16 | appendix.tex:588 | "unrelated to their difference in web prevalence" → "shows no detectable relation to …" | R #19 |
| 93 | B16 | appendix.tex:606 | "On the eight means of the panel" → "of the 22 models" | R #8 |
| 94 | B6 | appendix.tex:620 | ORs 0.33/0.23 described as averages over types and DCs; per-type passes (level 1 only \de; level 2 \de, \pg, control); \de{} − control ratio 0.45; DC split (CN 0.16/0.11 pass, US 0.67/0.44 do not; test has little power); heterogeneity named (\pg{} −41 pp grok-4.3, ≤1 pp terra/inkling/gemini-flash-lite); "paired differences" → "differences in mean refusal", −12.2 → −12.1 | D §14, R #13, R #14 |
| 95 | B6 | appendix.tex:633 | Table `tab:ladder`: $\chi^2(2)$ → $\chi^2(2)=3.83$ | R #15 |
| 96 | B6 | appendix.tex:634 | Table `tab:ladder`: $\chi^2(6)$ → $\chi^2(6)=27.60$ | R #15 |
| 97 | B16 | appendix.tex:646 | Fig. A5 caption: bands are $t$ intervals over the models of each group (four per DC, eight for all) | R #16 |
| 98 | B16 | make_tables.py:182–190 | `ai_scale_levels` generator: the direction-bias column and its interval are read from block 59 `bias_direction_by_level.csv` (full precision) instead of the 3-decimal block 61 values, which were rounded twice | R #9 |
| 99 | B16 | tables/ai_scale_levels.tex:8, :11, :15 | Regenerated: DE individual bias 0.35 → **0.36**; PG individual lower bound 0.47 → **0.48**; CT group lower bound −0.04 → **−0.03**. The other 13 generated tables and every other cell are byte-identical | R #9 |

**How row 99 was produced:** a throwaway copy of the patched `make_tables.py` was run with `ROOT` pinned to the
repository (inputs are read-only) and `OUT` pinned to the scratch `tables/`. No file in the repository was written or
modified (checked with `git status`, including `__pycache__`). The patched `make_tables.py` itself keeps its original
`ROOT`/`OUT`, so running it from the repository writes to `submission/tables/` as before.

## 2. Choices made where a source offered options or where I checked the audits against saved outputs

- **B1.** Only the B part was applied. The candidate-run overall numbers (87%, κ 0.73 [0.55; 0.90], 89/84%) and methods:30
  are unchanged, pending A4. The per-type 85/85/90 figures are the candidate run's (D §1 option 1B-i), so they are
  consistent with the overall numbers. I did not add the production-endpoint numbers (88%, κ 0.77), which belong to A4
  decision 1. `tab:harm` is kept, with its caption attributing the flags to the judge. D §1 1d option A would add "The flag
  is not validated" to the caption; that belongs to A4 decision 2 and was not added. The body text at :226 and :435 states
  the κ 0.00 result. I omitted the optional sentence giving nano's κ = 0.47 (already in Table `tab:judges`) and the
  optional rewording of "No candidate reached a useful agreement on harmfulness".
- **B2.** For methods:25 I used "(214 post hoc; …)". D's draft is longer and the paragraph had room for about 14
  characters; the full description is at appendix :184. I omitted D's optional "19 of 213 verdicts changed" and M10's
  optional 22-model Swahili note.
- **B3.** methods:10 reads "76 to 117 words" rather than D's "about 80 to 115 words (76 to 117)", to fit the line. The
  control's balance went into the control section (:139) rather than the design paragraph (:30).
- **B6 (R #13 is marked HUMAN DECISION).** I took the least-change option: keep the printed values, which are differences
  in mean rates, relabel them as such, and correct −12.2 to −12.1. The alternative was strictly paired values (−12.3,
  −9.9). The saved q values are kept; the BH families are A7. I did not add the optional per-DC rows to `tab:ladder`.
- **B7.** I omitted the optional :328 precision ("100 within each bootstrap replicate") and the Monte Carlo caveat on
  q = 0.047.
- **B8.** I built the singular-fit list from the saved `singular` column of blocks 31, 32, 45, 46, 58, 60, 64, 85 and 86,
  because S and M disagree:
  - Side model: all four neutral-pairing types are singular (S is right; M lists only SE and DE), and so is the pooled
    neutral fit (block 86).
  - Direction model: only the US joint control fit is singular, plus 11 of 32 by-counterpart fits (control 5, PG 3,
    SE 2, DE 1).
  - **Added, not in either audit:** the context × (PS vs control) interaction fits for \he{} and \pg{} are also singular
    (block 32, `glmm_context_interaction_omnibus.csv`).
- **B10.** The main-text change is only "every claim" → "most claims", which adds no length. The per-family statement of
  the inferential population is in the Resampling paragraph (:332), which Methods already points to ("Appendix A.12
  gives every formula, family …"). The retest disclosure (S #9) is A9 and was not applied.
- **B11.** Short forms were used in the main text: methods:30 as in row 4, and discussion:12 "on five models", shorter
  than S's optional draft. Appendix :211 uses M18's shorter wording.
- **B12.** Request weights are kept as primary, as in S's draft. results:69, discussion:4 and intro:14 are A8 and were
  not changed.
- **B14 (M12).** "one endpoint per model for the whole study" is left as is (A5). M12's draft states reasons for all six
  overrides. I checked `2_run_targets/provider_pins.json` and `common/models_panel.py`: reasons are documented for
  three of them (kimi-k3: DeepInfra served no reasoning; kimi-k2.6: rate limit; deepseek-v4-pro: first-party endpoint
  unreachable under the account's data policy). minimax-m3, gpt-5.6-luna and nova-2-lite are declared choices of a
  first-party or global endpoint. The text therefore says "in three cases because …".
- **B15.**
  - M24: M's draft says "minimal wording". The audit itself found 1 to 9 of the last 12 words changed, so I wrote "except
    in nine requests, where its wording changed".
  - M26: extended with the Fig. 2B neutral \de{} case (23 models), using M26's and R #25's own evidence.
- **B16.**
  - R #7: the caption's "mean over models" was checked against block 25's README (equal weight per model).
  - R #19 (HUMAN DECISION on also reporting the descriptive web-text association): least change, reworded only.
  - R #26 (HUMAN DECISION): R's draft applied; it shortens the text.
  - R #23: instead of "with its interval where one is plotted", the new text names the panel with no interval in its table
    (Fig. 2E).
  - R #16 is included. The MASTER summary does not name it, but it falls in B16's source range R6–R27. R #21 is excluded
    because it is A12.
- **B17.**
  - The Davidson clause uses the short form "in the spirit of \citet{davidson2025coups}". The report's longer form ("in the
    spirit of the testing for coup assistance that they call for") would have cost a main-text line.
  - The translation clause was hedged to "can bypass some models' refusal" (see §3).

## 3. B items not applied, and why

1. **M34-B12, Blodgett "distributes a resource unevenly" (appendix :352).** M marks it HUMAN DECISION: the next sentence
   relies on "uneven", so either the definition becomes Blodgett's ("allocates … unfairly across social groups") or
   "unevenly" stays and the definition is the authors'. Least-change option taken: **not changed**.
2. **B17, translation and refusal (related.tex:4): citations not added.** The Report's fix (#15) says the low-resource
   gap has largely closed for 2025–26 frontier models and that its sign varies by model. Both parts rest on citations
   that are **not in refs.bib**:
   - Lee et al. 2026, "ROK-FORTRESS: Measuring the Effect of Geopolitical Transcreation for National Security and Public
     Safety", arXiv:2605.14152 (not yet in refs.bib).
   - Zhang, Patel, Truong & Koyejo 2026, COLM 2026, arXiv:2605.17173.

   Only the model-specific hedge was applied. `marx2026multilingual`, which is in refs.bib, reports that simple
   translation no longer bypasses safety in 2024–25 commercial models (`AUDIT_SUMMARY.md` §B). It could support "less
   so in recent models", but that would cost about one more main-text line, so it was not added.
3. **discussion.tex:12, "reasoning lowers refusal on power-shifting and control requests alike".** D §14 drafts a fix
   ("on average, in power-shifting and control requests"). MASTER B6 lists only appendix :274, :620 and `tab:ladder`, so
   it was not applied. It now disagrees in emphasis with the corrected appendix :620.
4. **Out of B17's scope, left for the authors:**
   - The body related-work items still pending in `bibliography/PENDIENTES_v20.md` §1: Kulveit for "seize or concentrate
     power", Durmus next to Li for "depending on the prompt's language", Khorramrouz under "the identity of the user", and
     Haslett under "Geopolitical biases". B17 covers only related:4's Davidson and translation clauses.
   - The appendix item "Common Crawl shares are of web pages, not web text" (appendix :588, :593). It is not in M34 or
     any B row.
5. **Code and documentation outside the manuscript (not in the patch):**
   - Hardcoded "Laplace (nAGQ = 1)" in `4_analysis/analysis_30`–`33_*.py` READMEs and in the headers of
     `r/glmm_factor.R` and `r/glmm_origin.R` (S #7).
   - The `figA_judges.py` docstring says the five models were graded "in full" by both judges; only their power-shifting
     responses were (S #4).
   - The BH-family regex in `analysis_68_reasoning_glmm.py:120` is A7.

## 4. Needs figure regeneration (not run)

- **Fig. A2 by pairing (`figures/figA2_by_pairing.pdf`), row C stars.** Change
  `4_analysis/paper_figures/appendix/appendix_figures.py:214` from
  ```python
  for i, (T, est, lo, hi, qc) in ((1, (B, "OR", "OR_lo", "OR_hi", "q_bh")), (2, (C, "odds_ratio", "boot_lo", "boot_hi", "perm_q"))):
  ```
  to
  ```python
  for i, (T, est, lo, hi, qc) in ((1, (B, "OR", "OR_lo", "OR_hi", "q_bh")), (2, (C, "odds_ratio", "boot_lo", "boot_hi", "boot_q"))):
  ```
  R #11 cites line 218; the code is at line 214. I checked this against
  `4_analysis/results/75_fig3_dyads_separate/pC_requests_by_dyad.csv`: no row changes classification at q < .05 between
  `perm_q` and `boot_q`, so the regenerated figure should show the same stars. The caption change (row 81) is already in
  the patch.

No other B item needs a figure rerun. R #16 (Fig. A5) is caption-only. The token-weighted Fig. 4D is a new analysis
(section C of MASTER).

## 5. Compile and page-count results

The compile command in the `main.tex` header sets only `TEXINPUTS`, so bibtex cannot find `iclr2027_conference.bst`.
Both builds therefore also set `BSTINPUTS` to the same style folder. Both builds also need a fourth `pdflatex` pass to
clear "Label(s) may have changed"; after it, neither log has that warning.

| | v21 (before) | with patch (after) |
|---|---|---|
| Pages | 50 | 50 |
| LaTeX errors | 0 | 0 |
| Undefined references / citations | 0 / 0 | 0 / 0 |
| bibtex warnings | 0 | 0 |
| Overfull boxes | 0 | 0 |
| Underfull \hbox | 32 | 32 (no new ones) |
| Underfull \vbox (page glue stretched) | 3 (pp. 5, 6, 19) | 7 (pp. 3, 5 at badness 10000, 7, 8, 9, 19, 26) |
| Main text ends on page | 9 (Conclusion's last line at the bottom of p. 9; page 9 had no free lines) | **10** (the 6-line Conclusion paragraph moves to the top of p. 10) |
| References begin on page | 10 | 10 |

**Main-text overflow: 2 lines.**

- **Where the lines come from.** Counting body lines from page 1 to the end of the Conclusion gives 364 before and 366
  after. Every other main-text edit was fitted into the free space on its paragraph's last line. The two added lines are:
  - row 10, intro:10, "outside the health domain" (M31). The bullet had about 3 characters of room; the shorter
    "except in health" was tested and also costs the line.
  - row 13, discussion:12, "on five models" (B11). The paragraph had about 9 characters of room.
- **Tested.** Reverting both restores the Conclusion to page 9. Reverting either one alone does not. The new \vbox
  warnings are the same effect: the moved page breaks leave stretched glue on those pages.
- **Why 2 lines move a 6-line paragraph.** Page 9 had zero slack. The extra lines push the "2.4 Statistical analysis"
  heading from the bottom of page 3 to page 4, and the "Related work" heading from page 8 to page 9, so the whole
  Conclusion is set on page 10.

No content was cut to fit. Reverting rows 10 and 13 is enough to recover 9 pages; so is saving 2 lines elsewhere in the
main text.
