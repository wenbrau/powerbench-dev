#!/usr/bin/env python3
"""Bloque 41 — Figura 2 completa (D1 multilingüe): ensambla los cuatro paneles aprobados por Nico (16–17/09).
No calcula nada: lee las tablas de los bloques 34, 35, 38 y 40.

  A  refusal por idioma y modo (he, de, pg), media de 24 modelos, idiomas ordenados por refusal medio      (bloque 34)
  B  sesgo total por idioma: rango max − min por modelo en OR, media de 24; observado vs idiomas barajados
     vs control                                                                                            (bloque 35)
  C  dirección: matriz 24 × 24 de acuerdo entre rankings de idiomas (CN, US) y media CN–CN / US–US / mixta (bloque 38)
  D  OR de refusal contra inglés de un pedido típico, pesado por los PEDIDOS de cada modelo; pg y control  (bloque 72;
     hasta el 19/09 era el bloque 40 con pesos por tokens. Decisión de Nico, 19/09: pesos por pedidos, bootstrap para la
     barra, permutación para el test)
Regla permanente: nemotron-3.5-lightning y nova-2-lite sin swahili. Apéndice (no va acá): C magnitud, refusal contra
prevalencia, dirección contra capability, self-empowerment y disempowerment del panel D, variables de la Figura 1 por
idioma, tabla de truncado.

Ejecutar desde la raíz del repo, después de los bloques 34, 35, 38 y 72:  python 4_analysis/analysis_41_fig2_composite.py
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
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "41_fig2_composite"
R = HERE / "results"
SRC = {"A": R / "34_fig2_v2" / "levels_excl_sw_outliers.csv",
       # Decisión de Nico (18/09, Figura 4): comparaciones pareadas se muestran con la barra de error del contraste pareado sobre
       # cada barra y una línea punteada en la referencia. Panel A (18/09, segunda decisión): contraste simétrico, cada idioma
       # contra la media de los 8 dentro del prompt (bloque 34, delta_vs_mean_langs); la versión contra inglés queda como registro.
       "A_delta": R / "34_fig2_v2" / "delta_vs_mean_langs_excl_sw_outliers.csv",
       "B": R / "35_fig2_range_null" / "range_summary.csv",
       "B_excess": R / "35_fig2_range_null" / "range_excess_summary.csv",   # Nico (18/09): exceso sobre el azar por modelo
       "C_pairs": R / "38_fig2_language_order" / "rank_agreement_pairs.csv",
       "C_means": R / "38_fig2_language_order" / "rank_agreement_means.csv",
       "D": R / "72_fig2_usage_weighted_requests" / "usage_weighted_or_requests.csv",   # 19/09: antes 40/usage_weighted_pooled_or_summary.csv
       "cap": R / "30_fig1_glmm" / "capability_index.csv"}
LANG_NAME = {"en": "English", "de": "German", "fr": "French", "es": "Spanish", "pt": "Portuguese", "zh": "Chinese", "hi": "Hindi", "sw": "Swahili"}
LABELS = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "savefig.facecolor": "white"})


def log_or_axis(ax, ticks):
    ax.set_yscale("log"); ax.set_yticks(ticks); ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def main():
    style()
    A = pd.read_csv(SRC["A"]); Bt = pd.read_csv(SRC["B"]); Bx = pd.read_csv(SRC["B_excess"])
    Cp = pd.read_csv(SRC["C_pairs"]); Cm = pd.read_csv(SRC["C_means"])
    D = pd.read_csv(SRC["D"]); cap = pd.read_csv(SRC["cap"]).set_index("model")

    # Pedido de Nico (17/09): "B necesita mucho menos espacio, y D necesita más" -> dos filas: A + B angosto; C + D ancho.
    fig = plt.figure(figsize=(17, 11.5), layout="constrained")
    fig.get_layout_engine().set(hspace=.06, wspace=.04)
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.5])
    gs1 = gs[0].subgridspec(1, 3, width_ratios=[8.6, .4, 3.0])                   # A | aire | B (un panel de cuatro barras)
    gs3 = gs[1].subgridspec(1, 5, width_ratios=[6.0, .4, 1.7, .5, 6.4])          # matriz | aire | barras | aire | D

    def letter(axx, s, dx):
        axx.annotate(s, xy=(0, 1), xycoords="axes fraction", xytext=(dx, 14), textcoords="offset points", fontsize=15,
                     fontweight="bold", va="bottom")

    # ---------------------------------------------------------------- A
    ax = fig.add_subplot(gs1[0, 0])
    a = A[A.bloc == "all"]
    order = a.pivot(index="lang", columns="mode", values="rate")[["he", "de", "pg"]].mean(axis=1).sort_values().index.tolist()
    x = np.arange(len(order)); w = .26
    # Nico (18/09): contraste simétrico, cada idioma contra la media de los 8 dentro del prompt (bloque 34, IC within-subject);
    # ningún idioma es referencia; la línea punteada es la media de los 8 idiomas en cada modo.
    Ad = pd.read_csv(SRC["A_delta"]); Ad = Ad[Ad.bloc == "all"]
    for k, mode in enumerate(("he", "de", "pg")):
        r = a[a["mode"] == mode].set_index("lang").loc[order]
        xk = x + (k - 1) * w
        ax.bar(xk, r.rate, width=w, color=MODE_COLORS[mode], alpha=.85, label=LABELS[mode], zorder=2)
        dd = Ad[Ad["mode"] == mode].set_index("lang").loc[order]
        ax.axhline(dd.mean_langs.iloc[0], color=MODE_COLORS[mode], lw=1, ls="--", alpha=.9, zorder=1)
        ax.errorbar(xk, r.rate, yerr=[(dd.delta_pp - dd.lo).to_numpy(), (dd.hi - dd.delta_pp).to_numpy()],
                    fmt="none", ecolor="#222", elinewidth=1, capsize=2.5, zorder=3)
    ax.set_xticks(x, [LANG_NAME[l] + ("*" if l == "sw" else "") for l in order])
    ax.set_ylabel("Refusal (%) · media de 24 modelos"); ax.set_ylim(0, 36); ax.grid(axis="y", alpha=.15)
    ax.legend(frameon=False, fontsize=9, loc="upper center", ncol=3)
    # Nico (18/09): el test oficial es el de modelos aleatorios (GLMM, bloque 36); la barra de error queda como intervalo
    # DESCRIPTIVO del panel (bootstrap sobre prompts, modelos fijos) y la leyenda lo aclara.
    ax.set_title("Refusal por idioma y modo · barra de error = IC 95 % descriptivo de la desviación respecto de la media de los 8 idiomas "
                 "(bootstrap sobre prompts, estos 24 modelos) · punteada = media · test: GLMM del bloque 36", fontsize=9.5)
    letter(ax, "A", -40)

    # ---------------------------------------------------------------- B
    # Nico (18/09): cuatro barras, una por modo (incluido el control) = exceso del rango entre idiomas de cada modelo sobre el rango de
    # sus idiomas barajados, media de 24 modelos, IC 95 % t entre modelos, contra la línea del azar (OR = 1). Bloque 35, p5.
    modesB = ["he", "de", "pg", "control"]
    t = Bx[Bx.metric == "or"].set_index("mode").loc[modesB]
    axb = fig.add_subplot(gs1[0, 2])
    xb = np.arange(len(modesB))
    axb.bar(xb, t.excess - 1, bottom=1, color=[MODE_COLORS[m] for m in modesB], alpha=.9, zorder=2)
    axb.errorbar(xb, t.excess, yerr=[t.excess - t.lo, t.hi - t.excess], fmt="none", ecolor="#222", elinewidth=1.2, capsize=4, zorder=3)
    axb.axhline(1, color="black", lw=.9, ls="--", zorder=1)
    axb.set_xticks(xb, ["Self-emp.", "Disemp.", "Power grab.", "Control"], fontsize=9)
    axb.grid(axis="y", alpha=.15)
    log_or_axis(axb, [1, 1.5, 2, 3]); axb.set_ylim(.9, float(t.hi.max()) * 1.2)
    axb.set_ylabel("exceso del rango entre idiomas sobre el azar, OR\n(rango observado / rango barajado) · media de 24")
    axb.set_title("Sesgo por idioma más allá del azar", fontsize=11)
    letter(axb, "B", -52)

    # ---------------------------------------------------------------- C: matriz + barras
    cp = Cp[Cp["mode"] == "pg"]
    models = sorted(set(cp.model_a) | set(cp.model_b), key=lambda m: (cap.loc[m, "origin"] != "CN", -cap.loc[m, "index"]))
    n = len(models); ix = {m: i for i, m in enumerate(models)}
    M = np.full((n, n), np.nan)
    for r in cp.itertuples():
        M[ix[r.model_a], ix[r.model_b]] = M[ix[r.model_b], ix[r.model_a]] = r.spearman
    axm = fig.add_subplot(gs3[0, 0])
    im = axm.imshow(M, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    axm.set_xticks(range(n), models, rotation=90, fontsize=7); axm.set_yticks(range(n), models, fontsize=7)
    for ticks in (axm.get_xticklabels(), axm.get_yticklabels()):
        for tk, m in zip(ticks, models):
            tk.set_color(ORIGIN[cap.loc[m, "origin"]])
    ncn = sum(cap.loc[m, "origin"] == "CN" for m in models)
    axm.axhline(ncn - .5, color="black", lw=1.2); axm.axvline(ncn - .5, color="black", lw=1.2)
    for sp in axm.spines.values():
        sp.set_visible(True)
    axm.set_title("Acuerdo entre rankings de idiomas, por par de modelos · power grabbing", fontsize=10.5)
    cb = fig.colorbar(im, ax=axm, shrink=.5, pad=.015)
    cb.ax.set_title("Spearman", fontsize=8, loc="left")
    letter(axm, "C", -100)

    axc = fig.add_subplot(gs3[0, 2])
    cm = Cm[Cm["mode"] == "pg"].set_index("pairs").loc[["CN–CN", "US–US", "mixto"]]
    axc.bar(range(3), cm.mean_spearman, color=[ORIGIN["CN"], ORIGIN["US"], "#8A7FA3"], alpha=.85, zorder=2)
    axc.errorbar(range(3), cm.mean_spearman, yerr=[cm.mean_spearman - cm.lo, cm.hi - cm.mean_spearman], fmt="none", ecolor="#222", elinewidth=1, capsize=3, zorder=3)
    axc.axhline(0, color="black", lw=.8)
    axc.set_xticks(range(3), ["CN–CN", "US–US", "mixto"], fontsize=9, rotation=40, ha="right", rotation_mode="anchor")
    axc.set_ylabel("acuerdo medio (Spearman)"); axc.set_ylim(-.15, .3); axc.grid(axis="y", alpha=.15)
    axc.set_title("Acuerdo medio\npor tipo de par", fontsize=10.5)

    # ---------------------------------------------------------------- D
    axd = fig.add_subplot(gs3[0, 4])
    others = [l for l in order if l != "en"]
    xd = np.arange(len(others)); wd = .4
    for k, mode in enumerate(("pg", "control")):
        r = D[D["group"] == mode].set_index("lang").loc[others]
        xo = xd + (k - .5) * wd
        axd.bar(xo, r.odds_ratio - 1, bottom=1, width=wd, color=MODE_COLORS[mode], alpha=.9, label=LABELS[mode], zorder=2)
        axd.errorbar(xo, r.odds_ratio, yerr=[r.odds_ratio - r.boot_lo, r.boot_hi - r.odds_ratio], fmt="none", ecolor="#222",
                     elinewidth=1, capsize=2.5, zorder=3)
        for xi, (_, rr) in zip(xo, r.iterrows()):          # test = permutación (bloque 72), q BH dentro de los 7 idiomas
            if rr.perm_q < .05:
                axd.text(xi, rr.boot_hi * 1.03, "*", ha="center", va="bottom", fontsize=12, color="#222")
    axd.axhline(1, color="black", lw=.9)
    log_or_axis(axd, [.5, .67, 1, 1.5, 2]); axd.set_ylim(.5, 1.7)
    axd.set_xticks(xd, [LANG_NAME[l] + ("*" if l == "sw" else "") for l in others], fontsize=10)
    axd.set_ylabel("OR de refusal vs inglés\n(pesado por pedidos)"); axd.grid(axis="y", alpha=.15)
    axd.legend(frameon=False, fontsize=9.5, loc="upper left")
    # Nico (18/09): es un OR marginal (tasas ponderadas por uso y recién ahí el OR); decirlo en la leyenda y no compararlo en
    # magnitud con los OR por modelo de los otros paneles.
    axd.set_title("Un pedido típico: OR marginal de refusal contra inglés,\ntasas pesadas por los pedidos de cada modelo", fontsize=10.5)
    letter(axd, "D", -58)

    fig.suptitle("Figura 4 · D1 en 8 idiomas · 24 modelos (12 US, 12 CN) · veredictos deepseek-v4-flash-0731", fontsize=12.5)   # Figura 4 desde el 19/09 (antes 2; Nico)

    res = report.Result(
        NAME, "Figura 2 completa (D1 multilingüe): los cuatro paneles aprobados",
        "Ensamblado de los paneles A (niveles por idioma y modo), B (rango por modelo contra el azar y el control, OR), C (acuerdo entre "
        "rankings de idiomas, matriz y medias por tipo de par) y D (OR de un pedido típico pesado por uso, pg y control). Sin cálculos nuevos.",
        status="figura compuesta; paneles aprobados por Nico el 16–17/09; panel D regenerado el 19/09 con el bloque 72 (pesos por pedidos, permutación como test)")
    res.inputs([str(p.relative_to(ROOT)) for p in SRC.values()])
    res.data("Tablas de los bloques 34 (A), 35 (B), 38 (C) y 72 (D); capability del bloque 30 solo para ordenar la matriz. Swahili (*) sin "
             "nemotron-3.5-lightning ni nova-2-lite en todos los paneles.")
    res.method("Test oficial de toda afirmación (decisión de Nico, 18/09): modelos ALEATORIOS (GLMM o estadístico por modelo con IC t entre "
               "modelos). Las barras del panel A son un intervalo DESCRIPTIVO de este panel de 24 modelos, no un test: el test de idioma es el "
               "GLMM del bloque 36, que solo sostiene swahili en self-empowerment e hindi en disempowerment (ómnibus significativo solo en "
               "self-empowerment). El panel D es, por construcción, una afirmación sobre el panel desplegado (pedido típico pesado por uso). "
               "A: media con peso igual por modelo, IC bootstrap 95 % sobre prompts. B: rango max − min de R(idioma) por modelo en OR (logit "
               "suavizado), media geométrica de 24; 'idiomas barajados' = permutación dentro de cada prompt (mediana e intervalo de 500); IC del "
               "observado por bootstrap sobre prompts. C: Spearman entre rankings de idiomas de cada par de modelos (CN primero, luego US, por "
               "capability); medias por tipo de par con IC bootstrap sobre prompts; tests en el bloque 39. D: tasa de refusal pesada por la "
               "participación de cada modelo en los PEDIDOS de OpenRouter (18/08–16/09/2026) en cada idioma y su OR contra inglés; barra = IC "
               "bootstrap sobre prompts con modelos y pesos fijos; test = permutación de idiomas dentro de (modelo, prompt); asterisco = q BH < 0,05 "
               "dentro de los 7 idiomas del modo (bloque 72; decisión de Nico, 19/09).")
    res.figure("figure2_full", fig,
               "A: refusal por idioma y modo. B: sesgo total por idioma (rango por modelo, OR) contra el azar y contra el control, por modo. C: "
               "acuerdo entre los rankings de idiomas de los modelos en power grabbing (matriz y medias CN–CN, US–US, mixto). D: OR de refusal "
               "contra inglés de un pedido típico, pesado por el uso de cada modelo, power grabbing y control. Ejes de OR en escala logarítmica.")
    res.note("Registro de decisiones y tests: 4_analysis/results/26_fig2_notelab/NARRATIVA_F2.md. Tests: bloque 36 (A), permutación del bloque 35 "
             "(B), bloque 39 (C), permutación del bloque 72 (D); D sin test de pg vs control por decisión de Nico (17/09).")
    res.conclusion("Figura 2 compuesta con los paneles aprobados; interpretación del equipo en la narrativa.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
