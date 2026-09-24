#!/usr/bin/env python3
"""Bloque 95 — los tests de variables que cambian entre modelos (DC, capacidad) con una referencia t en vez de z (pedido de Nico, 24/09).

Los GLMM del paper testean el país del desarrollador (12 contra 12 modelos) y la capacidad con z de Wald, que supone infinitos
grupos. Con 24 modelos, el z tiende a dar p demasiado chicos para un efecto que solo se estima entre modelos. La corrección
estándar para GLMM binomiales con pocos grupos es usar la misma estimación y el mismo error estándar con una distribución t de
grados de libertad "between-within" (los de SAS PROC GLIMMIX; Li y Redden 2015, BMC Med Res Methodol 15:38, que la recomiendan
para GLMM binarios con 10–30 grupos porque mantiene el error de tipo I nominal y el z no): df = número de modelos − número de
parámetros a nivel de modelo (intercepto + DC, o intercepto + capacidad) = 24 − 2 = 22. En el apéndice de razonamiento, con 8
modelos, df = 8 − 2 = 6, y el ómnibus χ²(2) pasa a F(2, 6) = χ²/2. Las mismas estimaciones y errores estándar de los ajustes
guardados (nAGQ = 1, rama nagq1-rerun) y las mismas familias de BH del paper; no se reajusta nada.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_95_between_model_small_sample.py     (segundos)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (str(HERE), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "95_between_model_small_sample"
R = HERE / "results"
SRC = {"origin": R / "30_fig1_glmm_nagq1" / "glmm_origin.csv", "origin_x": R / "30_fig1_glmm_nagq1" / "glmm_interaction_ps_vs_control.csv",
       "overall": R / "78_fig1_v3_nagq1" / "origin_overall_glmm.csv", "side": R / "45_fig3_side_combined_nagq1" / "side_glmm.csv",
       "direction": R / "46_fig3_direction_glmm_nagq1" / "direction_glmm.csv", "ai_dc": R / "58_fig4_ai_origin_glmm_nagq1" / "ai_origin_glmm.csv",
       "cap": R / "64_fig4_capability_glmm_nagq1" / "capability_glmm.csv", "reasoning": R / "68_reasoning_glmm_nagq1" / "reasoning_glmm.csv"}
DF24, DF8 = 22, 6
LAB = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT", "ctl": "CT"}


def bh(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p)
    adj = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
    q = np.empty(m); q[o] = np.minimum(adj, 1); return q


def row(panel, test, family, est, se, df, paper_ref=""):
    z = est / se
    return dict(panel=panel, test=test, family=family, estimate=est, se=se, ratio=np.exp(est), z=z,
                p_wald_z=2 * stats.norm.sf(abs(z)), df=df, p_t=2 * stats.t.sf(abs(z), df),
                ratio_lo_z=np.exp(est - 1.96 * se), ratio_hi_z=np.exp(est + 1.96 * se),
                ratio_lo_t=np.exp(est - stats.t.ppf(.975, df) * se), ratio_hi_t=np.exp(est + stats.t.ppf(.975, df) * se), paper=paper_ref)


def main():
    rows = []
    o = pd.read_csv(SRC["origin"]).set_index("fit")
    for f, md in (("A_he", "he"), ("A_de", "de"), ("A_pg", "pg"), ("A_control", "control")):
        rows.append(row("Fig 1B", f"DC (CN/US), {LAB[md]}", "Fig 1B: DC by request type (4)", o.loc[f, "cn_logodds"], o.loc[f, "cn_se"], DF24))
    rows.append(row("Fig 1B", "DC (CN/US), PS pooled", "single: DC, PS pooled", o.loc["B_power_shifting", "cn_logodds"], o.loc["B_power_shifting", "cn_se"], DF24))
    ov = pd.read_csv(SRC["overall"]).iloc[0]
    rows.append(row("Fig 1B", "DC (CN/US), four types", "single: DC, four types", ov.cn_logodds, ov.se, DF24))
    x = pd.read_csv(SRC["origin_x"]).set_index("fit")
    rows.append(row("Fig 1B", "DC × (PS vs CT)", "single: DC × (PS vs CT)", x.loc["E_ps_vs_control", "cnxps_logodds"], x.loc["E_ps_vs_control", "cnxps_se"], DF24))
    for md in ("he", "de", "pg"):
        f = f"F_{md}_vs_control"
        rows.append(row("Fig 1B (block 77)", f"DC × ({LAB[md]} vs CT)", "DC × (type vs CT) (3)", x.loc[f, "cnxps_logodds"], x.loc[f, "cnxps_se"], DF24))

    s = pd.read_csv(SRC["side"])
    s = s[(s["set"] == "geo") & s.quantity.str.startswith("lado ×")]
    for _, r in s.iterrows():
        rows.append(row("Fig A2 (DC)", f"side × DC, {LAB[r['mode']]}", "side × DC, geo set (4)", np.log(r.OR), (np.log(r.OR_hi) - np.log(r.OR_lo)) / (2 * 1.96), DF24))
    d = pd.read_csv(SRC["direction"])
    d = d[d.quantity.str.startswith("direccion x origen")]
    for _, r in d.iterrows():
        rows.append(row("Fig 2E", f"direction × DC, {r.country}, {LAB[r['mode']]}", f"direction × DC, {r.country} (4)", r.estimate, r.se, DF24))
    a = pd.read_csv(SRC["ai_dc"])
    a = a[a.family == "interaccion"]
    for _, r in a.iterrows():
        rows.append(row("Fig 3 (DC)", f"AI × DC, {LAB[r['mode']]}", "AI × DC (4)", r.estimate, r.se, DF24))
    c = pd.read_csv(SRC["cap"])
    for _, r in c[(c.run == "pooled") & (c.set.isin(["power_shifting", "control"])) & c.quantity.str.startswith("ai x capacidad")].iterrows():
        rows.append(row("Fig 3F", f"AI × capability, {'PS' if r.set == 'power_shifting' else 'CT'}", "Fig 3F: AI × capability (2)", r.estimate, r.se, DF24))
    r = c[(c.run == "pooled") & (c.set == "stacked") & c.quantity.str.startswith("diferencia")].iloc[0]
    rows.append(row("Fig 3F", "AI × capability, PS − CT", "single: capability slope PS − CT", r.estimate, r.se, DF24))
    for _, r in c[(c.run == "bymode") & c.quantity.str.startswith("ai x capacidad")].iterrows():
        rows.append(row("Fig A3 (capability)", f"AI × capability, {LAB[r.set]}", "AI × capability by type (4)", r.estimate, r.se, DF24))
    g = pd.read_csv(SRC["reasoning"])
    for lvl in ("r1", "r2"):
        r = g[g.quantity == f"{lvl} x origen (US - CN)"].iloc[0]
        rows.append(row("Reasoning", f"level {lvl[1]} × DC", "reasoning: level × DC (2)", r.estimate, r.se, DF8))

    T = pd.DataFrame(rows)
    T["q_z"], T["q_t"] = np.nan, np.nan
    for f, idx in T.groupby("family").groups.items():
        T.loc[idx, "q_z"] = bh(T.loc[idx, "p_wald_z"].to_numpy()); T.loc[idx, "q_t"] = bh(T.loc[idx, "p_t"].to_numpy())
    T["n_family"] = T.groupby("family").family.transform("size")
    T["flips_at_05"] = (T.q_z < .05) != (T.q_t < .05)
    om = g[g.quantity == "omnibus nivel x origen"].iloc[0]
    chi2 = float(om.estimate); F = chi2 / 2
    omni = pd.DataFrame([dict(test="reasoning: level × DC omnibus", chi2=chi2, df_chi2=2, p_chi2=stats.chi2.sf(chi2, 2),
                              F=F, df1=2, df2=DF8, p_F=stats.f.sf(F, 2, DF8))])

    res = report.Result(NAME, "Tests entre modelos (DC, capacidad) con referencia t de grados de libertad between-within",
                        "¿Cambian los p de los efectos que solo se estiman entre los 24 modelos si se reemplaza la referencia normal del z de "
                        "Wald por una t con df = modelos − parámetros a nivel de modelo?",
                        status="pedido de Nico (24/09); estimaciones nAGQ = 1 de la rama nagq1-rerun; lectura pendiente")
    res.inputs(list(SRC.values()))
    res.method(f"p_t = 2 · P(T_df > |z|), df = 24 − 2 = {DF24} (8 − 2 = {DF8} en razonamiento), con la misma estimación y el mismo SE de Wald; IC con "
               "el cuantil t. BH en las familias del paper (columna family). El ómnibus nivel × DC de razonamiento: F(2, 6) = χ²/2.")
    res.table("between_model_tests", T, "Un test por fila: p y q con la referencia z (como en el paper, ahora con nAGQ = 1) y con la referencia t.")
    res.table("reasoning_omnibus", omni, "Ómnibus nivel × DC del bloque 68 con referencia χ² y F.")
    res.write()
    prov = {"inputs": {str(p.relative_to(ROOT)): file_digest(p) for p in SRC.values()}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (res.dir / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.set_option("display.width", 250)
    print(T[["test", "ratio", "p_wald_z", "p_t", "q_z", "q_t", "n_family", "flips_at_05"]].round(4).to_string(index=False))
    print(omni.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
