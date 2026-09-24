#!/usr/bin/env python3
"""Appendix figures for the language section (Figure 4 of the body), redrawn for the paper (21/09).

Redraws ONLY numbers already stored in result tables; nothing is estimated, resampled or tested here. The one derived
quantity is the BH adjustment over the three pair types of the agreement panel (figA4_by_mode, B), which is the exact call
the source plotting script makes when it draws its stars (review_fig_languages/panelC/panelC_with_tests.py::draw_final).

  figA4_mean_effects       A  block 82  language_deviation_ps.csv            (24 models, Swahili without 2)   stars: p_bh
                           B  block 72  usage_weighted_or_requests.csv       (24 models, Swahili without 2)   stars: boot_q
  figA4_pairs_prevalence   A  block 79  pairwise_bias_summary.csv            (24 models, Swahili without 2)   no test
                           B  block 80  pairs.csv + summary.csv (OLS line)   (24 models, Swahili without 2)   no test
  figA4_by_mode            A  review_fig_languages/panelD/F6_exceso_{mode}.csv (24 models)                   stars: q_bh
                           B  review_fig_languages/panelC/panelC_test_stats.csv (24 models)                  stars: BH over 3 pair types
  figA4_concordance        A,B review_fig_languages_22models/concordance/per_model.csv (22 models)            no q in source: no stars

Run from the repo root:  python 4_analysis/paper_figures/appendix/figA4_language_appendix.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "4_analysis" / "paper_figures"))
from _paperstyle import style, MODE_COLORS, ORIGIN, ORIGIN_LIGHT, or_axis, short  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from statsmodels.stats.multitest import multipletests  # noqa: E402

RES = ROOT / "4_analysis" / "results"
RFL = ROOT / "4_analysis" / "review_fig_languages"
R22 = ROOT / "4_analysis" / "review_fig_languages_22models"

FB, FT, FMIN, FL = 6.5, 6.0, 5.5, 9.0          # base, ticks, smallest, panel letters
W = 5.5
PS = "power_shifting"
MODES4 = ["he", "de", "pg", "control"]
SHORT = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT", PS: "PS"}
LANG_NAME = {"en": "English", "de": "German", "fr": "French", "es": "Spanish", "pt": "Portuguese", "zh": "Chinese",
             "hi": "Hindi", "sw": "Swahili"}
EXCL22 = {"nemotron-3.5-lightning", "nova-2-lite"}
KINDS = ["CN–CN", "US–US", "mixto"]                       # labels as stored in the source tables
KIND_LABEL = {"CN–CN": "CN–CN", "US–US": "US–US", "mixto": "Mixed"}
KIND_COLOR = {"CN–CN": ORIGIN["CN"], "US–US": ORIGIN["US"], "mixto": "#8A7FA3"}   # as in figure_paper.py panel C
CHANCE = "#9AA0A6"


def model_order(models=None):
    """US first, then CN; each by descending mean refusal over the four modes (block 78, rates_per_model.csv)."""
    r = pd.read_csv(RES / "78_fig1_v3_nagq1" / "rates_per_model.csv")
    r["mean4"] = r[MODES4].mean(axis=1)
    if models is not None:
        r = r[r.model.isin(models)]
    r = r.assign(o=r.origin.map({"US": 0, "CN": 1})).sort_values(["o", "mean4"], ascending=[True, False])
    return r.model.tolist(), dict(zip(r.model, r.origin))


def letter(fig, ax, s, x=None, dy=.012):
    x0, y0, w, h = ax.get_position().bounds
    fig.text(x0 - .06 if x is None else x, y0 + h + dy, s, fontsize=FL, fontweight="bold", ha="left", va="bottom")


def star(ax, x, y, va="bottom", **kw):
    ax.text(x, y, "*", ha="center", va=va, fontsize=FB + 1.5, fontweight="bold", color="#1A1A1A", **kw)


def save(fig, stem):
    for ext in ("pdf", "png"):
        out = HERE / f"{stem}.{ext}"
        fig.savefig(out, dpi=300)
        print("wrote", out.relative_to(ROOT))
    plt.close(fig)


def base_style():
    style()
    plt.rcParams.update({"font.size": FB, "axes.labelsize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT,
                         "legend.fontsize": FT, "axes.titlesize": FB + .5, "axes.titlepad": 3})


# ============================================================================ 1. mean effects
def fig_mean_effects():
    dev = pd.read_csv(RES / "82_fig2_language_glmm_ps_nagq1" / "language_deviation_ps.csv")
    orr = pd.read_csv(RES / "72_fig2_usage_weighted_requests" / "usage_weighted_or_requests.csv")
    langs = dev.lang.tolist()                                   # source order (de pt en es sw zh fr hi)
    fig = plt.figure(figsize=(W, 2.0))
    axA = fig.add_axes([.085, .275, .265, .575])
    axB = fig.add_axes([.445, .275, .545, .575])

    # A: deviation from the mean of the eight languages, pooled power shifting, Wald CI; stars = p_bh < .05
    x = np.arange(len(langs))
    axA.bar(x, dev.estimate, width=.62, color=MODE_COLORS[PS], zorder=2)
    axA.errorbar(x, dev.estimate, yerr=[dev.estimate - dev.lo, dev.hi - dev.estimate], fmt="none", ecolor="#222",
                 elinewidth=.6, capsize=1.4, capthick=.6, zorder=3)
    axA.axhline(0, color="black", lw=.6, zorder=1)
    for xi, r in zip(x, dev.itertuples()):
        if r.p_bh < .05:
            star(axA, xi, r.hi + .02)
    axA.set_xticks(x, [LANG_NAME[l] for l in langs], rotation=50, ha="right", rotation_mode="anchor")
    axA.set_xlim(-.6, len(langs) - .4)
    axA.set_ylim(-.5, .65); axA.set_yticks([-.4, -.2, 0, .2, .4, .6])
    axA.set_ylabel("Deviation (log-odds)")
    axA.grid(axis="y", alpha=.15)
    axA.set_title("Pooled power shifting")

    # B: odds ratio vs English, usage-weighted typical request, bootstrap CI, log axis; stars = boot_q < .05
    groups = MODES4 + [PS]
    langsB = [l for l in langs if l != "en"]
    xb = np.arange(len(langsB)); bw = .16
    for k, g in enumerate(groups):
        t = orr[orr.group == g].set_index("lang").loc[langsB]
        xs = xb + (k - 2) * bw
        axB.bar(xs, t.odds_ratio - 1, bottom=1, width=bw * .92, color=MODE_COLORS[g], label=SHORT[g], zorder=2)
        axB.errorbar(xs, t.odds_ratio, yerr=[t.odds_ratio - t.boot_lo, t.boot_hi - t.odds_ratio], fmt="none",
                     ecolor="#222", elinewidth=.5, capsize=1.0, capthick=.5, zorder=3)
        for xi, r in zip(xs, t.itertuples()):
            if r.boot_q < .05:
                star(axB, xi, r.boot_hi * 1.01)
    or_axis(axB, [.5, .67, 1, 1.5, 2], .52, 2.75)
    axB.set_yticks([.5, .67, 1, 1.5, 2], ["0.5", "0.67", "1", "1.5", "2"])
    axB.yaxis.set_minor_locator(mticker.NullLocator())
    axB.set_xticks(xb, [LANG_NAME[l] for l in langsB], rotation=30, ha="right", rotation_mode="anchor")
    axB.set_xlim(-.55, len(langsB) - .45)
    axB.set_ylabel("Odds ratio vs English")
    axB.legend(frameon=False, ncol=5, loc="lower left", bbox_to_anchor=(-.01, .985), handlelength=.9, handletextpad=.4,
               columnspacing=.9, borderaxespad=0, fontsize=FT)
    letter(fig, axA, "A", x=.005); letter(fig, axB, "B", x=.365)
    save(fig, "figA4_mean_effects")


# ============================================================================ 2. pairwise bias and web prevalence
def fig_pairs_prevalence(cell_values=True):
    summ = pd.read_csv(RES / "79_fig2_language_pairwise_bias" / "pairwise_bias_summary.csv")
    summ = summ[summ.group == PS].set_index(["lang_a", "lang_b"]).bias
    pairs = pd.read_csv(RES / "80_fig2_pairwise_bias_vs_prevalence" / "pairs.csv")
    ols = pd.read_csv(RES / "80_fig2_pairwise_bias_vs_prevalence" / "summary.csv").set_index("kind").loc["ols_28_pairs"]
    order = ["de", "pt", "en", "es", "sw", "zh", "fr", "hi"]        # block 79 order (LANGS in analysis_79)
    rows, cols = order[1:], order[:-1]
    M = np.full((len(rows), len(cols)), np.nan)
    for i, a in enumerate(rows):
        for j, b in enumerate(cols):
            if order.index(b) < order.index(a):
                M[i, j] = summ.loc[(a, b)]
    assert np.isfinite(M).sum() == 28

    fig = plt.figure(figsize=(W, 2.3))
    axA = fig.add_axes([.125, .195, .315, .71])
    axB = fig.add_axes([.60, .195, .385, .71])

    vlim = .25
    im = axA.imshow(np.ma.masked_invalid(M), cmap="RdBu_r", vmin=-vlim, vmax=vlim, aspect="auto")
    if cell_values:
        for i in range(len(rows)):
            for j in range(len(cols)):
                v = M[i, j]
                if np.isfinite(v):
                    s = f"{v:+.2f}".replace("0.", ".").replace("-", "−")
                    axA.text(j, i, s, ha="center", va="center", fontsize=FMIN,
                             color="white" if abs(v) > .15 else "#1A1A1A")
    axA.set_xticks(range(len(cols)), [LANG_NAME[l] for l in cols], rotation=35, ha="right", rotation_mode="anchor")
    axA.set_yticks(range(len(rows)), [LANG_NAME[l] for l in rows])
    axA.tick_params(length=0, pad=1.5)
    for sp in axA.spines.values():
        sp.set_visible(False)
    cax = axA.inset_axes([.60, .80, .36, .045])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=[-.2, 0, .2])
    cb.ax.tick_params(labelsize=FMIN, width=.4, length=1.5, pad=1); cb.outline.set_linewidth(.4)
    cb.ax.set_xticklabels(["−.2", "0", "+.2"])
    cb.set_label("Row refused more →", fontsize=FMIN, labelpad=1.5)
    cb.ax.xaxis.set_label_position("top")
    axA.set_title("Direction bias, row vs column", x=-.25)

    # B: one point per pair, descriptive OLS line over the 28 pairs (block 80 summary.csv)
    axB.axhline(0, color="black", lw=.6, zorder=1)
    axB.axvline(0, color="#BBBBBB", lw=.5, zorder=1)
    xx = np.array([pairs.dlog_share.min() - .2, pairs.dlog_share.max() + .2])
    axB.plot(xx, ols.intercept + ols.slope * xx, color="#222", lw=.9, zorder=2)
    axB.scatter(pairs.dlog_share, pairs.bias, s=11, color=MODE_COLORS[PS], edgecolor="white", linewidth=.4, zorder=3)
    axB.set_xlabel("log10 web-text share, row − column")
    axB.set_ylabel("Direction bias")
    axB.set_xlim(-4, 3.1); axB.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3])
    axB.set_ylim(-.07, .24); axB.set_yticks([-.05, 0, .05, .1, .15, .2])
    axB.grid(alpha=.15)
    axB.set_title("Bias vs web prevalence")
    letter(fig, axA, "A", x=.005); letter(fig, axB, "B", x=.50)
    save(fig, "figA4_pairs_prevalence")


# ============================================================================ 3. by mode (24 models)
def fig_by_mode():
    exc = {m: pd.read_csv(RFL / "panelD" / f"F6_exceso_{m}.csv").set_index("model") for m in MODES4}
    models, origin = model_order(exc["pg"].index.tolist())
    assert len(models) == 24
    E = np.array([[exc[m].loc[mod, "excess"] for m in MODES4] for mod in models])
    Q = np.array([[exc[m].loc[mod, "q_bh"] for m in MODES4] for mod in models])
    st = pd.read_csv(RFL / "panelC" / "panelC_test_stats.csv")
    st = st[st.test == "test1_langperm"]

    fig = plt.figure(figsize=(W, 3.15))
    axA = fig.add_axes([.195, .135, .20, .79])
    axB = fig.add_axes([.585, .135, .405, .79])

    # A: models x modes heatmap of excess range over chance (pp); star = per-model permutation q_bh < .05
    cmap = mcolors.LinearSegmentedColormap.from_list("exc", ["#FFFFFF", "#C9C3D6", "#6E6390", "#2E2445"])
    vmax = 40
    norm = mcolors.PowerNorm(gamma=.6, vmin=0, vmax=vmax)
    im = axA.imshow(np.clip(E, 0, None), cmap=cmap, norm=norm, aspect="auto")
    n = len(models)
    for i in range(n):
        for j in range(len(MODES4)):
            if Q[i, j] < .05:
                axA.text(j, i + .08, "*", ha="center", va="center", fontsize=FB + 1, fontweight="bold",
                         color="white" if norm(max(E[i, j], 0)) > .55 else "#1A1A1A")
    axA.set_yticks(range(n), [short(m) for m in models])
    for lab, m in zip(axA.get_yticklabels(), models):
        lab.set_color(ORIGIN[origin[m]])
    axA.set_xticks(range(len(MODES4)), [SHORT[m] for m in MODES4], rotation=35, ha="right", rotation_mode="anchor")
    axA.tick_params(length=0, pad=1.5)
    nus = sum(origin[m] == "US" for m in models)
    axA.axhline(nus - .5, color="black", lw=.6)
    for sp in axA.spines.values():
        sp.set_visible(False)
    cax = axA.inset_axes([1.06, .0, .07, .30])
    cb = fig.colorbar(im, cax=cax, orientation="vertical", ticks=[0, 10, 20, 30, 40])
    cb.ax.tick_params(labelsize=FMIN, width=.4, length=1.5, pad=1); cb.outline.set_linewidth(.4)
    cb.set_label("Excess over chance (pp)", fontsize=FMIN, labelpad=2)
    axA.set_title("Range beyond chance", x=-.3)

    # B: mean Spearman agreement by pair type and mode; grey band = 95% chance interval (languages permuted within
    # each model); star = BH q < .05 over the three pair types of the mode, as in panelC_with_tests.py::draw_final
    x = np.arange(len(MODES4)); bw = .25
    for k, kind in enumerate(KINDS):
        for xi, m in zip(x, MODES4):
            r = st[(st["mode"] == m) & (st.quantity == kind)].iloc[0]
            xk = xi + (k - 1) * bw
            axB.add_patch(plt.Rectangle((xk - bw * .43, r.null_lo), bw * .86, r.null_hi - r.null_lo, facecolor=CHANCE,
                                        alpha=.35, edgecolor="none", zorder=1))
            axB.bar(xk, r.observed, width=bw * .58, color=KIND_COLOR[kind], zorder=2,
                    label=KIND_LABEL[kind] if m == MODES4[0] else None)
    for xi, m in zip(x, MODES4):
        s = st[st["mode"] == m].set_index("quantity").loc[KINDS]
        q = multipletests(s.p.values, method="fdr_bh")[1]
        for k, (kind, qq) in enumerate(zip(KINDS, q)):
            if qq < .05:
                y = s.loc[kind, "observed"]; xk = xi + (k - 1) * bw
                if y >= 0:
                    star(axB, xk, max(y, s.loc[kind, "null_hi"]) + .005)
                else:
                    star(axB, xk, min(y, s.loc[kind, "null_lo"]) - .005, va="top")
    axB.axhline(0, color="black", lw=.6, zorder=1.5)
    axB.set_xticks(x, [SHORT[m] for m in MODES4])
    axB.set_xlim(-.55, len(MODES4) - .45)
    axB.set_ylim(-.23, .3); axB.set_yticks([-.2, -.1, 0, .1, .2, .3])
    axB.set_ylabel("Mean Spearman correlation between\ntwo models' language orders")
    axB.grid(axis="y", alpha=.15)
    h, l = axB.get_legend_handles_labels()
    h.append(Patch(facecolor=CHANCE, alpha=.35, edgecolor="none")); l.append("Chance (95%)")
    axB.legend(h, l, frameon=False, ncol=2, loc="lower left", handlelength=.9, handletextpad=.4, columnspacing=.9,
               borderaxespad=.2, fontsize=FT)
    axB.set_title("Agreement by pair type")
    letter(fig, axA, "A", x=.005); letter(fig, axB, "B", x=.475)
    save(fig, "figA4_by_mode")


# ============================================================================ 4. concordance across modes (22 models)
def fig_concordance():
    pm = pd.read_csv(R22 / "concordance" / "per_model.csv").set_index("model")
    assert len(pm) == 22 and not (set(pm.index) & EXCL22)
    models, origin = model_order(pm.index.tolist())
    pm = pm.loc[models]
    fig = plt.figure(figsize=(W, 2.3))
    axA = fig.add_axes([.075, .372, .41, .553])
    axB = fig.add_axes([.585, .372, .41, .553])
    x = np.arange(len(models))
    cols = [ORIGIN[origin[m]] for m in models]

    def draw(ax, obs, lo, hi, mu, sep_ymin=0):
        ax.vlines(x, lo, hi, color=CHANCE, alpha=.55, lw=3.2, zorder=1)
        ax.scatter(x, mu, marker="_", s=14, color="#555", linewidths=.8, zorder=2)
        ax.scatter(x, obs, s=12, color=cols, edgecolor="white", linewidth=.35, zorder=3)
        ax.set_xticks(x, [short(m) for m in models], rotation=90, fontsize=FMIN)
        for lab, m in zip(ax.get_xticklabels(), models):
            lab.set_color(ORIGIN[origin[m]])
        ax.set_xlim(-.7, len(models) - .3)
        ax.tick_params(axis="x", length=0, pad=1.5)
        ax.grid(axis="y", alpha=.15)
        nus = sum(origin[m] == "US" for m in models)
        ax.axvline(nus - .5, ymin=sep_ymin, color="#BBBBBB", lw=.5, zorder=0)

    draw(axA, pm.W_ps, pm.W_ps_null_lo, pm.W_ps_null_hi, pm.W_ps_null)
    axA.set_ylim(0, 1); axA.set_yticks([0, .25, .5, .75, 1])
    axA.set_ylabel("Kendall's W")
    axA.set_title("Agreement across power-shifting types")
    draw(axB, pm.rho_control_vs_ps, pm.rho_null_lo, pm.rho_null_hi, pm.rho_null, sep_ymin=.13)
    axB.axhline(0, color="black", lw=.6, zorder=0)
    axB.set_ylim(-1.14, 1.04); axB.set_yticks([-1, -.5, 0, .5, 1])
    axB.set_ylabel("Spearman correlation")
    axB.set_title("CT vs power-shifting types")
    leg = [Line2D([], [], ls="none", marker="o", ms=3.4, color="#444", label="Observed"),
           Line2D([], [], color=CHANCE, alpha=.55, lw=3.2, label="Chance (95%)"),
           Line2D([], [], ls="none", marker="_", ms=4, mew=.8, color="#555", label="Chance mean")]
    axB.legend(handles=leg, frameon=False, ncol=3, loc="lower left", handlelength=1.2, handletextpad=.6,
               columnspacing=1.2, borderaxespad=.1, fontsize=FMIN)
    letter(fig, axA, "A", x=.005); letter(fig, axB, "B", x=.505)
    save(fig, "figA4_concordance")


if __name__ == "__main__":
    base_style()
    which = sys.argv[1:] or ["mean_effects", "pairs_prevalence", "by_mode", "concordance"]
    for w in which:
        {"mean_effects": fig_mean_effects, "pairs_prevalence": fig_pairs_prevalence, "by_mode": fig_by_mode,
         "concordance": fig_concordance}[w]()
