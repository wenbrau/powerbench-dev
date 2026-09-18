"""F4 main panel WEIGHTED BY OPENROUTER USAGE, across the 4 specs: {pp, log-odds} x {no FE, prompt FE}.
Survey/probability weights w_m = model's 30d token share (renormalized within bloc). Weighted
pseudo-MLE point estimate + two-way (prompt x model) cluster-robust sandwich with weighted score
s_i = w_i (y_i - p_i) x_i (logit) or w_i e_i x_i (LPM). Unweighted estimate shown as a hollow
marker for comparison. REAL data (block 22) + real usage (inputs/openrouter_usage). log-OR 0 / pp 0
= no effect.
"""
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.transforms as mtransforms
import statsmodels.api as sm

warnings.filterwarnings("ignore")
R = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/22_d3_ai_final"
WF = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/40_fig2_usage_weighted/usage_weights.csv"
OUT = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/fig4_working/fig4_panel_main_usage_weighted.png"
MODES = ["he", "de", "pg", "control"]
MNAME = {"he": "Self-emp", "de": "Disemp", "pg": "Power grab", "control": "Control"}
COL = {"US": "#3B6EA5", "CN": "#B24747"}
FILL = {"US": "#9FBBD8", "CN": "#DFA9A9"}

wt = pd.read_csv(WF).set_index("model")["share"].to_dict()
rows = pd.read_csv(f"{R}/analysis_rows.csv.gz", low_memory=False)
rows = rows[rows["valid"] == True].copy()
rows["ai"] = (rows["condition"] == "ai").astype(float)
rows["w"] = rows["model"].map(wt).astype(float)


def meat(s, cl):
    cl = np.asarray(cl); k = s.shape[1]; M = np.zeros((k, k))
    for c in pd.unique(cl):
        g = s[cl == c].sum(0); M += np.outer(g, g)
    return M, len(pd.unique(cl))


def oneway_V(A_inv, s, cl):
    # weighting fixes the model distribution -> model is no longer a sampling dimension;
    # the remaining random component is the prompt, so cluster by PROMPT only.
    M, G = meat(s, cl)
    return A_inv @ (G/(G-1)*M) @ A_inv


def fit(mode, org, scale, use_fe, weighted):
    d = rows[(rows["mode"] == mode) & (rows["origin"] == org)]
    y = d["refuse"].to_numpy(float)
    w = d["w"].to_numpy(float) if weighted else np.ones(len(d))
    w = w / w.mean()
    if use_fe:
        if scale == "logodds":
            keep = d.groupby("prompt_id")["refuse"].transform("nunique") > 1
            d = d[keep]; y = d["refuse"].to_numpy(float)
            w = (d["w"].to_numpy(float) if weighted else np.ones(len(d))); w = w/w.mean()
        Xd = pd.get_dummies(d["prompt_id"], prefix="p").astype(float)
        X = np.column_stack([d["ai"].to_numpy(float), Xd.to_numpy()]); ai = 0
    else:
        X = np.column_stack([np.ones(len(d)), d["ai"].to_numpy(float)]); ai = 1
    clp, clm = d["prompt_id"].to_numpy(), d["model"].to_numpy()
    if scale == "pp":
        XtWX = X.T @ (w[:, None]*X); A_inv = np.linalg.inv(XtWX)
        beta = A_inv @ (X.T @ (w*y)); e = y - X @ beta
        s = (w*e)[:, None]*X
        V = oneway_V(A_inv, s, clp)
        return beta[ai]*100, np.sqrt(V[ai, ai])*100
    else:
        res = sm.GLM(y, X, family=sm.families.Binomial(), freq_weights=w).fit()
        beta = res.params; p = res.predict()
        A = X.T @ (X * (w*p*(1-p))[:, None]); A_inv = np.linalg.inv(A)
        s = (w*(y-p))[:, None]*X
        V = oneway_V(A_inv, s, clp)
        return beta[ai], np.sqrt(V[ai, ai])


# effective sample size (Kish) per bloc
for org in ["US", "CN"]:
    sh = rows[rows.origin == org].groupby("model")["w"].first().to_numpy()
    sh = sh/sh.sum()
    print(f"{org}: 12 modelos, ESS Kish = {1/np.sum(sh**2):.1f} modelos efectivos")

fig, axes = plt.subplots(2, 2, figsize=(13.5, 9))
specs = [("pp", False), ("pp", True), ("logodds", False), ("logodds", True)]
titles = ["pp · sin FE", "pp · con FE de prompt", "log-OR · sin FE", "log-OR · con FE de prompt"]
group_w = 2.2; bar_w = 0.82; offs = {"US": -0.48, "CN": 0.48}
centers = np.arange(len(MODES))*group_w
for ax, (scale, use_fe), title in zip(axes.flat, specs, titles):
    for gi, m in enumerate(MODES):
        for org in ["US", "CN"]:
            pos = centers[gi] + offs[org]
            ew, sew = fit(m, org, scale, use_fe, True)     # weighted
            eu, _ = fit(m, org, scale, use_fe, False)      # unweighted point
            lo, hi = ew-1.96*sew, ew+1.96*sew
            ax.bar(pos, ew, width=bar_w, facecolor=FILL[org], edgecolor=COL[org], lw=1.5, alpha=0.85, zorder=2)
            ax.errorbar(pos, ew, yerr=[[ew-lo], [hi-ew]], fmt="none", ecolor=COL[org], elinewidth=1.7, capsize=3.5, zorder=5)
            ax.scatter([pos], [eu], marker="_", s=340, color="black", zorder=6, linewidths=2)
    ax.axhline(0, color="#333", lw=1.0)
    ax.set_xticks([]); ax.set_xlim(centers[0]-group_w*0.42, centers[-1]+group_w*0.42)
    ax.grid(axis="y", ls=":", alpha=0.4)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=11.5, fontweight="bold")
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    for gi, m in enumerate(MODES):
        ax.text(centers[gi], -0.08, MNAME[m], transform=trans, ha="center", va="top", fontsize=9.5, fontweight="bold")
axes[0, 0].set_ylabel("Δ refusal (pp)", fontsize=11)
axes[1, 0].set_ylabel("log-OR (D3 vs D1)", fontsize=11)

fig.subplots_adjust(top=0.86, bottom=0.06, left=0.07, right=0.98, hspace=0.22, wspace=0.13)
fig.suptitle("Figura 4 · Panel main PONDERADO POR USO (OpenRouter, tokens 30d) — barra = ponderado (IC95% clusterizado por PROMPT; uso→modelo fijo), guion negro = no-ponderado",
             fontsize=11, y=0.955)
fig.legend(handles=[Line2D([0], [0], marker="s", color=COL["US"], ls="", ms=9, label="US"),
                    Line2D([0], [0], marker="s", color=COL["CN"], ls="", ms=9, label="CN"),
                    Line2D([0], [0], marker="_", color="black", ls="", ms=12, mew=2, label="estimador no-ponderado")],
           loc="center", bbox_to_anchor=(0.5, 0.905), ncol=3, fontsize=9.5, frameon=False)
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("saved", OUT)
