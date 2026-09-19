#!/usr/bin/env python3
"""Revisión de la figura de países (19/09, pedido de Wendy): el panel C (pedido típico, tasas pesadas por los pedidos de
cada modelo en OpenRouter, bloque 73) con geo (lado USA / lado China, las dos díadas juntas) y neutral (neutral A /
neutral B, la referencia) en dos subpaneles separados, en lugar de barras intercaladas por modo. No calcula nada: lee
side_or_requests.csv del bloque 73. Barra = IC 95 % bootstrap sobre prompts; asterisco = q < 0,05 del test de permutación
de lados dentro de (modelo, prompt, díada), BH dentro de los 4 modos del conjunto. Es un OR marginal de un pedido típico.
Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_countries/panelC/panelC_split.py
"""
from __future__ import annotations
import os, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
if str(HERE.parent / "panelB") not in sys.path:
    sys.path.insert(0, str(HERE.parent / "panelB"))
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np, pandas as pd
from panelB_fe_cluster import MODES, LABELS, ORIGIN, fmt_q
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83"}

SRC = ROOT / "4_analysis/results/73_fig3_usage_weighted_requests/side_or_requests.csv"
NL = chr(10)
SETS = (("geo", "#3B3B58", "lado USA / lado China (las dos díadas juntas)"), ("neutral", "#C9C9C9", "neutral A / neutral B (referencia)"))


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "savefig.facecolor": "white"})
    so = pd.read_csv(SRC).set_index(["set", "group"])
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), layout="constrained", sharey=True)
    x = np.arange(len(MODES))
    for ax, (st, col, lab) in zip(axes, SETS):
        r = so.loc[st].loc[list(MODES)]
        OR, lo, hi = r.odds_ratio.values, r.boot_lo.values, r.boot_hi.values
        ax.bar(x, OR - 1, bottom=1, width=.6, color=[MODE_COLORS[m] for m in MODES], zorder=2)
        ax.errorbar(x, OR, yerr=[OR - lo, hi - OR], fmt="none", ecolor="#111", elinewidth=1.2, capsize=4, zorder=3)
        for xi, h, q in zip(x, hi, r.perm_q.values):
            ax.text(xi, h * 1.02, fmt_q(q), ha="center", va="bottom", fontsize=8.5)
        ax.set_yscale("log"); ax.set_yticks([.7, .8, .9, 1, 1.1, 1.25, 1.5]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.set_minor_formatter(mticker.NullFormatter()); ax.set_ylim(.66, 1.55)
        ax.axhline(1, color="black", lw=1); ax.grid(axis="y", alpha=.15)
        ax.set_xticks(x, [LABELS[m] for m in MODES], fontsize=9, rotation=15, ha="right", rotation_mode="anchor")
        ax.set_title(lab, fontsize=10)
    axes[0].set_ylabel("OR de refusal, usuario del lado USA vs del lado China" + NL + "(tasas pesadas por pedidos; IC 95 % bootstrap; q = permutación + BH)")
    axes[0].text(.5, .985, "▲ rechaza más si el usuario es del lado USA", transform=axes[0].transAxes, ha="center", va="top", fontsize=8, color=ORIGIN["CN"], fontweight="bold")
    axes[0].text(.5, .015, "▼ rechaza más si el usuario es del lado China", transform=axes[0].transAxes, ha="center", va="bottom", fontsize=8, color=ORIGIN["US"], fontweight="bold")
    fig.suptitle("Un pedido típico: OR marginal de refusal según el lado del usuario, tasas pesadas por los pedidos de cada modelo", fontsize=11)
    fig.savefig(HERE / "panelC_split.png", dpi=150)
    print(so.loc[["geo", "neutral"]][["odds_ratio", "boot_lo", "boot_hi", "perm_q"]].round(3).to_string())


if __name__ == "__main__":
    main()
