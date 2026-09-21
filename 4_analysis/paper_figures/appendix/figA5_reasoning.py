#!/usr/bin/env python3
"""Appendix figure: refusal by mode with reasoning off and at the first two effort levels, for the 4 US models, the 4 CN models
and all 8 (one panel per mode).

Redraws numbers already stored (nothing is computed):
  4_analysis/results/68_reasoning_glmm/panel_a_curves.csv  (rate = mean with equal weight per model; lo, hi = 95% t CI across
  models; levels off / r1 / r2 = reasoning off / effort level 1 / effort level 2). Lower CI bounds below 0 are clipped at 0.
No stars (the figure shows descriptive curves; the test is the block-68 GLMM, reported in the caption).

Run from the repo root:  python 4_analysis/paper_figures/appendix/figA5_reasoning.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _paperstyle import style, MODE_COLORS, ORIGIN, ORIGIN_LIGHT, RESULTS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

MODES = ["he", "de", "pg", "ctl"]
LABEL = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "ctl": "Control"}
COLOR = {"he": MODE_COLORS["he"], "de": MODE_COLORS["de"], "pg": MODE_COLORS["pg"], "ctl": MODE_COLORS["control"]}
LEVELS = ["off", "r1", "r2"]
TICKS = ["Off", "Level 1", "Level 2"]   # x label: "Reasoning effort" (off = reasoning off; level k = effort level k)
GROUPS = {"US": dict(color=ORIGIN["US"], band=ORIGIN_LIGHT["US"], ls="-", marker="o", label="US models (4)"),
          "CN": dict(color=ORIGIN["CN"], band=ORIGIN_LIGHT["CN"], ls="-", marker="o", label="CN models (4)"),
          "all": dict(color="#222222", band="#BBBBBB", ls="--", marker="s", label="All 8 models")}
FB, FT, FL = 6.5, 6.0, 9.0
STEM = "figA5_reasoning"


def restyle():
    style()
    plt.rcParams.update({"legend.fontsize": FT, "axes.titlesize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT,
                         "axes.labelsize": FB, "font.size": FB})


def panel(ax, d, mode):
    xs = np.arange(3)
    for g in ("US", "CN", "all"):
        s = d[(d["mode"] == mode) & (d.group == g)].set_index("level").loc[LEVELS]; st = GROUPS[g]
        ax.fill_between(xs, s.lo.clip(lower=0), s.hi, color=st["band"], alpha=.35 if g != "all" else .3, lw=0, zorder=1)
        ax.plot(xs, s.rate, ls=st["ls"], marker=st["marker"], ms=2.2, lw=.9, color=st["color"], zorder=3)
    ax.set_xticks(xs, TICKS); ax.set_xlim(-.2, 2.2); ax.grid(axis="y", alpha=.15)
    ax.set_title(LABEL[mode], loc="center", color=COLOR[mode])


def main():
    restyle()
    d = pd.read_csv(RESULTS / "68_reasoning_glmm" / "panel_a_curves.csv")
    fig = plt.figure(figsize=(5.5, 1.8), layout="constrained")
    fig.get_layout_engine().set(w_pad=.02, h_pad=.04, wspace=.03)
    gs = fig.add_gridspec(1, 4)
    axes = [fig.add_subplot(gs[0, 0])]
    axes += [fig.add_subplot(gs[0, i], sharey=axes[0]) for i in range(1, 4)]
    for ax, mode in zip(axes, MODES):
        panel(ax, d, mode)
    axes[0].set_ylim(0, 60); axes[0].set_ylabel("Refusal (%)")
    fig.supxlabel("Reasoning effort", fontsize=FB)
    for ax in axes[1:]:
        ax.tick_params(labelleft=False)
    axes[0].legend(handles=[Line2D([], [], color=GROUPS[g]["color"], ls=GROUPS[g]["ls"], marker=GROUPS[g]["marker"], ms=2.4, lw=.9,
                                   label=GROUPS[g]["label"]) for g in ("US", "CN", "all")],
                   frameon=False, loc="upper right", handlelength=1.8, labelspacing=.25, borderaxespad=.1)
    fig.canvas.draw()
    for ax, s in zip(axes, "ABCD"):
        x0, y0, w, h = ax.get_position().bounds
        fig.text(max(x0 - .06, .002) if s == "A" else x0 - .02, y0 + h + .025, s, fontsize=FL, fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        out = HERE / f"{STEM}.{ext}"; fig.savefig(out, dpi=300); print("written:", out)
    plt.close(fig)


if __name__ == "__main__":
    main()
