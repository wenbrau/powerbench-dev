"""F4 sanity check: the pp main panel as a Linear Probability Model, two specs side by side, both
with two-way (prompt x model) cluster-robust SE:
  A) marginal LPM  y ~ ai          (== the paired-d estimator of fig4_panel_main)
  B) LPM + prompt FE  y ~ ai + C(prompt)
Documents that on this balanced paired design the two give the same point estimate. REAL data.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.transforms as mtransforms

R = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/22_d3_ai_final"
OUT = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/fig4_working/fig4_panel_main_lpm_check.png"
MODES = ["he", "de", "pg", "control"]
MNAME = {"he": "Self-emp", "de": "Disemp", "pg": "Power grab", "control": "Control"}
COL = {"US": "#3B6EA5", "CN": "#B24747"}
FILL = {"US": "#9FBBD8", "CN": "#DFA9A9"}


def ols_twoway(y, X, clp, clm):
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    k = X.shape[1]
    s = e[:, None] * X

    def meat(cl):
        cl = np.asarray(cl); M = np.zeros((k, k))
        for c in pd.unique(cl):
            g = s[cl == c].sum(0); M += np.outer(g, g)
        return M, len(pd.unique(cl))
    Mp, Gp = meat(clp); Mm, Gm = meat(clm)
    cell = pd.factorize(pd.Series(list(zip(clp, clm))))[0]; Mc, Gc = meat(cell)
    V = XtX_inv @ (Gp/(Gp-1)*Mp + Gm/(Gm-1)*Mm - Gc/(Gc-1)*Mc) @ XtX_inv
    return beta, np.sqrt(np.diag(V))


rows = pd.read_csv(f"{R}/analysis_rows.csv.gz", low_memory=False)
rows = rows[rows["valid"] == True].copy()
rows["ai"] = (rows["condition"] == "ai").astype(float)


def fit(mode, org, use_fe):
    d = rows[(rows["mode"] == mode) & (rows["origin"] == org)]
    y = d["refuse"].to_numpy(float)
    if use_fe:
        Xd = pd.get_dummies(d["prompt_id"], prefix="p").astype(float)
        X = np.column_stack([d["ai"].to_numpy(float), Xd.to_numpy()])
        ai_col = 0
    else:
        X = np.column_stack([np.ones(len(d)), d["ai"].to_numpy(float)])
        ai_col = 1
    beta, se = ols_twoway(y, X, d["prompt_id"].to_numpy(), d["model"].to_numpy())
    return beta[ai_col] * 100, se[ai_col] * 100


fig, axes = plt.subplots(1, 2, figsize=(13, 6), sharey=True)
group_w = 2.2; bar_w = 0.82; offs = {"US": -0.48, "CN": 0.48}
centers = np.arange(len(MODES)) * group_w
specs = [(axes[0], False, "A · LPM marginal  y ~ ai   (= d pareado, panel actual)"),
         (axes[1], True, "B · LPM + FE de prompt  y ~ ai + C(prompt)")]
print(f"{'spec':4s} {'mode':8s} {'bloc':4s} {'est(pp)':>8s} {'se':>6s}")
for ax, use_fe, title in specs:
    for gi, m in enumerate(MODES):
        for org in ["US", "CN"]:
            pos = centers[gi] + offs[org]
            est, se = fit(m, org, use_fe)
            lo, hi = est-1.96*se, est+1.96*se
            ax.bar(pos, est, width=bar_w, facecolor=FILL[org], edgecolor=COL[org], lw=1.6, alpha=0.85, zorder=2)
            ax.errorbar(pos, est, yerr=[[est-lo], [hi-est]], fmt="none", ecolor=COL[org], elinewidth=1.9, capsize=4, zorder=5)
            print(f"{'FE' if use_fe else 'marg':4s} {m:8s} {org:4s} {est:8.2f} {se:6.2f}")
    ax.axhline(0, color="#333", lw=1.1)
    ax.set_xticks([]); ax.set_xlim(centers[0]-group_w*0.42, centers[-1]+group_w*0.42)
    ax.grid(axis="y", ls=":", alpha=0.4)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=11)
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    for gi, m in enumerate(MODES):
        ax.text(centers[gi], -0.09, MNAME[m], transform=trans, ha="center", va="top", fontsize=10.5, fontweight="bold")
axes[0].set_ylabel("Δ refusal   D3 (agente IA) − D1 (humano)   (pp)", fontsize=11.5)

fig.subplots_adjust(top=0.80, bottom=0.11, left=0.07, right=0.98, wspace=0.06)
fig.suptitle("Figura 4 · Panel main como LPM — marginal vs con FE de prompt (IC95% two-way cluster prompt×modelo)", fontsize=12.5, y=0.95)
fig.legend(handles=[Line2D([0], [0], marker="s", color=COL["US"], ls="", ms=9, label="US"),
                    Line2D([0], [0], marker="s", color=COL["CN"], ls="", ms=9, label="CN")],
           loc="center", bbox_to_anchor=(0.5, 0.89), ncol=2, fontsize=9.5, frameon=False, columnspacing=2.2)
fig.text(0.02, 0.02, "En diseño balanceado el punto coincide; el FE puede ajustar levemente el SE al absorber varianza de prompt. LPM = lineal → no descarta prompts todo-cero.",
         ha="left", fontsize=8, color="#555")
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("saved", OUT)
