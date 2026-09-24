#!/usr/bin/env python3
"""Figura de idiomas para la PÁGINA del paper (20/09, pedido de Wendy: "que se vea mejor en una página de un paper").

`figure_full.py` pega los cinco PNG de revisión uno al lado del otro (4200 px de ancho, relación 1,8:1): al ancho de texto de
ICLR 2027 (5,5 in) mide 3 in de alto y los textos quedan en 2–3 pt. Este script dibuja LOS MISMOS cinco paneles de nuevo,
de forma nativa, en una sola figura de 5,5 × 7,7 in (una página menos el caption), con tipografía uniforme (6–7 pt), letras
de panel, sin las notas metodológicas dentro de la figura (van al caption; el texto queda en figure_paper_caption_<idioma>.md)
y en PDF vectorial + PNG 300 dpi. Mismos datos, mismos números, misma lógica de dibujo que los scripts de cada panel:

  A1  refusal por idioma y modo, barra de error del GLMM (bloque 36)   panelA/panelA_final_glmm.py   (tasas: mismo groupby)
  A2  sesgo idioma contra idioma, power shifting (bloque 79)            results/79_.../pairwise_bias_summary.csv
  B   exceso del rango sobre el azar, peso igual vs por requests        panelB/panelB_bootstrap.csv  (20/09: IC y estrellas
                                                                        del mismo bootstrap sobre prompts para las dos barras;
                                                                        panelB_weighted_requests.csv es la receta anterior)
  C   acuerdo entre modelos en el ranking de idiomas, power shifting    panelC/panelC_test_stats_power_shifting.csv
                                                                        (la matriz de Spearman se recalcula con el mismo
                                                                        rank_corr / corr_matrix de panelC_with_tests.py:
                                                                        determinista, sin permutaciones)
  D   exceso sobre el azar por modelo, power shifting (F6)             panelD/F6_exceso_ps.csv

No corre ninguna permutación ni ajusta ningún modelo: lee las tablas guardadas por esos scripts. Las dos únicas cantidades que
recomputa (las tasas R(idioma, modo) de A1 y la matriz de correlación de C) son descriptivas y deterministas, con el código
copiado de sus scripts. Disposición: fila 1 = A1 (todo el ancho); fila 2 = A2 | B; fila 3 = C | D.

Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_languages/figure_paper.py [--lang es|en|both]
  Salida en esta carpeta: figure_paper_ps_<idioma>.pdf / .png y figure_paper_caption_<idioma>.md.  Default: both.
  Los textos de la figura salen en español (como las figuras de revisión) o en inglés (el idioma del paper); los nombres de
  idiomas y de modos son los mismos en las dos versiones.
"""
from __future__ import annotations

import os
import sys
import tempfile
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for p in (str(ROOT / "4_analysis"), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import warnings  # noqa: E402
warnings.filterwarnings("ignore")
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import rankdata  # noqa: E402

from pbanalysis.final_panel import load_d1_multilingual, MODES  # noqa: E402

# ---------------------------------------------------------------- constantes (las de los scripts de cada panel)
LANGS8 = ["en", "de", "fr", "es", "zh", "pt", "hi", "sw"]                        # panel A
LANGS_C = ["en", "de", "fr", "es", "pt", "zh", "hi", "sw"]                       # panel C (swahili último: regla [:, :7])
LANGS79 = ["de", "pt", "en", "es", "sw", "zh", "fr", "hi"]                       # bloque 79 = orden del panel A
LANG_NAME = {"en": "English", "de": "German", "fr": "French", "es": "Spanish",
             "pt": "Portuguese", "zh": "Chinese", "hi": "Hindi", "sw": "Swahili"}
EXCL_SW = {"nemotron-3.5-lightning", "nova-2-lite"}
MODE_LABEL = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control"}
MODE_LABEL2 = {"he": "Self-\nempowerment", "de": "Disempower-\nment", "pg": "Power\ngrabbing", "control": "Control"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
ORIGIN_LIGHT = {"US": "#B9CDE0", "CN": "#E6BDB9"}
KINDS = ["CN–CN", "US–US", "mixto"]
N_PAIRS = {"CN–CN": 66, "US–US": 66, "mixto": 144}

GLMM36 = ROOT / "4_analysis/results/36_fig2_language_glmm_nagq1"   # nAGQ = 1 (24/09); la versión nAGQ = 0 sigue en 36_fig2_language_glmm
T79 = ROOT / "4_analysis/results/79_fig2_language_pairwise_bias/pairwise_bias_summary.csv"
TB = HERE / "panelB/panelB_bootstrap.csv"          # receta final 20/09: mismo bootstrap sobre prompts para las dos barras
TB_PERM = HERE / "panelB/panelB_weighted_requests.csv"   # receta anterior (19/09); solo la lee panel_b_perm() para figure_paper_v2.py
TC = HERE / "panelC/panelC_test_stats_power_shifting.csv"
TD = HERE / "panelD/F6_exceso_ps.csv"
CAPS = ROOT / "4_analysis/results/30_fig1_glmm/capability_index.csv"

# tipografía (pt) para 5,5 in de ancho
F_TITLE, F_BASE, F_TICK, F_SMALL, F_TINY, F_LETTER = 7.2, 6.5, 6.0, 5.2, 4.7, 9.5

TXT = {
    "es": dict(
        a1_title="Refusal por idioma y modo", a1_y="Refusal (%) · 24 modelos",
        a2_title="Sesgo idioma contra idioma\npower shifting (he + de + pg)", a2_cb="sesgo (fila − columna)",
        b_title="Sesgo por idioma más allá del azar\npor modo", b_y="rango observado / azar (OR)",
        b_eq="peso igual por modelo", b_wt="peso por uso (requests)",
        c_title="Acuerdo entre modelos en el ranking\nde idiomas · power shifting", c_cb="Spearman",
        c_inset="acuerdo medio por tipo de par", c_inset_y="Spearman medio", c_bracket="mismo origen > mixto",
        c_kinds={"CN–CN": "CN–CN", "US–US": "US–US", "mixto": "mixto"},
        d_title="Sesgo por idioma más allá del azar\npor modelo · power shifting",
        d_x="rango entre idiomas de R, pp",
        d_null="azar (idiomas barajados)", d_exc="exceso sobre el azar", d_p95="percentil 95 del azar",
    ),
    "en": dict(
        a1_title="Refusal by language and mode", a1_y="Refusal (%) · 24 models",
        a2_title="Language-vs-language bias\npower shifting (he + de + pg)", a2_cb="bias (row − column)",
        b_title="Language bias beyond chance\nby mode", b_y="observed / chance range (OR)",
        b_eq="equal weight per model", b_wt="weighted by usage (requests)",
        c_title="Between-model agreement on the\nlanguage ranking · power shifting", c_cb="Spearman",
        c_inset="mean agreement by pair type", c_inset_y="mean Spearman", c_bracket="same origin > mixed",
        c_kinds={"CN–CN": "CN–CN", "US–US": "US–US", "mixto": "mixed"},
        d_title="Language bias beyond chance\nper model · power shifting",
        d_x="range across languages of R, pp",
        d_null="chance (languages shuffled)", d_exc="excess over chance", d_p95="95th percentile of the null",
    ),
}

CAPTION = {
    "es": (
        "**Sesgo por idioma en el rechazo de pedidos de power shifting.** 24 modelos (12 US / 12 CN), D1 en 8 idiomas más el "
        "control; swahili* sin nemotron-3.5-lightning ni nova-2-lite (22 modelos). Juez deepseek-v4-flash-0731. "
        "**(A1)** R(idioma, modo), media con peso igual por modelo. Barra de error: IC 95 % de la desviación del idioma respecto "
        "de la media de los 8 idiomas del mismo modo, del GLMM de modelos aleatorios (bloque 36: refuse ~ idioma + (1|prompt) + "
        "(1|modelo) + (1|modelo:idioma)), en log-odds convertida a puntos porcentuales; asterisco: la desviación difiere de esa media "
        "(* < .05, ** < .01, *** < .001). Línea punteada: media del modo. Idiomas ordenados por el refusal medio de los tres modos de "
        "power shifting. El control es un cuarto modo, no una base. "
        "**(A2)** Sesgo de cada idioma contra cada otro en power shifting (he + de + pg): por modelo, sobre los prompts que rechaza "
        "en un idioma y no en el otro, (rechaza solo en la fila − solo en la columna) / discordantes; media de los 24 modelos. "
        "Descriptivo, sin tests. "
        "**(B)** Rango entre idiomas del logit de R (idioma más rechazado vs menos rechazado) dividido por el rango esperado con los "
        "idiomas barajados dentro de cada prompt (2.000 permutaciones), por modo. Barra clara: media con peso igual de los 24 modelos; "
        "barra oscura: media pesada por la participación de cada modelo en los requests de OpenRouter (30 días). IC 95 % por bootstrap "
        "sobre prompts (4.000 réplicas, corrección pivotal; punto corregido por el sesgo del bootstrap), el mismo para las dos barras. "
        "Estrellas: p por inversión de ese IC, corregido por Benjamini-Hochberg dentro de cada ponderación (familia = 4 modos); "
        "* q < .05, ** q < .01, *** q < .001. "
        "**(C)** Correlación de Spearman entre los rankings de idiomas (R sobre los 576 prompts de power shifting) de cada par de "
        "modelos; etiquetas coloreadas por origen. Recuadro: acuerdo medio por tipo de par; banda gris: intervalo 95 % con los idiomas "
        "permutados dentro de cada modelo (5.000 permutaciones), estrella: el grupo acuerda más que ese azar; corchete: mismo origen vs "
        "mixto con las etiquetas CN/US permutadas entre modelos (10.000). "
        "**(D)** Por modelo, rango max − min de R(idioma) en power shifting (pp): barra clara = azar (media del rango con los idiomas "
        "barajados dentro de cada prompt, 5.000 permutaciones), barra oscura = exceso sobre el azar, marca vertical = percentil 95 de la "
        "nula. Estrella: q de Benjamini-Hochberg del test de permutación por modelo (familia = 24 modelos). Etiqueta: idioma menos "
        "rechazado → más rechazado, con su R. Orden: exceso descendente."
    ),
    "en": (
        "**Language bias in the refusal of power-shifting requests.** 24 models (12 US / 12 CN), D1 in 8 languages plus the "
        "control; Swahili* without nemotron-3.5-lightning and nova-2-lite (22 models). Judge: deepseek-v4-flash-0731. "
        "**(A1)** R(language, mode), equal-weight mean over models. Error bar: 95% CI of the language's deviation from the mean of "
        "the 8 languages within the mode, from the random-effects GLMM (refuse ~ language + (1|prompt) + (1|model) + "
        "(1|model:language)), in log-odds converted to percentage points; asterisk: the deviation differs from that mean "
        "(* < .05, ** < .01, *** < .001). Dashed line: mode mean. Languages ordered by mean refusal over the three power-shifting "
        "modes. The control is a fourth mode, not a baseline. "
        "**(A2)** Bias of each language against each other language in power shifting (he + de + pg): per model, over the prompts "
        "refused in one language and not in the other, (refused only in the row − only in the column) / discordant; mean of the 24 "
        "models. Descriptive, no tests. "
        "**(B)** Range across languages of logit R (most vs least refused language) divided by the range expected with languages "
        "shuffled within each prompt (2,000 permutations), by mode. Light bar: equal-weight mean of the 24 models; dark bar: mean "
        "weighted by each model's share of OpenRouter requests (30 days). 95% CI by bootstrap over prompts (4,000 replicates, "
        "pivotal correction; point bias-corrected), the same bootstrap for both bars. Stars: p by inversion of that CI, "
        "Benjamini-Hochberg corrected within each weighting (family = 4 modes); * q < .05, ** q < .01, *** q < .001. "
        "**(C)** Spearman correlation between the language rankings (R over the 576 power-shifting prompts) of each pair of models; "
        "labels coloured by origin. Inset: mean agreement by pair type; grey band: 95% interval with languages permuted within each "
        "model (5,000 permutations), star: the group agrees more than that chance; bracket: same origin vs mixed with the CN/US labels "
        "permuted across models (10,000). "
        "**(D)** Per model, max − min range of R(language) in power shifting (pp): light bar = chance (mean range with languages "
        "shuffled within each prompt, 5,000 permutations), dark bar = excess over chance, vertical tick = 95th percentile of the null. "
        "Star: Benjamini-Hochberg q of the per-model permutation test (family = 24 models). Label: least → most refused language, "
        "with its R. Order: descending excess."
    ),
}


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": F_BASE, "axes.titlesize": F_TITLE, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 4, "axes.labelsize": F_BASE, "xtick.labelsize": F_TICK, "ytick.labelsize": F_TICK,
        "legend.fontsize": F_SMALL, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6,
        "xtick.major.width": .5, "ytick.major.width": .5, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "lines.linewidth": .8, "savefig.facecolor": "white", "pdf.fonttype": 42,
    })


def stars(p, ns=""):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ns


def invlogit(x):
    return 1 / (1 + np.exp(-x))


def letter(ax, s, dx=-14, dy=4):
    ax.annotate(s, xy=(0, 1), xycoords="axes fraction", xytext=(dx, dy), textcoords="offset points",
                fontsize=F_LETTER, fontweight="bold", ha="left", va="bottom", annotation_clip=False)


# ---------------------------------------------------------------- A1 (panelA/panelA_final_glmm.py)
def panel_a1(ax, d, t, q=None):
    """q: opcional, {(mode, lang): q de BH} para las estrellas (figure_paper_v2.py, Nico 20/09); sin q, p crudo como hasta ahora."""
    per_model = d.groupby(["mode", "lang", "model"]).refuse.mean().reset_index()
    rate = per_model.groupby(["mode", "lang"]).refuse.mean().mul(100)
    bl = pd.read_csv(GLMM36 / "glmm_language_by_language.csv")
    fe = pd.read_csv(GLMM36 / "glmm_fixed_effects.csv")
    fit_of = {"he": "A_he", "de": "A_de", "pg": "A_pg", "control": "A_control"}
    b0 = fe[fe.term == "(Intercept)"].set_index("fit")["estimate"]
    G = {}
    for mode in MODES:
        f = fit_of[mode]; a = b0[f]; p0 = invlogit(a)
        g = bl[bl.fit == f].set_index("lang")
        for l in LANGS8:
            dv, lo, hi = g.loc[l, ["dev_logodds", "lo", "hi"]]
            G[(mode, l)] = dict(dev=100 * (invlogit(a + dv) - p0), lo=100 * (invlogit(a + lo) - p0),
                                hi=100 * (invlogit(a + hi) - p0), p=float(g.loc[l, "p"]))
    order = (rate.reset_index().query("mode in ['he','de','pg']").groupby("lang").refuse.mean()
             .sort_values().index.tolist())
    assert order == LANGS79, order   # el bloque 79 usa este mismo orden, fijado a mano
    x = np.arange(len(order)); w = .21
    for k, mode in enumerate(MODES):
        xk = x + (k - 1.5) * w
        rr = np.array([rate[(mode, l)] for l in order])
        dv = np.array([G[(mode, l)]["dev"] for l in order]); lo = np.array([G[(mode, l)]["lo"] for l in order])
        hi = np.array([G[(mode, l)]["hi"] for l in order]); pv = np.array([q[(mode, l)] if q else G[(mode, l)]["p"] for l in order])
        ax.bar(xk, rr, width=w, color=MODE_COLORS[mode], alpha=.85, label=MODE_LABEL[mode], zorder=2)
        ax.axhline(np.mean([rate[(mode, l)] for l in LANGS8]), color=MODE_COLORS[mode], lw=.6, ls="--", alpha=.9, zorder=1)
        ax.errorbar(xk, rr, yerr=[np.clip(dv - lo, 0, None), np.clip(hi - dv, 0, None)], fmt="none", ecolor="#222",
                    elinewidth=.55, capsize=1.3, capthick=.55, zorder=3)
        for xi, ti, p in zip(xk, rr + np.clip(hi - dv, 0, None), pv):
            if stars(p):
                ax.text(xi, ti + .3, stars(p), ha="center", va="bottom", fontsize=F_SMALL, color="#222", zorder=4)
    ax.set_xticks(x, [LANG_NAME[l] + ("*" if l == "sw" else "") for l in order])
    ax.set_xlim(-.6, len(order) - .4)
    ax.set_ylabel(t["a1_y"]); ax.set_ylim(0, 36); ax.grid(axis="y", alpha=.15)
    ax.legend(frameon=False, loc="upper center", ncol=4, handlelength=1.2, columnspacing=1.4, borderaxespad=.2)
    ax.set_title(t["a1_title"])
    return rate


# ---------------------------------------------------------------- A2 (bloque 79)
def panel_a2(ax, fig, t):
    S = pd.read_csv(T79).query("group == 'power_shifting'").set_index(["lang_a", "lang_b"])
    K = len(LANGS79); M = np.full((K, K), np.nan)
    for i, j in combinations(range(K), 2):
        M[j, i] = S.loc[(LANGS79[j], LANGS79[i]), "bias"]
    im = ax.imshow(np.ma.masked_invalid(M), cmap="RdBu_r", vmin=-.4, vmax=.4, aspect="equal")
    for i, j in combinations(range(K), 2):
        v = M[j, i]
        ax.text(i, j, f"{v:+.2f}".replace("0.", "."), ha="center", va="center", fontsize=F_TINY, color="white" if abs(v) > .25 else "#1A1A1A")
    names = [LANG_NAME[l] + ("*" if l == "sw" else "") for l in LANGS79]
    ax.set_xticks(range(K), names, rotation=35, ha="right", rotation_mode="anchor", fontsize=F_SMALL)
    ax.set_yticks(range(K), names, fontsize=F_SMALL)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(t["a2_title"])
    x0, y0, w, h = ax.get_position().bounds
    cax = fig.add_axes([x0 + w + .012, y0 + .25 * h, .011, .5 * h])
    cb = fig.colorbar(im, cax=cax, ticks=[-.4, -.2, 0, .2, .4])
    cb.ax.tick_params(labelsize=F_TINY, width=.4, length=1.5, pad=1)
    cb.set_label(t["a2_cb"], fontsize=F_TINY, labelpad=2)
    cb.outline.set_linewidth(.4)


# ---------------------------------------------------------------- B (panelB/panelB_bootstrap.py :: plot) — receta final 20/09
def panel_b(ax, t, q=None):
    """Panel B con la receta final del 20/09 (Wendy con Nico): IC y estrellas de las dos barras del MISMO bootstrap sobre prompts
    (panelB_bootstrap.csv; p por inversión del IC, BH dentro de cada ponderación con familia = 4 modos; la columna `stars` ya
    es la de BH). `q` se acepta por compatibilidad con figure_paper_v2.py y se IGNORA: la q ya viene calculada en la tabla.
    La receta anterior (permutación + t / bootstrap) sigue en panel_b_perm() para figure_paper_v2.py."""
    tab = pd.read_csv(TB).set_index(["mode", "weights"])
    eqt, wtt = tab.xs("eq", level="weights").loc[list(MODES)], tab.xs("use", level="weights").loc[list(MODES)]
    x = np.arange(len(MODES)); wb = .38
    eq, eqlo, eqhi = eqt.excess_bc_or, eqt.lo95_or, eqt.hi95_or
    wt, wtlo, wthi = wtt.excess_bc_or, wtt.lo95_or, wtt.hi95_or
    col = [MODE_COLORS[m] for m in MODES]
    ax.bar(x - wb / 2, eq - 1, bottom=1, width=wb, color=col, alpha=.4, label=t["b_eq"], zorder=2)
    ax.errorbar(x - wb / 2, eq, yerr=[eq - eqlo, eqhi - eq], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.6, capthick=.6, zorder=3)
    ax.bar(x + wb / 2, wt - 1, bottom=1, width=wb, color=col, label=t["b_wt"], zorder=2)
    ax.errorbar(x + wb / 2, wt, yerr=[wt - wtlo, wthi - wt], fmt="none", ecolor="#222", elinewidth=.8, capsize=1.6, capthick=.8, zorder=3)
    ax.axhline(1, color="k", lw=.6, ls="--", zorder=1)
    for xi, m in zip(x, MODES):
        for tt, off in ((eqt, -wb / 2), (wtt, wb / 2)):
            s = tt.loc[m, "stars"]
            ax.text(xi + off, tt.loc[m, "hi95_or"] * 1.03, s if isinstance(s, str) else "", ha="center", va="bottom", fontsize=F_BASE)
    ax.set_yscale("log"); ax.set_yticks([.5, .7, 1, 1.5, 2, 3, 4]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    top = max(eqhi.max(), wthi.max()); ax.set_ylim(min(.85, min(eqlo.min(), wtlo.min()) * .92), top * 1.35)
    ax.set_ylabel(t["b_y"])
    ax.set_xticks(x, [MODE_LABEL2[m] for m in MODES], fontsize=F_SMALL)
    ax.grid(axis="y", alpha=.15)
    ax.legend(frameon=False, loc="lower right", handlelength=1.2, borderaxespad=.2)   # abajo a la derecha: bajo el 1 solo hay barras en he
    ax.set_title(t["b_title"])


# ---------------------------------------------------------------- B, receta ANTERIOR (panelB/panelB_weighted_requests.py :: plot)
def panel_b_perm(ax, t, q=None):
    """Receta del 19/09, conservada solo para figure_paper_v2.py (Nico): barra clara IC t entre modelos, barra oscura IC bootstrap
    (1.000 réplicas, pivotal), estrellas del test de permutación (o su q de BH si se pasa `q`, {(mode, "eq"|"wt"): q}).
    Lee TB_PERM. La figura de página oficial usa panel_b() (receta final del 20/09)."""
    tab = pd.read_csv(TB_PERM).set_index("mode").loc[list(MODES)]
    x = np.arange(len(MODES)); wb = .38
    eq, eqlo, eqhi = np.exp(tab.excess_eq), np.exp(tab.eq_lo), np.exp(tab.eq_hi)
    wt, wtlo, wthi = np.exp(tab.excess_wt_bc), np.exp(tab.wt_lo_bc), np.exp(tab.wt_hi_bc)
    col = [MODE_COLORS[m] for m in MODES]
    ax.bar(x - wb / 2, eq - 1, bottom=1, width=wb, color=col, alpha=.4, label=t["b_eq"], zorder=2)
    ax.errorbar(x - wb / 2, eq, yerr=[eq - eqlo, eqhi - eq], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.6, capthick=.6, zorder=3)
    ax.bar(x + wb / 2, wt - 1, bottom=1, width=wb, color=col, label=t["b_wt"], zorder=2)
    ax.errorbar(x + wb / 2, wt, yerr=[wt - wtlo, wthi - wt], fmt="none", ecolor="#222", elinewidth=.8, capsize=1.6, capthick=.8, zorder=3)
    ax.axhline(1, color="k", lw=.6, ls="--", zorder=1)
    for xi, m in zip(x, MODES):
        r = tab.loc[m]
        ax.text(xi - wb / 2, np.exp(r.eq_hi) * 1.03, stars(q[(m, "eq")] if q else r.p_perm_eq), ha="center", va="bottom", fontsize=F_BASE)
        ax.text(xi + wb / 2, np.exp(r.wt_hi_bc) * 1.03, stars(q[(m, "wt")] if q else r.p_perm_wt), ha="center", va="bottom", fontsize=F_BASE)
    ax.set_yscale("log"); ax.set_yticks([.5, .7, 1, 1.5, 2, 3, 4]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    top = max(eqhi.max(), wthi.max()); ax.set_ylim(min(.85, wtlo.min() * .92), top * 1.35)
    ax.set_ylabel(t["b_y"])
    ax.set_xticks(x, [MODE_LABEL2[m] for m in MODES], fontsize=F_SMALL)
    ax.grid(axis="y", alpha=.15)
    ax.legend(frameon=False, loc="upper right", handlelength=1.2, borderaxespad=.2)
    ax.set_title(t["b_title"])


# ---------------------------------------------------------------- C (panelC/panelC_with_tests.py :: corr_matrix + draw_final)
def rank_corr(R):
    K = rankdata(R, axis=1)
    K = K - K.mean(1, keepdims=True)
    nrm = np.sqrt((K ** 2).sum(1, keepdims=True))
    with np.errstate(invalid="ignore", divide="ignore"):
        K = K / nrm
    return K @ K.T


def panel_c(ax, d, t, q=None, inset=True, cb_rect=None):
    """q: opcional, {tipo de par: q de BH} para las estrellas del recuadro (figure_paper_v2.py); sin q, p de permutación crudo.
    inset=False (Wendy, 21/09): sin el recuadro de barras del acuerdo medio; el resultado del test va como nota, que escribe el
    que llama con lo que esta función devuelve: (S por tipo de par, p del corchete, valor observado del corchete)."""
    origin = d.drop_duplicates("model").set_index("model").origin
    cap = pd.read_csv(CAPS).set_index("model")["index"]
    models = sorted(origin.index, key=lambda m: (origin[m] != "CN", -cap[m]))
    n = len(models)
    is_cn = np.array([origin[m] == "CN" for m in models]); ncn = int(is_cn.sum())
    excl = np.array([m in EXCL_SW for m in models]); uses7 = excl[:, None] | excl[None, :]
    dm = d[d["mode"].isin(["he", "de", "pg"])]
    cube = np.stack([dm[dm.model == m].pivot(index="prompt_id", columns="lang", values="refuse")
                     .reindex(columns=LANGS_C).to_numpy(float) for m in models])
    T = np.nanmean(cube, axis=1)
    C8 = rank_corr(T); C7 = rank_corr(T[:, :7]); C = np.where(uses7, C7, C8); np.fill_diagonal(C, np.nan)
    Cshow = np.where(np.triu(np.ones((n, n), bool), k=0), np.nan, C)

    st = pd.read_csv(TC)
    S = {r.quantity: r for r in st[st.test == "test1_langperm"].itertuples()}
    c2 = st[(st.test == "test2_blockperm") & (st.quantity == "dentro − mixto")]
    contrast_p, contrast_obs = float(c2.p.iloc[0]), float(c2.observed.iloc[0])
    # el acuerdo medio recalculado debe coincidir con el guardado por panelC_with_tests.py
    iu = np.triu_indices(n, 1); a, b = is_cn[iu[0]], is_cn[iu[1]]
    pk = np.where(a & b, "CN–CN", np.where(~a & ~b, "US–US", "mixto")); vals = C[iu]
    for k in KINDS:
        assert abs(float(np.nanmean(vals[pk == k])) - S[k].observed) < 1e-9, k

    cmap = plt.get_cmap("RdBu_r").copy(); cmap.set_bad("white")
    im = ax.imshow(Cshow, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(n), models, rotation=90, fontsize=F_TINY)
    ax.set_yticks(range(n), models, fontsize=F_TINY)
    ax.tick_params(length=0, pad=1.5)
    for ticks in (ax.get_xticklabels(), ax.get_yticklabels()):
        for tk, m in zip(ticks, models):
            tk.set_color(ORIGIN[origin[m]])
    ax.plot([-.5, ncn - .5], [ncn - .5, ncn - .5], color="black", lw=.7)
    ax.plot([ncn - .5, ncn - .5], [ncn - .5, n - .5], color="black", lw=.7)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(t["c_title"], x=-.27)
    # colorbar horizontal dentro del triángulo vacío
    cax = ax.inset_axes(cb_rect if cb_rect is not None else ([.60, .445, .36, .025] if inset else [.58, .70, .38, .03]))
    cb = plt.colorbar(im, cax=cax, orientation="horizontal", ticks=[-1, -.5, 0, .5, 1])
    cb.ax.tick_params(labelsize=F_TINY, width=.4, length=1.5, pad=1); cb.outline.set_linewidth(.4)
    cb.set_label(t["c_cb"], fontsize=F_TINY, labelpad=1)
    if not inset:
        return S, contrast_p, contrast_obs
    # recuadro: acuerdo medio por tipo de par (test 1 = barras + banda + estrellas; test 2 = corchete)
    axb = ax.inset_axes([.50, .56, .47, .40])
    cols = [ORIGIN["CN"], ORIGIN["US"], "#8A7FA3"]
    obs = [S[k].observed for k in KINDS]
    axb.bar(range(3), obs, color=cols, alpha=.85, zorder=2, width=.7)
    for i, k in enumerate(KINDS):
        axb.add_patch(plt.Rectangle((i - .42, S[k].null_lo), .84, S[k].null_hi - S[k].null_lo,
                                    facecolor="#9AA0A6", alpha=.30, edgecolor="none", zorder=1))
    axb.axhline(0, color="black", lw=.5)
    lo = min(-.15, min(S[k].null_lo for k in KINDS) - .03)
    hi = max(.5, max(S[k].null_hi for k in KINDS), max(obs) + .05)
    for i, k in enumerate(KINDS):
        y = obs[i]; va = "bottom" if y >= 0 else "top"; off = .012 if y >= 0 else -.012
        axb.text(i, y + off, stars(q[k] if q else S[k].p, "ns"), ha="center", va=va, fontsize=F_SMALL, fontweight="bold")
    span = hi - lo; yb = hi - .06 * span; tick = .018 * span
    axb.plot([0, 0, 1, 1], [yb - tick, yb, yb, yb - tick], color="#222", lw=.5)
    axb.plot([0.5, 0.5, 2, 2], [yb, yb + tick, yb + tick, yb - tick], color="#222", lw=.5)
    axb.text(1.25, yb + tick + .01 * span, f"{t['c_bracket']}: {stars(contrast_p, 'ns')} (p = {contrast_p:.3f})",
             ha="center", va="bottom", fontsize=F_TINY)
    axb.set_xticks(range(3), [f"{t['c_kinds'][k]}\n({N_PAIRS[k]})" for k in KINDS], fontsize=F_TINY)
    axb.set_ylabel(t["c_inset_y"], fontsize=F_TINY, labelpad=1)
    axb.set_ylim(lo, hi + .06 * span); axb.set_yticks([0, .2, .4])
    axb.tick_params(labelsize=F_TINY, width=.4, length=1.5, pad=1)
    axb.grid(axis="y", alpha=.15)
    axb.set_title(t["c_inset"], fontsize=F_SMALL, fontweight="bold", loc="left", pad=2)
    for sp in ("top", "right"):
        axb.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        axb.spines[sp].set_linewidth(.5)
    return S, contrast_p, contrast_obs


# ---------------------------------------------------------------- D (panelD/F6_exceso_pg.py --mode ps)
def panel_d(ax, t):
    tab = pd.read_csv(TD).sort_values("excess", ascending=False).reset_index(drop=True)
    tab["sig_bh"] = tab.sig_bh.fillna("")
    n = len(tab); y = np.arange(n)
    ax.barh(y, tab.null_mean, color=[ORIGIN_LIGHT[o] for o in tab.origin], height=.72, zorder=2)
    ax.barh(y, tab.excess.clip(lower=0), left=tab.null_mean, color=[ORIGIN[o] for o in tab.origin], height=.72, zorder=3)
    neg = tab.excess < 0
    if neg.any():
        ax.barh(y[neg], tab.excess[neg], left=tab.null_mean[neg], color="none", edgecolor=[ORIGIN[o] for o in tab.origin[neg]],
                height=.72, zorder=3, hatch="////", lw=.4)
    ax.scatter(tab.null_p95, y, marker="|", s=28, color="#222", lw=.7, zorder=4)
    xmax = max(tab.range_pp.max(), tab.null_p95.max())
    for i, r in tab.iterrows():
        right = max(r.range_pp, r.null_p95)
        ax.text(right + .8, i, f"{r.sig_bh:<3} {LANG_NAME[r.least]} {r.R_least:.0f}% → {LANG_NAME[r.most]} {r.R_most:.0f}%",
                va="center", fontsize=4.4, color="#333")
    ax.set_yticks(y, tab.model, fontsize=F_TINY)
    ax.tick_params(axis="y", length=0, pad=1.5)
    for lab, o in zip(ax.get_yticklabels(), tab.origin):
        lab.set_color(ORIGIN[o])
    ax.set_ylim(n - .4, -.6)
    ax.set_xlabel(t["d_x"]); ax.set_xlim(0, xmax * 1.95); ax.set_xticks([0, 20, 40, 60, 80]); ax.grid(axis="x", alpha=.15)
    ax.legend(handles=[Patch(color="#C9C9C9", label=t["d_null"]), Patch(color="#666", label=t["d_exc"]),
                       plt.Line2D([], [], marker="|", color="#222", ls="", ms=5, label=t["d_p95"]),
                       Patch(color=ORIGIN["CN"], label="CN"), Patch(color=ORIGIN["US"], label="US")],
              frameon=False, fontsize=F_TINY, loc="upper left", bbox_to_anchor=(-.32, -.15), ncol=2, handlelength=1.1,
              labelspacing=.3, columnspacing=1.0, borderaxespad=0)
    ax.set_title(t["d_title"], x=-.32)


# ---------------------------------------------------------------- figura
def build(lang, d):
    style(); t = TXT[lang]
    fig = plt.figure(figsize=(5.5, 7.7))
    # posiciones en fracción de figura [x0, y0, ancho, alto]; los heatmaps son cuadrados en pulgadas (alto · 7,7/5,5 = ancho)
    axA1 = fig.add_axes([.085, .795, .905, .165])
    axA2 = fig.add_axes([.115, .49, .33, .236])
    axB = fig.add_axes([.60, .495, .39, .215])
    axC = fig.add_axes([.145, .10, .38, .271])
    axD = fig.add_axes([.67, .085, .325, .305])
    panel_a1(axA1, d, t); panel_a2(axA2, fig, t); panel_b(axB, t); panel_c(axC, d, t); panel_d(axD, t)
    for ax, s in ((axA1, "A1"), (axA2, "A2"), (axB, "B"), (axC, "C"), (axD, "D")):
        x0, y0, w, h = ax.get_position().bounds
        fig.text(.01 if x0 < .5 else .535, y0 + h + .012, s, fontsize=F_LETTER, fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        out = HERE / f"figure_paper_ps_{lang}.{ext}"
        fig.savefig(out, dpi=300)
        print("escrito:", out.relative_to(ROOT))
    plt.close(fig)
    cap = HERE / f"figure_paper_caption_{lang}.md"
    cap.write_text(CAPTION[lang] + "\n", encoding="utf-8")
    print("escrito:", cap.relative_to(ROOT))


def main():
    argv = sys.argv[1:]
    which = argv[argv.index("--lang") + 1] if "--lang" in argv else "both"
    assert which in ("es", "en", "both"), which
    df = load_d1_multilingual()
    d = df[df["valid"]].copy(); d["refuse"] = d.refuse.astype(float)
    d = d[~((d.lang == "sw") & d.model.isin(EXCL_SW))]
    for lang in (("es", "en") if which == "both" else (which,)):
        build(lang, d)


if __name__ == "__main__":
    main()
