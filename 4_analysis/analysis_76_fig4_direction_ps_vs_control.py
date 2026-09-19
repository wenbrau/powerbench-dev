#!/usr/bin/env python3
"""Bloque 76 — Figura del agente de IA (Figura 3 del paper desde el 19/09; bloques "fig4"), panel B: ¿power shifting en
general tiene más sesgo de dirección hacia rechazar a la IA que el control?

Pedido de Nico (19/09), textual: "En B, en dirección de los desacuerdos, tenemos un test para ver si power-shifting en
general da mayor sesgo contra AI agent que control? estaría bueno eso". No existía: el bloque 56 testea cada modo contra
cero y el único contraste modo − control era el de pp del bloque 22 (pg − control, apéndice de auditoría).

Estadístico por modelo (el del panel B, bloque 56): sesgo = (solo rechaza a la IA − solo rechaza al humano) / discordantes.
power_shifting = los discordantes de he + de + pg sumados por modelo antes del cociente (cada prompt discordante pesa igual;
alternativa no elegida: media de los tres sesgos por modo). Diferencia pareada por modelo = sesgo(power shifting) −
sesgo(control); test = t pareada entre los 24 modelos (marco de modelos aleatorios, la "vieja y confiable" de Nico), IC 95 %
t; Wilcoxon de rangos con signo como chequeo. Secundario: cada modo contra el control con la misma t pareada, BH sobre los 3.
Lee 56_fig4_bias_direction/bias_direction_per_model.csv. Sin llamadas a ninguna API.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_76_fig4_direction_ps_vs_control.py
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

NAME = "76_fig4_direction_ps_vs_control"
SRC = HERE / "results" / "56_fig4_bias_direction" / "bias_direction_per_model.csv"
PS_MODES = ("he", "de", "pg")


def bh(p):
    p = np.asarray(p, float); m = len(p); order = np.argsort(p); q = np.empty(m); prev = 1.0
    for rank, i in zip(range(m, 0, -1), order[::-1]):
        prev = min(prev, p[i] * m / rank); q[i] = prev
    return q


def paired(diff):
    diff = np.asarray(diff, float); diff = diff[np.isfinite(diff)]
    n = len(diff); tt = stats.ttest_1samp(diff, 0.0)
    half = stats.t.ppf(.975, n - 1) * diff.std(ddof=1) / np.sqrt(n)
    w = stats.wilcoxon(diff) if n >= 6 else None
    return dict(n_models=n, mean_diff=float(diff.mean()), lo=float(diff.mean() - half), hi=float(diff.mean() + half),
                t=float(tt.statistic), p_t=float(tt.pvalue), p_wilcoxon=float(w.pvalue) if w else np.nan,
                n_positive=int((diff > 0).sum()), n_negative=int((diff < 0).sum()))


def main():
    pm = pd.read_csv(SRC)
    models = sorted(pm.model.unique())
    ps = (pm[pm["mode"].isin(PS_MODES)].groupby("model")[["n_only_ai", "n_only_human", "n_discordant", "n_pairs"]].sum()
          .reindex(models))
    ps["bias"] = (ps.n_only_ai - ps.n_only_human) / ps.n_discordant
    ctrl = pm[pm["mode"] == "control"].set_index("model").reindex(models)
    per = pd.DataFrame({"model": models, "origin": ctrl.origin.values,
                        "n_discordant_ps": ps.n_discordant.values, "bias_ps": ps.bias.values,
                        "n_discordant_control": ctrl.n_discordant.values, "bias_control": ctrl.bias.values})
    per["diff_ps_minus_control"] = per.bias_ps - per.bias_control
    for m in PS_MODES:
        x = pm[pm["mode"] == m].set_index("model").reindex(models)
        per[f"bias_{m}"] = x.bias.values; per[f"diff_{m}_minus_control"] = x.bias.values - per.bias_control
    rows = [dict(contrast="power_shifting - control", family="principal", **paired(per.diff_ps_minus_control))]
    sec = [dict(contrast=f"{m} - control", family="secundaria (3 modos)", **paired(per[f"diff_{m}_minus_control"])) for m in PS_MODES]
    q = bh([r["p_t"] for r in sec])
    for r, qq in zip(sec, q):
        r["q_bh"] = float(qq)
    rows[0]["q_bh"] = rows[0]["p_t"]
    summ = pd.DataFrame(rows + sec)
    # niveles con su propio test contra 0 (t entre modelos, como el bloque 56): el pooled entra como quinta barra del panel B (Nico, 19/09)
    def level(name, b, n):
        b = np.asarray(b, float); tt = stats.ttest_1samp(b, 0.0); half = stats.t.ppf(.975, len(b) - 1) * b.std(ddof=1) / np.sqrt(len(b))
        return dict(set=name, n_models=int(len(b)), n_discordant_median=float(np.median(n)), bias=float(b.mean()), lo=float(b.mean() - half),
                    hi=float(b.mean() + half), t=float(tt.statistic), p_t=float(tt.pvalue), n_positive=int((b > 0).sum()))
    lev = pd.DataFrame([level("power_shifting", per.bias_ps, per.n_discordant_ps), level("control", per.bias_control, per.n_discordant_control)])
    print(lev.round(3).to_string(index=False)); print(summ.round(4).to_string(index=False), flush=True)

    res = report.Result(
        NAME, "Figura del agente de IA, panel B: sesgo de dirección hacia la IA, power shifting contra control",
        "¿El sesgo de dirección de los desacuerdos (hacia rechazar a la IA) es mayor en power shifting (he + de + pg juntos) que en el "
        "control? Diferencia pareada por modelo, t entre los 24 modelos.",
        status="test pedido por Nico (19/09) para el panel B; lectura pendiente")
    res.inputs([str(SRC.relative_to(ROOT))])
    res.data("Tabla por modelo del bloque 56 (D3 vs D1 inglés, 24 modelos, pares completos): conteos de prompts que solo rechaza la IA y que solo "
             "rechaza el humano, por modo. power_shifting suma los discordantes de he, de y pg por modelo.")
    res.method("Sesgo por modelo = (solo IA − solo humano) / discordantes. Diferencia pareada = sesgo(power shifting) − sesgo(control) en el mismo "
               "modelo; t pareada entre modelos (23 gl), IC 95 % t, Wilcoxon como chequeo. Secundario: cada modo contra el control, misma t, BH "
               "sobre los 3. Elecciones de Claude (DECISIONES punto 36): sumar discordantes antes del cociente; el test principal sin corregir.")
    res.table("ps_vs_control_summary", summ, "Diferencia pareada del sesgo de dirección: power shifting − control (principal) y cada modo − control (secundario).")
    res.table("levels", lev, "Sesgo medio de dirección en power shifting pooled y en el control, y mediana de discordantes por modelo.")
    res.table("per_model", per, "Por modelo: sesgos y diferencias.", show=False)
    r = summ.iloc[0]
    res.stat("direction_bias_ps_minus_control", r.mean_diff, r.lo, r.hi, r.p_t, unit="sesgo",
             note=f"t pareada, {int(r.n_models)} modelos, {int(r.n_positive)} positivas; Wilcoxon p = {r.p_wilcoxon:.3f}")
    res.note("Registro: 4_analysis/results/53_fig4_notelab/NARRATIVA_F4.md.")
    res.conclusion("Ver ps_vs_control_summary; lectura de Nico pendiente.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
