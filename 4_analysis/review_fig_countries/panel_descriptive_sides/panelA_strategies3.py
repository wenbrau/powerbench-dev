#!/usr/bin/env python3
"""Idea de Wendy (2026-09-20) para el panel A: mantener los colores principales del modo, las dos barras
desaturadas (una más que otra) y un FONDO clarito azul (lado USA) / rojo (lado China) detrás de cada barra.
Tres variantes: fondo a toda altura; fondo solo arriba de la barra; fondo a toda altura con desaturación igual.
Set geo, 4 modos, con IC 95 % t entre 24 modelos.

Uso:  python 4_analysis/review_fig_countries/panel_descriptive_sides/panelA_strategies3.py
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


def main():
    pmr = pd.read_csv(PMR)
    x = np.arange(len(MODES)); w = .38; YM = 42
    styles = ["10 · fondo clarito a toda altura · US menos desat. (20 %), China más (45 %)",
              "11 · fondo clarito solo ARRIBA de la barra · misma desaturación que 10",
              "12 · fondo clarito a toda altura · ambas igual de desaturadas (30 %)"]
    fig, axes = plt.subplots(1, len(styles), figsize=(19, 5), sharey=True)
    for ax, sty in zip(axes, styles):
        for i, m in enumerate(MODES):
            for side, off in (("us", -w / 2), ("cn", w / 2)):
                mu, lo, hi = ci(pmr, m, side)
                base = MODE_COLORS[m]; tgt = US if side == "us" else CN
                xx = x[i] + off
                if sty.startswith("12"):
                    f = .30
                else:
                    f = .20 if side == "us" else .45
                # fondo clarito del lado
                if sty.startswith("11"):
                    ax.bar(xx, YM - mu, w + .02, bottom=mu, color=tgt, alpha=.14, lw=0, zorder=1)
                else:
                    ax.bar(xx, YM, w + .02, color=tgt, alpha=.14, lw=0, zorder=1)
                ax.bar(xx, mu, w, color=mix(base, "#FFFFFF", f), edgecolor=mix(base, "#FFFFFF", f * .5), lw=.6, zorder=2)
                ax.errorbar(xx, mu, yerr=[[mu - lo], [hi - mu]], fmt="none", ecolor="#222", elinewidth=1.1, capsize=3, capthick=1.1, zorder=5)
        ax.set_xticks(x, [LAB[m] for m in MODES], fontsize=8.5, rotation=20, ha="right", rotation_mode="anchor")
        ax.set_title(sty, fontsize=8.8, fontweight="bold"); ax.grid(axis="y", alpha=.15); ax.set_ylim(0, YM)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Refusal (%) · media 24 modelos", fontsize=9)
    fig.legend(handles=[Patch(fc=US, alpha=.14, label="fondo azul = usuario lado USA"), Patch(fc=CN, alpha=.14, label="fondo rojo = usuario lado China")],
               frameon=False, fontsize=10, loc="upper center", ncol=2, bbox_to_anchor=(.5, 1.07))
    fig.suptitle("Panel A: colores del modo desaturados + fondo clarito azul/rojo por lado · set geo, IC 95 % t · elegir una", fontsize=12, y=1.14)
    out = HERE / "panelA_strategies3.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
