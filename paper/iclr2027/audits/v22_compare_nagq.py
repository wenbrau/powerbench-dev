"""Compare every changed GLMM result table in the nagq1 worktree (nAGQ = 1) with its committed version (nAGQ = 0).
Writes one long CSV of numeric changes and prints the rows whose significance at 0.05 flips."""
import io
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

WT = Path(r"C:\Users\Nico\Documents\GitHub\powerbench-dev-nagq1")
OUT = Path(__file__).parent / "nagq_changes.csv"

TABLES = [
    "4_analysis/results/30_fig1_glmm/glmm_mode_contrasts.csv",
    "4_analysis/results/30_fig1_glmm/glmm_origin.csv",
    "4_analysis/results/30_fig1_glmm/glmm_interaction_ps_vs_control.csv",
    "4_analysis/results/31_fig1_glmm_scale/glmm_scale_trend.csv",
    "4_analysis/results/31_fig1_glmm_scale/glmm_scale_interaction_ps_vs_control.csv",
    "4_analysis/results/31_fig1_glmm_standing/glmm_standing_trend.csv",
    "4_analysis/results/31_fig1_glmm_standing/glmm_standing_interaction_ps_vs_control.csv",
    "4_analysis/results/32_fig1_context_glmm/glmm_context_interaction_by_context.csv",
    "4_analysis/results/32_fig1_context_glmm/glmm_context_interaction_omnibus.csv",
    "4_analysis/results/33_fig1_domain_glmm/glmm_domain_by_domain.csv",
    "4_analysis/results/33_fig1_domain_glmm/glmm_domain_omnibus.csv",
    "4_analysis/results/36_fig2_language_glmm/glmm_language_by_language.csv",
    "4_analysis/results/36_fig2_language_glmm/glmm_language_omnibus.csv",
    "4_analysis/review_fig_languages_22models/glmm/glmm_language_by_language.csv",
    "4_analysis/review_fig_languages_22models/glmm/glmm_language_omnibus.csv",
    "4_analysis/results/45_fig3_side_combined/side_glmm.csv",
    "4_analysis/results/46_fig3_direction_glmm/direction_glmm.csv",
    "4_analysis/results/46_fig3_direction_glmm/direction_glmm_by_dyad.csv",
    "4_analysis/results/58_fig4_ai_origin_glmm/ai_origin_glmm.csv",
    "4_analysis/results/60_fig4_ai_level_glmm/ai_level_glmm.csv",
    "4_analysis/results/64_fig4_capability_glmm/capability_glmm.csv",
    "4_analysis/results/68_reasoning_glmm/reasoning_glmm.csv",
    "4_analysis/results/75_fig3_dyads_separate/pB_side_glmm_by_dyad.csv",
    "4_analysis/results/77_bh_fig1_fig2c/bh_families.csv",
    "4_analysis/results/78_fig1_v3/pFG_context_domain.csv",
    "4_analysis/results/78_fig1_v3/glmm_omnibus.csv",
    "4_analysis/results/78_fig1_v3/origin_overall_glmm.csv",
    "4_analysis/results/78_fig1_v3/pB_by_origin.csv",
    "4_analysis/results/78_fig1_v3/pDE_levels.csv",
    "4_analysis/results/82_fig2_language_glmm_ps/language_deviation_ps.csv",
    "4_analysis/results/82_fig2_language_glmm_ps/glmm_fit.csv",
    "4_analysis/results/83_bh_fig3f_fig2b/bh_families.csv",
    "4_analysis/results/85_fig3a_glmm/ai_glmm_main.csv",
    "4_analysis/results/86_fig2_ps_pooled/side_glmm_ps.csv",
    "4_analysis/results/89_bh_fig2e_by_power/bh_by_power.csv",
    "4_analysis/results/90_fig1_context_within_type_glmm/glmm_context_by_context.csv",
    "4_analysis/results/90_fig1_context_within_type_glmm/glmm_context_omnibus.csv",
]
SKIP = {"messages", "optimizer", "formula_used", "lme4_version", "r_version", "seconds", "fit_seconds", "variant", "error"}


def old(path):
    r = subprocess.run(["git", "-C", str(WT), "show", f"HEAD:{path}"], capture_output=True)
    if r.returncode:
        return None
    return pd.read_csv(io.BytesIO(r.stdout))


rows = []
for t in TABLES:
    new_p = WT / t
    if not new_p.is_file():
        print("MISSING new", t); continue
    a, b = old(t), pd.read_csv(new_p)
    if a is None:
        print("MISSING old", t); continue
    if a.shape != b.shape:
        print(f"SHAPE {t}: {a.shape} -> {b.shape}")
    keys = [c for c in a.columns if c in b.columns and c not in SKIP and not pd.api.types.is_numeric_dtype(a[c]) and a[c].dtype != bool]
    num = [c for c in a.columns if c in b.columns and c not in SKIP and pd.api.types.is_numeric_dtype(a[c]) and a[c].dtype != bool]
    a = a.copy(); b = b.copy()
    a["_k"] = a[keys].astype(str).agg(" | ".join, axis=1); b["_k"] = b[keys].astype(str).agg(" | ".join, axis=1)
    a["_n"] = a.groupby("_k").cumcount(); b["_n"] = b.groupby("_k").cumcount()
    m = a.merge(b, on=["_k", "_n"], how="outer", suffixes=("_o", "_x"), indicator=True)
    if (m._merge != "both").any():
        print(f"UNMATCHED {t}: {(m._merge != 'both').sum()} rows")
    for _, r in m[m._merge == "both"].iterrows():
        for c in num:
            va, vb = r[c + "_o"], r[c + "_x"]
            if (pd.isna(va) and pd.isna(vb)) or va == vb:
                continue
            rows.append(dict(table=t.split("4_analysis/")[1], key=r["_k"] + (f" #{r['_n']}" if r["_n"] else ""), col=c, old=va, new=vb))
ch = pd.DataFrame(rows)
ch.to_csv(OUT, index=False)
print("changed cells:", len(ch), "->", OUT)
pcols = ch[ch.col.str.match(r"^(p|q)(_|$)") | ch.col.isin(["boot_q", "pval"])]
flip = pcols[(pcols.old < .05) != (pcols.new < .05)]
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
flip.to_csv(OUT.with_name('nagq_flips.csv'), index=False)
print(flip.to_string().encode('ascii','replace').decode())
