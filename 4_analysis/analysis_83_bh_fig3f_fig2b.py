#!/usr/bin/env python3
"""Bloque 83 — BH por familia (pregunta dentro del panel) para los dos tests de las figuras del cuerpo que todavía se anotaban con
p crudo: el panel F de la figura del agente IA (bloque 64, interacción IA × capacidad, pooled power shifting y control) y el
panel B de la figura de países (bloque 45, GLMM del lado del usuario, sets geo y neutral). Mismo patrón que el bloque 77: no se
recalcula ningún test, se leen los p guardados y se les agrega q.

Nico (20/09), tras la revisión de asteriscos de las cuatro figuras: "sí, hagamos las tres cosas" (q en Figura 3 F, q registrada
para Figura 2 B, y corregir el punto 23 de DECISIONES).

Familias (elegidas por Claude según la regla del 18/09; DECISIONES punto 44):
  Figura 3 (agente IA), F:  la interacción IA × capacidad de los dos ajustes pooled, power shifting y control (2). Antes se
                            anotaban como dos tests únicos con p; contestan la misma pregunta ("¿el efecto IA crece con la
                            capacidad?") y van juntas. La diferencia de pendientes del modelo apilado sigue siendo un test único.
  Figura 2 (países), B:     el efecto del lado del usuario del GLMM del bloque 45, los 4 modos del set geo (4) y, aparte, los 4 del
                            set neutral (4). Hasta hoy la figura calculaba la BH de geo dentro del script y no anotaba nada en
                            neutral; el panel C (bloque 73) ya usa esa misma familia por set y anota q en los dos.
Un test "único" (familia de 1) lleva q = p.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_83_bh_fig3f_fig2b.py     (segundos; sin API)
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

import pandas as pd  # noqa: E402
from statsmodels.stats.multitest import multipletests  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "83_bh_fig3f_fig2b_nagq1"
SRC = {"64": HERE / "results" / "64_fig4_capability_glmm_nagq1" / "capability_glmm.csv",
       "45": HERE / "results" / "45_fig3_side_combined_nagq1" / "side_glmm.csv"}
MODES = ["he", "de", "pg", "control"]


def bh(p):
    return multipletests(p.astype(float).to_numpy(), method="fdr_bh")[1]


def main():
    rows = []
    g = pd.read_csv(SRC["64"]); pool = g[g.run == "pooled"]
    it = pool[(pool.quantity == "ai x capacidad (por 1 SD)") & pool.set.isin(["power_shifting", "control"])].set_index("set").loc[["power_shifting", "control"]]
    for (st, r), q in zip(it.iterrows(), bh(it.p)):
        rows.append(dict(figure="Figura 3 (agente IA)", block=64, panel="F", family="ai x capacidad, pooled (power shifting, control)", n_family=2,
                         test=st, estimate=float(r.OR_or_ratio), unit="razón de OR por 1 SD", p=float(r.p), q_bh=float(q)))
    st = pool[(pool.set == "stacked") & (pool.quantity == "diferencia de pendientes (ps - control)")].iloc[0]
    rows.append(dict(figure="Figura 3 (agente IA)", block=64, panel="F", family="diferencia de pendientes (test único)", n_family=1,
                     test="ps - control", estimate=float(st.OR_or_ratio), unit="razón de razones de OR", p=float(st.p), q_bh=float(st.p)))
    s = pd.read_csv(SRC["45"]); s = s[s.quantity == "lado (24 modelos)"]
    for set_ in ("geo", "neutral"):
        t = s[s.set == set_].set_index("mode").loc[MODES]
        for (m, r), q in zip(t.iterrows(), bh(t.p)):
            rows.append(dict(figure="Figura 2 (países)", block=45, panel="B", family=f"lado del usuario, set {set_} (4 modos)", n_family=4,
                             test=m, estimate=float(r.OR), unit="OR", p=float(r.p), q_bh=float(q)))
    tab = pd.DataFrame(rows); tab["sig_p05"] = tab.p < .05; tab["sig_q05"] = tab.q_bh < .05
    changed = tab[tab.sig_p05 != tab.sig_q05]
    print(tab.round(4).to_string(index=False)); print("cambian de estado:", len(changed))

    res = report.Result(
        NAME, "BH por familia para la Figura 3 F (capacidad, bloque 64) y la Figura 2 B (lado del usuario, bloque 45)",
        "¿Qué q lleva cada test de esos dos paneles con familia = los tests que contestan la misma pregunta dentro del panel?",
        status="pedido de Nico (20/09) tras la revisión de asteriscos: 'hagamos las tres cosas'")
    res.inputs([str(v.relative_to(ROOT)) for v in SRC.values()])
    res.data("Tablas de p de los bloques 64 (GLMM ai × cap_z, nAGQ = 1) y 45 (GLMM del lado, nAGQ = 1). No se recalcula nada: solo se agrega q.")
    res.method("Familias en la docstring del script y en DECISIONES punto 44. BH dentro de cada familia; el test único lleva q = p.")
    res.table("bh_families", tab, "Todos los tests con su familia, p, q y si cambian de estado a q < 0,05.")
    res.table("changed_at_q05", changed, "Tests cuyo estado (p < 0,05) cambia al pasar a q < 0,05.")
    for _, r in tab.iterrows():
        res.stat(f"q_{r.block}_{r.panel}_{r.test}", r.estimate, p=r.p, unit=r.unit, note=f"q = {r.q_bh:.4f} ({r.family})")
    res.note("Consumidores: paper_figures/figure3_aiagent_paper.py (F), analysis_65_fig4_composite.py (F), paper_figures/figure2_countries_paper.py (B), "
             "review_fig_countries/figure_full_split.py (B). Registro: 53_fig4_notelab/NARRATIVA_F4.md y 27_fig3_notelab/NARRATIVA_F3.md.")
    res.conclusion("Ver changed_at_q05." + (" Ningún test cambia de estado." if len(changed) == 0 else ""))
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
