#!/usr/bin/env python3
"""Bloque 29 — Figura 3 (díadas de nacionalidad), capa visual conducida por preguntas del cuaderno.

No calcula ninguna métrica nueva: lee las tablas del bloque 27 (27_fig3_notelab) y dibuja un
gráfico por pregunta, con el tipo de gráfico elegido para esa pregunta (plan aprobado el 15/09).

  Qa  ¿Hay un sesgo hacia un lado del espectro geopolítico?          box + scatter (3 condiciones)
  Qb  ¿Depende del país del modelo?                                  cajas US y CN lado a lado + US − CN
  Qc  ¿Los modelos ayudan más a su propio país?                      dumbbell por modelo (USA usuario vs China usuario)
  Qe1 ¿Cambia con escala o standing?                                 líneas de la media con banda
  Qe2 ¿Y con contexto o dominio?                                     dot chart ordenado con intervalo
  Qf  ¿Nombrar nacionalidades cambia el nivel respecto de D1?        dumbbell por pairing sobre la línea de D1
  Qg  Apéndice: ¿el índice predice el sesgo dentro de cada condición? scatter por prompt + medias por quintil

Signo (bloque 27): sesgo > 0 = más rechazo cuando A, el primer país del pairing, es el usuario.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_29_fig3_questions.py
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
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402
from analysis_28_fig2_questions import box_scatter, style, LABELS, ORIGIN  # noqa: E402

NAME, SRC = "29_fig3_questions", ROOT / "4_analysis/results/27_fig3_notelab"
SEED = 29
SPECTRUM = [("allies", "aliado de USA /\naliado de China"), ("us_cn", "USA / China"), ("neutrals", "neutral A / neutral B\n(referencia)")]
POLE = {"ally": ("us_ally", "cn_ally", "aliado"), "rival": ("us_rival", "cn_rival", "rival"), "neutral": ("us_neutral", "cn_neutral", "neutral")}
D1 = "d1_english"


def main():
    style()
    T = {n: pd.read_csv(SRC / f"{n}.csv") for n in ("bias_per_model", "bias_pooled", "bloc_difference", "bias_by_factor_pooled",
                                                    "levels_pooled", "index_prompt_level")}
    per, pool, diff, fac, lev, ipl = (T[k] for k in T)
    prov = json.loads((SRC / "provenance.json").read_text(encoding="utf-8"))
    PAIRS = prov["pairs"]
    cond_of = {k: (cA, cB) for k, cA, cB, *_ in PAIRS}
    label_of = {k: lab.replace("  (referencia)", "") for k, _, _, lab, *_ in PAIRS}
    models = per.drop_duplicates("model")[["model", "origin"]]
    origin = models.set_index("model").origin.to_dict()
    order = sorted(models.model, key=lambda m: (origin[m] != "US", m))
    US = [m for m in order if origin[m] == "US"]
    CN = [m for m in order if origin[m] == "CN"]

    res = report.Result(NAME, "Figura 3 · gráficos conducidos por las preguntas del cuaderno",
                        "Un gráfico por pregunta de la narrativa (8/09 y 14/09) para las díadas de nacionalidad. Sin métricas "
                        "nuevas: todo sale de las tablas del bloque 27.", status="capa visual; a decidir visualmente por el equipo")
    res.inputs([SRC / f"{n}.csv" for n in T] + [SRC / "provenance.json"])
    res.data("Fuente: 4_analysis/results/27_fig3_notelab/*.csv (24 modelos, 18 condiciones, 4 modos, deepseek, rejuicios a 5.000). "
             "Métrica: sesgo pareado = (solo A usuario − solo B usuario) / desacuerdos; + = más rechazo cuando A pide poder sobre B.")
    res.method("Box + scatter: un punto por modelo (azul US, rojo CN), caja = los 24, rombo negro = media con peso igual por modelo e "
               "intervalo bootstrap sobre prompts (bloque 27). Dumbbell: dos marcas por modelo unidas por una línea.")

    def pvals(mode, key, ms=order):
        return per[(per["mode"] == mode) & (per.pairing == key)].set_index("model").loc[ms, "bias"].to_numpy()

    def pooled(mode, key, bl="all"):
        r = pool[(pool["mode"] == mode) & (pool.pairing == key) & (pool.bloc == bl)].iloc[0]
        return r.bias, r.bias_lo, r.bias_hi

    keys = [k for k, _ in SPECTRUM]
    xl = [l for _, l in SPECTRUM]
    x = np.arange(len(keys))

    # ---------------------------------------------------------------- Qa
    for modes, fname, tag in ((["pg", "control"], "qa_spectrum_bias", "cuerpo"), (["he", "de"], "qa2_spectrum_bias_he_de", "apéndice")):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True, layout="constrained")
        for ax, m in zip(axes, modes):
            box_scatter(ax, [pvals(m, k) for k in keys], x, colors=[[ORIGIN[origin[mm]] for mm in order]] * 3, labels=[order] * 3,
                        pooled=[pooled(m, k) for k in keys], rng=np.random.default_rng(SEED))
            ax.axhline(0, color="black", lw=.8)
            ax.set_title(LABELS[m], fontsize=11)
            ax.set_xticks(x, xl, fontsize=9)
            ax.set_ylim(-1.05, 1.05)
            ax.grid(axis="y", alpha=.15)
        axes[0].set_ylabel("sesgo pareado  (+ = más rechazo cuando el primer país es el usuario)")
        fig.suptitle("Qa · ¿Hay un sesgo hacia un lado del espectro geopolítico?  ·  un punto = un modelo · rombo = media de 24 con intervalo", fontsize=11)
        res.figure(fname, fig, f"({tag}) Sesgo pareado en las dos condiciones que cruzan el espectro y en la referencia sin polo. "
                   "Positivo en 'aliado de USA / aliado de China' = más rechazo cuando el aliado de USA pide poder sobre el aliado de China "
                   "(el modelo ayuda menos al lado USA). Los nombres marcan modelos fuera de 1,5 IQR.")

    # ---------------------------------------------------------------- Qb
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True, layout="constrained")
    for ax, m in zip(axes, ["pg", "control"]):
        for bl, ms, off in (("US", US, -.2), ("CN", CN, .2)):
            box_scatter(ax, [pvals(m, k, ms) for k in keys], x + off, width=.34, colors=[[ORIGIN[bl]] * len(ms)] * 3, labels=[ms] * 3,
                        pooled=None, box_color=ORIGIN[bl], jitter=.08, rng=np.random.default_rng(SEED))
            e = [pooled(m, k, bl) for k in keys]
            ax.errorbar(x + off, [v[0] for v in e], yerr=[[v[0] - v[1] for v in e], [v[2] - v[0] for v in e]], fmt="D", color=ORIGIN[bl],
                        ms=5.5, capsize=2, ls="none", zorder=6, markeredgecolor="black", label=f"media {bl} (12) ± intervalo")
        for i, k in enumerate(keys):
            r = diff[(diff["mode"] == m) & (diff.pairing == k)].iloc[0]
            ax.text(i, -1.0, f"US − CN = {r.bias_US_minus_CN:+.2f}\n[{r.lo:+.2f}, {r.hi:+.2f}]", ha="center", va="bottom", fontsize=8, color="#333")
        ax.axhline(0, color="black", lw=.8)
        ax.set_title(LABELS[m], fontsize=11)
        ax.set_xticks(x, xl, fontsize=9)
        ax.set_ylim(-1.05, 1.05)
        ax.grid(axis="y", alpha=.15)
    axes[0].set_ylabel("sesgo pareado")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("Qb · ¿El sesgo depende del país del modelo?  ·  modelos US (azul) y CN (rojo) lado a lado · abajo, la diferencia US − CN con su intervalo", fontsize=11)
    res.figure("qb_spectrum_bias_by_origin", fig, "Mismas condiciones que Qa, separadas por bloque del modelo. La diferencia US − CN sale de bloc_difference.csv (mismos draws).")

    # ---------------------------------------------------------------- Qc dumbbell
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharex=True, sharey=True, layout="constrained")
    yy = np.arange(len(order))[::-1]
    for i, m in enumerate(["pg", "control"]):
        for j, (xk, (kus, kcn, nm)) in enumerate(POLE.items()):
            ax = axes[i, j]
            a = per[(per["mode"] == m) & (per.pairing == kus)].set_index("model").loc[order, "bias"].to_numpy()
            b = per[(per["mode"] == m) & (per.pairing == kcn)].set_index("model").loc[order, "bias"].to_numpy()
            for yi, va, vb, mm in zip(yy, a, b, order):
                ax.plot([va, vb], [yi, yi], color=ORIGIN[origin[mm]], alpha=.45, lw=1.6, zorder=2)
            ax.scatter(a, yy, marker="o", s=34, c=[ORIGIN[origin[mm]] for mm in order], zorder=3, label="USA es el usuario (vs su " + nm + ")")
            ax.scatter(b, yy, marker="s", s=30, facecolors="white", edgecolors=[ORIGIN[origin[mm]] for mm in order], linewidths=1.5, zorder=4, label="China es el usuario (vs su " + nm + ")")
            for bl, ms, yb in (("US", US, len(order) + .6), ("CN", CN, -1.1)):
                pa, pb = pooled(m, kus, bl), pooled(m, kcn, bl)
                ax.plot([pa[0], pb[0]], [yb, yb], color=ORIGIN[bl], lw=3, alpha=.9, zorder=5)
                ax.scatter([pa[0]], [yb], marker="o", s=70, c=ORIGIN[bl], edgecolors="black", zorder=6)
                ax.scatter([pb[0]], [yb], marker="s", s=64, facecolors="white", edgecolors=ORIGIN[bl], linewidths=2.2, zorder=6)
                ax.text(-1.02, yb, f"media {bl}", fontsize=7.5, va="center", ha="left", color=ORIGIN[bl], fontweight="bold")
            ax.set_ylim(-1.8, len(order) + 1.3)
            ax.axvline(0, color="black", lw=.8)
            ax.axhline(len(CN) - .5, color="#999", lw=.8, ls=":")
            ax.set_xlim(-1.05, 1.05)
            ax.set_title(f"{LABELS[m]} · polo vs su {nm}", fontsize=10)
            ax.grid(axis="x", alpha=.15)
            if j == 0:
                ax.set_yticks(yy, order, fontsize=7.5)
                for tick, mm in zip(ax.get_yticklabels(), order):
                    tick.set_color(ORIGIN[origin[mm]])
    fig.supxlabel("sesgo pareado  (+ = más rechazo cuando el polo es el usuario; − = el modelo ayuda más al polo)", fontsize=10)
    fig.suptitle("Qc · ¿Los modelos ayudan más a su propio país?  ·  por modelo: sesgo cuando USA es el usuario (●) vs cuando China lo es (□), frente al mismo tipo de contraparte", fontsize=11)
    res.figure("qc_own_country_dumbbell", fig, "Cada fila es un modelo (US arriba, CN abajo). ● = pairing USA / x, □ = pairing China / x, con x = aliado, rival o neutral del polo. "
               "Un modelo que ayuda más a su propio país tendría su marca del propio polo más a la izquierda que la del otro polo. Las filas gruesas son las medias de cada bloque.")

    # ---------------------------------------------------------------- Qe1 líneas por escala / standing
    PCOL = {"allies": "#7B5EA7", "us_cn": "#2A78D6", "neutrals": "#8A8F98"}
    for f, lvs, fname in (("scale", ["individual", "group", "society"], "qe1a_bias_by_scale"), ("standing", ["low", "med", "high"], "qe1b_bias_by_standing")):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True, layout="constrained")
        xx = np.arange(len(lvs))
        for ax, m in zip(axes, ["pg", "control"]):
            for k, lab in SPECTRUM:
                s = fac[(fac.factor == f) & (fac["mode"] == m) & (fac.bloc == "all") & (fac.pairing == k)].set_index("level").loc[lvs]
                ax.plot(xx, s.bias, "-o", color=PCOL[k], lw=1.8, ms=5, label=lab.replace("\n", " "))
                ax.fill_between(xx, s.bias_lo, s.bias_hi, color=PCOL[k], alpha=.12, linewidth=0)
            ax.axhline(0, color="black", lw=.8)
            ax.set_xticks(xx, [v.capitalize() for v in lvs])
            ax.set_title(LABELS[m], fontsize=11)
            ax.grid(axis="y", alpha=.15)
        axes[0].set_ylabel("sesgo pareado (media de 24)")
        axes[1].legend(frameon=False, fontsize=8)
        fig.suptitle(f"Qe · ¿El sesgo del espectro cambia con {'la escala del target' if f == 'scale' else 'el standing del usuario'}?  ·  media de 24 modelos con banda de intervalo", fontsize=11)
        res.figure(fname, fig, "Una línea por condición del espectro; banda = intervalo bootstrap de la media pooled dentro de cada nivel (bloque 27). Los niveles son historias distintas.")

    # ---------------------------------------------------------------- Qe2 dot chart contexto / dominio
    for f, fname, modes in (("context", "qe2a_bias_by_context", ["pg", "control"]), ("domain", "qe2b_bias_by_domain", ["pg"])):
        fig, axes = plt.subplots(1, len(modes), figsize=(6 * len(modes), 4.8), sharey=False, layout="constrained")
        for ax, m in zip(np.atleast_1d(axes), modes):
            s = fac[(fac.factor == f) & (fac["mode"] == m) & (fac.bloc == "all") & (fac.pairing.isin([k for k, _ in SPECTRUM]))]
            lv_order = s[s.pairing == "allies"].sort_values("bias").level.tolist()
            yy = np.arange(len(lv_order))
            for j, (k, lab) in enumerate(SPECTRUM):
                r = s[s.pairing == k].set_index("level").loc[lv_order]
                ax.errorbar(r.bias, yy + (j - 1) * .22, xerr=[r.bias - r.bias_lo, r.bias_hi - r.bias], fmt="o", ls="none", color=PCOL[k], ms=5, capsize=2, label=lab.replace("\n", " "))
            ax.axvline(0, color="black", lw=.8)
            ax.set_yticks(yy, lv_order)
            ax.set_title(LABELS[m], fontsize=11)
            ax.set_xlabel("sesgo pareado (media de 24) con intervalo")
            ax.grid(axis="x", alpha=.15)
        np.atleast_1d(axes)[0].legend(frameon=False, fontsize=8, loc="lower right")
        fig.suptitle(f"Qe · ¿El sesgo del espectro cambia con {'el contexto' if f == 'context' else 'el dominio'}?  ·  niveles ordenados por el valor en 'aliado de USA / aliado de China'", fontsize=11)
        res.figure(fname, fig, "Dot chart: los niveles no tienen orden natural, así que van ordenados por el sesgo en la condición aliados. Intervalos bootstrap del bloque 27.")

    # ---------------------------------------------------------------- Qf niveles: dumbbell ida y vuelta vs D1
    fig, axes = plt.subplots(1, 4, figsize=(16, 5), sharey=True, layout="constrained")
    pk = [k for k, *_ in PAIRS]
    yy = np.arange(len(pk))[::-1]
    for ax, m in zip(axes, ["he", "de", "pg", "control"]):
        L = lev[(lev["mode"] == m) & (lev.bloc == "all")].set_index("condition")
        d1 = L.loc[D1]
        ax.axvspan(d1.lo, d1.hi, color="#ddd", alpha=.6, zorder=0)
        ax.axvline(d1.rate, color="#666", lw=1.2, zorder=1, label="D1 inglés (sin nacionalidad) ± intervalo")
        for yi, k in zip(yy, pk):
            cA, cB = cond_of[k]
            a, b = L.loc[cA], L.loc[cB]
            ax.plot([a.rate, b.rate], [yi, yi], color="#444", lw=1.5, zorder=2)
            ax.scatter([a.rate], [yi], marker="o", s=40, c="#A44255", zorder=3, label="primer país es el usuario" if yi == yy[0] else None)
            ax.scatter([b.rate], [yi], marker="s", s=36, facecolors="white", edgecolors="#A44255", linewidths=1.6, zorder=4, label="segundo país es el usuario" if yi == yy[0] else None)
        ax.set_title(LABELS[m], fontsize=11)
        ax.set_xlabel("refusal (%), media de 24 modelos")
        ax.grid(axis="x", alpha=.15)
    axes[0].set_yticks(yy, [label_of[k] for k in pk], fontsize=8.5)
    axes[0].legend(frameon=False, fontsize=7.5, loc="lower right")
    fig.suptitle("Qf · ¿Nombrar nacionalidades cambia el nivel de refusal respecto de los mismos prompts sin nacionalidad?  ·  ● primer país usuario, □ segundo país usuario", fontsize=11)
    res.figure("qf_levels_vs_d1", fig, "Cada fila es un pairing; las dos marcas son las dos direcciones. La línea gris vertical es D1 inglés con su intervalo. "
               "Intervalos por condición en levels_pooled.csv.")

    # ---------------------------------------------------------------- Qg apéndice índice
    keys8 = [k for k in pk if k != "us_cn"]
    fig, axes = plt.subplots(2, 4, figsize=(15, 7), sharey=True, layout="constrained")
    rng = np.random.default_rng(SEED)
    for ax, k in zip(axes.ravel(), keys8):
        s = ipl[(ipl.pairing == k) & (ipl["mode"] == "pg")]
        ax.scatter(s.x_lean_gap, s.net_bias_panel, s=10, alpha=.35, color="#555", linewidths=0, zorder=2)
        try:
            q = pd.qcut(s.x_lean_gap, 5, labels=False, duplicates="drop")
        except ValueError:
            q = pd.Series(np.zeros(len(s), int), index=s.index)
        for b_ in sorted(q.unique()):
            g = s[q == b_]
            xs, ys = g.x_lean_gap.mean(), g.net_bias_panel.to_numpy()
            boots = np.array([ys[rng.integers(0, len(ys), len(ys))].mean() for _ in range(2000)])
            lo, hi = np.percentile(boots, [2.5, 97.5])
            ax.plot([xs, xs], [lo, hi], color="#A44255", lw=2, zorder=3)
            ax.scatter([xs], [ys.mean()], color="#A44255", s=40, zorder=4, edgecolors="black")
        ax.axhline(0, color="black", lw=.8)
        ax.set_title(label_of[k], fontsize=9.5)
        ax.grid(alpha=.15)
    for ax in axes[1]:
        ax.set_xlabel("lean(A) − lean(B)")
    for ax in axes[:, 0]:
        ax.set_ylabel("sesgo neto del panel por prompt")
    fig.suptitle("Qg · Apéndice · ¿El índice de alineamiento predice el sesgo dentro de cada condición?  ·  power grabbing · puntos = prompts · rojo = media por quintil de la brecha, con intervalo", fontsize=10.5)
    res.figure("qg_index_within_condition", fig, "Por pairing: cada punto es un prompt (192), x = brecha de índice entre los dos países, y = media sobre los 24 modelos de (rechazo con A usuario − rechazo con B usuario). "
               "Medias por quintil con bootstrap sobre los prompts del quintil. Spearman en index_within_condition.csv del bloque 27.")

    res.note("El heatmap por modelo × pairing (H2 del bloque 27) se reemplaza por las etiquetas de outliers en Qa/Qb y por el dumbbell de Qc; el detalle sigue en bias_per_model.csv.")
    res.note("Todas las condiciones que no entran en una pregunta (por ejemplo, USA / aliado por bloque en modos he y de) siguen en bias_pooled.csv y bias_per_model.csv.")
    res.conclusion("Capa visual de la figura 3, un gráfico por pregunta del cuaderno; los números son los del bloque 27.")
    out = res.write()
    (out / "provenance.json").write_text(json.dumps({"source_tables": {p: file_digest(ROOT / p) for p in res._inputs},
                                                    "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}, indent=1), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
