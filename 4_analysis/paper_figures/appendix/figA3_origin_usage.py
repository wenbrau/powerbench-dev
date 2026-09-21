#!/usr/bin/env python3
"""Appendix figure: AI-agent bias by model origin (A) and for a usage-weighted typical request (B).

Redraws numbers already stored by blocks 57 and 74 (nothing is computed):
  A  4_analysis/results/57_fig4_by_origin/bias_direction_by_origin.csv   (mean of 12 models, 95% t CI; no q column -> no stars)
  B  4_analysis/results/74_fig4_usage_weighted_requests/usage_weighted_or_requests.csv
     (odds_ratio, boot_lo, boot_hi; star where boot_q < 0.05)

Run from the repo root:  python 4_analysis/paper_figures/appendix/figA3_origin_usage.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _paperstyle import style, MODE_COLORS, ORIGIN, or_axis, RESULTS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

MODES = ["he", "de", "pg", "control"]
SHORT = {"he": "Self-emp.", "de": "Disemp.", "pg": "Power grab.", "control": "Control", "power_shifting": "Power shift."}
FB, FT, FL = 6.5, 6.0, 9.0
STEM = "figA3_origin_usage"


def restyle():
    style()
    plt.rcParams.update({"legend.fontsize": FT, "axes.titlesize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT,
                         "axes.labelsize": FB, "font.size": FB})


def panel_a(ax, d):
    x = np.arange(len(MODES)); w = .38
    for k, org in enumerate(("US", "CN")):
        s = d[d.origin == org].set_index("mode").loc[MODES]; xo = x + (k - .5) * w
        ax.bar(xo, s["mean"], width=w * .95, color=ORIGIN[org], zorder=2)
        ax.errorbar(xo, s["mean"], yerr=[s["mean"] - s.lo, s.hi - s["mean"]], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.3, capthick=.6, zorder=3)
    ax.axhline(0, color="black", lw=.6, ls="--", zorder=1)
    ax.set_xticks(x, [SHORT[m] for m in MODES]); ax.set_xlim(-.6, len(MODES) - .4)
    ax.set_ylim(-.15, 1.0); ax.set_yticks([0, .25, .5, .75]); ax.grid(axis="y", alpha=.15)
    ax.set_ylabel("Bias toward refusing the AI")
    ax.legend(handles=[Patch(facecolor=ORIGIN["US"], label="US models"), Patch(facecolor=ORIGIN["CN"], label="CN models")],
              frameon=False, loc="upper right", ncol=2, handlelength=1.0, columnspacing=.8, borderaxespad=.1)
    ax.set_title("By model origin")


def panel_b(ax, d):
    groups = MODES + ["power_shifting"]
    s = d.set_index("group").loc[groups]
    x = np.array([0, 1, 2, 3, 4.35])
    cols = [MODE_COLORS[g] for g in groups]
    ax.bar(x, s.odds_ratio - 1, bottom=1, width=.62, color=cols, zorder=2)
    ax.errorbar(x, s.odds_ratio, yerr=[s.odds_ratio - s.boot_lo, s.boot_hi - s.odds_ratio], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.3, capthick=.6, zorder=3)
    for xi, (_, r) in zip(x, s.iterrows()):
        if r.boot_q < .05:
            ax.text(xi, r.boot_hi * 1.01, "*", ha="center", va="bottom", fontsize=FB + 1)
    or_axis(ax, [1, 1.25, 1.5, 2], .93, 2.45)
    ax.axhline(1, color="black", lw=.6, ls="--", zorder=1)
    ax.axvline(3.68, color="#999", lw=.5, ls=":")
    ax.set_xticks(x, [SHORT[g] for g in groups]); ax.set_xlim(-.6, 4.95)
    ax.set_ylabel("Odds ratio, AI vs human")
    ax.set_title("Usage-weighted typical request")


def main():
    restyle()
    A = pd.read_csv(RESULTS / "57_fig4_by_origin" / "bias_direction_by_origin.csv")
    B = pd.read_csv(RESULTS / "74_fig4_usage_weighted_requests" / "usage_weighted_or_requests.csv")
    fig = plt.figure(figsize=(5.5, 1.8), layout="constrained")
    fig.get_layout_engine().set(w_pad=.02, h_pad=.04, wspace=.06)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0])
    axA, axB = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    panel_a(axA, A); panel_b(axB, B)
    for ax in (axA, axB):
        ax.tick_params(axis="x", labelrotation=30)
        for t in ax.get_xticklabels():
            t.set_ha("right"); t.set_rotation_mode("anchor")
    fig.canvas.draw()
    for ax, s in ((axA, "A"), (axB, "B")):
        x0, y0, w, h = ax.get_position().bounds
        fig.text(max(x0 - .075, .002), y0 + h + .02, s, fontsize=FL, fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        out = HERE / f"{STEM}.{ext}"; fig.savefig(out, dpi=300); print("written:", out)
    plt.close(fig)


if __name__ == "__main__":
    main()
