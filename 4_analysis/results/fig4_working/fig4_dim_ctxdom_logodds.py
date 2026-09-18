"""F4 dimension study (log-odds): the pg AI-agent effect (log-OR of D3 vs D1) WITHIN each context
and each domain. Per bloc, per dimension: logit refuse ~ ai + C(level) + ai:C(level); the ai
effect at level L = b_ai + g_L (reconstructed as c'beta, SE sqrt(c'Vc)), two-way (prompt x model)
cluster-robust. log-OR 0 = no bias. Dashed = bloc overall pg effect. REAL data (block 22).
"""
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import statsmodels.api as sm

warnings.filterwarnings("ignore")
R = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/22_d3_ai_final"
OUT = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/fig4_working/fig4_dim_ctxdom_logodds.png"
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


def level_effects(dim, org):
    d = rows[rows.origin == org]
    levels = sorted(d[dim].unique())
    ref = levels[0]
    cols_data = {"const": 1.0, "ai": d.ai.values}
    for lv in levels[1:]:
        ind = (d[dim] == lv).astype(float)
        cols_data[f"L_{lv}"] = ind.values
        cols_data[f"ai_{lv}"] = (d.ai*ind).values
    X = pd.DataFrame(cols_data)
    cols, beta, V = logit_twoway_full(d.refuse.to_numpy(float), X, d.prompt_id.to_numpy(), d.model.to_numpy())
    out = []
    for lv in levels:
        c = np.zeros(len(cols)); c[cols.index("ai")] = 1
        if lv != ref:
            c[cols.index(f"ai_{lv}")] = 1
        est = c @ beta; se = np.sqrt(c @ V @ c)
        out.append((lv, est, se))
    # overall effect
    Xo = pd.DataFrame({"const": 1.0, "ai": d.ai.values})
    _, bo, Vo = logit_twoway_full(d.refuse.to_numpy(float), Xo, d.prompt_id.to_numpy(), d.model.to_numpy())
    return out, bo[1]


fig, axes = plt.subplots(1, 2, figsize=(13, 7))
for ax, dim in zip(axes, ["context", "domain"]):
    allres = {}
    overall = {}
    for org in ["US", "CN"]:
        allres[org], overall[org] = level_effects(dim, org)
    levels = [lv for lv, _, _ in allres["US"]]
    for i, lv in enumerate(levels):
        yy = len(levels) - i
        for org, dy in [("US", 0.16), ("CN", -0.16)]:
            _, est, se = allres[org][i]
            ax.errorbar(est, yy+dy, xerr=1.96*se, fmt="o", ms=6, color=COL[org], ecolor=COL[org],
                        elinewidth=1.4, capsize=3, zorder=3)
    for org in ["US", "CN"]:
        ax.axvline(overall[org], color=COL[org], ls="--", lw=1.2, alpha=0.7)
    ax.axvline(0, color="#333", lw=1.1)
    ax.set_yticks(range(1, len(levels)+1)); ax.set_yticklabels(levels[::-1], fontsize=9.5)
    ax.set_ylim(0.4, len(levels)+0.6)
    ax.set_title(f"por {dim}", fontsize=12, fontweight="bold")
    ax.set_xlabel("log-OR del efecto-agente (pg)   ·   0 = sin sesgo", fontsize=10)
    ax.grid(axis="x", ls=":", alpha=0.4)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    sec = ax.secondary_xaxis("top", functions=(np.exp, np.log)); sec.set_xlabel("OR", fontsize=9)
    sec.set_xticks([0.7, 1, 1.5, 2, 3])

fig.subplots_adjust(top=0.83, bottom=0.12, left=0.13, right=0.97, wspace=0.35)
fig.suptitle("Figura 4 · Sesgo pg hacia el agente por CONTEXTO y por DOMINIO (log-odds)", fontsize=13, y=0.965)
fig.legend(handles=[Line2D([0], [0], marker="o", color=COL["US"], ls="", ms=8, label="US"),
                    Line2D([0], [0], marker="o", color=COL["CN"], ls="", ms=8, label="CN"),
                    Line2D([0], [0], ls="--", color="#888", label="efecto global del bloque")],
           loc="center", bbox_to_anchor=(0.5, 0.9), ncol=3, fontsize=9, frameon=False)
fig.text(0.02, 0.02, "logit(refuse) ~ ai + C(nivel) + ai×C(nivel) por bloque · efecto-agente en cada nivel = b_ai+g_nivel · IC95% two-way cluster (prompt×modelo)",
         ha="left", fontsize=7.8, color="#555")
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("saved", OUT)
