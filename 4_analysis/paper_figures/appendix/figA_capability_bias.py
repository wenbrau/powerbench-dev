#!/usr/bin/env python3
"""Appendix figure: each model's bias against its capability index, in the three identity manipulations (Nico, 25/09).

Rows: AI-agent requester (log OR, agent vs human; GLMM line of Figure 3F, block 64; q from block 83), nationality
(|direction| - chance on the geopolitical set, Figure 2B's quantity; OLS line, block 97), language (range across the eight
languages minus its chance value, pp, Figure 4E's quantity; OLS line, block 97). Columns: pooled power shifting, control.
Per-model values: block 96 (B_per_model_values.csv) and block 84 (AI agent). No number is computed here.

Run from the repo root:  python 4_analysis/paper_figures/appendix/figA_capability_bias.py
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paperstyle import ROOT, RESULTS, ORIGIN  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FB, FT = 6.5, 6.0
PM = pd.read_csv(RESULTS / "96_exploratory_order_capability" / "B_per_model_values.csv")
AI = pd.read_csv(RESULTS / "84_fig3f_ivw_nagq1" / "capability_per_model_log_or_ivw.csv")
FITS = pd.read_csv(RESULTS / "97_fig1c_fig2a_intervals_capability" / "capability_bias_fits.csv").set_index(["experiment", "set"])
GL = pd.read_csv(RESULTS / "64_fig4_capability_glmm_nagq1" / "capability_glmm.csv")
CAP = pd.read_csv(RESULTS / "30_fig1_glmm_nagq1" / "capability_index.csv")
MU, SD = CAP["index"].mean(), CAP["index"].std(ddof=1)
ROWS = [("ai_agent", "AI agent", "log OR, agent vs human"),
        ("nationality", "Nationality", "|bias| $-$ chance"),
        ("language", "Language", "range $-$ chance (pp)")]
COLS = [("power_shifting", "power shifting"), ("control", "control")]
COLVAL = {("nationality", "power_shifting"): "B1_geo_excess_ps", ("nationality", "control"): "B1_geo_excess_ct",
          ("language", "power_shifting"): "B2_range_excess_pp_ps", ("language", "control"): "B2_range_excess_pp_ct"}


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": FB, "axes.titlesize": FB + .5, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 3, "axes.labelsize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT, "legend.fontsize": FT,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6, "xtick.major.width": .5, "ytick.major.width": .5,
        "xtick.major.size": 2.2, "ytick.major.size": 2.2, "lines.linewidth": .8, "savefig.facecolor": "white", "pdf.fonttype": 42,
    })


def points(exp_, st):
    if exp_ == "ai_agent":
        s = AI[AI.set == ("power_shifting_pooled" if st == "power_shifting" else "control")]
        return s.capability.to_numpy(), s.log_or.to_numpy(), s.origin.to_numpy()
    d = PM[["capability_index", COLVAL[(exp_, st)], "origin"]].dropna()
    return d.capability_index.to_numpy(), d[COLVAL[(exp_, st)]].to_numpy(), d.origin.to_numpy()


def line(exp_, st, xs):
    zs = (xs - MU) / SD
    if exp_ == "ai_agent":   # the GLMM line of Figure 3F, marginalised over the prompt intercept
        g = GL[(GL.run == "pooled") & (GL.set == st)].set_index("quantity")
        ai, it = g.loc["ai (capacidad media)"], g.loc["ai x capacidad (por 1 SD)"]
        att = float(np.sqrt(1 + (16 * np.sqrt(3) / (15 * np.pi)) ** 2 * ai.sd_prompt ** 2))
        return (ai.estimate + it.estimate * zs) / att
    f = FITS.loc[(exp_, st)]
    return f.intercept + f.slope_per_sd * zs


def main():
    style()
    fig, axes = plt.subplots(3, 2, figsize=(5.5, 5.2), sharex=True, layout="constrained")
    for r, (exp_, rtitle, ylab) in enumerate(ROWS):
        for c, (st, ctitle) in enumerate(COLS):
            ax = axes[r, c]
            x, y, o = points(exp_, st)
            for org in ("US", "CN"):
                m = o == org
                ax.plot(x[m], y[m], "o", ms=2.6, color=ORIGIN[org], alpha=.85, zorder=3)
            xs = np.linspace(np.nanmin(x) - 1, np.nanmax(x) + 1, 50); ys = line(exp_, st, xs)
            ax.plot(xs, ys, color="#222222", lw=1.0, zorder=4)
            if FITS.loc[(exp_, st), "q_bh"] < .05:
                ax.text(xs[-1] + .6, ys[-1], "*", ha="left", va="center", fontsize=FB + 2, zorder=5)
            ax.axhline(0, color="black", lw=.5, ls=":", zorder=1); ax.grid(alpha=.15)
            ax.set_title(f"{rtitle}: {ctitle}", fontsize=FB)
            if c == 0:
                ax.set_ylabel(ylab)
            if r == 2:
                ax.set_xlabel("capability index (%)")
        lo = min(axes[r, 0].get_ylim()[0], axes[r, 1].get_ylim()[0]); hi = max(axes[r, 0].get_ylim()[1], axes[r, 1].get_ylim()[1])
        axes[r, 0].set_ylim(lo, hi); axes[r, 1].set_ylim(lo, hi)
    axes[0, 1].legend(handles=[Line2D([], [], marker="o", ls="", ms=3, color=ORIGIN["US"], label="US model"),
                               Line2D([], [], marker="o", ls="", ms=3, color=ORIGIN["CN"], label="CN model")], frameon=False, loc="upper left")
    for ext in ("pdf", "png"):
        out = HERE / f"figA_capability_bias.{ext}"; fig.savefig(out, dpi=300); print("written:", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
