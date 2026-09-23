#!/usr/bin/env python3
"""Figura 3 COMPACTA para el cuerpo del paper (21/09). Los mismos seis paneles y los mismos números que figure3_aiagent_paper.py
(lee las mismas tablas, no calcula nada), en 5,5 × 4,2 in: tipografía nunca menor a 6 pt; sin Δ, q, conteos ni recuadros dentro
de la figura (estrellas para q < 0,05; el resto va al pie). Disposición: fila 1 = A | B | C; fila 2 = D y E (heatmaps, apilados) |
F (power shifting y control, apilados).

Ejecutar desde la raíz del repo:  python 4_analysis/paper_figures/figure3_compact.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paperstyle import HERE, ROOT, MODES, PS, MODE_LABEL, MODE_COLORS, ORIGIN  # noqa: E402
import figure3_aiagent_paper as f3  # noqa: E402
from figure3_aiagent_paper import load, CONTEXTS, DOMAINS  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

FB, FT, FL = 6.5, 6.0, 9.0
SHORT = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT"}
CTX_SHORT = {"Interpersonal": "Interpers.", "Government": "Governm."}


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": FB, "axes.titlesize": FB + .5, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 3, "axes.labelsize": FB, "xtick.labelsize": FT, "ytick.labelsize": FT, "legend.fontsize": FT,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6, "xtick.major.width": .5, "ytick.major.width": .5,
        "xtick.major.size": 2.2, "ytick.major.size": 2.2, "xtick.major.pad": 1.5, "ytick.major.pad": 1.5, "axes.labelpad": 1.5,
        "lines.linewidth": .8, "savefig.facecolor": "white", "pdf.fonttype": 42,
    })


def panel_a(ax, lv, dl):
    est = {c: lv[lv.condition == c].set_index("mode").loc[MODES, "estimate"].to_numpy() for c in ("human", "ai")}
    d = dl.set_index("mode").loc[MODES]
    x = np.arange(len(MODES)); w = .36; cols = [MODE_COLORS[m] for m in MODES]
    for cond, off, alpha in (("human", -.19, .45), ("ai", .19, .95)):
        ax.bar(x + off, est[cond], width=w, color=cols, alpha=alpha, edgecolor=cols, lw=.5, zorder=2)
    for xi, h in zip(x, est["human"]):
        ax.plot([xi - .01, xi + .37], [h, h], ls="--", lw=.6, color="#F2F2F2", zorder=3)
    ax.errorbar(x + .19, est["ai"], yerr=[d.estimate - d.lo, d.hi - d.estimate], fmt="none", ecolor="#222222", elinewidth=.6, capsize=1.3, capthick=.6, zorder=4)
    ax.set_xticks(x, [SHORT[m] for m in MODES], rotation=35, ha="right", rotation_mode="anchor"); ax.set_xlim(-.7, len(MODES) - .4)
    ax.set_ylabel("Refusal (%)"); ax.set_ylim(0, 45); ax.grid(axis="y", alpha=.15)
    ax.legend(handles=[Patch(facecolor="#888888", alpha=.45, edgecolor="#888888", label="human user"), Patch(facecolor="#888888", alpha=.95, label="AI-agent user")],
              frameon=False, loc="upper left", handlelength=1.3, borderaxespad=.1)
    ax.set_title("Human vs AI requester")


def panel_b(ax, s, ps):
    s = s.set_index("mode").loc[MODES]; x = np.arange(len(MODES))
    ax.bar(x, s.bias, width=.6, color=[MODE_COLORS[m] for m in MODES], zorder=2)
    ax.errorbar(x, s.bias, yerr=[s.bias - s.lo, s.hi - s.bias], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.3, capthick=.6, zorder=3)
    for xi, (_, r) in zip(x, s.iterrows()):
        if r.q_bh < .05:
            ax.text(xi, r.hi + .02, "*", ha="center", va="bottom", fontsize=FB + 1)
    q = ps.set_index("set").loc["power_shifting"]; xq = len(MODES) + .35
    ax.bar(xq, q.bias, width=.6, color=MODE_COLORS[PS], zorder=2)
    ax.errorbar(xq, q.bias, yerr=[[q.bias - q.lo], [q.hi - q.bias]], fmt="none", ecolor="#222", elinewidth=.6, capsize=1.3, capthick=.6, zorder=3)
    if q.p_t < .05:
        ax.text(xq, q.hi + .02, "*", ha="center", va="bottom", fontsize=FB + 1)
    ax.axvline(len(MODES) - .35, color="#999", lw=.5, ls=":"); ax.axhline(0, color="black", lw=.6, ls="--", zorder=1)
    ax.set_xticks(list(x) + [xq], [SHORT[m] for m in MODES] + ["PS"], rotation=35, ha="right", rotation_mode="anchor"); ax.set_xlim(-.7, xq + .6)
    ax.set_ylim(-.1, .85); ax.set_yticks([0, .25, .5, .75]); ax.set_ylabel("Bias toward refusing the AI"); ax.grid(axis="y", alpha=.15)
    ax.set_title("Direction of disagreements")


def panel_c(ax, cells, tp):
    x = np.arange(len(MODES)); w = .36
    for k, lv in enumerate(("individual", "society")):
        for i, mode in enumerate(MODES):
            r = cells[(cells["mode"] == mode) & (cells.level == lv)].iloc[0]; xi = x[i] + (k - .5) * w
            ax.bar(xi, r.bias, width=w * .92, facecolor="white", edgecolor=MODE_COLORS[mode], hatch="////" if lv == "individual" else "xxxx", lw=.5, zorder=2)
            ax.errorbar(xi, r.bias, yerr=[[r.bias - r.lo], [r.hi - r.bias]], fmt="none", ecolor="#222", elinewidth=.55, capsize=1.2, capthick=.55, zorder=3)
    tt = tp[tp.dim == "scale"].set_index("mode")
    for i, mode in enumerate(MODES):
        if tt.loc[mode].q_bh < .05:
            ax.text(x[i], float(cells[cells["mode"] == mode].hi.max()) + .02, "*", ha="center", va="bottom", fontsize=FB + 1)
    ax.axhline(0, color="black", lw=.6, ls="--", zorder=1)
    ax.set_xticks(x, [SHORT[m] for m in MODES], rotation=35, ha="right", rotation_mode="anchor"); ax.set_ylim(-.5, 1.0); ax.set_yticks([-.25, 0, .25, .5, .75, 1]); ax.grid(axis="y", alpha=.15)
    ax.set_ylabel("Bias toward refusing the AI")
    ax.legend(handles=[Patch(facecolor="white", edgecolor="#666666", hatch="///", lw=.6, label="individual"), Patch(facecolor="white", edgecolor="#666666", hatch="xxx", lw=.6, label="society")],
              handlelength=1.6, handleheight=1.0, frameon=False, loc="lower center", ncol=2, columnspacing=1.0, borderaxespad=.1)
    ax.set_title("Individual vs society")


def heat(ax, s, levels, modes, title):
    piv = lambda col: s.pivot(index="mode", columns="level", values=col).reindex(index=modes, columns=levels)  # noqa: E731
    M, Q = piv("bias"), piv("q_bh")
    im = ax.imshow(M.to_numpy(float), cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    for i in range(len(modes)):
        for j in range(len(levels)):
            v, q = M.iloc[i, j], Q.iloc[i, j]; sig = bool(np.isfinite(v) and q < .05)
            ax.text(j, i, "" if np.isnan(v) else f"{v:+.2f}".replace("+0.", "+.").replace("-0.", "-."), ha="center", va="center", fontsize=FT,
                    color="white" if (np.isfinite(v) and abs(v) > .55) else "#1A1A1A", fontweight="bold" if sig else "normal", zorder=4)
            if sig:
                ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, fill=False, edgecolor="black", lw=.8, zorder=3))
    ax.set_xticks(range(len(levels)), [CTX_SHORT.get(l, l) for l in levels], fontsize=FT, rotation=30, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(modes)), [SHORT[m] for m in modes], fontsize=FT); ax.tick_params(length=0, pad=1.2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(title)
    return im


def panel_f(ax, pm, fr, cap, title, show_legend):
    for org in ("US", "CN"):
        s = pm[pm.origin == org]
        ax.errorbar(s.capability, s.log_or, yerr=1.96 * s.se, fmt="o", color=ORIGIN[org], ecolor=ORIGIN[org], elinewidth=.5, alpha=.75, ms=2.0, capsize=1, zorder=3)
    mu, sd = cap["index"].mean(), cap["index"].std(ddof=1)
    ai, it = fr.loc["ai (capacidad media)"], fr.loc["ai x capacidad (por 1 SD)"]
    att = float(np.sqrt(1 + (16 * np.sqrt(3) / (15 * np.pi)) ** 2 * ai.sd_prompt ** 2))
    xs = np.linspace(pm.capability.min() - 1, pm.capability.max() + 1, 50); zs = (xs - mu) / sd
    ax.plot(xs, (ai.estimate + it.estimate * zs) / att, color="#222222", lw=1.0, zorder=4)
    ax.axhline(0, color="black", lw=.5, ls=":", zorder=1); ax.grid(alpha=.15)
    ax.set_title(title); ax.set_ylabel("log-OR")
    if show_legend:
        ax.legend(handles=[Line2D([], [], marker="o", ls="", ms=2.5, color=ORIGIN["US"], label="US model"), Line2D([], [], marker="o", ls="", ms=2.5, color=ORIGIN["CN"], label="CN model")],
                  frameon=False, loc="upper left", ncol=2, columnspacing=.8, handlelength=1.0, borderaxespad=.1, labelspacing=.2)


def build(d):
    style()
    fig = plt.figure(figsize=(5.5, 3.6), layout="constrained")
    fig.get_layout_engine().set(w_pad=.02, h_pad=.02, hspace=.06, wspace=.02)
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.15])
    g1 = gs[0].subgridspec(1, 3, wspace=.1)
    axA, axB, axC = (fig.add_subplot(g1[0, i]) for i in range(3))
    panel_a(axA, d["A_levels"], d["A_delta"]); panel_b(axB, d["B"], d["B_ps"]); panel_c(axC, d["C_cells"], d["C_t"])
    g2 = gs[1].subgridspec(2, 2, width_ratios=[3.0, 1.9], height_ratios=[4.3, 3.6], wspace=.06, hspace=.1)
    axD, axF1, axE, axF2 = fig.add_subplot(g2[0, 0]), fig.add_subplot(g2[0, 1]), fig.add_subplot(g2[1, 0]), fig.add_subplot(g2[1, 1])
    DE = d["DE"]
    heat(axD, DE[DE.dim == "context"], CONTEXTS, MODES, "Bias by context and request type")
    imE = heat(axE, DE[DE.dim == "domain"], DOMAINS, MODES[:3], "Bias by domain and request type")
    cax = axE.inset_axes([1.01, .15, .025, .7])
    cb = fig.colorbar(imE, cax=cax, orientation="vertical", ticks=[-1, 0, 1]); cb.ax.tick_params(labelsize=FT, width=.4, length=1.5, pad=1); cb.outline.set_linewidth(.4)
    gl = d["F_glmm"]; pool = gl[gl.run == "pooled"]; pm = d["F_pm"]
    panel_f(axF1, pm[pm.set == "power_shifting_pooled"], pool[pool.set == "power_shifting"].set_index("quantity"), d["cap"], "Capability: power shifting", False)
    panel_f(axF2, pm[pm.set == "control"], pool[pool.set == "control"].set_index("quantity"), d["cap"], "Capability: control", True)
    axF2.set_xlabel("capability index (%)"); axF1.tick_params(labelbottom=False)
    ylo = min(axF1.get_ylim()[0], axF2.get_ylim()[0]); yhi = max(axF1.get_ylim()[1], axF2.get_ylim()[1])
    for a in (axF1, axF2):
        a.set_ylim(ylo, yhi); a.set_xlim(axF1.get_xlim()[0], axF1.get_xlim()[1])
    fig.canvas.draw()
    from _paperstyle import letters
    letters(fig, [(axA, "A", .004), (axB, "B", None), (axC, "C", None), (axD, "D", .004), (axE, "E", .004), (axF1, "F", None)])
    for ext in ("pdf", "png"):
        out = HERE / f"figure3_compact_en.{ext}"; fig.savefig(out, dpi=300); print("escrito:", out.relative_to(ROOT))
    plt.close(fig)


if __name__ == "__main__":
    build(load())
