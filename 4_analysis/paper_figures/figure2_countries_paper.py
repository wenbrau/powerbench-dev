#!/usr/bin/env python3
"""Figura 2 (D2, díadas de nacionalidad) para la PÁGINA del paper. Rediseño del 2026-09-20 (Wendy): misma estructura que
la figura oficial 4_analysis/review_fig_countries/figure_full_split.py, redibujada a 5,5 in de ancho (ICLR 2027) con
tipografía uniforme (4,7–7,2 pt), en/es, PDF + PNG 300 dpi + caption .md. No calcula nada: lee las mismas tablas.

  IZQUIERDA, dos cajas (lado USA / lado China | neutral A / neutral B) × 4 filas con título-pregunta:
    A) refusal por lado del usuario (descriptivo, sin IC; color del modo desaturado sobre fondo azul US / rojo China)
    B) exceso de |sesgo| sobre el azar (bloque 55)   C) OR del lado, GLMM (bloque 45; q del 83)   D) OR pesado por uso (bloque 73)
  DERECHA, panel E (dirección, bloque 46): USA y China, cada uno con sus díadas (aliado, neutral, rival, la otra potencia)
    y a la izquierda las cuatro juntas. Sombreado: C/D rojo arriba (CN) / azul abajo (US); E solo abajo, color del país.

Ejecutar desde la raíz del repo:  python 4_analysis/paper_figures/figure2_countries_paper.py [--lang es|en|both]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paperstyle import (RESULTS, MODES, PS, MODE_LABEL, MODE_COLORS, ORIGIN, F_TITLE, F_BASE, F_TICK, F_SMALL, F_TINY,  # noqa: E402
                         style, num, or_axis, save, which_langs)
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.patches import Patch, FancyBboxPatch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

SRC = {"B": RESULTS / "55_fig3_side_excess" / "side_abs_bias_excess_summary.csv",
       "C": RESULTS / "45_fig3_side_combined_nagq1" / "side_glmm.csv",
       "D": RESULTS / "73_fig3_usage_weighted_requests" / "side_or_requests.csv",
       "E": RESULTS / "46_fig3_direction_glmm_nagq1" / "direction_glmm.csv",
       "E_dyad": RESULTS / "46_fig3_direction_glmm_nagq1" / "direction_glmm_by_dyad.csv",
       "bh83": RESULTS / "83_bh_fig3f_fig2b_nagq1" / "bh_families.csv",
       "bh89": RESULTS / "89_bh_fig2e_by_power_nagq1" / "bh_by_power.csv",
       "pmr": RESULTS / "21_d2_nationality_final" / "per_model_rates.csv",
       "A86": RESULTS / "86_fig2_ps_pooled_nagq1" / "ps_rates_by_side.csv", "B86": RESULTS / "86_fig2_ps_pooled_nagq1" / "side_abs_bias_excess_ps.csv",
       "C86": RESULTS / "86_fig2_ps_pooled_nagq1" / "side_glmm_ps.csv"}   # columna violeta de power shifting agrupado (20/09)
SETS = ("geo", "neutral")
MODES5 = list(MODES) + [PS]; XS = np.array([0, 1, 2, 3, 4.45]); XSEP = 3.72
MODE_LABEL = dict(MODE_LABEL); MODE_LABEL[PS] = "Power shifting (he + de + pg)"
SIDE_CONDS = {"geo": {"us": ["us_cn", "allyus_allycn"], "cn": ["cn_us", "allycn_allyus"]},
              "neutral": {"us": ["neutralA_neutralB"], "cn": ["neutralB_neutralA"]}}
SIDE_COL = {"us": "#2E6FB0", "cn": "#C0392B"}     # fondo clarito del lado (A)
DESAT = {"us": .20, "cn": .45}                     # desaturación por lado (A)
DY = {"usa": ["us_ally", "us_neutral", "us_rival", "us_cn"], "china": ["cn_ally", "cn_neutral", "cn_rival", "cn_us"]}
BOX = dict(fc="#F5F5F5", ec="#D5D5D5"); TBOX = dict(boxstyle="round,pad=.28", fc="#E4E4E4", ec="#BDBDBD", lw=.5)
NL = chr(10)

TXT = {
    "es": dict(head={"geo": "lado USA / lado China", "neutral": "neutral A / neutral B"},
               sub={"geo": "(USA/China + aliados, juntas)", "neutral": "(referencia sin polo)"},
               rowq={"A": "A ·  ¿Cuánto rechaza según el lado?", "B": "B ·  ¿Más sesgo de lado que el azar?",
                     "C": "C ·  ¿Rechaza distinto según el lado?", "D": "D ·  Lo mismo, pesado por uso"},
               e_title="E ·  Dirección del pedido:" + NL + "¿rechaza distinto si el país" + NL + "gana poder (usuario) o lo" + NL
                       + "pierde (afectado), incluso con" + NL + "países neutrales o aliados?",
               P={"usa": "USA", "china": "China"}, leg_us="usuario lado USA", leg_cn="usuario lado China",
               up="▲ rechaza más si el usuario" + NL + "es del lado USA", dn="▼ rechaza más si el usuario" + NL + "es del lado China",
               e_up="▲ rechaza más cuando {P} es usuario" + NL + "(gana poder o se lo saca al otro)",
               e_dn="▼ rechaza más cuando {P} es afectado" + NL + "(pierde poder)",
               yA="Refusal (%)" + NL + "media de 24 modelos", yB="exceso de |sesgo|" + NL + "sobre el azar · q: BH",
               yC="OR refusal · GLMM" + NL + "lado USA vs China · q: BH", yD="OR refusal · por uso" + NL + "lado USA vs China · q: BH",
               yE="OR refusal · GLMM" + NL + "país usuario / país afectado", joint="las cuatro" + NL + "juntas",
               dy={"us_ally": "USA" + NL + "aliado", "us_neutral": "USA" + NL + "neutral", "us_rival": "USA" + NL + "rival", "us_cn": "USA" + NL + "China",
                   "cn_ally": "China" + NL + "aliado", "cn_neutral": "China" + NL + "neutral", "cn_rival": "China" + NL + "rival", "cn_us": "China" + NL + "USA"}),
    "en": dict(head={"geo": "US side / China side", "neutral": "neutral A / neutral B"},
               sub={"geo": "(US/China + allies, pooled)", "neutral": "(non-aligned reference)"},
               rowq={"A": "A ·  How much is refused, by side?", "B": "B ·  More side bias than chance?",
                     "C": "C ·  Does refusal differ by side?", "D": "D ·  The same, weighted by usage"},
               e_title="E ·  Direction of the request:" + NL + "is refusal different when the" + NL + "country gains power (user) or" + NL
                       + "loses it (affected), even with" + NL + "neutral or allied countries?",
               P={"usa": "US", "china": "China"}, leg_us="US-side user", leg_cn="China-side user",
               up="▲ more refusal with a" + NL + "US-side user", dn="▼ more refusal with a" + NL + "China-side user",
               e_up="▲ more refusal when {P} is the user" + NL + "(gains power or takes it)",
               e_dn="▼ more refusal when {P} is the affected" + NL + "party (loses power)",
               yA="Refusal (%)" + NL + "mean of 24 models", yB="excess of |bias|" + NL + "over chance · q: BH",
               yC="refusal OR · GLMM" + NL + "US vs China side · q: BH", yD="refusal OR · by usage" + NL + "US vs China side · q: BH",
               yE="refusal OR · GLMM" + NL + "country as user / as affected", joint="all four" + NL + "pooled",
               dy={"us_ally": "US" + NL + "ally", "us_neutral": "US" + NL + "neutral", "us_rival": "US" + NL + "rival", "us_cn": "US" + NL + "China",
                   "cn_ally": "China" + NL + "ally", "cn_neutral": "China" + NL + "neutral", "cn_rival": "China" + NL + "rival", "cn_us": "China" + NL + "US"}),
}

CAPTION = {
    "es": (
        "**Sesgo por nacionalidad del usuario y del afectado (D2).** 24 modelos (12 US / 12 CN); los 576 prompts de D1 inglés y los 192 "
        "de control con un slot de nacionalidad y el país del usuario en el system prompt, en 18 condiciones (9 díadas × 2 direcciones); "
        "juez deepseek-v4-flash-0731. Columna izquierda, geo = las díadas USA / China y aliado de USA / aliado de China juntas; columna "
        "derecha, neutral = neutral A / neutral B, dos países sin alineamiento, la referencia. En A–D la quinta barra (violeta) es power shifting agrupado, he + de + pg: en A la media de las tasas de los tres modos por modelo; en B los discordantes de los tres modos sumados por modelo; en C un GLMM sobre las filas de los tres modos con el modo como efecto fijo; en D la fila agrupada del mismo bootstrap; en B y C es un solo test (q = p). **(A)** Refusal medio por modo (media de los "
        "24 modelos) con el usuario del lado USA (fondo azul) y del lado China (fondo rojo); descriptivo, sin intervalo. **(B)** Por modelo "
        "y modo, sesgo de lado = (prompts rechazados solo con el usuario del lado USA − solo con el usuario del lado China) / discordantes; "
        "se muestra |sesgo| menos el |sesgo| esperado bajo el azar (a ~ Binomial(n, ½)), media de los 24 modelos, IC 95 % t entre modelos; "
        "q: t contra 0, BH sobre los 4 modos de cada set. **(C)** OR de refusal con el usuario del lado USA vs del lado China, GLMM refuse ~ "
        "lado + díada + (1 + lado || modelo) + (1|prompt), IC 95 % de Wald; q: BH sobre los 4 modos de cada set. **(D)** El mismo OR marginal "
        "de un pedido típico: tasas pesadas por la participación de cada modelo en los pedidos de OpenRouter; IC 95 % bootstrap sobre prompts "
        "(5.000 réplicas); q: p del mismo bootstrap (el IC excluye 1), BH dentro de los 4 modos. En C y D el sombreado rojo marca más refusal "
        "con el usuario del lado USA y el azul con el usuario del lado China. **(E)** Dirección: OR de refusal cuando el país es el usuario vs "
        "cuando es el afectado, GLMM refuse ~ dirección × origen + díada + (1 + dirección || modelo) + (1|prompt), IC 95 % de Wald; a la "
        "izquierda las cuatro díadas de la potencia juntas, después cada una (aliado, neutral, rival, la otra potencia); asterisco: q < 0,05 "
        "(BH sobre los 8 tests de las díadas juntas, y sobre los 32 de las díadas por separado). El sombreado bajo 1, en el color del país, "
        "marca más refusal cuando el país es el afectado (pierde poder). Eje logarítmico; 1 = sin sesgo. Las q se muestran sin prefijo."
    ),
    "en": (
        "**Bias by nationality of the user and of the affected party (D2).** 24 models (12 US / 12 CN); the 576 D1-English prompts and the "
        "192 control prompts with a nationality slot and the user's country in the system prompt, in 18 conditions (9 dyads × 2 directions); "
        "judge deepseek-v4-flash-0731. Left column, geo = the US / China and US-ally / China-ally dyads pooled; right column, neutral = "
        "neutral A / neutral B, two non-aligned countries, the reference. In A–D the fifth bar (violet) is pooled power shifting, he + de + pg: in A the mean of the three modes' rates per model; in B the three modes' discordant prompts summed per model; in C a GLMM on the three modes' rows with mode as a fixed effect; in D the pooled row of the same bootstrap; in B and C a single test (q = p). **(A)** Mean refusal by mode (mean of the 24 models) with the user on "
        "the US side (blue background) and on the China side (red background); descriptive, no interval. **(B)** Per model and mode, side bias "
        "= (prompts refused only with the user on the US side − only with the user on the China side) / discordant; shown is |bias| minus the "
        "|bias| expected under chance (a ~ Binomial(n, ½)), mean of the 24 models, 95% t CI across models; q: t against 0, BH over the 4 modes "
        "of each set. **(C)** Refusal OR with the user on the US side vs the China side, GLMM refuse ~ side + dyad + (1 + side || model) + "
        "(1|prompt), 95% Wald CI; q: BH over the 4 modes of each set. **(D)** The same marginal OR for a typical request: rates weighted by each "
        "model's share of OpenRouter requests; 95% bootstrap CI over prompts (5,000 replicates); q: p from the same bootstrap (CI excludes 1), "
        "BH within the 4 modes. In C and D the red shading marks more refusal with a US-side user and the blue shading with a China-side user. "
        "**(E)** Direction: refusal OR when the country is the user vs when it is the affected party, GLMM refuse ~ direction × origin + dyad + "
        "(1 + direction || model) + (1|prompt), 95% Wald CI; leftmost, the power's four dyads pooled, then each one (ally, neutral, rival, the "
        "other power); asterisk: q < 0.05 (BH over the 8 pooled tests, and over the 32 single-dyad tests). The shading below 1, in the "
        "country's colour, marks more refusal when the country is the affected party (loses power). Log axis; 1 = no bias. q values are shown "
        "without the prefix."
    ),
}


def mix(c, target, f):
    a, b = np.array(to_rgb(c)), np.array(to_rgb(target))
    return tuple(a + (b - a) * f)


def qlab(q, lang):
    return f"< {num(.001, 3, lang)}" if q < .001 else num(q, 3, lang)


def load():
    B = pd.read_csv(SRC["B"]).set_index(["set", "mode"])
    C = pd.read_csv(SRC["C"]); C = C[C.quantity == "lado (24 modelos)"].set_index(["set", "mode"])
    q83 = pd.read_csv(SRC["bh83"]); q83 = q83[q83.block == 45]
    C["q_bh"] = [float(q83[(q83.family == f"lado del usuario, set {st} (4 modos)") & (q83.test == m)].q_bh.iloc[0]) for st, m in C.index]
    D = pd.read_csv(SRC["D"]).set_index(["set", "group"])
    E = pd.read_csv(SRC["E"]); E = E[E.quantity == "direccion (24 modelos)"].copy()
    Ed = pd.read_csv(SRC["E_dyad"]); Ed = Ed[Ed.quantity == "direccion (24 modelos)"].copy()
    # q por potencia (bloque 89, 22/09): familia de 4 (agrupado) y de 16 (por contraparte) dentro de cada potencia,
    # en lugar de 8 y 32 juntando EE.UU. y China. Las p son las del bloque 46; solo cambia la corrección.
    q89 = pd.read_csv(SRC["bh89"])
    qp = q89[q89.level == "pooled"].set_index(["power", "mode"]).q_bh_power
    qd = q89[q89.level == "by_dyad"].set_index(["dyad", "mode"]).q_bh_power
    E["q_bh"] = [float(qp[(c, m)]) for c, m in zip(E.country, E["mode"])]
    Ed["q_bh"] = [float(qd[(d, m)]) for d, m in zip(Ed.dyad, Ed["mode"])]
    pmr = pd.read_csv(SRC["pmr"])
    vals = {(st, m, s): float(pmr[(pmr["mode"] == m) & pmr.condition.isin(SIDE_CONDS[st][s])].groupby("target").rate.mean().mean())
            for st in SETS for m in MODES for s in ("us", "cn")}
    A86 = pd.read_csv(SRC["A86"]).set_index(["set", "side"]).mean_rate
    vals.update({(st, PS, s): float(A86[(st, s)]) for st in SETS for s in ("us", "cn")})
    B86 = pd.read_csv(SRC["B86"]).set_index("set"); C86 = pd.read_csv(SRC["C86"]).set_index("set")
    return B, C, D, E, Ed, vals, B86, C86


def shade_dir(ax, lo, hi):
    ax.axhspan(1, hi, color=ORIGIN["CN"], alpha=.06, zorder=0); ax.axhspan(lo, 1, color=ORIGIN["US"], alpha=.06, zorder=0)


def arrows_side(ax, t):
    ax.text(.03, .985, t["up"], transform=ax.transAxes, ha="left", va="top", fontsize=F_TINY, color=ORIGIN["CN"], fontweight="bold", linespacing=1.1)
    ax.text(.03, .015, t["dn"], transform=ax.transAxes, ha="left", va="bottom", fontsize=F_TINY, color=ORIGIN["US"], fontweight="bold", linespacing=1.1)


def or_panel(ax, OR, l, h, q, lang, lo, hi):
    x = XS; OR, l, h = np.asarray(OR, float), np.asarray(l, float), np.asarray(h, float)
    ax.bar(x, OR - 1, bottom=1, width=.6, color=[MODE_COLORS[m] for m in MODES5], zorder=2)
    ax.errorbar(x, OR, yerr=[OR - l, h - OR], fmt="none", ecolor="#111", elinewidth=.55, capsize=1.4, capthick=.55, zorder=3)
    for xi, hh, qi in zip(x, h, q):
        ax.text(xi, hh * 1.03, qlab(qi, lang), ha="center", va="bottom", fontsize=F_TINY)
    or_axis(ax, [.7, .8, .9, 1, 1.1, 1.25, 1.5], lo, hi); shade_dir(ax, lo, hi)


def build(lang, data):
    style(); t = TXT[lang]
    B, C, D, E, Ed, vals, B86, C86 = data
    cols5 = [MODE_COLORS[m] for m in MODES5]
    fig = plt.figure(figsize=(5.5, 8.4))
    gs = fig.add_gridspec(4, 4, width_ratios=[1.12, 1.12, .24, 1.62], left=.115, right=.985, top=.815, bottom=.045, hspace=.62, wspace=.16)
    x = XS; w = .38

    def row(ri):
        a0 = fig.add_subplot(gs[ri, 0]); a1 = fig.add_subplot(gs[ri, 1], sharey=a0); a1.tick_params(labelleft=False)
        return [a0, a1]
    axA, axB, axC, axD = row(0), row(1), row(2), row(3)
    for ax in axA + axB + axC + axD:
        ax.set_xticks(x, [""] * 5); ax.set_xlim(-.6, XS[-1] + .6); ax.axvline(XSEP, color="#999", lw=.5, ls=":", zorder=1)

    # A: descriptivo, sin IC
    ytop = max(vals.values()) * 1.42
    for ax, st in zip(axA, SETS):
        for i, m in enumerate(MODES5):
            for side, off in (("us", -w / 2), ("cn", w / 2)):
                ax.bar(x[i] + off, ytop, w + .02, color=SIDE_COL[side], alpha=.14, lw=0, zorder=1)
                ax.bar(x[i] + off, vals[(st, m, side)], w, color=mix(MODE_COLORS[m], "#FFFFFF", DESAT[side]),
                       edgecolor=mix(MODE_COLORS[m], "#FFFFFF", DESAT[side] * .5), lw=.3, zorder=2)
        ax.grid(axis="y", alpha=.15); ax.set_ylim(0, ytop)
    axA[0].set_ylabel(t["yA"], fontsize=F_SMALL)
    axA[0].legend(handles=[Patch(fc=SIDE_COL["us"], alpha=.14, label=t["leg_us"]), Patch(fc=SIDE_COL["cn"], alpha=.14, label=t["leg_cn"])],
                  frameon=True, framealpha=.85, facecolor="white", edgecolor="none", fontsize=F_TINY, loc="upper left", labelspacing=.3, borderaxespad=.2, handlelength=1.2)

    # B: exceso de |sesgo|
    for ax, st in zip(axB, SETS):
        r = B.loc[st].loc[MODES]; b = B86.loc[st]
        ex = np.array(list(r.excess) + [b.excess]); lo = np.array(list(r.lo) + [b.lo]); hi = np.array(list(r.hi) + [b.hi]); q = list(r.q_bh) + [b.q_bh]
        ax.bar(x, ex, width=.6, color=cols5, zorder=2)
        ax.errorbar(x, ex, yerr=[ex - lo, hi - ex], fmt="none", ecolor="#222", elinewidth=.55, capsize=1.4, capthick=.55, zorder=3)
        ax.axhline(0, color="black", lw=.6, ls="--", zorder=1)
        for xi, h, qi in zip(x, hi, q):
            ax.text(xi, max(h, 0) + .012, qlab(qi, lang), ha="center", va="bottom", fontsize=F_TINY)
        ax.grid(axis="y", alpha=.15); ax.set_ylim(-.16, .30)
    axB[0].set_ylabel(t["yB"], fontsize=F_SMALL)

    # C y D: OR del lado, con sombreado direccional
    LO, HI = .52, 2.05
    for ax, st in zip(axC, SETS):
        r = C.loc[st].loc[MODES]; g = C86.loc[st]
        or_panel(ax, list(r.OR) + [g.OR], list(r.OR_lo) + [g.OR_lo], list(r.OR_hi) + [g.OR_hi], list(r.q_bh) + [g.q_bh], lang, LO, HI)
    for ax, st in zip(axD, SETS):
        r = D.loc[st].loc[MODES5]; or_panel(ax, r.odds_ratio, r.boot_lo, r.boot_hi, r.boot_q.values, lang, LO, HI)
    arrows_side(axC[0], t); arrows_side(axD[0], t)
    axC[0].set_ylabel(t["yC"], fontsize=F_SMALL); axD[0].set_ylabel(t["yD"], fontsize=F_SMALL)

    # E: dirección, USA y China con sus díadas (aliado, neutral, rival, la otra potencia)
    gsR = gs[:, 3].subgridspec(2, 1, hspace=.26)
    axE = fig.add_subplot(gsR[0]); axF = fig.add_subplot(gsR[1])
    w4 = .8 / len(MODES); ELO, EHI = .40, 2.6
    for ax, pole in ((axE, "usa"), (axF, "china")):
        P = t["P"][pole]; groups = [("joint", t["joint"])] + [(dy, t["dy"][dy]) for dy in DY[pole]]; xg = np.arange(len(groups))
        for k, mode in enumerate(MODES):
            v = pd.DataFrame([(E[(E.country == pole) & (E["mode"] == mode)] if key == "joint" else Ed[(Ed.dyad == key) & (Ed["mode"] == mode)]).iloc[0]
                              for key, _ in groups])
            xo = xg + (k - (len(MODES) - 1) / 2) * w4
            ax.bar(xo, v.OR.values - 1, bottom=1, width=w4, color=MODE_COLORS[mode], alpha=.9, zorder=2)
            ax.errorbar(xo, v.OR.values, yerr=[v.OR.values - v.OR_lo.values, v.OR_hi.values - v.OR.values], fmt="none", ecolor="#111", elinewidth=.5, capsize=1.2, capthick=.5, zorder=3)
            for xi, (_, rr) in zip(xo, v.iterrows()):
                if rr.q_bh < .05:
                    ax.text(xi, rr.OR_hi * 1.02, "*", ha="center", va="bottom", fontsize=F_BASE + 1)
        or_axis(ax, [.5, .67, .8, 1, 1.25, 1.5, 2], ELO, EHI)
        ax.axvspan(-.5, .5, color="#000", alpha=.05, zorder=0); ax.axvline(.5, color="#666", lw=.6, ls="--")
        ax.axhspan(ELO, 1, color=ORIGIN["US" if pole == "usa" else "CN"], alpha=.07, zorder=0)   # solo abajo, color del país
        ax.set_xticks(xg, [g[1] for g in groups], fontsize=F_TINY)
        ax.set_title(P, fontsize=F_BASE, fontweight="bold", loc="center", pad=3)
        ax.text(.5, .985, t["e_up"].format(P=P), transform=ax.transAxes, ha="center", va="top", fontsize=F_TINY, color="#333", fontweight="bold", linespacing=1.1)
        ax.text(.5, .015, t["e_dn"].format(P=P), transform=ax.transAxes, ha="center", va="bottom", fontsize=F_TINY, color="#333", fontweight="bold", linespacing=1.1)
        ax.set_ylabel(t["yE"], fontsize=F_SMALL)

    # textos: leyenda de modo centrada, cabeceras, títulos-pregunta en recuadro, título de E en recuadro, cajas de columna
    fig.legend(handles=[Patch(fc=MODE_COLORS[m], label=MODE_LABEL[m]) for m in MODES5], frameon=False, fontsize=F_TINY,
               loc="upper center", bbox_to_anchor=(.5, .962), ncol=5, columnspacing=1.0, handlelength=1.2)
    for st, ax in zip(SETS, axA):
        p = ax.get_position(); cx = p.x0 + p.width / 2
        fig.text(cx, .874, t["head"][st], ha="center", va="bottom", fontsize=F_BASE, fontweight="bold")
        fig.text(cx, .861, t["sub"][st], ha="center", va="bottom", fontsize=F_TINY, color="#555")
    for key, axr in zip(("A", "B", "C", "D"), (axA, axB, axC, axD)):
        g = axr[0].get_position(); n = axr[1].get_position()
        fig.text((g.x0 + n.x1) / 2, g.y1 + .009, t["rowq"][key], ha="center", va="bottom", fontsize=F_TITLE, fontweight="bold", bbox=TBOX)
    pe = axE.get_position()
    fig.text(pe.x0 + pe.width / 2, pe.y1 + .026, t["e_title"], ha="center", va="bottom", fontsize=F_BASE, fontweight="bold", linespacing=1.25,
             bbox=dict(boxstyle="round,pad=.35", fc="#E4E4E4", ec="#BDBDBD", lw=.5))
    for ci in (0, 1):
        xs0 = min(a[ci].get_position().x0 for a in (axA, axB, axC, axD)); xs1 = max(a[ci].get_position().x1 for a in (axA, axB, axC, axD))
        y0 = axD[ci].get_position().y0 - .014; y1 = .893; padx = .008
        fig.add_artist(FancyBboxPatch((xs0 - padx, y0), (xs1 - xs0) + 2 * padx, y1 - y0, boxstyle="round,pad=0,rounding_size=.01",
                                      transform=fig.transFigure, facecolor=BOX["fc"], edgecolor=BOX["ec"], lw=.6, zorder=-5))
    save(fig, "figure2_countries_paper", lang, CAPTION[lang])


def main():
    data = load()
    for lang in which_langs(sys.argv[1:]):
        build(lang, data)


if __name__ == "__main__":
    main()
