#!/usr/bin/env python3
"""Figura 2 COMPACTA para el cuerpo del paper (21/09). Los mismos cinco paneles (A–D a la izquierda, geo | neutral; E a la derecha,
US y China) y los mismos números que figure2_countries_paper.py (lee las mismas tablas, no calcula nada), en 5,5 × 4,3 in:
tipografía nunca menor a 6 pt; sin valores de q, flechas ni títulos-pregunta dentro de la figura (estrellas para q < 0,05; el resto
va al pie).

Ejecutar desde la raíz del repo:  python 4_analysis/paper_figures/figure2_compact.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paperstyle import HERE, ROOT, MODES, PS, MODE_COLORS, ORIGIN, or_axis  # noqa: E402
RESULTS97 = ROOT / "4_analysis" / "results" / "97_fig1c_fig2a_intervals_capability"
from figure2_countries_paper import load, SETS, MODES5, XS, XSEP, SIDE_COL, DESAT, DY, mix, shade_dir  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

FB, FT, FL = 6.5, 6.0, 9.0
MODE_LEG = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT", PS: "PS (pooled)"}
NEUTRAL_BG = "#666666"   # (25/09) backdrop of the neutral-countries column in A: grey, since neither side there is the US or China
DYL = {"us_ally": "ally", "us_neutral": "neutral", "us_rival": "rival", "us_cn": "China", "cn_ally": "ally", "cn_neutral": "neutral", "cn_rival": "rival", "cn_us": "US"}


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": FB, "axes.titlesize": FB + .5, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 3, "axes.labelsize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT, "legend.fontsize": FT,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6, "xtick.major.width": .5, "ytick.major.width": .5,
        "xtick.major.size": 2.2, "ytick.major.size": 2.2, "xtick.major.pad": 1.5, "ytick.major.pad": 1.5, "axes.labelpad": 1.5,
        "lines.linewidth": .8, "savefig.facecolor": "white", "pdf.fonttype": 42,
    })


def or_panel(ax, OR, l, h, q, lo, hi, shade=True):
    x = XS; OR, l, h = np.asarray(OR, float), np.asarray(l, float), np.asarray(h, float)
    ax.bar(x, OR - 1, bottom=1, width=.6, color=[MODE_COLORS[m] for m in MODES5], zorder=2)
    ax.errorbar(x, OR, yerr=[OR - l, h - OR], fmt="none", ecolor="#111", elinewidth=.55, capsize=1.3, capthick=.55, zorder=3)
    for xi, o, ll, hh, qi in zip(x, OR, l, h, q):
        if qi < .05:
            if o >= 1:
                ax.text(xi, hh * 1.02, "*", ha="center", va="bottom", fontsize=FB + 1)
            else:
                ax.text(xi, ll / 1.03, "*", ha="center", va="top", fontsize=FB + 1)
    or_axis(ax, [.7, 1, 1.5], lo, hi)
    if shade:   # US / China shading only in the US side / China side column (25/09)
        shade_dir(ax, lo, hi)


def build(data):
    style()
    B, C, D, E, Ed, vals, B86, C86 = data
    cols5 = [MODE_COLORS[m] for m in MODES5]
    # 3.95 -> 3.15 in (23/09, to fit 9 pages): the margins and the gaps between rows keep their size in inches, the panels get shorter
    H0, H = 3.95, 3.15
    top, bottom = 1 - ((1 - .83) * H0 - .15) / H, .065 * H0 / H   # the legend takes one row instead of two (-.15 in)
    gap = .45 * ((.83 - .065) * H0 / (4 + 3 * .45))              # the old gap between rows, in inches
    rowh = ((top - bottom) * H - 3 * gap) / 4
    fig = plt.figure(figsize=(5.5, H))
    gs = fig.add_gridspec(4, 4, height_ratios=[.75, 1.08, 1.08, 1.08], width_ratios=[1.0, 1.0, .22, 1.6], left=.085, right=.985, top=top, bottom=bottom, hspace=gap / rowh, wspace=.14)
    x = XS; w = .38

    def row(ri):
        a0 = fig.add_subplot(gs[ri, 0]); a1 = fig.add_subplot(gs[ri, 1], sharey=a0); a1.tick_params(labelleft=False)
        return [a0, a1]
    axA, axB, axC, axD = row(0), row(1), row(2), row(3)
    for ax in axA + axB + axC + axD:
        ax.set_xticks(x, [""] * 5); ax.set_xlim(-.6, XS[-1] + .6); ax.axvline(XSEP, color="#999", lw=.5, ls=":", zorder=1)

    # 95% t interval across the 24 models for each bar, as in Figure 1A (block 97, Nico 25/09)
    CI = pd.read_csv(RESULTS97 / "fig2a_side_rates_ci.csv").set_index(["set", "mode", "side"])
    ytop = max(max(vals.values()), float(CI.hi.max())) * 1.08
    for ax, st in zip(axA, SETS):
        for i, m in enumerate(MODES5):
            if st != "geo":   # one grey backdrop for the pair, same span as the two side backdrops (no overlap seam)
                ax.bar(x[i], ytop, 2 * w + .02, color=NEUTRAL_BG, alpha=.14, lw=0, zorder=1)
            for side, off in (("us", -w / 2), ("cn", w / 2)):
                if st == "geo":
                    ax.bar(x[i] + off, ytop, w + .02, color=SIDE_COL[side], alpha=.14, lw=0, zorder=1)
                ax.bar(x[i] + off, vals[(st, m, side)], w, color=mix(MODE_COLORS[m], "#FFFFFF", DESAT[side]),
                       edgecolor=mix(MODE_COLORS[m], "#FFFFFF", DESAT[side] * .5), lw=.3, zorder=2)
                ci = CI.loc[(st, m, side)]
                assert abs(float(ci["mean"]) - vals[(st, m, side)]) < 1e-6
                ax.errorbar(x[i] + off, ci["mean"], yerr=[[ci["mean"] - ci.lo], [ci.hi - ci["mean"]]], fmt="none", ecolor="#222", elinewidth=.5, capsize=1.0, capthick=.5, zorder=3)
        ax.grid(axis="y", alpha=.15); ax.set_ylim(0, ytop)
    axA[0].set_ylabel("Refusal (%)")
    axA[0].set_title("Refusal by user's side"); axA[1].set_title("neutral countries", fontweight="normal")

    for ax, st in zip(axB, SETS):
        r = B.loc[st].loc[MODES]; b = B86.loc[st]
        ex = np.array(list(r.excess) + [b.excess]); lo = np.array(list(r.lo) + [b.lo]); hi = np.array(list(r.hi) + [b.hi]); q = list(r.q_bh) + [b.q_bh]
        ax.bar(x, ex, width=.6, color=cols5, zorder=2)
        ax.errorbar(x, ex, yerr=[ex - lo, hi - ex], fmt="none", ecolor="#222", elinewidth=.55, capsize=1.3, capthick=.55, zorder=3)
        ax.axhline(0, color="black", lw=.6, ls="--", zorder=1)
        for xi, h, qi in zip(x, hi, q):
            if qi < .05:
                ax.text(xi, max(h, 0) + .005, "*", ha="center", va="bottom", fontsize=FB + 1)
        ax.grid(axis="y", alpha=.15); ax.set_ylim(-.145, .30)   # data span -0.13 to 0.22, plus room for the asterisks inside the axes (Nico 23/09: tighter axes)
    axB[0].set_ylabel("|bias|" + chr(10) + "$-$ chance"); axB[0].set_title("Bias beyond chance")

    LO, HI = .68, 1.62   # data span 0.72 to 1.37 in C and D, plus the asterisks inside the axes (Nico 23/09: tighter axes)
    for ax, st in zip(axC, SETS):
        r = C.loc[st].loc[MODES]; g = C86.loc[st]
        or_panel(ax, list(r.OR) + [g.OR], list(r.OR_lo) + [g.OR_lo], list(r.OR_hi) + [g.OR_hi], list(r.q_bh) + [g.q_bh], LO, HI, shade=st == "geo")
    for ax, st in zip(axD, SETS):
        r = D.loc[st].loc[MODES5]; or_panel(ax, r.odds_ratio, r.boot_lo, r.boot_hi, r.boot_q.values, LO, HI, shade=st == "geo")
    axC[0].set_ylabel("OR (GLMM)"); axC[0].set_title("US side vs China side")
    axD[0].set_ylabel("OR (usage-wt.)"); axD[0].set_title("Same, usage-weighted")

    gsR = gs[:, 3].subgridspec(2, 1, hspace=.26 * H0 / H)   # a bit less gap so that each E panel stays as tall as its y label
    axE = fig.add_subplot(gsR[0]); axF = fig.add_subplot(gsR[1])
    w4 = .8 / len(MODES); ELO, EHI = .5, 1.9   # data span 0.58 to 1.65, plus the asterisks (Nico 23/09: tighter axes)
    for ax, pole in ((axE, "usa"), (axF, "china")):
        P = "US" if pole == "usa" else "China"
        groups = [("joint", "all four")] + [(dy, DYL[dy]) for dy in DY[pole]]; xg = np.arange(len(groups))
        for k, mode in enumerate(MODES):
            v = pd.DataFrame([(E[(E.country == pole) & (E["mode"] == mode)] if key == "joint" else Ed[(Ed.dyad == key) & (Ed["mode"] == mode)]).iloc[0]
                              for key, _ in groups])
            xo = xg + (k - (len(MODES) - 1) / 2) * w4
            ax.bar(xo, v.OR.values - 1, bottom=1, width=w4, color=MODE_COLORS[mode], alpha=.9, zorder=2)
            ax.errorbar(xo, v.OR.values, yerr=[v.OR.values - v.OR_lo.values, v.OR_hi.values - v.OR.values], fmt="none", ecolor="#111", elinewidth=.5, capsize=1.1, capthick=.5, zorder=3)
            for xi, (_, rr) in zip(xo, v.iterrows()):
                if rr.q_bh < .05:   # above the interval when OR > 1, below it when OR < 1
                    if rr.OR >= 1:
                        ax.text(xi, rr.OR_hi * 1.02, "*", ha="center", va="bottom", fontsize=FB + 1)
                    else:
                        ax.text(xi, rr.OR_lo / 1.03, "*", ha="center", va="top", fontsize=FB + 1)
        or_axis(ax, [.5, .67, 1, 1.5], ELO, EHI)
        ax.axvspan(-.5, .5, color="#000", alpha=.05, zorder=0); ax.axvline(.5, color="#666", lw=.6, ls="--")
        ax.axhspan(ELO, 1, color=ORIGIN["US" if pole == "usa" else "CN"], alpha=.07, zorder=0)
        ax.set_xticks(xg, [g[1] for g in groups], fontsize=FT)
        ax.set_ylabel(f"OR, {P} as user / as target")
        ax.set_title(f"Bias with respect to {P}")

    fig.legend(handles=[Patch(fc=MODE_COLORS[m], label=MODE_LEG[m]) for m in MODES5] + [Patch(fc=SIDE_COL["us"], alpha=.2, label="US-side user"), Patch(fc=SIDE_COL["cn"], alpha=.2, label="China-side user")],
               frameon=False, fontsize=FT, loc="upper center", bbox_to_anchor=(.5, 1.0), ncol=7, columnspacing=1.0, handlelength=1.1)
    for st, ax in zip(SETS, axA):
        p = ax.get_position()
        fig.text(p.x0 + p.width / 2, p.y1 + .06 * H0 / H, "US side / China side" if st == "geo" else "neutral A / neutral B", ha="center", va="bottom", fontsize=FB, fontweight="bold")
    for key, axr, xo in (("A", axA, .008), ("B", axB, .008), ("C", axC, .008), ("D", axD, .008)):
        g = axr[0].get_position(); fig.text(xo, g.y1 + .012 * H0 / H, key, fontsize=FL, fontweight="bold", ha="left", va="bottom")
    pe = axE.get_position(); fig.text(pe.x0 - .1, pe.y1 + .012 * H0 / H, "E", fontsize=FL, fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        out = HERE / f"figure2_compact_en.{ext}"; fig.savefig(out, dpi=300); print("escrito:", out.relative_to(ROOT))
    plt.close(fig)


if __name__ == "__main__":
    build(load())
