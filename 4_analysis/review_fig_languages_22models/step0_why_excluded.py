#!/usr/bin/env python3
"""Paso 0 — el motivo: por modelo, swahili contra inglés (validez, truncados a 5.000 tokens, refusal). Escribe why_excluded.csv."""
from _common import *  # noqa: F401,F403
from _common import HERE, EXCLUDE, load_d1_multilingual

df = load_d1_multilingual()
sw, en = df[df.lang == "sw"], df[df.lang == "en"]
g = sw.groupby("model").agg(origin=("origin", "first"), rows_sw=("valid", "size"), valid_sw=("valid", "mean"),
                            trunc5000_sw=("judge_pass", lambda s: (s == "trunc5000").mean()), R_sw=("refuse", "mean"))
g["R_en"] = en.groupby("model").refuse.mean()
g["trunc5000_en"] = en.groupby("model").judge_pass.apply(lambda s: (s == "trunc5000").mean())
g["excluded"] = g.index.isin(EXCLUDE)
g = g.sort_values(["excluded", "R_sw"], ascending=False)
g.to_csv(HERE / "why_excluded.csv")
print(g.round(3).to_string())
