# Brief: add an OpenRouter batch path for the Anthropic targets

*Written 2026-09-08. Hand this whole file to the instance doing the work. Everything below was
measured against the live API on that date; re-check anything you are about to rely on, because
provider line-ups and prices move.*

---

## 0. Scope, in one line, because it is easy to get wrong

**You are adapting the runner that produces the PowerBench experiment itself** —
`2_run_targets/run_targets_pinned.py`, the script that runs D1 / D2 / D3 and the control banks
against the target models and grades every answer with the judge. That is the run this is meant to
make cheaper.

**You are NOT adapting the capability probe.** `run_capability_probe.py` is a small
multiple-choice eval used to rank models before committing to a run; it is already finished and
cost about $23 in total. It appears in this brief only as a **cheap place to smoke-test your batch
transport**, because it shares the same engine and has no judge. Do not deliver "batch works on
the probe" and stop.

**There is a second deliverable in §4c**, added 2026-09-08: the panel does not run one programme
but three configurations, with different banks and different reasoning arms per group of models,
and nothing in the code expresses that today. It is not part of the batch transport, but it lands
on the same runner and the same confirmation gate. Read §4c before designing §4's restructuring, so
the two fit together instead of colliding.

## 0b. Which document wins

`notebooks/PowerBench.md` is the dated lab notebook and **the authoritative record of this
project**, verified by the researchers. If any other `.md` in the repo — this brief, `CLAUDE.md`,
`README.md`, `PLAN.md`, `draft.md`, anything — contradicts it, **the notebook is right and the
other file is stale**. Read the notebook's recent entries before you start, and when you find a
contradiction, say so rather than silently picking one.

## 0c. Read these first, in this order

1. `notebooks/PowerBench.md` — the lab notebook. Most recent entries first. This is the ground
   truth (see §0b).
2. `CLAUDE.md` — the top notice describes the current project; **section 6b** is the operating
   manual for the panel, the pins and the runners. Sections 1–4 and 7–9 are the frozen hackathon
   study and do not describe what you are working on.
3. `common/models_panel.py` — the model registry. Its docstring opens with a section addressed to
   AI agents about spending money. Read that section before you run anything.
4. `2_run_targets/run_targets_pinned.py` — **the runner you are extending.**
5. `VERSIONS.md` — which banks and runs are current, which are provenance.
6. `2_run_targets/run_capability_probe.py` — same engine, no judge. Your smoke-test venue only.

## 1. What this project is, in one paragraph

PowerBench measures how readily LLMs assist with **power-grabbing** — a first-person advisory
request that increases the user's power and reduces another party's, by means that are not
illegal — and how that varies with language, the user's prior standing, the nationalities in the
prompt, and whether the narrator is an AI agent. Each row is one prompt to one target model, whose
answer is then graded by a fixed **judge** model into refuse / not-refuse. The scientific claim
rests on comparing models, so **anything that changes serving conditions between rows of the same
model is a confound**, not a detail.

## 1b. What the run you are adapting actually looks like

Per row, `run_targets_pinned.py` makes **two** paid calls: the **target** answers a prompt, then
the **judge** grades that answer. Your batch path has to deal with both, and they are not
symmetric — see §3 for why only the target side should be batched.

The banks, per model (see `CLAUDE.md` and `VERSIONS.md` for the exact filenames and the current
versions):

| bank | rows per model |
|---|---:|
| D1 English | 576 |
| D1, the other 7 languages | 576 × 7 |
| D2 geobloc (**17** nationality conditions × 576 — see §1c) | **9,792** |
| D3, AI-agent narrator | 504 |
| control D1, 8 languages | 192 × 8 |
| control D2 geobloc (**17** × 192) | **3,264** |
| control D3 | 192 |
| **total, full programme** | **19,896** |

So a model on the full programme is tens of thousands of target calls, not hundreds. That is the
scale that makes a 50% discount worth engineering for, and it is also why an un-collected batch is
a serious loss rather than an annoyance.

Note what this means for batch sizing and for the 24-hour collection window: a single bank does not
fit the mental model of "one small job". Decide early whether one batch is one bank, one language,
or a fixed chunk size, and write the reason down.

## 1c. D2 is growing from 14 conditions to 17, and three of them are a back-fill

**Decided 2026-09-08, not yet built.** D2's 14 conditions are all directed dyads and every one of
them has the US or China on one side (`us_ally`/`ally_us`, `us_rival`/`rival_us`,
`us_neutral`/`neutral_us`, `cn_ally`/`ally_cn`, `cn_rival`/`rival_cn`, `cn_neutral`/`neutral_cn`,
`us_cn`/`cn_us`). There are three country pools behind them: **A** = US allies / China rivals,
**B** = China allies / US rivals, **N** = neutrals. Because no condition omits both superpowers,
the design cannot currently separate "the model defers to superpowers" from "the model tracks the
alliance axis". Three conditions are being added to fix that:

| new condition | dyad | why |
|---|---|---|
| `usally_cnally` | A → B | the alliance contrast with **both** superpowers removed |
| `cnally_usally` | B → A | the other direction: A→B ≠ B→A in bloc terms |
| `neutral_neutral` | N → N | same pool on both sides, so direction carries no bloc information — one condition is enough. This is the floor: a gap here means the effect is not about blocs at all |

Per model that is **+1,728 rows in D2** (3 × 576) and **+576 in control D2** (3 × 192) —
**+2,304**, taking the full programme from 17,592 to 19,896 rows.

**Three things this changes for you:**

1. **The banks do not exist yet.** They are rendered by
   `1_create_dataset/build/render_dyads_geobloc.py` from the same 21-country pools, and the control
   side by the same path that produced `dataset2_control_dyads_geobloc.v1.1.jsonl`. That work is a
   **prerequisite outside this task** — do not start batching D2 assuming the 17-condition bank is
   on disk. Check `VERSIONS.md` and the notebook for whether it has landed.

2. **For the six already-run models this is a back-fill, and the resume handles it for free.** D2
   row ids are `<pair_id>-<condition>` (`p2s-000-r1-us_ally`) and are unique — 8,064 distinct ids
   for 8,064 rows, verified 2026-09-08. The three new conditions produce ids that have never been
   seen, so pointing the runner at the 17-condition bank with the **same output file** as the
   original run issues only the 2,304 new rows and skips the 8,064 existing ones. This only works
   if you keep the same `--out`; writing to a new file throws the resume away and re-runs
   everything. Say which you did in the `.meta.json`.

3. **Sizing.** D2 is now 9,792 of the 19,896 rows in a full programme — **49%**, and the single
   most expensive thing to get wrong. §8 already tells you to prove `--batch` on D3 (504) or
   control D3 (192) first; the growth of D2 makes that advice stronger, not weaker.

## 2. The single most important constraint

Every target call is made under conditions we have fixed and verified, and the verification is
per row:

- a **pinned endpoint**, by full tag (`anthropic`, `openai/flex`, `baseten/fp8`), with
  `allow_fallbacks: false` — see `2_run_targets/provider_pins.json`;
- `temperature: 0` where the endpoint accepts the parameter;
- a **reasoning arm** — `off` (reasoning disabled, and `usage.completion_tokens_details.
  reasoning_tokens` must come back ≤ 1) or `floor` / `on` (run at the model's minimum declared
  effort). **A row that fails its arm's check is re-sent, up to `--max-attempts` (3).**

That last line is the whole difficulty of this task. Read section 4.

Also non-negotiable: `CANARY.md`. These prompts must never enter a training corpus. Any tier or
endpoint whose discount is paid for with our data — Meta's `-contributor` models are the known
example — is forbidden regardless of price.

## 3. What was measured about batch on 2026-09-08

All four Anthropic models in the panel have a `:batch` variant at **exactly half price**, served
by the **first-party `anthropic` endpoint**:

| model | sync pin today | sync $/M in-out | `:batch` endpoint | batch $/M in-out |
|---|---|---|---|---|
| `anthropic/claude-haiku-4.5` | `anthropic` | 1.00 / 5.00 | `anthropic` (1 ep) | **0.50 / 2.50** |
| `anthropic/claude-sonnet-5` | `anthropic` | 2.00 / 10.00 | `anthropic` (1 ep) | **1.00 / 5.00** |
| `anthropic/claude-opus-5` | `anthropic` | 5.00 / 25.00 | `anthropic` (1 ep) | **2.50 / 12.50** |
| `anthropic/claude-fable-5.1` | `anthropic` | 10.00 / 50.00 | `anthropic` (1 ep) | **5.00 / 25.00** |

**This is the good case, and it is why the task is worth doing.** A `:batch` model id has exactly
one endpoint, so `provider.only` cannot choose anything — normally that means batch forces a
serving-stack change. Here it does not: all four are already pinned to `anthropic`, and the batch
variant is served by `anthropic`. **Same lab, same endpoint, half the price.** Verify this is
still true before you rely on it (`GET /api/v1/models/<id>:batch/endpoints`).

Two things that are **not** in scope, and should stay that way:

- **Do not batch the judge.** `deepseek/deepseek-v4-flash-0731` is locked to `morph/bf16` in
  `common/judge_config.py`. Its `:batch` variant is served by `together` at $0.14/$0.28 — a
  different stack *and* more expensive than the cheapest sync endpoint. Batching it would change
  the grader mid-study to save nothing.
- **Do not batch the non-Anthropic targets.** OpenAI and Google already have a `flex` tier at the
  same 50% discount, synchronous, on the endpoint we already pin — `openai/flex`,
  `google-ai-studio/flex`. Anthropic is the only lab in the panel with no flex tier, which is
  exactly why it is the only one worth this work.

Batch mechanics, as of the last check: `POST /api/beta/batches`, results collected within a 24-hour
window, and a `:batch` model id returns **404 to a synchronous chat/completions call** — so you
cannot smoke-test one with a normal request, and there is no way to pre-audit a batch endpoint the
way `audit_provider_flags.py` audits a sync one. Confirm the current endpoint shape from
OpenRouter's own docs rather than from this paragraph.

## 4. The hard part: verification is per row and batch is asynchronous

The runner's inner loop is, in effect:

```python
while attempts < MAX_ATTEMPTS:
    txt, usage, provider = call(...)
    if txt.startswith("__ERROR__") or verified(arm, usage) or arm == "floor":
        break
```

`verified()` reads `reasoning_tokens` out of the response and decides whether the row is usable.
Under batch there is no response to inspect until the whole job returns, so this loop cannot exist
in its current form. **The adaptation is a restructuring, not a flag.**

The pattern to implement:

1. build the whole job (one request per row, each carrying a stable `custom_id` that encodes
   `(target, row id)` so results can be joined back);
2. submit; poll; collect;
3. **verify every returned row exactly as the sync path does**, using the same `verified()`;
4. **re-submit the failures as a second batch**, and repeat up to the same attempt budget;
5. write rows to the same JSONL as the sync runner, with the same schema, so the analysis layer
   cannot tell which path produced a row — except for one new provenance field (see §6).

Do not simplify by dropping the verification. It is the reason the data is trustworthy.

### 4a. Anthropic's current models cannot be made to think on every request

This was researched on 2026-09-08 against Anthropic's own documentation, and it changes what the
`reasoning` stratum means for this lab. **It is not a bug in this repo and not a provider fault.**

Anthropic has two thinking modes. The old one, *extended thinking*
(`thinking: {type: "enabled", budget_tokens: N}`), makes Claude think on **every** request. The new
one, *adaptive thinking*, lets the model decide. From
[the extended-thinking docs](https://platform.claude.com/docs/en/build-with-claude/extended-thinking):

> Expect a behavioral difference, not just a syntax change. With a fixed budget, Claude thinks on
> every request. **With adaptive thinking, Claude decides whether and how much to think on each
> request, and at lower effort settings it may skip thinking entirely on easy inputs.**

And the models that are adaptive-only, where `type: "enabled"` now returns a **400**:

> You are moving to Claude Opus 4.7, Claude Opus 4.8, **Claude Opus 5, Claude Sonnet 5, Claude
> Fable 5.1**, Claude Mythos 5.1, Claude Fable 5, or Claude Mythos 5.

All three of our Anthropic reasoning-capable targets are on that list. So:

- **There is no "always thinks, at minimum depth" condition available for opus-5, sonnet-5 or
  fable-5.1.** The fixed-budget mode that would produce it is rejected by the model.
- `mandatory: true` in OpenRouter's metadata means "you cannot send a disable flag", **not** "it
  always thinks". For Anthropic those two are no longer the same statement, and the panel's
  `reasoning` stratum quietly assumes they are.
- Our measurement matches the documentation exactly: at its floor effort, fable-5.1 emitted zero
  thinking tokens on **all 398** rows of the capability probe, and gpt-6-astra, glm-5.3 and
  glm-5.3-flash skip thinking more often on items that other models found easy (ρ = −0.55, −0.39,
  −0.40). Documented behaviour, reproduced.

Raise this with the user before batching anything Anthropic. It is a design question about what
the reasoning stratum can claim, and it is bigger than the transport change you were asked for.

### 4b. What that means for the batch job itself

`claude-fable-5.1` returned **zero API-level reasoning tokens on all 398 rows** of the capability
probe at its floor effort — and it was not refusing to think. Its replies are ~158 characters of
worked algebra ending in the answer: it reasons **in the visible response text**, where
`reasoning_tokens` cannot see it. `claude-opus-5` does the same in the off arm, with explicit
`<thinking>` tags on 70 of 398 rows. Two Anthropic models out of two.

Consequence for you: **under the current `verified()`, every fable row fails, so every fable row
would be re-sent — three full batches for nothing, and the re-sends cannot succeed, because §4a
says the model is behaving as designed.** Batching fable is pointless until the
verification can recognise reasoning that arrives as text. Either:

- fix `verified()` first (there is a proposal in `4_analysis/reports/results_capability.html`
  §7e, and a length-based detector implemented in
  `4_analysis/reports/build_capability_report.py`) — but note the detector works there only
  because the expected answer is a single letter, and **does not transfer to the PowerBench banks,
  where the answer is prose**; or
- scope this task to haiku-4.5, sonnet-5 and opus-5, and say plainly that fable is excluded until
  the verification question is settled.

The second is the honest default. Do not quietly widen `verified()` to make a batch job succeed.

## 4c. A second deliverable: scope and arm are not uniform across the panel

This is **separate from the batch transport** and probably larger. It is listed here because it
touches the same runner and the same plan-and-confirm gate, and doing them blind of each other
will hurt.

### What the strata actually are

One operating principle covers the whole panel: **every model is asked for the least reasoning its
endpoint allows.** For some that floor is "off" and we can verify it held; for others the floor is
`low` or `minimal` and we cannot. That is the entire A/B distinction:

- **A — reasoning disabled, verified per row** from `reasoning_tokens`.
- **B — reasoning enabled at the model's floor**, not verifiable.

Say it that way and nothing else, because **what "the floor" means behaviourally differs per model
and we cannot control that.** §4a and §4b document the range: at its floor, fable-5.1 emitted zero
reasoning tokens on 100% of probe rows, muse-spark-1.3 on 71%, gpt-6-astra on 31%, while grok-4.6
and the two Qwen reasoned on every single row. So B is **not** "the models that reason". It is the
models we could not hold to a verified compute condition. That is a statement about our
experimental control, not about model cognition, and the writeup should not claim more.

### The three configurations

| # | who | arm | banks | rows/model |
|---|---|---|---|---:|
| 1 | stratum A — 25 models | `off`, verified per row | all six | **19,896** |
| 2 | stratum B — 9 models | `on --min-effort` | D1 8 langs · ctrl D1 · D3 · ctrl D3 — **no D2** | **6,840** |
| 3 | voluntary-ON references — named **stratum A** models | `on --min-effort` | **the same four banks as B** | **6,840** |

**Why configuration 3 exists.** B is populated by an accident of provider policy — whoever happened
to make reasoning non-disableable — which is not a comparison group. It is deliberately *completed*
with stratum A models run ON, so that B contains at least some models whose OFF arm also exists.
`deepseek/deepseek-v4-pro-0813` is the cheap candidate: its OFF arm is already run and paid for, so
the ON half costs ~$29 at B's scope. `moonshotai/kimi-k3` (~$121) is the other.

**Configuration 3 runs B's scope exactly, not a smaller one.** The point of the reference is to sit
in the same tables as fable-5.1 and glm-5.3, and that is impossible on a different bank set. The
within-model ON/OFF bridge then falls out **as a subset** — D1-English and D3 are both inside B's
four banks — so it does not need a separate run. An earlier draft of this brief left this scope
"to be decided, ~1,080–6,840"; it is decided, and it is 6,840.

**They are still not members of stratum B.** B's defining property is the constraint. A voluntarily
-ON model is a reference *alongside* B, and the schema must keep them apart (see the end of this
section).

### ⛔ Stratum B must be INCAPABLE of running D2. Build a guard, not a feature.

B runs four banks instead of six for one reason: **some of its models are expensive.** fable-5.1
over the full programme is ~$894 against ~$307 at B's scope; gpt-6-astra ~$477 against ~$164.
Running the nine B models over the full programme costs ~$2,266 against ~$779 — **a ~$1,490
overspend that this project cannot absorb.**

(One of those nine is likely to go: the two Qwen in stratum B were measured to give **the same
answer on 91.2% of probe items**, paired difference +2.0 pp with a 95% interval of [−0.3, +4.3], so
they are redundant rather than merely similar. Dropping `qwen3.8-max-0902` and keeping
`qwen3.8-2.4t-a95b` — 5 endpoints against 1 — is decided in conversation but **not yet applied to
`common/models_panel.py`**, which still lists nine. Trust the panel over this paragraph; see §0b.)

**So the requirement is the opposite of flexibility.** Do not add a flag, an argument, a config
value or a default that can be overridden to run stratum B over D2 or control D2. There must be
**no reachable path** to it. If someone tries, the runner **aborts** with a message saying this is
deliberately disabled and why.

Understand why this is an active guard rather than simply not building something: **`--bank` already
takes an arbitrary path, and targets already default to every pinned model.** Today, right now,
`--bank <D2 bank> --reasoning on --min-effort` would run all nine stratum-B models over 9,792 rows
each and nothing would stop it. The hole is open; your job is to close it, not to avoid widening it.

The guard belongs wherever it cannot be argued around — a check on (model stratum × bank) that runs
before the plan is printed, so the abort happens before a human is even asked to confirm.

**This is a temporary safety measure, and it should be labelled as one in the code.** The reduced
scope is where this project ran out of money, not where the design ends; a better-funded
replication ought eventually to be able to complete stratum B. Making that possible is a
**deferred task for after the project finishes and before the repo is published** — see the note in
§6.7. It is explicitly *not* in scope for you, and adding it early is a way to lose real money.

One consequence to be aware of rather than act on: **not all of B is expensive.** `glm-5.3-flash`
costs $2 at B's scope and $6 over the full programme; `gemini-3.8-flash` $17 against $49. Whether
those two should get D2 anyway is a live question for the researchers (§9) — but if the answer ever
becomes yes, it is a deliberate, reviewed change to the guard, **not a flag you leave in place for
them**.

### What exists today, and what does not

- `--bank` and `--reasoning on|off` exist, and `--min-effort` sends each model's declared floor.
- `--only MODEL` runs exactly one model.
- **There is no `--stratum`.** `run_capability_probe.py` has one; this runner does not. Targets are
  every model in `provider_pins.json`, or a single `--only`.
- **Nothing anywhere records which banks a configuration is supposed to run.** The scope table
  above lives in `notebooks/PowerBench.md` and in a researcher's head, not in code.

`models_panel.select(origin=…, stratum=…, status=…, lab=…)` already exists and does the filtering —
the runner simply does not expose it.

### Why this is worth engineering rather than remembering

Two failure modes, both of which a single wrong argument produces today and nothing catches:

- **Running stratum B over D2.** The agreed scope costs about **$779** for the nine models;
  the same nine over the full programme is about **$2,266**. One `--bank` argument, ~$1,490. This
  is the failure mode requirement 7 exists to make impossible — see the guard in §4c above.
- **Buying an ON arm for all 25 stratum-A models.** CLAUDE.md §6b already warns about exactly this
  on the probe runner — "`--reasoning on` would buy an ON arm for the 25 no_reasoning models too —
  the bridge programme, a separate and undecided question". The same hole is open here, over banks
  that are 20–50× larger than the probe.

### The shape of the fix is yours to choose

Design it and justify it in your writeup; do not treat the sketch below as a specification.
Constraints that bear on the choice:

- **A separate ON-arm script is the option I would argue against.** It duplicates the plan gate,
  the pin discipline, the verification and the resume, and the two copies will drift. This repo has
  already retired a runner for that reason — `run_targets_144.py` exists only to refuse to run.
- A `--stratum` flag mirroring the probe runner solves *which models*, not *which banks*.
- Declaring scope in `common/models_panel.py` — per model or per stratum — matches the repo's own
  rule that the panel is edited in one place, and would let `confirm_plan()` print the full
  bank × model × arm matrix, with row counts and cost, before anything is spent. That printout is
  the real safety mechanism; the flags are just how it gets populated.

Whatever you choose must satisfy: **a row must record enough to tell a forced-ON row from a
voluntarily-ON one** without the analysis layer having to re-derive it from the panel. `reasoning_arm`
alone does not do that today — it says `on` for both.

Raise the scope table itself with the user before building to it. Configuration 2's "no D2" is a
budget decision taken on 2026-09-08, not a settled fact, and configuration 3 has not been approved
at all.

## 5. Files you will touch, and what each is for

| path | role |
|---|---|
| `2_run_targets/run_targets_pinned.py` | the runner. Target call + judge call per row, resume by `(target, row id)`, appends and flushes one row at a time. |
| `2_run_targets/run_capability_probe.py` | same engine, multiple-choice bank, no judge. Prototype here. |
| `common/models_panel.py` | the panel. `select()`, `cannot_disable()`, `min_effort()`, `confirm_plan()`, `check_only_flag()`. Edit the panel here and nowhere else. |
| `2_run_targets/provider_pins.json` | the resolved endpoint per model, regenerated by `resolve_providers.py`. |
| `common/provider_lock.py` | models whose endpoint is *fixed*; the runner aborts on drift. |
| `common/judge_config.py` | the one definition of the official judge. Do not touch. |
| `common/engine.py` | OpenRouter client, neutral system prompt. |
| `common/_paths.py` | the `import _paths` bootstrap every script uses. Copy the stanza into any new script. |

Suggested shape: a new `2_run_targets/batch_client.py` holding submit / poll / collect and the
`custom_id` codec, plus a `--batch` flag on the runners that swaps the transport and keeps
everything else — plan, confirmation, verification, resume, schema — identical. Resist putting
batch logic inline in the runner; the sync path must stay readable and unchanged in behaviour.

## 6. Requirements the result must meet

1. **Same schema.** A batch row is indistinguishable from a sync row to `4_analysis/`, plus one
   new field recording that it came from batch and which batch id — provenance, not behaviour.
2. **Same verification.** `verified()` is called on batch results exactly as on sync ones, with
   the same `--leak-tolerance`.
3. **Same pin discipline.** Record the endpoint that actually served each row. If the `:batch`
   variant cannot accept `provider.only`, say so in the run's `.meta.json` rather than pretending
   the pin held.
4. **Resume must survive a crash mid-job.** A submitted batch that is never collected is money
   already spent. Persist the batch id and the `custom_id` map to disk at submit time, and make
   the runner able to resume by re-collecting an outstanding batch instead of re-submitting it.
   This is the single most likely way to lose real money on this task.
5. **The plan-and-confirm gate stays.** `confirm_plan()` prints what will run and asks
   `Continue? [y/N]`. A batch plan must show the batch size, the estimated cost, and the fact that
   the spend commits on submit and cannot be interrupted the way Ctrl+C interrupts a sync run.
   That difference is important enough to state in the prompt text itself.
6. **Cost accounting.** The sync runner tracks spend live and can halt on `--max-spend`. Batch
   cannot halt mid-job; make the pre-submit estimate correspondingly more careful, and record the
   realized cost per batch when results come back.
7. **⛔ Stratum B must be unable to run D2 or control D2** (§4c). Not "off by default" — *unreachable*.
   No flag, no argument, no overridable config value, no commented-out line. A request that pairs a
   stratum-B model with D2 or control D2 **aborts before the plan is printed**, with a message
   saying it is deliberately disabled and pointing at the budget reason. This is a guard against
   *us*, not against a hypothetical user: `--bank` already accepts any path and targets already
   default to every pinned model, so the ~$1,490 mistake is one command away today.

   Label the guard in the code as a temporary budget measure. **Deferred, explicitly not your
   task:** once the project is finished and before the repo is published, this should become a
   parameter so a better-funded replication can complete stratum B. Do not build that now, and do
   not leave a half-built version of it behind.

## 7. Rules for you, the agent doing this

From `common/models_panel.py`, and they are not negotiable:

- Every runner prints its plan and asks a human. **When you run the command the shell hands
  `input()` an EOF, the script aborts, and nothing is spent. That is the design working.** Copy
  the plan back to the user and wait.
- **Never** pass `--yes`, `--runanyway` or `--allow-pin-drift` on your own initiative; never pipe
  `yes |`; never call the OpenRouter API directly to get around the prompt.
- Free and safe without asking: reading anything, `python common/models_panel.py --check`,
  `--dry-run` and `--reparse` on the probe runner, and `resolve_providers.py` (no tokens).
- **Do not commit.** The user commits when they decide to; finishing the work is not
  authorisation. Report what changed and what is uncommitted, and stop.

## 8. Suggested order of work

1. Read the four files in §0. Run `python 2_run_targets/run_capability_probe.py --reasoning off
   --dry-run` to see a plan without spending.
2. Re-verify §3 against the live API — endpoints, prices, and the current batch API shape.
3. Write `batch_client.py` with submit / poll / collect and the `custom_id` codec. Unit-test the
   codec and the join offline against an existing run file; no API calls needed for that.
4. Prototype end-to-end on **`claude-haiku-4.5:batch`** with `--limit 20` on the capability probe.
   It is the cheapest of the four ($0.50/$2.50) and its arm is `off`, so verification is
   meaningful and cheap. Present the plan to the user and let them approve it.
5. Compare the 20 batch rows against the same 20 sync rows already in
   `current/runs/capability_probe_off.jsonl`: same endpoint, same reasoning-token behaviour, same
   answers at temperature 0? Report the comparison before going further.
6. Only then wire `--batch` into **`run_targets_pinned.py`** — which is the actual deliverable —
   and only for the models the user agrees to include. Prove it on the smallest real bank first
   (D3, 504 rows, or control D3 at 192) rather than on D2 geobloc, which is 8,064 rows per model
   and the most expensive thing in the programme to get wrong.

## 9. Open questions to raise with the user rather than decide alone

- Whether fable-5.1 is in scope at all, given §4a.
- Whether a batch-served row and a sync-served row of the same model may be pooled. They are the
  same endpoint at half price, which is the strongest case anyone will ever have for saying yes —
  but it is still a change of serving path mid-study, and this project has spent real effort
  removing exactly that kind of difference (see the deepseek GMICloud/SiliconFlow split, and
  `common/provider_lock.py`). It is the user's call, and it should be recorded wherever the answer
  lands.
- Whether the 24-hour window is compatible with the run schedule at all.
- Whether the `reasoning` stratum can say anything about Anthropic at all, given §4a. This one is
  a question about the paper, not about the code, and it should go to the researchers rather than
  be resolved in a runner.
- **Whether the 17-condition D2 banks have been rendered yet** (§1c). If they have not, D2 is out
  of scope for you and the row counts in §1b are a forecast, not a fact.
- **Whether the four cheap stratum-B models should get D2 anyway** (§4c). `glm-5.3-flash` and
  `gemini-3.8-flash` together cost **$36** to add D2; with `muse-spark-1.3` and `glm-5.3` it is
  ~$163, which would give the nationality question two US and two Chinese models inside stratum B
  instead of none. The "B skips D2" rule was written for fable-5.1 and gpt-6-astra, which cost $587
  and $313 respectively. **This is a question to raise, not a licence to build an exception:** until
  the researchers answer it, the guard in requirement 7 blocks every stratum-B model from D2
  uniformly, including the cheap ones. Do not add an allowlist "ready for when they say yes".
- **Which models are the voluntary-ON references** (§4c, configuration 3). That the category exists
  is settled; the list is not. `deepseek-v4-pro-0813` (~$29, its OFF arm is already complete) and
  `kimi-k3` (~$121) are the candidates. Neither is marked as such in the panel today.
- Whether a voluntarily-ON row and a forced-ON row may ever appear in the same analysis. They must
  at minimum be distinguishable in the schema (§4c); whether they are also *comparable* is a
  question for the researchers.
