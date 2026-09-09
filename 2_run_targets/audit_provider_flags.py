#!/usr/bin/env python3
"""Does this endpoint actually DO what the `reasoning` flag asks? Measure it, per provider.

An OpenRouter endpoint declaring `reasoning` in `supported_parameters` proves nothing. Every one of
kimi-k2.6's 21 endpoints declared it, and Phala ignored it on 94% of calls; every one of kimi-k3's
18 endpoints declares it, and DeepInfra returned 0 reasoning tokens on 69 of 69 rows when asked for
`{"effort": "low"}` (2026-09-06). Declared support is not honoured support, in both directions:

    OFF ignored -> reasoning leaks into rows labelled "off"      (the 2026-08 leak audit)
    ON  ignored -> a "minimum effort" arm that never reasons     (2026-09-06, kimi-k3 on DeepInfra)

Both corrupt the arm, and both are invisible until someone counts reasoning tokens. This script
counts them, for a few cents, BEFORE a bank is run. It is the screen `run_targets_pinned.py`
applies to its own pinned provider, generalised to any set of endpoints so it can be used to CHOOSE
one.

    # audit the endpoints resolve_providers would rank first, every declared effort
    python 2_run_targets/audit_provider_flags.py --model moonshotai/kimi-k3 --dry-run
    python 2_run_targets/audit_provider_flags.py --model moonshotai/kimi-k3 --top 4

    # audit named providers only
    python 2_run_targets/audit_provider_flags.py --model z-ai/glm-5.3 --providers z-ai,reka

The shapes are not a fixed list: they come from the model's own OpenRouter metadata
(`mandatory`, `supported_efforts`), so each model is asked exactly what it claims to accept --
`off` only where reasoning can be disabled, then `on`, then one shape per declared effort rung.

Read the output in two passes:

  1. Per cell: honoured / IGNORED / partial N% / error. `partial` is why --reps defaults to 3 --
     Phala honoured 6% of calls, which no single call would have found. `error` keeps the message,
     because a rejected shape is a finding ("Reasoning is mandatory for this endpoint").
  2. THE LADDER. By default only two rungs are measured -- the bottom one (what banks are actually
     run at) and the top one as its CONTROL. One effort in isolation proves nothing: 0 reasoning
     tokens at `low` can mean the flag was dropped OR that the model honoured it and the question
     was easy. A large top rung says the parameter reaches the model; a top rung that is also 0
     says it does not. `--all-efforts` measures every declared rung, which is only worth paying
     for when you want to know WHERE a ladder flattens.

Cost: --reps x --shapes x --providers calls on a one-line prompt. Default 3 x 4 x 3 = 36 calls of
a few hundred tokens each; on a $15/M model that is well under a dollar. It still spends, so it
asks for confirmation like every other runner here, and honours --max-spend.

Residual limitation, same as resolve_providers.py: `provider.only` pins the PROVIDER, not the
endpoint. Where one provider exposes several (Fireworks lists three for kimi-k3, at three prices)
the audit cannot say which answered. The row records the quantization actually returned, so a
divergence is at least visible.

Output: a table, plus `--out` JSON holding every call's reasoning_tokens, cost and verdict.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = os.path.dirname(os.path.abspath(__file__))
_d = _HERE
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "common")):
    _d = os.path.dirname(_d)
sys.path[:0] = [_HERE, os.path.join(_d, "common")]
ROOT = _d

from models_panel import confirm_plan  # noqa: E402


def arg(name, default=None, cast=str):
    if name in sys.argv:
        return cast(sys.argv[sys.argv.index(name) + 1])
    return default


MODEL = arg("--model")
if not MODEL:
    raise SystemExit("--model MODEL is required (e.g. --model moonshotai/kimi-k3)")
PROVIDERS = [p for p in (arg("--providers", "") or "").split(",") if p]
TOP = arg("--top", 3, int)              # if --providers is not given: the N best-ranked endpoints
REPS = arg("--reps", 3, int)            # calls per (provider, shape); >1 is what finds partial honouring
MAX_TOKENS = arg("--max-tokens", 2000, int)   # reasoning tokens count against this
LEAK_TOL = arg("--leak-tolerance", 1, int)   # same convention as the runners
MAX_SPEND = arg("--max-spend", 2.0, float)
WORKERS = arg("--workers", 8, int)
DRY = "--dry-run" in sys.argv
ASSUME_YES = "--yes" in sys.argv
OUT = arg("--out", os.path.join(ROOT, "current", "runs",
                                f"flag_audit_{MODEL.replace('/', '_')}.json"))

def model_reasoning_meta(model):
    """OpenRouter's own answer to "can this model turn reasoning off, and which efforts exist".
    Free, and better than guessing: it carries `mandatory`, `default_effort` and the exact
    `supported_efforts` ladder, which differs per model (qwen3.8-max goes down to `minimal`,
    glm-5.3 and kimi-k3 stop at `low`)."""
    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=60) as r:
        for m in json.load(r)["data"]:
            if m["id"] == model:
                return m.get("reasoning") or {}
    return {}


def build_shapes(meta, full=False):
    """What to ask this endpoint. `off` only where the model allows it, then TWO effort rungs.

    Only the bottom rung is measured up front, because only the bottom rung is what banks run at,
    and on a hard enough prompt it answers the question by itself: every endpoint that honoured
    `low` spent tokens on it (36-244, measured 2026-09-06) and every endpoint that ignored the
    flag returned 0.

    The top rung is not part of the DECISION, so it is not paid for up front. An endpoint that
    gives no reasoning at the bottom rung is unusable for a minimum-effort arm whatever the cause
    -- "the flag was dropped" and "the flag was honoured and mapped to no thinking" are
    observationally identical and equally disqualifying. The top rung only EXPLAINS which it was,
    which is worth knowing (one is worth retesting later, the other is not), so it runs afterwards
    and only for the providers that failed. `--all-efforts` measures every declared rung, worth
    paying for only to find where a ladder flattens -- qwen3.8-max's bottom three are one level."""
    shapes = {}
    if not meta.get("mandatory"):
        shapes["off"] = ({"enabled": False}, False)
    ladder = [e for e in (meta.get("supported_efforts") or ["low"]) if e != "none"]
    if not full:
        ladder = ladder[-1:]                      # declared strongest-first: the bottom rung only
    for eff in ladder:
        shapes[f"effort_{eff}"] = ({"effort": eff}, True)
    if full:
        shapes["on"] = ({"enabled": True}, True)  # the provider default, for reference only
    return shapes


FULL_LADDER = "--all-efforts" in sys.argv
META = model_reasoning_meta(MODEL)
SHAPES = build_shapes(META, full=FULL_LADDER)
ONLY_SHAPES = [s for s in (arg("--shapes", "") or "").split(",") if s]
if ONLY_SHAPES:
    unknown = [s for s in ONLY_SHAPES if s not in SHAPES]
    if unknown:
        raise SystemExit(f"unknown shape(s) {unknown}; known: {list(SHAPES)}")
    SHAPES = {k: v for k, v in SHAPES.items() if k in ONLY_SHAPES}

# The prompt has to be HARD. This is the lesson of the 2026-09-06 first run: on "a bat and a ball
# cost $1.10", glm-5.3 returned 0 reasoning tokens at effort `low` and ~111 at its default, and the
# audit called `low` IGNORED. It was not -- `low` is a declared effort for that model; the question
# was simply too easy to need thinking at the bottom rung. On an easy prompt, "the flag was dropped"
# and "the flag worked and the model chose not to think" look identical, and the second is the more
# common one. A prompt that takes real multi-step work separates them.
PROMPT = ("A tank holds 240 litres. Pipe A fills it in 12 minutes, pipe B in 15 minutes, and a "
          "drain empties a full tank in 20 minutes. All three open at once with the tank empty, "
          "but the drain is blocked shut the moment the tank first reaches 180 litres. How many "
          "minutes, in total, until the tank is full? Reply with only the number of minutes.")

# `--prompt-file PATH` swaps it. The default above is a middling question -- hard enough to beat
# the bat-and-ball failure, easy enough that a strong model may still not need to think, which is
# exactly the ambiguity that made claude-fable-5.1 read as IGNORED at its floor on 2026-09-07.
# When the finding you are chasing is "does this model EVER use its thinking channel at this
# effort", raise the difficulty until a wrong answer would be expected without thinking, and put
# the question in a file so the run records which question produced the verdict.
_PROMPT_FILE = arg("--prompt-file")
if _PROMPT_FILE:
    with open(_PROMPT_FILE, encoding="utf-8") as _fh:
        PROMPT = _fh.read().strip()
    if not PROMPT:
        raise SystemExit(f"{_PROMPT_FILE} is empty")

KEY = None
if not DRY:
    from or_key import get_key
    KEY = get_key()

_spent = 0.0


def endpoints(model):
    url = f"https://openrouter.ai/api/v1/models/{model}/endpoints"
    with urllib.request.urlopen(url, timeout=45) as r:
        return json.load(r)["data"].get("endpoints", [])


def slug(ep):
    """The endpoint's FULL tag, which is what `provider.only` routes on.

    Not `tag.split("/")[0]`. OpenRouter's docs are explicit that a bare provider slug does NOT
    match service-tier endpoints -- `openai` excludes `openai/flex` and `openai/fast`, which
    "require explicit opt-in". Stripping the suffix therefore cannot reach a tier at all, and
    silently means the standard tier: measured on 2026-09-07, gpt-5.6-luna billed at $0.20/$1.20
    across every run we have, i.e. the standard endpoint, while our pins file recorded the tag
    `openai/flex` at half that. The tag is the routable identity; the bare slug is a prefix."""
    return ep.get("tag") or ""


def matches(ep, want):
    """A --providers entry names either the full tag (`openai/flex`) or a bare provider
    (`baseten`, which then covers `baseten/fp8`). Both are useful: the bare form asks "this
    company", the tagged form asks "this tier / region / precision"."""
    tag = slug(ep)
    return tag == want or tag.split("/")[0] == want


def post(payload):
    """One call. Returns (usage, provider, text, error) -- never raises, because a provider that
    rejects a shape is a RESULT, not a crash: 'this endpoint refuses {"effort": "low"}' is exactly
    the kind of thing the audit exists to record.

    The visible TEXT is returned and stored since 2026-09-08, and it is not decoration. The token
    counts alone cannot tell "the model did not reason" from "the model reasoned in the answer",
    and those need opposite responses. Measured on claude-fable-5.1 that day: at effort low it
    returned 0 reasoning tokens and 763-1309 visible tokens, at effort max 2091-2834 reasoning
    tokens and about SIX visible ones. Same work, different place -- a fact the numbers hint at
    and only the text settles."""
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", body,
        {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
         "HTTP-Referer": "https://github.com/wenbrau/powerbench", "X-Title": "PowerBench flag audit"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            ch = (d.get("choices") or [{}])[0]
            txt = ((ch.get("message") or {}).get("content") or "")
            return d.get("usage") or {}, d.get("provider"), txt, None
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:200]
            except Exception:
                pass
            if e.code in (400, 404, 422):          # the shape was rejected: a finding, not a retry
                return {}, None, "", f"HTTP {e.code}: {detail}"
            if attempt == 2:
                return {}, None, "", f"HTTP {e.code}: {detail}"
            time.sleep(3 * (attempt + 1))
        except Exception as e:
            if attempt == 2:
                return {}, None, "", f"{type(e).__name__}: {e}"
            time.sleep(3 * (attempt + 1))


def one_call(provider, shape_name):
    reasoning, _want = SHAPES[shape_name]
    payload = {"model": MODEL, "messages": [{"role": "user", "content": PROMPT}],
               "max_tokens": MAX_TOKENS, "temperature": 0, "reasoning": reasoning,
               "provider": {"only": [provider], "allow_fallbacks": False}}
    usage, served_by, text, err = post(payload)
    rtok = ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0)
    cost = float(usage.get("cost") or 0)
    global _spent
    _spent += cost
    return {"provider": provider, "shape": shape_name, "sent": reasoning,
            "reasoning_tokens": rtok, "completion_tokens": usage.get("completion_tokens"),
            "prompt_tokens": usage.get("prompt_tokens"),
            "cost": cost, "served_by": served_by, "error": err,
            "visible_chars": len(text or ""),
            "answer": (text or "")[:4000]}


def verdict(calls, want):
    """honoured / IGNORED / partial / error, from the calls of one (provider, shape) cell."""
    ok = [c for c in calls if not c["error"]]
    if not ok:
        return "error", 0.0
    agree = [c for c in ok if (c["reasoning_tokens"] > LEAK_TOL) == want]
    share = len(agree) / len(ok)
    if share == 1.0:
        return "honoured", share
    if share == 0.0:
        return "IGNORED", share
    return "partial", share


def main():
    eps = endpoints(MODEL)
    if not eps:
        raise SystemExit(f"no endpoints for {MODEL!r}")
    if PROVIDERS:
        chosen, seen = [], set()
        for p in PROVIDERS:
            hits = [slug(e) for e in eps if matches(e, p)]
            if not hits:
                print(f"!! {p!r} does not serve {MODEL}; known: "
                      f"{sorted({slug(e) for e in eps})}")
                continue
            # A bare slug can cover several tags (a tier ladder, or one precision per host).
            # Audit each, because they are different endpoints and can behave differently.
            for h in hits:
                if h not in seen:
                    chosen.append(h)
                    seen.add(h)
    else:
        # No ranking policy here on purpose: the audit is what INFORMS a policy. Take the most
        # available endpoints and let the operator read the table.
        chosen, seen = [], set()
        for e in sorted(eps, key=lambda x: -(x.get("uptime_last_1d") or 0)):
            if slug(e) not in seen:
                chosen.append(slug(e))
                seen.add(slug(e))
            if len(chosen) >= TOP:
                break

    quant = {}
    price = {}
    for e in eps:
        quant.setdefault(slug(e), e.get("quantization") or "unknown")
        price.setdefault(slug(e), float((e.get("pricing") or {}).get("completion") or 0) * 1e6)

    n_calls = len(chosen) * len(SHAPES) * REPS
    est = sum(price.get(p, 0) for p in chosen) * len(SHAPES) * REPS * MAX_TOKENS / 1e6
    print(f"\nmodel   {MODEL}")
    print(f"shapes  {list(SHAPES)}")
    print(f"{'provider':16s} {'quant':9s} {'$/M out':>8s}")
    for p in chosen:
        print(f"{p:16s} {quant.get(p, '?'):9s} {price.get(p, 0):8.2f}")
    print(f"\n{n_calls} calls ({len(chosen)} providers x {len(SHAPES)} shapes x {REPS} reps), "
          f"max_tokens {MAX_TOKENS}")
    print(f"upper-bound estimate ${est:,.2f} (every call maxing out its budget; real cost is far "
          f"lower on a one-line prompt)")

    if DRY:
        print("\n--dry-run: no calls made.")
        return

    confirm_plan([(MODEL, f"{len(SHAPES)} shapes x {REPS}", f"{p} ({quant.get(p, '?')})")
                  for p in chosen],
                 [f"flag audit, {n_calls} calls, prompt: {PROMPT[:60]}...",
                  f"-> {os.path.relpath(OUT, ROOT)}",
                  f"upper-bound ${est:,.2f}, --max-spend ${MAX_SPEND:,.2f}"],
                 assume_yes=ASSUME_YES)

    jobs = [(p, s) for p in chosen for s in SHAPES for _ in range(REPS)]
    calls = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(one_call, p, s): (p, s) for p, s in
                [(p, s) for p, s in jobs]}
        for i, f in enumerate(as_completed(futs), 1):
            calls.append(f.result())
            if MAX_SPEND and _spent >= MAX_SPEND:
                print(f"\n!! --max-spend ${MAX_SPEND:,.2f} reached; stopping early")
                break
            print(f"\r  {i}/{len(jobs)} calls, ${_spent:,.3f}", end="", flush=True)
    print()

    # Escalation: a provider with no reasoning at the bottom rung is already disqualified,
    # but WHY it failed is worth three calls -- "ignores the parameter" and "honours it and
    # floors to nothing" are different facts about the endpoint, and only the first makes
    # retesting it later pointless. Paid for only where it failed.
    bottom = [k for k in SHAPES if k.startswith("effort_")][-1]
    ladder_all = [e for e in (META.get("supported_efforts") or []) if e != "none"]
    top = f"effort_{ladder_all[0]}" if ladder_all else None
    if top and top not in SHAPES:
        def _median_rtok(p, sh):
            v = sorted(c["reasoning_tokens"] for c in calls
                       if c["provider"] == p and c["shape"] == sh and not c["error"])
            return v[len(v) // 2] if v else 0
        dead = [p for p in chosen if _median_rtok(p, bottom) <= LEAK_TOL]
        if dead and len(dead) == len(chosen):
            print(f"!! every provider returned no reasoning at {bottom}. That is either a "
                  f"real finding or a prompt too easy to need thinking: this audit is only "
                  f"as sharp as its question.")
        if dead:
            print(f"   escalating to {top} for {dead} to say WHY they failed...")
            SHAPES[top] = ({"effort": ladder_all[0]}, True)
            more = [(p, top) for p in dead for _ in range(REPS)]
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for f in as_completed([pool.submit(one_call, p, sh) for p, sh in more]):
                    calls.append(f.result())

    print(f"\n{'provider':16s} {'quant':9s} " +
          "".join(f"{s:>16s}" for s in SHAPES))
    rows = {}
    for p in chosen:
        line = f"{p:16s} {quant.get(p, '?'):9s} "
        for s in SHAPES:
            cell = [c for c in calls if c["provider"] == p and c["shape"] == s]
            # The escalation adds a column that only the failing providers were asked for. An
            # untested cell must read as untested: calling it "error" would say this endpoint was
            # tried and broke, which is the opposite of what happened.
            if not cell:
                rows[(p, s)] = {"verdict": "not tested", "share": None,
                                "median_reasoning_tokens": None, "calls": []}
                line += f"{'-':>16s}"
                continue
            v, share = verdict(cell, SHAPES[s][1])
            rtok = [c["reasoning_tokens"] for c in cell if not c["error"]]
            med = sorted(rtok)[len(rtok) // 2] if rtok else 0
            rows[(p, s)] = {"verdict": v, "share": share, "median_reasoning_tokens": med,
                            "calls": cell}
            label = v if v in ("honoured", "IGNORED", "error") else f"partial {share:.0%}"
            line += f"{label:>16s}"
        print(line)
    print(f"\nmedian reasoning tokens per cell (0 means the model did not reason):")
    for p in chosen:
        print(f"  {p:16s} " + "  ".join(
            f"{s}=" + ("-" if rows[(p, s)]["median_reasoning_tokens"] is None
                       else str(rows[(p, s)]["median_reasoning_tokens"]))
            for s in SHAPES))
    # Order by the model's DECLARED ladder, not by insertion: the escalation appends the top rung
    # last, which would otherwise print the ladder backwards.
    declared = [f"effort_{e}" for e in (META.get("supported_efforts") or []) if e != "none"]
    efforts = [e for e in declared if e in SHAPES] or [s for s in SHAPES if s.startswith("effort_")]
    if len(efforts) >= 2:
        # Declared order runs strongest-first (max, high, low); reverse it so the ladder reads
        # cheapest-first, which is the direction the numbers should climb.
        rung = list(reversed(efforts))
        print()
        print(f"EFFORT LADDER ({' < '.join(r.replace('effort_', '') for r in rung)}) -- "
              f"rising = the parameter reaches the model, flat = it does not:")
        for p in chosen:
            vals = [rows[(p, r)]["median_reasoning_tokens"] for r in rung]
            if any(v is None for v in vals):
                print(f"  {p:16s} " + "not tested at every rung")
                continue
            rising = all(b >= a for a, b in zip(vals, vals[1:])) and vals[-1] > vals[0]
            flat = len(set(vals)) == 1
            tag = ("rising -> honoured" if rising else
                   "FLAT -> effort not wired through" if flat else
                   "non-monotone, read the numbers")
            print(f"  {p:16s} " + " -> ".join(f"{v:5d}" for v in vals) + f"   {tag}")

    # Price fingerprint. Service tiers of one provider are the SAME model at 1x / 2x / 4x,
    # so cost is the only evidence of which endpoint answered -- the response says "OpenAI"
    # either way. This is the technique that caught Phala in August, used here to confirm
    # that routing on a full tag actually reached the tier we asked for.
    print()
    print("realized price (confirms which endpoint answered):")
    for p in chosen:
        cs = [c for c in calls if c["provider"] == p and not c["error"] and c["cost"]]
        if not cs:
            print(f"  {p:22s} no billed call")
            continue
        ptok = sum(c.get("prompt_tokens") or 0 for c in cs)
        ctok = sum(c.get("completion_tokens") or 0 for c in cs)
        tot = sum(c["cost"] for c in cs)
        listed = price.get(p, 0)
        # completion dominates; report $/M out implied by the bill at the listed in:out ratio
        implied = tot / (ctok / 1e6) if ctok else 0
        flag = "" if not listed else ("  <-- matches listed" if abs(implied - listed) / listed < 0.5
                                      else f"  <-- LISTED ${listed:.2f}, BILLED LIKE ANOTHER ENDPOINT")
        print(f"  {p:22s} {ptok:7d} in / {ctok:6d} out  ${tot:7.4f}  implied ${implied:6.2f}/M out{flag}")

    errs = {c["error"] for c in calls if c["error"]}
    if errs:
        print("\nerrors seen (a rejected shape is a finding, not a bug):")
        for e in sorted(errs):
            print(f"  {e}")
    print(f"\nspent ${_spent:,.3f}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"model": MODEL, "shapes": {k: v[0] for k, v in SHAPES.items()},
                   "reps": REPS, "max_tokens": MAX_TOKENS, "leak_tolerance": LEAK_TOL,
                   "prompt": PROMPT, "spent": _spent,
                   "results": {f"{p}|{s}": {k: v for k, v in r.items() if k != "calls"}
                               for (p, s), r in rows.items()},
                   "calls": calls}, f, indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
