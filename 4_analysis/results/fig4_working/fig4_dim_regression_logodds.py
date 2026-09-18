"""F4 dimension contrasts on the LOG-ODDS scale (pg). Logistic with ai x level interactions:
  logit P(refuse) = b0 + b_ai*ai + (scale dummies) + (standing dummies)
                    + g*(ai*scale) + g*(ai*standing)
The ai:level coefficients are how the AI-agent log-OR shifts at each level vs reference
(scale ref = society, standing ref = low). All pairwise level contrasts = c'beta, SE = sqrt(c'Vc),
two-way (prompt x model) cluster-robust. exp(contrast) = ratio of ORs. REAL data (block 22).
"""
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import statsmodels.api as sm

warnings.filterwarnings("ignore")
R = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/22_d3_ai_final"
OUT = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/fig4_working/fig4_dim_regression_logodds.png"
COL = {"US": "#3B6EA5", "CN": "#B24747"}


def logit_twoway_full(y, X, clp, clm):
    res = sm.Logit(y, X).fit(disp=0, method="newton", maxiter=100)
    beta = res.params.to_numpy(); p = res.predict(); k = X.shape[1]
    A = X.T.to_numpy() @ (X.to_numpy() * (p*(1-p))[:, None]); A_inv = np.linalg.inv(A)
    s = (y - p)[:, None] * X.to_numpy()

    def meat(cl):
        cl = np.asarray(cl); M = np.zeros((k, k))
        for c in pd.unique(cl):
            g = s[cl == c].sum(0); M += np.outer(g, g)
        return M, len(pd.unique(cl))
    Mp, Gp = meat(clp); Mm, Gm = meat(clm)
    cell = pd.factorize(pd.Series(list(zip(clp, clm))))[0]; Mc, Gc = meat(cell)
    V = A_inv @ (Gp/(Gp-1)*Mp + Gm/(Gm-1)*Mm - Gc/(Gc-1)*Mc) @ A_inv
    return list(X.columns), beta, V


rows = pd.read_csv(f"{R}/analysis_rows.csv.gz", low_memory=False)
rows = rows[(rows["valid"] == True) & (rows["mode"] == "pg")].copy()
rows["ai"] = (rows["condition"] == "ai").astype(float)

CONTRASTS = [("Individual − Society", {"ai_ind": 1}),
             ("Group − Society", {"ai_grp": 1}),
             ("Individual − Group", {"ai_ind": 1, "ai_grp": -1}),
             ("High − Low", {"ai_high": 1}),
             ("Med − Low", {"ai_med": 1}),
             ("High − Med", {"ai_high": 1, "ai_med": -1})]

fits = {}
for org in ["US", "CN"]:
    d = rows[rows.origin == org]
    ind = (d.scale == "individual").astype(float); grp = (d.scale == "group").astype(float)
    med = (d.standing == "med").astype(float); high = (d.standing == "high").astype(float)
    X = pd.DataFrame({"const": 1.0, "ai": d.ai.values, "ind": ind.values, "grp": grp.values,
                      "med": med.values, "high": high.values,
                      "ai_ind": (d.ai*ind).values, "ai_grp": (d.ai*grp).values,
                      "ai_med": (d.ai*med).values, "ai_high": (d.ai*high).values})
    fits[org] = logit_twoway_full(d.refuse.to_numpy(float), X, d.prompt_id.to_numpy(), d.model.to_numpy())


def contrast(org, wd):
    cols, beta, V = fits[org]
    c = np.zeros(len(cols))
    for name, w in wd.items():
        c[cols.index(name)] = w
    return c @ beta, np.sqrt(c @ V @ c)


fig, ax = plt.subplots(figsize=(7.8, 6))
n = len(CONTRASTS)
print(f"{'contrast':22s} bloc  logROR   [95% CI]")
for i, (lab, wd) in enumerate(CONTRASTS):
    yy = n - i
    for org, dy in [("US", 0.16), ("CN", -0.16)]:
        est, se = contrast(org, wd)
        lo, hi = est-1.96*se, est+1.96*se
        ax.errorbar(est, yy+dy, xerr=[[est-lo], [hi-est]], fmt="o", ms=7, color=COL[org], ecolor=COL[org],
                    elinewidth=1.7, capsize=3.5, zorder=3)
        print(f"{lab:22s} {org}  {est:+.3f}  [{lo:+.3f},{hi:+.3f}]  ROR={np.exp(est):.2f}")

ax.axvline(0, color="#333", lw=1.1)
ax.set_yticks(range(1, n+1)); ax.set_yticklabels([l for l, _ in CONTRASTS][::-1], fontsize=10.5)
ax.set_ylim(0.4, n+0.7)
ax.set_xlabel("Contraste en log-OR del efecto-agente (pg)   ·   0 = mismo efecto", fontsize=10.5)


def bracket(y0, y1, label, xb=-0.42):
    tr = ax.get_yaxis_transform()
    ax.plot([xb, xb], [y0, y1], color="#888", lw=1.2, transform=tr, clip_on=False)
    for yy in (y0, y1):
        ax.plot([xb, xb+0.02], [yy, yy], color="#888", lw=1.2, transform=tr, clip_on=False)
    ax.text(xb-0.03, (y0+y1)/2, label, transform=tr, rotation=90, va="center", ha="center",
            fontsize=9.5, color="#555", fontweight="bold")


bracket(3.7, 6.3, "ESCALA\ndel target")
bracket(0.7, 3.3, "STANDING\ndel usuario")
ax.grid(axis="x", ls=":", alpha=0.4)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
sec = ax.secondary_xaxis("top", functions=(np.exp, np.log)); sec.set_xlabel("ROR (ratio de OR)", fontsize=9.5)
sec.set_xticks([0.5, 0.7, 1, 1.5, 2])

fig.subplots_adjust(top=0.82, bottom=0.13, left=0.40, right=0.97)
fig.suptitle("Figura 4 · Contrastes del sesgo pg en LOG-ODDS — escala y standing", fontsize=12.5, y=0.975)
fig.legend(handles=[Line2D([0], [0], marker="o", color=COL["US"], ls="", ms=8, label="US"),
                    Line2D([0], [0], marker="o", color=COL["CN"], ls="", ms=8, label="CN")],
           loc="center", bbox_to_anchor=(0.5, 0.9), ncol=2, fontsize=10, frameon=False, columnspacing=2.2)
fig.text(0.02, 0.02, "logit(refuse) ~ ai + escala + standing + ai×escala + ai×standing, por bloque · coef ai×nivel · IC95% two-way cluster (prompt×modelo)",
         ha="left", fontsize=7.8, color="#555")
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("saved", OUT)
