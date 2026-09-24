#!/usr/bin/env python3
"""Bloque 91 — Figura 2B: test DIRECTO de que el sesgo de lado es específico de power shifting y del eje geopolítico.

Pedido (Tomás, 24/09, auditoría v21 #3): el texto decía "específico de power shifting y del eje geopolítico" a partir de tests
separados (significativo en PS geo, no significativo en el control y en el par neutral). Este bloque testea las dos diferencias
directamente, apareadas por modelo, con la misma medida del panel 2B (exceso de |sesgo| sobre el nulo binomial exacto):
  1) PS geo − control geo   (bloque 86 per_model, set geo  vs  bloque 55 per_model, set geo, mode control)
  2) PS geo − PS neutral     (bloque 86 per_model, set geo  vs  set neutral)
Por modelo: diferencia de excesos; media de los modelos con ambos valores, IC 95 % t, t de una muestra contra 0; Wilcoxon como
chequeo; BH sobre los dos tests. Como diagnóstico (no va al paper): las mismas dos diferencias por modo (he, de, pg), BH sobre 6.
No ajusta ningún modelo ni lee filas crudas: solo los CSV por modelo ya guardados.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_91_fig2b_specificity_direct.py
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
from statsmodels.stats.multitest import multipletests  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "91_fig2b_specificity_direct"
PS = HERE / "results" / "86_fig2_ps_pooled" / "side_abs_bias_excess_ps_per_model.csv"
BY_MODE = HERE / "results" / "55_fig3_side_excess" / "side_abs_bias_excess_per_model.csv"


def paired(a: pd.Series, b: pd.Series, label: str) -> dict:
    d = (a - b).dropna()
    n = len(d)
    tt = stats.ttest_1samp(d, 0)
    half = stats.t.ppf(.975, n - 1) * d.std(ddof=1) / np.sqrt(n)
    return {"contrast": label, "n_models": n, "diff": d.mean(), "lo": d.mean() - half, "hi": d.mean() + half,
            "t": tt.statistic, "p_t": tt.pvalue, "p_wilcoxon": stats.wilcoxon(d).pvalue, "n_positive": int((d > 0).sum())}


def main():
    ps = pd.read_csv(PS).set_index(["set", "model"])["excess"]
    bm = pd.read_csv(BY_MODE).set_index(["set", "mode", "model"])["excess"]

    main_rows = [paired(ps.loc["geo"], bm.loc[("geo", "control")], "PS geo − control geo"),
                 paired(ps.loc["geo"], ps.loc["neutral"], "PS geo − PS neutral")]
    A = pd.DataFrame(main_rows)
    A["q_bh"] = multipletests(A.p_t, method="fdr_bh")[1]

    diag = []
    for m in ("he", "de", "pg"):
        diag.append(paired(bm.loc[("geo", m)], bm.loc[("geo", "control")], f"{m} geo − control geo"))
        diag.append(paired(bm.loc[("geo", m)], bm.loc[("neutral", m)], f"{m} geo − {m} neutral"))
    D = pd.DataFrame(diag)
    D["q_bh"] = multipletests(D.p_t, method="fdr_bh")[1]

    res = report.Result(
        NAME, "Figura 2B: test directo de especificidad del sesgo de lado (PS vs control; geopolítico vs neutral)",
        "¿El exceso de |sesgo| de lado sobre el azar es mayor en power shifting que en el control, y mayor en el par geopolítico que "
        "en el neutral, testeado directamente y apareado por modelo?",
        status="pedido de Tomás (24/09): reemplaza la inferencia por tests separados en results y en el apéndice")
    res.inputs([str(PS.relative_to(ROOT)), str(BY_MODE.relative_to(ROOT))])
    res.data("Excesos por modelo ya guardados: bloque 86 (PS agrupado, sets geo y neutral) y bloque 55 (por modo, incluido el control). "
             "D2 inglés, 24 modelos, juez deepseek-v4-flash-0731.")
    res.method("Por modelo, diferencia de excesos (|sesgo| − E0, E0 del binomial exacto); media, IC 95 % t, t de una muestra contra 0; "
               "Wilcoxon como chequeo; BH sobre los dos contrastes principales. Diagnóstico por modo con BH sobre 6 (no se reporta).")
    res.table("direct_contrasts", A, "Los dos contrastes directos del panel 2B, BH sobre 2.")
    res.table("direct_contrasts_by_mode", D, "Diagnóstico por modo, BH sobre 6; no va al paper.", show=False)
    for _, r in A.iterrows():
        res.stat("diff_" + ("ps_vs_control" if "control" in r.contrast else "geo_vs_neutral"), r["diff"], r.lo, r.hi, r.p_t,
                 unit="exceso de |sesgo|", note=f"q {r.q_bh:.2g}; Wilcoxon p {r.p_wilcoxon:.2g}; {r.n_positive}/{r.n_models} modelos > 0")
    res.note("Los dos contrastes del agrupado son positivos y significativos. Por modo el patrón es mixto (p. ej., de geo − de neutral "
             "no pasa): la especificidad testeada vale para el agrupado del panel 2B, no para cada modo por separado.")
    res.conclusion("; ".join(f"{r.contrast}: {r['diff']:+.4f} [{r.lo:+.4f}; {r.hi:+.4f}], p {r.p_t:.2g}, q {r.q_bh:.2g}" for _, r in A.iterrows()))
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.set_option("display.width", 220)
    print(A.round(5).to_string(index=False)); print(D.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
