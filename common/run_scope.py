"""What each configuration is allowed to run: bank families, the scope table, and the guard.

`common/models_panel.py` answers "who is in the study, in which arm, on which endpoint". It does
NOT answer "over which banks", and until 2026-09-08 nothing did: the scope table lived in
`notebooks/PowerBench.md` and in a researcher's head, while `--bank` took an arbitrary path and
`--targets` defaulted to every pinned model. This module is that missing half.

Three things live here.

1. BANK FAMILIES, decided from the bank's CONTENT, not its filename. `bank_family()` reads the
   rows and asks what the design is: a nationality dyad carries `user_nationality` /
   `affected_nationality` and a `<user_context>` system prompt, an AI-narrator row carries
   `narrator`, a control row carries `mode == "no_power_shifting"` and `trigger` instead of
   `domain`. Filenames were rejected as the signal on purpose -- a guard that a rename defeats is
   not a guard, and this one exists to stop a ~$1,490 mistake.

2. THE SCOPE TABLE (`CONFIGURATIONS`): the three programmes the panel actually runs, each with its
   models, its arm and its banks, with row counts. It is printed by the runners before anything is
   spent, so a human approving a plan can see the configuration it belongs to.

3. THE GUARD (`assert_scope_allowed`), which aborts BEFORE the plan is printed -- before a human is
   even asked to confirm -- when a (model, arm, bank) triple is outside the funded scope.

    import _paths  # noqa: F401
    from run_scope import bank_family, assert_scope_allowed, CONFIGURATIONS

CLI (free, no API calls):
    python common/run_scope.py                       the scope table with row counts and the guard
    python common/run_scope.py --classify PATH ...   what family each bank is, and why

=================================================================================================
THE GUARD IS DELIBERATE AND HAS NO OVERRIDE. READ BEFORE "FIXING" IT.
=================================================================================================
Stratum B -- and any run in a reasoning-enabled arm -- may not touch the nationality banks (D2,
control D2). This is not a default, not a config value and not a flag: there is no argument that
turns it off, and adding one would defeat the point.

Why, in the numbers that decided it (2026-09-08): stratum B at its agreed scope -- D1 in 8
languages, control D1, D3, control D3, 6,840 rows per model -- costs about $779 for the nine
models. The same nine over the full programme, i.e. with D2 and control D2 added, is about $2,266.
D2 is 9,792 of the 19,896 rows in a full programme, 49% of it, and stratum B's models are the
expensive ones: fable-5.1 alone is ~$894 over the full programme against ~$307 at B's scope,
gpt-6-astra ~$477 against ~$164. One `--bank` argument is the difference, and this project cannot
absorb it.

It is a BUDGET measure, not a design boundary. The reduced scope is where this project ran out of
money, not where the science ends, and a better-funded replication ought to be able to complete
stratum B. Turning this into a parameter is a DEFERRED task for after the project finishes and
before the repo is published -- see requirement 7 of `2_run_targets/BATCH_ADAPTATION_BRIEF.md`.
Doing it early is a way to lose real money, so it is not half-built here.

Not covered by this guard, and a live question rather than a settled one: whether the four CHEAP
stratum-B models should get D2 anyway (glm-5.3-flash and gemini-3.8-flash together cost ~$36 to
add it; with muse-spark-1.3 and glm-5.3 it is ~$163, which would give the nationality question two
US and two Chinese models inside stratum B instead of none). Until the researchers answer, the
guard blocks every stratum-B model uniformly, including the cheap ones. There is deliberately no
allowlist standing ready for a yes.
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from models_panel import MODELS, NO_REASONING, REASONING, select  # noqa: E402

ROOT = os.path.dirname(_HERE)

# ------------------------------------------------------------------ bank families

D1 = "d1"
D1_CONTROL = "control_d1"
D2 = "d2"
D2_CONTROL = "control_d2"
D3 = "d3"
D3_CONTROL = "control_d3"
PROBE = "capability_probe"
UNKNOWN = "unknown"

#: The nationality banks. These are the ones the guard protects: they are 49% of a full programme
#: and the only family whose row count multiplies by a condition count (14 today, 17 once the
#: usally_cnally / cnally_usally / neutral_neutral conditions of 2026-09-08 are rendered).
NATIONALITY_BANKS = frozenset({D2, D2_CONTROL})

#: Arms in which the model is thinking. `off` is the verified-disabled arm; `on` and `floor` both
#: mean reasoning tokens are being paid for, whether we asked for them (`on`) or the endpoint left
#: us no choice (`floor`).
REASONING_ARMS = frozenset({"on", "floor"})

FAMILY_LABEL = {
    D1: "D1 (power tensor)",
    D1_CONTROL: "control D1 (no_power_shifting)",
    D2: "D2 (nationality dyads, geobloc)",
    D2_CONTROL: "control D2 (nationality dyads)",
    D3: "D3 (AI-agent narrator)",
    D3_CONTROL: "control D3 (AI-agent narrator)",
    PROBE: "capability probe (GPQA + MMLU-Pro)",
    UNKNOWN: "unrecognised bank",
}

CONTROL_MODE = "no_power_shifting"


def classify_rows(rows) -> tuple[str, str]:
    """(family, the evidence for it) for an already-loaded bank.

    Deliberately ANY-row, not all-row: a bank that contains even one nationality-dyad row is
    treated as a nationality bank. For a guard that is the right bias -- the failure it prevents
    is expensive and the false positive is a message asking a human to look.
    """
    rows = list(rows)
    if not rows:
        return UNKNOWN, "empty bank"

    def any_row(fn):
        return next((r for r in rows if fn(r)), None)

    hit = any_row(lambda r: "options" in r and "answer" in r and "prompt" in r)
    if hit is not None:
        return PROBE, "rows carry `options` + `answer`: a multiple-choice item, not a scenario"

    control = any_row(lambda r: r.get("mode") == CONTROL_MODE) is not None
    # Every shape the nationality design takes on disk, rendered or not. The UNRENDERED source
    # banks (`nat_slot` + a literal `{NAT}` in the prompt) count too: they are the same design one
    # step earlier, and a guard that only recognises the finished article invites someone to point
    # the runner at the ingredient. `nationality` alone catches the single-country render
    # (dataset2_full_576.v6r2.rendered.jsonl, condition "nat"), which is a nationality bank
    # without being a dyad.
    hit = any_row(lambda r: r.get("user_nationality") or r.get("affected_nationality")
                  or r.get("nationality") or r.get("nat_slot")
                  or "{NAT}" in str(r.get("prompt") or "")
                  or "<user_context>" in str(r.get("system_prompt") or ""))
    if hit is not None:
        why = ("rows carry a nationality slot (`user_nationality` / `affected_nationality` / "
               "`nationality` / `nat_slot` / a literal {NAT}) and/or a <user_context> system "
               f"prompt -- e.g. id {hit.get('id')!r}, condition {hit.get('condition')!r}")
        return (D2_CONTROL if control else D2), why

    hit = any_row(lambda r: r.get("narrator"))
    if hit is not None:
        why = f"rows carry `narrator` = {hit.get('narrator')!r}: the AI-agent recast"
        return (D3_CONTROL if control else D3), why

    if control:
        return D1_CONTROL, f"every mode is {CONTROL_MODE!r} and no nationality or narrator slot"
    if any_row(lambda r: r.get("mode")) is not None:
        langs = sorted({r.get("lang") for r in rows if r.get("lang")})
        return D1, (f"power modes, no nationality slot, no narrator; "
                    f"{len(langs)} language(s): {','.join(langs[:8])}")
    return UNKNOWN, "no `mode`, no nationality slot, no narrator, no multiple-choice options"


def bank_family(bank_path: str, rows=None) -> tuple[str, str]:
    """(family, evidence) for a bank on disk. Pass `rows` if the caller already loaded them."""
    if rows is None:
        rows = []
        with open(bank_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return classify_rows(rows)


# ------------------------------------------------------------------ the scope table

#: Rows per model, per bank family, at the CURRENT bank versions (2026-09-08). D2's 9,792 assumes
#: the 17-condition bank of the 2026-09-08 decision; the bank on disk today still has 14
#: conditions (8,064 rows), so `python common/run_scope.py` prints both the declared figure and
#: what it finds. Treat these as planning figures, not as a count of any file.
ROWS_PER_MODEL = {
    D1: 576 * 8,            # 8 languages over identical cells
    D1_CONTROL: 192 * 8,
    D2: 576 * 17,           # 17 conditions once usally_cnally / cnally_usally / neutral_neutral land
    D2_CONTROL: 192 * 17,
    D3: 504,
    D3_CONTROL: 192,
}

#: The four banks stratum B runs: everything except the nationality families.
B_SCOPE = (D1, D1_CONTROL, D3, D3_CONTROL)
#: The full programme.
FULL_SCOPE = (D1, D1_CONTROL, D2, D2_CONTROL, D3, D3_CONTROL)

CONFIGURATIONS = {
    "A_off": {
        "title": "Stratum A -- reasoning disabled, verified per row",
        "arm": "off",
        "banks": FULL_SCOPE,
        "stratum": NO_REASONING,
        "note": "the main programme. Reasoning is switched off and the row carries the proof "
                "(`reasoning_ok`, from usage.completion_tokens_details.reasoning_tokens).",
    },
    "B_floor": {
        "title": "Stratum B -- reasoning at the model's floor, not verifiable",
        "arm": "on",
        "banks": B_SCOPE,
        "stratum": REASONING,
        "note": "the endpoint refuses to disable reasoning, so these models are run at the "
                "smallest effort they accept. NO D2: see the header of this file for the "
                "$779-vs-$2,266 arithmetic. What `the floor` means behaviourally differs per "
                "model and we cannot control it -- at its floor fable-5.1 emitted zero reasoning "
                "tokens on 100% of capability-probe rows, muse-spark-1.3 on 71%, gpt-6-astra on "
                "31%, while grok-4.6 and qwen3.8-2.4t reasoned on every one. So B is NOT `the "
                "models that reason`; it is the models we could not hold to a verified compute "
                "condition. That is a statement about our experimental control, not about model "
                "cognition, and the writeup should not claim more.",
    },
    "ON_reference": {
        "title": "Voluntary-ON references -- stratum A models run ON at B's scope",
        "arm": "on",
        "banks": B_SCOPE,
        "stratum": NO_REASONING,
        "note": "NOT APPROVED YET (2026-09-08). Stratum B is populated by an accident of provider "
                "policy -- whoever happened to make reasoning non-disableable -- which is not a "
                "comparison group. Completing it with stratum-A models run ON gives B some models "
                "whose OFF arm also exists, and the within-model ON/OFF bridge then falls out as a "
                "subset (D1-English and D3 are both inside B's four banks). Candidates named in "
                "conversation: deepseek/deepseek-v4-pro-0813 (~$29; its OFF arm is already run and "
                "paid for) and moonshotai/kimi-k3 (~$121). The LIST IS NOT SETTLED, so no model is "
                "marked as one here -- and nothing needs it to be: a row records `reasoning_forced`, "
                "so a voluntarily-ON row is told from a forced-ON one without consulting any list. "
                "These models are references ALONGSIDE stratum B, never members of it: B's defining "
                "property is the constraint.",
    },
}


def rows_for(banks) -> int:
    return sum(ROWS_PER_MODEL.get(b, 0) for b in banks)


def configuration_of(stratum: str, arm: str) -> str | None:
    """Which configuration a (stratum, arm) pair belongs to, or None if it is not one of the three."""
    if arm == "off" and stratum == NO_REASONING:
        return "A_off"
    if arm in REASONING_ARMS and stratum == REASONING:
        return "B_floor"
    if arm in REASONING_ARMS and stratum == NO_REASONING:
        return "ON_reference"
    return None


# ------------------------------------------------------------------ the guard

class ScopeViolation(SystemExit):
    """Raised instead of running. A SystemExit subclass so it stops a runner the way the other
    pre-spend refusals in this repo do, and so `except Exception` cannot swallow it."""


_BUDGET_NOTE = (
    "   Why: stratum B at its agreed scope (D1 8 langs + control D1 + D3 + control D3, 6,840 rows\n"
    "   per model) costs about $779 for its nine models. The same nine over the full programme is\n"
    "   about $2,266 -- D2 is 49% of a full programme and B's models are the expensive ones\n"
    "   (fable-5.1 ~$894 vs ~$307, gpt-6-astra ~$477 vs ~$164). That ~$1,490 is money this project\n"
    "   does not have.\n"
    "   This is a TEMPORARY BUDGET MEASURE, deliberately with no flag, no argument and no config\n"
    "   value that lifts it. If the decision changes, it changes in common/run_scope.py, reviewed,\n"
    "   by a person -- see the header of that file."
)


def assert_scope_allowed(family: str, targets, arms: dict, bank_label: str = "") -> None:
    """Abort unless every (model, arm) may run over a bank of this family.

    Called by the runners BEFORE `confirm_plan()`, so an out-of-scope request never even reaches
    the human confirmation -- there is nothing to approve.

    Two rules, and the second implies the first today. Both are stated because they fail
    differently: rule 1 is about the model (stratum B is defined by the constraint), rule 2 is
    about the money (a reasoning-enabled arm over D2 is expensive whoever is running it, and it is
    how configuration 3 would blow its budget).
    """
    if family not in NATIONALITY_BANKS:
        return

    where = f" ({bank_label})" if bank_label else ""
    label = FAMILY_LABEL.get(family, family)

    # Rule 1 -- stratum B may not run the nationality banks. Requirement 7 of the batch brief.
    forced = [t for t in targets if MODELS.get(t, {}).get("stratum") == REASONING]
    if forced:
        raise ScopeViolation(
            f"\n!! REFUSING TO RUN: stratum B over {label}{where}.\n"
            f"   models: {', '.join(forced)}\n"
            f"   Stratum B (reasoning cannot be disabled) is funded for D1 in 8 languages, control\n"
            f"   D1, D3 and control D3 only -- NOT for D2 or control D2.\n"
            f"{_BUDGET_NOTE}\n")

    # Rule 2 -- no reasoning-enabled arm over the nationality banks, whatever the stratum. This is
    # what stops configuration 3 (a stratum-A model run ON as a reference for B) from quietly
    # buying D2 at B's prices, and what stops `--reasoning on` over D2 for the 25 stratum-A models.
    hot = sorted(t for t in targets if arms.get(t) in REASONING_ARMS)
    if hot:
        raise ScopeViolation(
            f"\n!! REFUSING TO RUN: a reasoning-enabled arm over {label}{where}.\n"
            f"   models: {', '.join(f'{t} (arm={arms.get(t)})' for t in hot)}\n"
            f"   The nationality banks are funded for the VERIFIED-OFF arm only. A voluntary-ON\n"
            f"   reference (configuration `ON_reference`) runs stratum B's scope exactly -- the same\n"
            f"   four banks -- because the point of the reference is to sit in the same tables as\n"
            f"   fable-5.1 and glm-5.3, which is impossible on a different bank set.\n"
            f"{_BUDGET_NOTE}\n")


def assert_targets_chosen(arm: str, explicit: bool) -> None:
    """A reasoning-enabled arm must NAME its models. It may never fall back to the whole panel.

    The second failure mode of the batch brief's section 4c, and the one CLAUDE.md section 6b
    already warns about on the probe runner: with no selector the target list is every pinned
    model, so `--reasoning on` buys an ON arm for the 25 stratum-A models too -- over banks 20-50x
    larger than the probe. Cheap to prevent, expensive to notice afterwards.
    """
    if arm in REASONING_ARMS and not explicit:
        raise ScopeViolation(
            "\n!! REFUSING TO RUN: --reasoning on with no target selection.\n"
            "   The default target list is EVERY pinned model, so this would buy an ON arm for the\n"
            "   25 stratum-A models as well as the 9 of stratum B -- the voluntary-ON reference\n"
            "   programme, which is not approved, over banks 20-50x larger than the capability probe.\n"
            "   Name what you mean: --stratum reasoning, --only MODEL, or TARGETS=a,b in the "
            "environment.\n")


# ------------------------------------------------------------------------------------- CLI
def _cli():
    args = sys.argv[1:]
    if "--classify" in args:
        for p in args[args.index("--classify") + 1:]:
            if p.startswith("--"):
                break
            fam, why = bank_family(p)
            n = sum(1 for line in open(p, encoding="utf-8") if line.strip())
            guard = "BLOCKED for stratum B / any ON arm" if fam in NATIONALITY_BANKS else "-"
            print(f"{os.path.basename(p):52s} {fam:14s} {n:7d} rows  {guard}")
            print(f"    {why}")
        return

    print("PowerBench run scope -- who runs what, and what the guard forbids\n")
    for key, cfg in CONFIGURATIONS.items():
        models = select(stratum=cfg["stratum"], status=("run", "pending"))
        n = rows_for(cfg["banks"])
        print(f"[{key}]  {cfg['title']}")
        print(f"   arm    : {cfg['arm']}")
        print(f"   banks  : {', '.join(cfg['banks'])}")
        print(f"   rows   : {n:,} per model")
        print(f"   models : {len(models)} in stratum {cfg['stratum']}"
              + ("  <- NOT APPROVED; list not settled" if key == "ON_reference" else ""))
        print(f"   note   : {cfg['note'][:300]}")
        print()
    print(f"GUARD: {sorted(NATIONALITY_BANKS)} may be run ONLY in the verified-off arm, and never "
          f"by a stratum-{REASONING} model.")
    print("       No flag lifts it. See the header of common/run_scope.py.\n")
    banks_dir = os.path.join(ROOT, "current", "banks")
    if os.path.isdir(banks_dir):
        print("banks on disk:")
        for name in sorted(os.listdir(banks_dir)):
            if not name.endswith(".jsonl") or ".provenance" in name or ".verify" in name:
                continue
            p = os.path.join(banks_dir, name)
            try:
                fam, _ = bank_family(p)
                n = sum(1 for line in open(p, encoding="utf-8") if line.strip())
            except (OSError, ValueError):
                continue
            mark = "  <- guarded" if fam in NATIONALITY_BANKS else ""
            print(f"  {name:56s} {fam:14s} {n:7d}{mark}")


if __name__ == "__main__":
    _cli()
