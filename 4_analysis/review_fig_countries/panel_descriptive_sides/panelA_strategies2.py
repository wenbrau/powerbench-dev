#!/usr/bin/env python3
"""Estrategias SIMÉTRICAS para lado USA / lado China en el panel A (pedido de Wendy 2026-09-20:
ninguna de las anteriores; la desaturada hace ver a China como secundario; que el color cambie para
LOS DOS lados con la misma entidad). Set geo, 4 modos, dos barras/modo, con IC 95 % t entre 24 modelos.

Uso:  python 4_analysis/review_fig_countries/panel_descriptive_sides/panelA_strategies2.py
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
US, CN = "#2E6FB0", "#C0392B"
PMR = ROOT / "4_analysis/results/21_d2_nationality_final/per_model_rates.csv"
CONDS = {"us": ["us_cn", "allyus_allycn"], "cn": ["cn_us", "allycn_allyus"]}


def ci(pmr, mode, side):
    v = pmr[(pmr["mode"] == mode) & pmr.condition.isin(CONDS[side])].groupby("target").rate.mean().to_numpy()
    m = v.mean(); h = tdist.ppf(.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v))
    return m, m - h, m + h


def mix(c, target, f):
    a, b = np.array(to_rgb(c)), np.array(to_rgb(target))
    return tuple(a + (b - a) * f)


def eb(ax, xx, mu, lo, hi):
    ax.errorbar(xx, mu, yerr=[[mu - lo], [hi - mu]], fmt="none", ecolor="#222", elinewidth=1.1, capsize=3, capthick=1.1, zorder=5)


def main():
    pmr = pd.read_csv(PMR)
    x = np.arange(len(MODES)); w = .38
    styles = ["6 · tinte simétrico 45 % (modo → azul US / rojo China)",
              "7 · tinte simétrico 70 %",
              "8 · modo + banda superior del color del lado (ambos)",
              "9 · modo + marco grueso del color del lado (ambos)"]
    fig, axes = plt.subplots(1, len(styles), figsize=(19, 4.8), sharey=True)
    for ax, sty in zip(axes, styles):
        for i, m in enumerate(MODES):
            for side, off in (("us", -w / 2), ("cn", w / 2)):
                mu, lo, hi = ci(pmr, m, side)
                base = MODE_COLORS[m]; tgt = US if side == "us" else CN
                xx = x[i] + off
                if sty.startswith("6"):
                    ax.bar(xx, mu, w, color=mix(base, tgt, .45), edgecolor=mix(base, tgt, .7), lw=.6, zorder=2)
                elif sty.startswith("7"):
                    ax.bar(xx, mu, w, color=mix(base, tgt, .70), edgecolor=tgt, lw=.6, zorder=2)
                elif sty.startswith("8"):
                    ax.bar(xx, mu, w, color=base, edgecolor=base, lw=.5, zorder=2)
                    ax.bar(xx, mu * .18, w, bottom=mu * .82, color=tgt, edgecolor=tgt, lw=0, zorder=3)
                elif sty.startswith("9"):
                    ax.bar(xx, mu, w, facecolor=base, edgecolor=tgt, lw=3.2, zorder=2)
                eb(ax, xx, mu, lo, hi)
        ax.set_xticks(x, [LAB[m] for m in MODES], fontsize=8, rotation=20, ha="right", rotation_mode="anchor")
        ax.set_title(sty, fontsize=9.5, fontweight="bold"); ax.grid(axis="y", alpha=.15); ax.set_ylim(0, 40)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Refusal (%) · media 24 modelos", fontsize=9)
    fig.legend(handles=[Patch(fc=US, label="lado USA (azul)"), Patch(fc=CN, label="lado China (rojo)")],
               frameon=False, fontsize=10, loc="upper center", ncol=2, bbox_to_anchor=(.5, 1.07))
    fig.suptitle("Estrategias SIMÉTRICAS lado USA / lado China (ambos cambian de color) · set geo, IC 95 % t · elegir una", fontsize=12, y=1.14)
    out = HERE / "panelA_strategies2.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
