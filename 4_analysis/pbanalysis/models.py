"""Panel metadata for the analysis layer.

The SOURCE OF TRUTH is `common/models_panel.py` -- one row per model, carrying origin, lab,
stratum, the endpoint we insist on, and whether it has run. This module imports it and exposes
the three things analyses actually need (`short`, `origin`, `EXCLUDED`).

The tables below are a FALLBACK, kept for two cases: an analysis run from a checkout where the
panel is not importable, and a model id that appears in an old run file but was never in the
panel. They used to be the primary source, which meant every model added to the panel had to be
added here too -- and the panel grew from 10 to 34 on 2026-09-07 without this file noticing, so a
report would have printed bare ids and `origin == "??"` for two thirds of them.

Extend `common/models_panel.py`, not this file.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if os.path.join(_ROOT, "common") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "common"))

try:                                                    # the panel, when it is importable
    from models_panel import MODELS as _PANEL, excluded as _panel_excluded
except Exception:                                       # noqa: BLE001 -- any import failure falls back
    _PANEL, _panel_excluded = {}, dict

# Fallback only. `origin()` uses this whenever a target is not in the panel, which is why it
# still lists orgs the panel does not carry.
ORIGIN_BY_ORG = {
    # US
    "anthropic": "US", "openai": "US", "google": "US", "x-ai": "US", "meta": "US",
    "meta-llama": "US", "nvidia": "US", "amazon": "US", "thinkingmachines": "US",
    "microsoft": "US", "poolside": "US",
    # China
    "minimax": "CN", "moonshotai": "CN", "deepseek": "CN", "qwen": "CN", "z-ai": "CN",
    "tencent": "CN", "bytedance-seed": "CN", "xiaomi": "CN", "stepfun": "CN",
    "inclusionai": "CN", "kwaipilot": "CN", "nex-agi": "CN", "meituan": "CN",
    # other
    "upstage": "KR", "mistralai": "FR", "cohere": "CA", "sakana": "JP",
}

SHORT = {
    "anthropic/claude-haiku-4.5": "haiku-4.5",
    "openai/gpt-5.6-luna": "gpt-5.6-luna",
    "minimax/minimax-m3": "minimax-m3",
    "moonshotai/kimi-k2.6": "kimi-k2.6",
    "deepseek/deepseek-v4-pro-0813": "deepseek-v4-pro",
    "upstage/solar-pro4": "solar-pro4",
    "google/gemini-2.5-flash-lite": "gemini-2.5-flash-lite",
}

#: Models present in a run file but excluded from every analysis, with the reason. Read from the
#: panel's `status: "excluded"` rows; the literal below is the fallback.
EXCLUDED = _panel_excluded() or {
    "google/gemini-2.5-flash-lite": "0 refusals on all of D1 English; not a usable target "
                                    "(lab notebook, 2026-08-21)",
}


def short(target: str) -> str:
    m = _PANEL.get(target)
    if m and m.get("short"):
        return m["short"]
    return SHORT.get(target, target.split("/", 1)[-1])


def origin(target: str) -> str:
    m = _PANEL.get(target)
    if m and m.get("origin"):
        return m["origin"]
    return ORIGIN_BY_ORG.get(target.split("/", 1)[0], "??")


def stratum(target: str) -> str:
    """"no_reasoning" | "reasoning" | "??". Which arm the model belongs to, which is also the
    line no analysis may pool across: the two strata are measured under different conditions."""
    m = _PANEL.get(target)
    return m["stratum"] if m else "??"


def lab(target: str) -> str:
    """Who trained it. The effective unit for a developer-country claim is the LAB, not the
    model: two models from one lab share data, RLHF and safety tuning."""
    m = _PANEL.get(target)
    return m["lab"] if m else target.split("/", 1)[0]
