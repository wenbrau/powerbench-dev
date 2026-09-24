#!/usr/bin/env python3
"""Figura 4 (idiomas, 22 modelos) COMPACTA para el cuerpo del paper (21/09). Los mismos seis paneles y los mismos números que
figure_22models.py (mismas tablas, mismas funciones de dibujo donde se reutilizan; no calcula nada), en 5,5 × 4,3 in: tipografía
nunca menor a 6 pt; sin notas ni etiquetas de texto dentro de la figura más allá de las estrellas (BH) y las etiquetas de eje.
Disposición: fila 1 = A | B | C; fila 2 = D | E | F.

Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_languages_22models/figure_22models_compact.py
"""
from __future__ import annotations

from _common import HERE, ROOT, MODES, LANG_NAME, load22
import sys
sys.path.insert(0, str(ROOT / "4_analysis" / "paper_figures"))
from _paperstyle import short  # noqa: E402
import figure_paper as fp
import figure_paper_v2 as fv2
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- las mismas redirecciones que figure_22models.py
fp.GLMM36 = HERE / "glmm_nagq1"
fp.TB = HERE / "panelD_bootstrap.csv"
fp.TC = HERE / "panelF_test_stats_power_shifting.csv"
fp.TD = HERE / "F6_exceso_ps.csv"
fp.EXCL_SW = set()
fp.N_PAIRS = {"CN–CN": 66, "US–US": 45, "mixto": 120}
fv2.R81 = HERE / "concordance"
fv2.HERE = HERE
fv2.fp = fp

FB, FT, FL = 6.5, 6.0, 9.0
for mod in (fp, fv2):
    mod.F_TITLE, mod.F_BASE, mod.F_TICK, mod.F_SMALL, mod.F_TINY, mod.F_LETTER = FB + .5, FB, FT, FT, FT, FL
fp.MODE_LABEL2 = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT"}
fp.MODE_LABEL = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT"}      # panel A legend
fv2.MODE_SHORT = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT"}     # panel B and C ticks
ORIGIN, ORIGIN_LIGHT = fp.ORIGIN, fp.ORIGIN_LIGHT


def panel_e(ax):
    tab = pd.read_csv(fp.TD).sort_values("excess", ascending=False).reset_index(drop=True)
    tab["sig_bh"] = tab.sig_bh.fillna("")
    n = len(tab); y = np.arange(n)
    ax.barh(y, tab.null_mean, color=[ORIGIN_LIGHT[o] for o in tab.origin], height=.72, zorder=2)
    ax.barh(y, tab.excess.clip(lower=0), left=tab.null_mean, color=[ORIGIN[o] for o in tab.origin], height=.72, zorder=3)
    neg = tab.excess < 0
    if neg.any():
        ax.barh(y[neg], tab.excess[neg], left=tab.null_mean[neg], color="none", edgecolor=[ORIGIN[o] for o in tab.origin[neg]], height=.72, zorder=3, hatch="////", lw=.4)
    ax.scatter(tab.null_p95, y, marker="|", s=24, color="#222", lw=.7, zorder=4)
    for i, r in tab.iterrows():
        if r.sig_bh:
            ax.text(max(r.range_pp, r.null_p95) + .6, i, "*", va="center", ha="left", fontsize=FB + 1)
    ax.set_yticks(y, [short(m) for m in tab.model], fontsize=FT); ax.tick_params(axis="y", length=0, pad=1.2)
    for lab, o in zip(ax.get_yticklabels(), tab.origin):
        lab.set_color(ORIGIN[o])
    ax.set_ylim(n - .4, -.6); ax.set_xlabel("refusal range (pp)"); ax.set_xlim(0, float(tab.range_pp.max()) * 1.15); ax.grid(axis="x", alpha=.15)
    ax.legend(handles=[Patch(color="#C9C9C9", label="chance"), Patch(color="#666", label="excess")], frameon=False, fontsize=FT, loc="lower right",
              handlelength=1.0, labelspacing=.2, borderaxespad=.2)
    ax.set_title("Range per model")


def panel_f_inset(axF, S, contrast_p, qf):
    """Mean agreement by pair type (CN-CN, US-US, mixed), chance band from languages permuted within each model, stars = BH over the
    three pair types; bracket = same-DC against mixed pairs (DC labels permuted across models). Stored tests, nothing recomputed."""
    from matplotlib.patches import Rectangle
    axb = axF.inset_axes([.43, .60, .56, .36])
    kinds = list(fp.KINDS); cols = [ORIGIN["CN"], ORIGIN["US"], "#8A7FA3"]
    obs = [float(S[k].observed) for k in kinds]
    axb.bar(range(3), obs, color=cols, alpha=.9, width=.66, zorder=2)
    for i, k in enumerate(kinds):
        axb.add_patch(Rectangle((i - .4, float(S[k].null_lo)), .8, float(S[k].null_hi - S[k].null_lo), facecolor="#9AA0A6", alpha=.30, edgecolor="none", zorder=1))
        if qf[k] < .05:
            axb.text(i, obs[i] + .01, "*", ha="center", va="bottom", fontsize=FB + 1)
    axb.axhline(0, color="black", lw=.5, zorder=3)
    yb, tk = .215, .015
    axb.plot([0, 0, 1, 1], [yb - tk, yb, yb, yb - tk], color="#222", lw=.5)
    axb.plot([.5, .5, 2, 2], [yb, yb + tk, yb + tk, yb - tk], color="#222", lw=.5)
    if contrast_p < .05:
        axb.text(1.25, yb + tk + .003, "*", ha="center", va="bottom", fontsize=FB + 1)
    axb.set_xticks(range(3), ["CN–CN", "US–US", "mixed"], fontsize=FT, rotation=0, ha="center"); axb.set_xlim(-.6, 2.6); axb.set_ylim(-.12, .29); axb.set_yticks([0, .1, .2])
    axb.set_ylabel("mean ρ", fontsize=FT, labelpad=1); axb.tick_params(labelsize=FT, width=.4, length=1.5, pad=1)
    for sp in ("top", "right"):
        axb.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        axb.spines[sp].set_linewidth(.5)


def build(d):
    fp.style(); t = dict(fp.TXT["en"]); t2 = fv2.TXT["en"]
    t["a1_y"] = "Refusal (%)"
    plt.rcParams.update({"axes.titlesize": FB + .5, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlepad": 3, "legend.fontsize": FT})
    per_model = d.groupby(["mode", "lang", "model"]).refuse.mean().reset_index()
    rate = per_model.groupby(["mode", "lang"]).refuse.mean().mul(100)
    order = rate.reset_index().query("mode in ['he','de','pg']").groupby("lang").refuse.mean().sort_values().index.tolist()
    fp.LANGS79 = order
    # 4.7 -> 3.81 in (23/09, to fit 9 pages): margins and gaps keep their size in inches; the top row is 0.47 in and the
    # bottom row 0.42 in shorter (F keeps its aspect and is anchored at the top)
    H0, H = 4.7, 3.81
    def pos(x, y_in, w, h_in):
        return [x, y_in / H, w, h_in / H]
    fig = plt.figure(figsize=(5.5, H))
    axA = fig.add_axes(pos(.075, 2.776, .43, .658))
    axB = fig.add_axes(pos(.635, 2.776, .15, .658))
    axC = fig.add_axes(pos(.84, 2.776, .15, .658))
    axD = fig.add_axes(pos(.075, .423, .15, 1.836))
    axE = fig.add_axes(pos(.335, .3525, .17, 1.9065))
    axF = fig.add_axes(pos(.63, .423, .36, 1.836)); axF.set_anchor("N")
    qa, qd, qf, qtab = fv2.bh_q()
    fp.panel_a1(axA, d, t, q=qa); fv2.panel_a2_bump(axB, t2); fv2.panel_b_bars(axC, t2); fp.panel_b(axD, t, q=qd); panel_e(axE)
    S, contrast_p, _ = fp.panel_c(axF, d, t, q=qf, inset=False, cb_rect=[.02, -.07, .42, .03])
    LANG_ABBR = {"en": "Eng", "es": "Spa", "de": "Ger", "fr": "Fre", "hi": "Hin", "sw": "Swa", "zh": "Chi", "pt": "Por"}   # (Nico, 23/09) unrotated
    axA.set_xticks(axA.get_xticks(), [LANG_ABBR[l] for l in order], fontsize=FT, rotation=0, ha="center"); axA.set_title("Refusal by language and request type")
    axA.set_ylim(0, 35); axA.legend(frameon=False, loc="upper left", ncol=4, handlelength=1.1, columnspacing=1.0, borderaxespad=.2, fontsize=FT)
    for txt in list(axB.texts):   # language names on the left side only (Nico, 23/09)
        if txt.get_position()[0] > 1.5:
            txt.remove(); continue
        txt.set_text(txt.get_text().rstrip("*")); txt.set_fontsize(FT)
    axB.set_xlim(-1.35, 3.35)
    from collections import defaultdict
    groups = defaultdict(list)
    for txt in axB.texts:
        x, y = txt.get_position(); groups[(round(x, 2), round(y, 3))].append(txt)
    for (x, y), ts in groups.items():
        if len(ts) > 1:
            for k, txt in enumerate(ts):
                txt.set_position((x, y + (k - (len(ts) - 1) / 2) * .55))
    axB.set_title("Language order"); axB.set_ylabel("")
    axB.set_xticks(axB.get_xticks(), [lab.get_text() for lab in axB.get_xticklabels()], fontsize=FT, rotation=0, ha="center")
    import re
    for txt in list(axC.texts):   # the p labels of the two one-sample tests become stars (p < 0.05); the values go to the appendix table
        m = re.search(r"p\s*([<=])\s*([0-9.]+)", txt.get_text())
        if m and float(m.group(2)) < .05 or (m and m.group(1) == "<"):
            txt.set_text("*"); txt.set_fontsize(FB + 1)
        else:
            txt.remove()
    axC.set_title(""); axC.set_title("", loc="center"); axC.set_title("Order across" + chr(10) + "request types", loc="left"); axC.set_ylabel(""); axC.set_xticks([0, 1], ["PS", "CT"], fontsize=FT, rotation=0, ha="center")
    axC.set_ylim(-.05, .8)
    axD.set_title("Range beyond" + chr(10) + "chance"); axD.set_ylabel("observed / chance range")
    h, l = axD.get_legend_handles_labels(); axD.legend(h, ["equal", "usage"], frameon=False, loc="lower right", handlelength=1.0, borderaxespad=.1, labelspacing=.2, fontsize=FT)
    for ax_ in (axA, axD):   # one significance level in every body figure: * = q < 0.05
        for txt in ax_.texts:
            if txt.get_text().strip() and set(txt.get_text().strip()) == {"*"}:
                txt.set_text("*")
    axD.set_xticks(range(len(MODES)), [fp.MODE_LABEL2[m] for m in MODES], fontsize=FT, rotation=0, ha="center")
    axF.set_title("Model agreement", x=0); axF.tick_params(axis="x", labelsize=FT); axF.tick_params(axis="y", labelsize=FT)
    for cbax in axF.child_axes:   # the colorbar (the only child so far)
        cbax.set_xticks([-1, 0, 1])
    panel_f_inset(axF, S, contrast_p, qf)   # after the loop above, which would reset its ticks
    axF.set_xticks([])   # rows and columns list the same models in the same order; the column labels do not fit
    _labs = axF.get_yticklabels(); _cols = [l.get_color() for l in _labs]
    axF.set_yticks(axF.get_yticks(), [short(l.get_text()) for l in _labs])
    for l, c in zip(axF.get_yticklabels(), _cols):
        l.set_color(c)
    fig.canvas.draw()
    for ax, s, xo in ((axA, "A", .008), (axB, "B", .525), (axC, "C", .812), (axD, "D", .008), (axE, "E", .255), (axF, "F", .545)):
        x0, y0, w, h = ax.get_position().bounds
        fig.text(xo, y0 + h + .012 * H0 / H, s, fontsize=FL, fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        out = HERE / f"figure_22models_compact_en.{ext}"; fig.savefig(out, dpi=300); print("escrito:", out.relative_to(ROOT))
    plt.close(fig)
    stray = HERE / fv2.BHQ_NAME
    if stray.exists():
        stray.unlink()


if __name__ == "__main__":
    d, _ = load22()
    build(d)
