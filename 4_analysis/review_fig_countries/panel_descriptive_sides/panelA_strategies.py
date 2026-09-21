#!/usr/bin/env python3
"""Comparación de estrategias para codificar lado USA / lado China en las barras del panel A descriptivo
(pedido de Wendy 2026-09-20: las rayas rojas/azules "se ven de otro color"; probar varias y elegir).
Set geo, 4 modos, dos barras por modo (US / China), CON IC 95 % t entre 24 modelos.

Uso:  python 4_analysis/review_fig_countries/panel_descriptive_sides/panelA_strategies.py
"""
from __future__ import annotations
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for p in (str(ROOT / "4_analysis"), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb
import numpy as np, pandas as pd
from scipy.stats import t as tdist

MODES = ("he", "de", "pg", "control")
LAB = {"he": "Self-emp.", "de": "Disemp.", "pg": "Power grab.", "control": "Control"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83"}
US, CN = "#326CA0", "#B44941"
PMR = ROOT / "4_analysis/results/21_d2_nationality_final/per_model_rates.csv"
CONDS = {"us": ["us_cn", "allyus_allycn"], "cn": ["cn_us", "allycn_allyus"]}


def ci(pmr, mode, side):
    v = pmr[(pmr["mode"] == mode) & pmr.condition.isin(CONDS[side])].groupby("target").rate.mean().to_numpy()
    m = v.mean(); h = tdist.ppf(.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v))
    return m, m - h, m + h


def blend(c, f):  # mezcla con blanco, f=0 sin cambio, f=1 blanco
    r, g, b = to_rgb(c); return (r + (1 - r) * f, g + (1 - g) * f, b + (1 - b) * f)


def eb(ax, xx, mu, lo, hi):
    ax.errorbar(xx, mu, yerr=[[mu - lo], [hi - mu]], fmt="none", ecolor="#222", elinewidth=1.1, capsize=3, capthick=1.1, zorder=5)


def main():
    pmr = pd.read_csv(PMR)
    x = np.arange(len(MODES)); w = .38
    styles = ["1 · claro / oscuro", "2 · borde de color del lado", "3 · rayas de color del lado",
              "4 · desaturado (China más pálido)", "5 · clave de color debajo"]
    fig, axes = plt.subplots(1, len(styles), figsize=(20, 4.6), sharey=True)
    plt.rcParams["hatch.linewidth"] = 1.6
    for ax, sty in zip(axes, styles):
        for i, m in enumerate(MODES):
            for side, off in (("us", -w / 2), ("cn", w / 2)):
                mu, lo, hi = ci(pmr, m, side)
                col = MODE_COLORS[m]
                if sty.startswith("1"):
                    ax.bar(x[i] + off, mu, w, color=col, alpha=.95 if side == "us" else .42, edgecolor=col, lw=.5, zorder=2)
                elif sty.startswith("2"):
                    ax.bar(x[i] + off, mu, w, facecolor=col, edgecolor=US if side == "us" else CN, lw=3, zorder=2)
                elif sty.startswith("3"):
                    ax.bar(x[i] + off, mu, w, facecolor=col, edgecolor=US if side == "us" else CN,
                           hatch="////" if side == "us" else "\\\\\\\\", lw=1.2, zorder=2)
                elif sty.startswith("4"):
                    ax.bar(x[i] + off, mu, w, color=col if side == "us" else blend(col, .55), edgecolor=col, lw=.6, zorder=2)
                elif sty.startswith("5"):
                    ax.bar(x[i] + off, mu, w, color=col, edgecolor=col, lw=.5, zorder=2)
                    ax.add_patch(plt.Rectangle((x[i] + off - w / 2, -2.1), w, 1.4, color=US if side == "us" else CN, clip_on=False, zorder=3))
                eb(ax, x[i] + off, mu, lo, hi)
        ax.set_xticks(x, [LAB[m] for m in MODES], fontsize=8, rotation=20, ha="right", rotation_mode="anchor")
        ax.set_title(sty, fontsize=10, fontweight="bold"); ax.grid(axis="y", alpha=.15); ax.set_ylim(0, 40)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Refusal (%) · media 24 modelos", fontsize=9)
    fig.legend(handles=[Patch(fc="#888", label="usuario lado USA"), Patch(fc="#888", alpha=.42, label="usuario lado China"),
                        Patch(fc="none", edgecolor=US, lw=2, label="azul = lado USA"), Patch(fc="none", edgecolor=CN, lw=2, label="rojo = lado China")],
               frameon=False, fontsize=9, loc="upper center", ncol=4, bbox_to_anchor=(.5, 1.06))
    fig.suptitle("Estrategias para lado USA / lado China en el panel A (set geo, con IC 95 % t)  ·  elegir una", fontsize=12, y=1.12)
    out = HERE / "panelA_strategies.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
