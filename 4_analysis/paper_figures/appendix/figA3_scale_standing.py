#!/usr/bin/env python3
"""Appendix figure: direction bias toward refusing the AI-agent requester by scale of the affected party (A) and by the
requester's prior standing (B), per mode.

Redraws numbers already stored (nothing is computed):
  points/bars  4_analysis/results/59_fig4_by_dimension/bias_direction_by_level.csv  (bias, lo, hi: mean over models, 95% t CI)
  stars        4_analysis/results/60_fig4_ai_level_glmm/bias_direction_paired_t.csv (q_bh < 0.05; paired t per model,
               level 3 vs level 1 = society - individual / high - low, BH over the 4 modes of each dimension; the same test the
               body figure's individual-vs-society panel uses)

Run from the repo root:  python 4_analysis/paper_figures/appendix/figA3_scale_standing.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _paperstyle import style, MODE_COLORS, RESULTS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

MODES = ["he", "de", "pg", "control"]
LABEL = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control"}
LEVELS = {"scale": ["individual", "group", "society"], "standing": ["low", "med", "high"]}
TICK = {"individual": "Individual", "group": "Group", "society": "Society", "low": "Low", "med": "Medium", "high": "High"}
XLAB = {"scale": "Scale of the affected party", "standing": "Requester's prior standing"}
TITLE = {"scale": "By scale", "standing": "By standing"}
FB, FT, FL = 6.5, 6.0, 9.0
STEM = "figA3_scale_standing"
DODGE = {"he": -.15, "de": -.05, "pg": .05, "control": .15}


def restyle():
    style()
    plt.rcParams.update({"legend.fontsize": FT, "axes.titlesize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT,
                         "axes.labelsize": FB, "font.size": FB})


def panel(ax, lv, tt, dim, first):
    s = lv[lv.dim == dim]; xs = np.arange(3)
    q = tt[tt.dim == dim].set_index("mode").q_bh
    for mode in MODES:
        r = s[s["mode"] == mode].set_index("level").loc[LEVELS[dim]]
        x = xs + DODGE[mode]
        ax.errorbar(x, r.bias, yerr=[r.bias - r.lo, r.hi - r.bias], fmt="-o", color=MODE_COLORS[mode], ecolor=MODE_COLORS[mode],
                    ms=2.4, lw=.9, elinewidth=.6, capsize=1.2, capthick=.6, zorder=3)
        if q[mode] < .05:   # level 3 vs level 1 contrast significant: star right of the level-3 cluster
            ax.text(2.27, float(r.bias.iloc[-1]), "*", ha="left", va="center", fontsize=FB + 1.5, color=MODE_COLORS[mode], zorder=5)
    ax.axhline(0, color="black", lw=.6, ls="--", zorder=1)
    ax.set_xticks(xs, [TICK[l] for l in LEVELS[dim]]); ax.set_xlim(-.4, 2.45)
    ax.set_ylim(-.35, 1.1); ax.set_yticks([-.25, 0, .25, .5, .75, 1]); ax.grid(axis="y", alpha=.15)
    ax.set_xlabel(XLAB[dim])
    if first:
        ax.set_ylabel("Bias toward refusing the AI")
    ax.set_title(TITLE[dim])


def main():
    restyle()
    lv = pd.read_csv(RESULTS / "59_fig4_by_dimension" / "bias_direction_by_level.csv")
    tt = pd.read_csv(RESULTS / "60_fig4_ai_level_glmm" / "bias_direction_paired_t.csv")
    fig = plt.figure(figsize=(5.5, 1.9), layout="constrained")
    fig.get_layout_engine().set(w_pad=.02, h_pad=.04, wspace=.06)
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, .42])
    axA = fig.add_subplot(gs[0, 0]); axB = fig.add_subplot(gs[0, 1], sharey=axA); axL = fig.add_subplot(gs[0, 2]); axL.axis("off")
    panel(axA, lv, tt, "scale", True); panel(axB, lv, tt, "standing", False)
    axB.tick_params(labelleft=False)
    axL.legend(handles=[Line2D([], [], color=MODE_COLORS[m], marker="o", ms=2.4, lw=.9, label=LABEL[m]) for m in MODES],
               frameon=False, loc="center left", handlelength=1.4, labelspacing=.5, borderaxespad=0)
    fig.canvas.draw()
    for ax, s in ((axA, "A"), (axB, "B")):
        x0, y0, w, h = ax.get_position().bounds
        fig.text(max(x0 - .07, .002) if ax is axA else x0 - .03, y0 + h + .02, s, fontsize=FL, fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        out = HERE / f"{STEM}.{ext}"; fig.savefig(out, dpi=300); print("written:", out)
    plt.close(fig)


if __name__ == "__main__":
    main()
