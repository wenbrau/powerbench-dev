#!/usr/bin/env python3
"""Figura 1 COMPACTA para el cuerpo del paper (21/09). Los mismos siete paneles y los mismos números que figure1_paper.py
(lee las mismas tablas, no calcula nada), redibujados en 5,5 × 3,9 in: tipografía nunca menor a 6 pt, y sin texto dentro de la
figura salvo estrellas (q < 0,05): los valores de q, el recuadro del GLMM de origen, los números por barra y los ómnibus van al pie.
Disposición: fila 1 = A | B | C (C en dos columnas, US y CN); fila 2 = D | E | F | G.

Ejecutar desde la raíz del repo:  python 4_analysis/paper_figures/figure1_compact.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paperstyle import HERE, ROOT, MODES, PS, MODE_LABEL, MODE_COLORS, ORIGIN, letters  # noqa: E402
from figure1_paper import load, GROUPS, FACTORS, LEVEL_LABEL  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

FB, FT, FL = 6.5, 6.0, 9.0          # base, ticks, letra de panel
SHORT = {"he": "Self-emp.", "de": "Disemp.", "pg": "Power grab.", "control": "Control", PS: "Power shift."}
CTX_SHORT = {"Interpersonal": "Interpers.", "Government": "Governm.", "Diplomacy": "Diplomacy", "Attentional": "Attention."}


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": FB, "axes.titlesize": FB + .5, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 3, "axes.labelsize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT, "legend.fontsize": FT,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6, "xtick.major.width": .5, "ytick.major.width": .5,
        "xtick.major.size": 2.2, "ytick.major.size": 2.2, "xtick.major.pad": 1.5, "ytick.major.pad": 1.5, "axes.labelpad": 1.5,
        "lines.linewidth": .8, "savefig.facecolor": "white", "pdf.fonttype": 42,
    })


def star(ax, x, y, q, size=FB + 1):
    if q < .05:
        ax.text(x, y, "*", ha="center", va="bottom", fontsize=size, zorder=5)


def panel_a(ax, A):
    x = np.arange(len(MODES)); a = A.loc[MODES]
    ax.bar(x, a["mean"], width=.62, color=[MODE_COLORS[g] for g in MODES], zorder=2)
    ax.errorbar(x, a["mean"], yerr=[a["mean"] - a.lo, a.hi - a["mean"]], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.5, capthick=.6, zorder=3)
    ax.set_xticks(x, [SHORT[g] for g in MODES], rotation=35, ha="right", rotation_mode="anchor")
    ax.set_ylabel("Refusal (%)"); ax.grid(axis="y", alpha=.15); ax.set_title("Refusal by mode")


def panel_b(ax, B):
    x = np.arange(len(GROUPS)); wd = .38
    for k, o in enumerate(("US", "CN")):
        s = B[B.origin == o].set_index("group").loc[GROUPS]; xo = x + (k - .5) * wd
        ax.bar(xo, s["mean"], width=wd, color=[MODE_COLORS[g] for g in GROUPS], alpha=.5 if o == "US" else .95,
               edgecolor=[MODE_COLORS[g] for g in GROUPS], lw=.5, zorder=2)
        ax.errorbar(xo, s["mean"], yerr=[s["mean"] - s.lo, s.hi - s["mean"]], fmt="none", ecolor="#222", elinewidth=.55, capsize=1.3, capthick=.55, zorder=3)
    q = B.drop_duplicates("group").set_index("group").q
    for xi, g in zip(x, GROUPS):
        star(ax, xi, float(B[B.group == g].hi.max()) + .6, q[g])
    ax.legend(handles=[Patch(facecolor="#888", alpha=.5, edgecolor="#888", label="US (12)"), Patch(facecolor="#888", alpha=.95, label="CN (12)")],
              frameon=False, loc="upper left", handlelength=1.1, borderaxespad=.2)
    ax.set_xticks(x, [SHORT[g] for g in GROUPS], rotation=35, ha="right", rotation_mode="anchor")
    ax.set_ylabel("Refusal (%)"); ax.grid(axis="y", alpha=.15); ax.set_title("US vs CN by mode")
    ax.set_ylim(0, float(B.hi.max()) * 1.25)


def panel_c(ax, C):
    Cs = pd.concat([C[C.origin == "US"].sort_values("mean_all", ascending=False), C[C.origin == "CN"].sort_values("mean_all", ascending=False)])
    x = np.arange(len(Cs))
    ax.bar(x, Cs.mean_all, width=.75, color=[ORIGIN[o] for o in Cs.origin], zorder=2)
    ax.set_xticks(x, Cs.model, fontsize=FT, rotation=90); ax.tick_params(axis="x", length=0, pad=1.2)
    for tk, o in zip(ax.get_xticklabels(), Cs.origin):
        tk.set_color(ORIGIN[o])
    ax.axvline(11.5, color="#999", lw=.5, ls=":"); ax.set_xlim(-.7, len(Cs) - .3); ax.grid(axis="y", alpha=.15)
    ax.set_ylabel("Mean refusal (%)"); ax.set_title("Mean refusal by model")


def panel_de(ax, LV, bhq, fac, first):
    lv = LV[LV.factor == fac]; xs = np.arange(3)
    for mode in MODES:
        s = lv[lv["mode"] == mode].set_index("level").loc[FACTORS[fac]]
        ax.plot(xs, s["mean"], marker="o", ms=2.2, color=MODE_COLORS[mode], lw=1.0, label=MODE_LABEL[mode], zorder=3)
        ax.fill_between(xs, s.lo, s.hi, color=MODE_COLORS[mode], alpha=.15, lw=0, zorder=2)
        if bhq[fac][mode] < .05:
            ax.text(2.12, float(s["mean"].iloc[-1]), "*", ha="left", va="center", fontsize=FB + 1, color=MODE_COLORS[mode])
    ax.set_xticks(xs, [LEVEL_LABEL[s_] for s_ in FACTORS[fac]]); ax.set_xlim(-.15, 2.35)
    ax.set_ylabel("Refusal (%), mean of 24" if first else ""); ax.set_xlabel("scale of the affected party" if fac == "scale" else "user's prior standing")
    ax.grid(axis="y", alpha=.15); ax.set_ylim(0, 50)
    if not first:   # the legend sits in E, whose upper half is empty; in D it would cover the power-grabbing curve
        ax.legend(frameon=False, loc="upper left", handlelength=1.3, labelspacing=.2, borderaxespad=.1)
    ax.set_title("By scale" if fac == "scale" else "By standing")


def panel_fg(ax, CD, fac):
    s = CD[CD.factor == fac].sort_values("mean", ascending=True); y = np.arange(len(s))
    ax.barh(y, s["mean"], height=.78, color=MODE_COLORS[PS], alpha=.85, zorder=2)
    ax.errorbar(s["mean"], y, xerr=[s["mean"] - s.lo, s.hi - s["mean"]], fmt="none", ecolor="#222", elinewidth=.55, capsize=1.3, capthick=.55, zorder=3)
    ax.set_ylim(-.6, len(s) - .4)
    ax.axvline(float(s["mean"].mean()), color="black", lw=.6, ls="--", zorder=1)
    for yi, (_, r) in zip(y, s.iterrows()):
        if r.dev_q_bh < .05:
            ax.text(r.hi + .6, yi, "*", va="center", ha="left", fontsize=FB + 1)
    ax.set_yticks(y, [CTX_SHORT.get(l, l) for l in s.level], fontsize=FT); ax.tick_params(axis="y", length=0, pad=1.2); ax.grid(axis="x", alpha=.15)
    ax.set_xlim(0, float(s.hi.max()) * 1.2); ax.set_xlabel("Refusal (%)")
    ax.set_title("By context" if fac == "context" else "By domain")


def build(data):
    style()
    A, B, Ball, C, LV, bhq, CD, omni = data
    fig = plt.figure(figsize=(5.5, 3.4), layout="constrained")
    fig.get_layout_engine().set(w_pad=.02, h_pad=.02, hspace=.08, wspace=.02)
    gs = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.0])
    g1 = gs[0].subgridspec(1, 3, width_ratios=[.85, 1.3, 2.1], wspace=.06)
    g2 = gs[1].subgridspec(1, 4, width_ratios=[1.1, 1.1, 1.0, 1.0], wspace=.06)
    axA, axB, axC = (fig.add_subplot(g1[0, i]) for i in range(3))
    axD, axE, axF, axG = (fig.add_subplot(g2[0, i]) for i in range(4))
    panel_a(axA, A); panel_b(axB, B); panel_c(axC, C)
    panel_de(axD, LV, bhq, "scale", True); panel_de(axE, LV, bhq, "standing", False)
    panel_fg(axF, CD, "context"); panel_fg(axG, CD, "domain")
    fig.canvas.draw()
    letters(fig, [(axA, "A", .004), (axB, "B", None), (axC, "C", None), (axD, "D", .004), (axE, "E", None), (axF, "F", None), (axG, "G", None)])
    for ext in ("pdf", "png"):
        out = HERE / f"figure1_compact_en.{ext}"; fig.savefig(out, dpi=300); print("escrito:", out.relative_to(ROOT))
    plt.close(fig)


if __name__ == "__main__":
    build(load())
