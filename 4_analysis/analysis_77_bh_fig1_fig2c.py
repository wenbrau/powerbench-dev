#!/usr/bin/env python3
"""Bloque 77 — BH por familia (pregunta dentro del panel) para los tests que no la tenían: Figura 1 (bloques 30 y 31: modos,
origen, escala, standing) y el panel C de la figura de idioma (bloque 39: acuerdo entre rankings de idiomas).

Regla del paper (Nico, 18/09): Benjamini-Hochberg dentro de cada familia, y una familia es el conjunto de tests que contestan
la misma pregunta dentro de un panel. Nico (19/09): "hay que correr lo de BH para los bloques que faltan, con las familias por
pregunta como siempre hicimos". Este bloque no recalcula ningún test: lee los p de los bloques 30, 31 y 39 y les agrega q.

Familias (elegidas por Claude según la regla; anotadas en DECISIONES_A_REVISAR.md, punto 37):
  Figura 1, modos (30):        los 2 contrastes de − he y pg − de.
  Figura 1, origen (30):       los 4 efectos principales CN − US por modo; aparte, las 3 interacciones CN × (modo vs control)
                               por modo; el pooled de power shifting (efecto y su interacción) como tests únicos.
  Figura 1, escala (31):       las 4 pendientes por modo; aparte, las 3 interacciones (pendiente × modo vs control); pooled solo.
  Figura 1, standing (31):     ídem escala.
  Idioma C (39):               por pregunta y sobre los 4 modos: "dentro − mixto" (4); "CN–CN − mixto" y "US–US − mixto" (8);
                               "todos los pares" contra idiomas barajados (4); "CN–CN", "US–US" y "mixto" contra idiomas barajados (12).
                               Los p del bloque 39 son unilaterales (p_right), como los definió ese bloque.
Un test "único" (familia de 1) lleva q = p.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_77_bh_fig1_fig2c.py     (segundos; sin API)
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

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "77_bh_fig1_fig2c_nagq1"
R = HERE / "results"
SRC = {"modes": R / "30_fig1_glmm_nagq1" / "glmm_mode_contrasts.csv",
       "origin": R / "30_fig1_glmm_nagq1" / "glmm_origin.csv",
       "origin_x": R / "30_fig1_glmm_nagq1" / "glmm_interaction_ps_vs_control.csv",
       "scale": R / "31_fig1_glmm_scale_nagq1" / "glmm_scale_trend.csv",
       "scale_x": R / "31_fig1_glmm_scale_nagq1" / "glmm_scale_interaction_ps_vs_control.csv",
       "standing": R / "31_fig1_glmm_standing_nagq1" / "glmm_standing_trend.csv",
       "standing_x": R / "31_fig1_glmm_standing_nagq1" / "glmm_standing_interaction_ps_vs_control.csv",
       "order": R / "39_fig2_order_stats" / "order_agreement_tests.csv"}
MODES = ["he", "de", "pg", "control"]


def bh(p):
    p = np.asarray(p, float); m = len(p); order = np.argsort(p); q = np.empty(m); prev = 1.0
    for rank, i in zip(range(m, 0, -1), order[::-1]):
        prev = min(prev, p[i] * m / rank); q[i] = prev
    return q


def rows_from(df, block, panel, family, key_col, est_col, p_col, keys, labels=None, single=False):
    out = []
    for k in keys:
        r = df[df[key_col] == k].iloc[0]
        out.append(dict(figure=panel.split(" · ")[0], block=block, panel=panel, family=family, test=labels[k] if labels else str(k),
                        estimate=float(r[est_col]), p=float(r[p_col]), singular=bool(r["singular"]) if "singular" in df.columns else np.nan,
                        n_family=1 if single else len(keys)))
    return out


def main():
    d = {k: pd.read_csv(v) for k, v in SRC.items()}
    L = {"A_he": "he", "A_de": "de", "A_pg": "pg", "A_control": "control", "B_power_shifting": "power shifting (pooled)",
         "F_he_vs_control": "he vs control", "F_de_vs_control": "de vs control", "F_pg_vs_control": "pg vs control",
         "E_ps_vs_control": "power shifting vs control (pooled)"}
    fam = []
    # ---- Figura 1
    fam += rows_from(d["modes"], "30", "Figura 1 · A modos", "contrastes de modo (2)", "fit", "m2_logodds", "m2_p", ["he_vs_de", "de_vs_pg"],
                     {"he_vs_de": "de − he", "de_vs_pg": "pg − de"})
    fam += rows_from(d["origin"], "30", "Figura 1 · origen", "efecto CN − US por modo (4)", "fit", "cn_logodds", "cn_p", ["A_he", "A_de", "A_pg", "A_control"], L)
    fam += rows_from(d["origin"], "30", "Figura 1 · origen", "efecto CN − US, pooled (1)", "fit", "cn_logodds", "cn_p", ["B_power_shifting"], L, single=True)
    fam += rows_from(d["origin_x"], "30", "Figura 1 · origen", "interacción CN × (modo vs control) por modo (3)", "fit", "cnxps_logodds", "cnxps_p",
                     ["F_he_vs_control", "F_de_vs_control", "F_pg_vs_control"], L)
    fam += rows_from(d["origin_x"], "30", "Figura 1 · origen", "interacción CN × (power shifting vs control), pooled (1)", "fit", "cnxps_logodds", "cnxps_p",
                     ["E_ps_vs_control"], L, single=True)
    for dim in ("scale", "standing"):
        P = f"Figura 1 · {'C escala' if dim == 'scale' else 'D standing'}"
        fam += rows_from(d[dim], "31", P, f"pendiente de {dim} por modo (4)", "fit", "x_logodds", "x_p", ["A_he", "A_de", "A_pg", "A_control"], L)
        fam += rows_from(d[dim], "31", P, f"pendiente de {dim}, pooled (1)", "fit", "x_logodds", "x_p", ["B_power_shifting"], L, single=True)
        fam += rows_from(d[f"{dim}_x"], "31", P, f"interacción {dim} × (modo vs control) por modo (3)", "fit", "xxps_logodds", "xxps_p",
                         ["F_he_vs_control", "F_de_vs_control", "F_pg_vs_control"], L)
        fam += rows_from(d[f"{dim}_x"], "31", P, f"interacción {dim} × (power shifting vs control), pooled (1)", "fit", "xxps_logodds", "xxps_p",
                         ["E_ps_vs_control"], L, single=True)
    # ---- idioma, panel C (bloque 39): p unilaterales p_right, como los definió el bloque
    o = d["order"]
    groups = {"mismo origen − mixto, por modo (4)": ["dentro − mixto"],
              "cada bloque − mixto, por modo (8)": ["CN–CN − mixto", "US–US − mixto"],
              "orden compartido, todos los pares, por modo (4)": ["todos los pares"],
              "cada tipo de par contra idiomas barajados, por modo (12)": ["CN–CN", "US–US", "mixto"]}
    for family, stats_ in groups.items():
        sub = o[o.statistic.isin(stats_)]
        for _, r in sub.iterrows():
            fam.append(dict(figure="Figura de idioma (4 del paper)", block="39", panel="idioma · C acuerdo entre rankings", family=family,
                            test=f"{r.statistic} · {r['mode']}", estimate=float(r.observed), p=float(r.p_right), singular=np.nan, n_family=len(sub)))
    tab = pd.DataFrame(fam)
    tab["q_bh"] = np.nan
    for (panel, family), sub in tab.groupby(["panel", "family"], sort=False):
        tab.loc[sub.index, "q_bh"] = bh(sub.p.values)
    tab["sig_p05"] = tab.p < .05; tab["sig_q05"] = tab.q_bh < .05
    changed = tab[tab.sig_p05 != tab.sig_q05]
    print(tab[["panel", "family", "test", "estimate", "p", "q_bh", "n_family", "singular"]].round(4).to_string(index=False))
    print("\ncambian de estado al corregir:"); print(changed[["panel", "family", "test", "p", "q_bh"]].round(4).to_string(index=False), flush=True)

    res = report.Result(
        NAME, "BH por familia para los tests de la Figura 1 (bloques 30, 31) y del panel C de idioma (bloque 39)",
        "¿Qué tests de la Figura 1 (modos, origen, escala, standing) y del acuerdo entre rankings de idiomas sobreviven la corrección de "
        "Benjamini-Hochberg con familia = los tests que contestan la misma pregunta dentro del panel?",
        status="pedido de Nico (19/09): BH con familias por pregunta para los bloques que no la tenían; sin recalcular ningún test")
    res.inputs([str(v.relative_to(ROOT)) for v in SRC.values()])
    res.data("Tablas de p de los bloques 30, 31 y 39 (GLMM con nAGQ = 1 en 30 y 31; permutaciones en 39). No se recalcula nada: solo se agrega q.")
    res.method("Familias en la docstring del script y en DECISIONES punto 37. BH dentro de cada familia; los tests únicos (pooled) llevan q = p. "
               "En el bloque 39 se corrige p_right (unilateral), tal como lo definió ese bloque.")
    res.table("bh_families", tab, "Todos los tests con su familia, p, q y si cambian de estado a q < 0,05.")
    res.table("changed_at_q05", changed, "Tests cuyo estado (p < 0,05) cambia al pasar a q < 0,05.")
    for _, r in changed.iterrows():
        res.stat(f"changed_{r.block}_{r.test}", r.estimate, p=r.p, unit="log-odds o Spearman", note=f"q = {r.q_bh:.3f} ({r.family})")
    res.note("Registro: 25_fig1_notelab/NARRATIVA_F1.md (Figura 1) y 26_fig2_notelab/NARRATIVA_F2.md (panel C de idioma).")
    res.conclusion("Ver changed_at_q05. Las lecturas del cuerpo que dependan de un test que cambie de estado se revisan con Nico.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
