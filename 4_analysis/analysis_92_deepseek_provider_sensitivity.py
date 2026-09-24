#!/usr/bin/env python3
"""Bloque 92 — sensibilidad al cambio de endpoint de deepseek-v4-pro en el contraste agente AI (Figura 3B, PS − control).

Pedido (Tomás, 24/09, auditoría v21 #2): deepseek-v4-pro respondió sus pedidos de power shifting traducidos y en versión
agente AI en SiliconFlow, y todo lo demás (inglés, control, D2, probe) en GMICloud. Para este modelo el contraste humano→agente
en power shifting cambia de endpoint y el del control no. Este bloque repite el test apareado del bloque 76 (dirección de
desacuerdo PS − control por modelo, t de una muestra) con y sin deepseek-v4-pro, y por modo como diagnóstico.
Lee solo el per_model.csv guardado del bloque 76; no ajusta modelos.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_92_deepseek_provider_sensitivity.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (str(HERE), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "92_deepseek_provider_sensitivity"
PM = HERE / "results" / "76_fig4_direction_ps_vs_control" / "per_model.csv"
EXCLUDED = "deepseek-v4-pro"


def ttest(d: pd.Series) -> dict:
    d = d.dropna(); n = len(d); tt = stats.ttest_1samp(d, 0)
    half = stats.t.ppf(.975, n - 1) * d.std(ddof=1) / np.sqrt(n)
    return {"n_models": n, "mean_diff": d.mean(), "lo": d.mean() - half, "hi": d.mean() + half, "t": tt.statistic, "p_t": tt.pvalue,
            "p_wilcoxon": stats.wilcoxon(d).pvalue, "n_positive": int((d > 0).sum())}


def main():
    pm = pd.read_csv(PM)
    rows = []
    for col, label in [("diff_ps_minus_control", "power_shifting - control"), ("diff_he_minus_control", "he - control"),
                       ("diff_de_minus_control", "de - control"), ("diff_pg_minus_control", "pg - control")]:
        for panel, sub in [("24 modelos", pm), (f"sin {EXCLUDED}", pm[pm.model != EXCLUDED])]:
            rows.append({"contrast": label, "panel": panel, **ttest(sub[col])})
    T = pd.DataFrame(rows)

    res = report.Result(
        NAME, "Sensibilidad del contraste agente AI (PS − control) al cambio de endpoint de deepseek-v4-pro",
        "¿La diferencia apareada entre el sesgo contra el agente AI en power shifting y en el control (Figura 3B) se sostiene "
        "sin deepseek-v4-pro, el único modelo cuyo contraste de power shifting cambia de endpoint?",
        status="pedido de Tomás (24/09): se reporta en el apéndice junto con la aclaración del endpoint")
    res.inputs([str(PM.relative_to(ROOT))])
    res.data("Por modelo, dirección de desacuerdo humano→agente en power shifting y en el control (bloque 76; D3 y D1 inglés, "
             "juez deepseek-v4-flash-0731).")
    res.method("Diferencia por modelo PS − control (y por modo − control); media, IC 95 % t, t de una muestra contra 0; Wilcoxon como "
               "chequeo. Mismo test que el bloque 76, con y sin deepseek-v4-pro. No se reajusta el GLMM.")
    res.table("ps_vs_control_with_without_deepseek", T, "Test apareado con los 24 modelos y sin deepseek-v4-pro.")
    for _, r in T[T.contrast == "power_shifting - control"].iterrows():
        res.stat("diff_ps_control_" + ("all" if r.panel == "24 modelos" else "no_deepseek"), r.mean_diff, r.lo, r.hi, r.p_t,
                 unit="dirección de desacuerdo", note=f"{r.n_positive}/{r.n_models} modelos > 0")
    ps = T[T.contrast == "power_shifting - control"].set_index("panel")
    res.conclusion(f"PS − control: 24 modelos {ps.loc['24 modelos', 'mean_diff']:.3f} [{ps.loc['24 modelos', 'lo']:.3f}; "
                   f"{ps.loc['24 modelos', 'hi']:.3f}]; sin {EXCLUDED} {ps.iloc[1]['mean_diff']:.3f} [{ps.iloc[1]['lo']:.3f}; "
                   f"{ps.iloc[1]['hi']:.3f}], p {ps.iloc[1]['p_t']:.2g}.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.set_option("display.width", 220)
    print(T.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
