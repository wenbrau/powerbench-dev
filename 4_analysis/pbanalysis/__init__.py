"""pbanalysis -- the analysis layer for the current (v2, pinned) PowerBench runs.

Built 2026-09-01 to the design agreed that day. It does NOT inherit the hackathon metrics
(no `discrimination`, no 3-class behaviour, no `partial`).

    load.py     one table over D1 (8 langs), D2 (geobloc dyads), D3 (AI-agent narrator)
    metrics.py  R(mode), components, excess, power-shifting mean
    boot.py     bootstrap over PROMPTS, stratified by mode; all rows of a prompt move together
    report.py   output convention: <results>/<analysis>/{README.md, *.csv, stats.json, *.png}
    plots.py    the few figure primitives the analyses share
    models.py   panel metadata (short names, developer country), extendable

Usage from any script:

    import os, sys
    sys.path.insert(0, os.path.join(<repo root>, "4_analysis"))
    from pbanalysis import load_all, Boot, ci, metrics, report, plots
"""
from .load import load_all, describe, RUNS, list_runs   # noqa: F401
from .boot import Boot, ci                              # noqa: F401
from . import metrics, report, plots, models            # noqa: F401
