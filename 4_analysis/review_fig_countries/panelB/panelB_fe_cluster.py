#!/usr/bin/env python3
"""Revisión de la figura de países (19/09, pedido de Wendy): el mismo estimando del panel B (log-OR del lado del usuario)
con un logit de EFECTOS FIJOS por prompt y por modelo, y errores estándar agrupados (cluster) por modelo, en lugar del
GLMM de efectos aleatorios del bloque 45. Por conjunto (geo / neutral) y modo:

    logit(π_i) = β₁·side_i + β₂·dyad_i + α_m(i) + γ_p(i)

    side = 1 usuario del lado USA, 0 usuario del lado China; dyad = 1 aliados, 0 USA / China (solo geo);
    (con efectos fijos la codificación centrada del GLMM no hace falta: 1/0 y ±½ dan el mismo β₁ y el mismo SE,
    solo corren la constante y los efectos fijos de modelo; verificado en geo pg, 19/09.)
    α_m = 24 efectos fijos de modelo; γ_p = 192 efectos fijos de prompt. Máxima verosimilitud sin condicionar
    (dummies); SE sándwich agrupado por modelo (24 clusters, corrección G/(G−1)·(N−1)/(N−K)); IC 95 % con la normal
    (como el Wald del GLMM) y con t(23) (Cameron y Miller 2015, pocos clusters). Los prompts sin variación en refuse
    dentro del conjunto × modo (todos 0 o todos 1) se sacan: en un logit con efectos fijos su dummy diverge y no aportan
    nada al contraste de lado, que es dentro del prompt. q = BH sobre los 4 modos de geo; neutral es la referencia, sin q.
Lee las mismas filas que el bloque 45 (load_d2_final, condiciones válidas). Compara con side_glmm.csv del bloque 45.
Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_countries/panelB/panelB_fe_cluster.py
"""
from __future__ import annotations
import os, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
for p in (str(HERE.parent.parent), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
from pbanalysis.final_conditions import load_d2_final

SETS = {"geo": [("us_cn", "us_cn", "cn_us"), ("allies", "allyus_allycn", "allycn_allyus")],
        "neutral": [("neutrals", "neutralA_neutralB", "neutralB_neutralA")]}
MODES = ("he", "de", "pg", "control")
LABELS = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
GLMM = ROOT / "4_analysis/results/45_fig3_side_combined/side_glmm.csv"
NL = chr(10)


def bh(p):
    p = np.asarray(p, float); m = len(p); order = np.argsort(p); q = np.empty(m); prev = 1.0
    for rank, i in zip(range(m, 0, -1), order[::-1]):
        prev = min(prev, p[i] * m / rank); q[i] = prev
    return q


def fmt_q(q):
    return ("q < 0,001" if q < .001 else f"q = {q:.3f}").replace(".", ",")


def long_table(d2):
    rows = []
    for st, dyads in SETS.items():
        for dy, cA, cB in dyads:
            for cond, side in ((cA, 1), (cB, 0)):
                x = d2[(d2.condition == cond) & d2.valid][["refuse", "mode", "prompt_id", "model"]].copy()
                x["set"], x["dyad"], x["side"] = st, int(dy == "allies"), side
                rows.append(x)
    g = pd.concat(rows, ignore_index=True)
    g["refuse"] = g.refuse.astype(int)
    return g


def fit_fe(dd):
    """Logit con dummies de modelo y prompt; devuelve el coeficiente de side con SE cluster por modelo."""
    n0 = len(dd); p0 = dd.prompt_id.nunique()
    keep_p = dd.groupby("prompt_id").refuse.transform(lambda s: 0 < s.mean() < 1)
    dd = dd[keep_p]
    keep_m = dd.groupby("model").refuse.transform(lambda s: 0 < s.mean() < 1)
    dd = dd[keep_m]
    X = pd.concat([dd[["side"]].astype(float),
                   dd[["dyad"]].astype(float) if dd.dyad.nunique() > 1 else pd.DataFrame(index=dd.index),
                   pd.get_dummies(dd.model, prefix="m", drop_first=True, dtype=float),
                   pd.get_dummies(dd.prompt_id, prefix="p", drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X)
    y = dd.refuse.astype(float)
    groups = pd.factorize(dd.model)[0]
    res = sm.Logit(y, X).fit(method="newton", maxiter=200, disp=0,
                             cov_type="cluster", cov_kwds={"groups": groups, "use_correction": True})
    b, se = res.params["side"], res.bse["side"]
    G = dd.model.nunique()
    z = b / se; p_norm = 2 * stats.norm.sf(abs(z)); p_t = 2 * stats.t.sf(abs(z), G - 1)
    tq = stats.t.ppf(.975, G - 1)
    return dict(logOR=b, se=se, z=z, p=p_norm, p_t23=p_t, OR=np.exp(b), OR_lo=np.exp(b - 1.96 * se), OR_hi=np.exp(b + 1.96 * se),
                OR_lo_t=np.exp(b - tq * se), OR_hi_t=np.exp(b + tq * se), n_rows=len(dd), n_rows_in=n0,
                n_prompts=dd.prompt_id.nunique(), n_prompts_in=p0, n_models=G, converged=bool(res.mle_retvals["converged"]))


def main():
    g = long_table(load_d2_final())
    out = []
    for st in SETS:
        for md in MODES:
            r = fit_fe(g[(g.set == st) & (g["mode"] == md)])
            out.append(dict(set=st, mode=md, **r)); print(st, md, f"OR {r['OR']:.3f} [{r['OR_lo']:.3f}; {r['OR_hi']:.3f}] p {r['p']:.3f}"
                                                            f"  prompts {r['n_prompts']}/{r['n_prompts_in']}  conv {r['converged']}", flush=True)
    fe = pd.DataFrame(out)
    fe["q_bh"] = np.nan
    geo = fe.set == "geo"
    fe.loc[geo, "q_bh"] = bh(fe.loc[geo, "p"].values)

    glmm = pd.read_csv(GLMM); glmm = glmm[glmm.quantity == "lado (24 modelos)"][["set", "mode", "estimate", "se", "OR", "OR_lo", "OR_hi", "p"]]
    glmm.columns = ["set", "mode", "glmm_logOR", "glmm_se", "glmm_OR", "glmm_OR_lo", "glmm_OR_hi", "glmm_p"]
    cmp = fe.merge(glmm, on=["set", "mode"])
    cmp.to_csv(HERE / "panelB_fe_cluster.csv", index=False)

    # ---- figura: FE + cluster (lleno) junto al GLMM (contorno), geo y neutral
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "savefig.facecolor": "white"})
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2), layout="constrained", sharey=True)
    x = np.arange(len(MODES)); wd = .36
    for ax, st in zip(axes, SETS):
        r = cmp[cmp.set == st].set_index("mode").loc[list(MODES)]
        col = "#3B3B58" if st == "geo" else "#C9C9C9"
        ax.bar(x - wd / 2, r.OR - 1, bottom=1, width=wd, color=col, zorder=2, label="logit con efectos fijos de prompt y de modelo, SE agrupado por modelo (24 clusters)")
        ax.errorbar(x - wd / 2, r.OR, yerr=[r.OR - r.OR_lo, r.OR_hi - r.OR], fmt="none", ecolor="#111", elinewidth=1.2, capsize=3, zorder=3)
        ax.errorbar(x - wd / 2, r.OR, yerr=[r.OR - r.OR_lo_t, r.OR_hi_t - r.OR], fmt="none", ecolor="#111", elinewidth=.7, capsize=0, zorder=3, alpha=.6)
        ax.bar(x + wd / 2, r.glmm_OR - 1, bottom=1, width=wd, facecolor="none", edgecolor=col, lw=1.5, zorder=2, label="GLMM: intercepto y pendiente de lado aleatorios por modelo, intercepto aleatorio por prompt (panel B actual)")
        ax.errorbar(x + wd / 2, r.glmm_OR, yerr=[r.glmm_OR - r.glmm_OR_lo, r.glmm_OR_hi - r.glmm_OR], fmt="none", ecolor="#666", elinewidth=1.2, capsize=3, zorder=3)
        if st == "geo":
            for xi, h, q in zip(x - wd / 2, r.OR_hi_t, r.q_bh):
                ax.text(xi, h * 1.02, fmt_q(q), ha="center", va="bottom", fontsize=8)
        ax.set_yscale("log"); ax.set_yticks([.7, .8, .9, 1, 1.1, 1.25, 1.5]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.set_minor_formatter(mticker.NullFormatter()); ax.set_ylim(.62, 1.62)
        ax.axhline(1, color="black", lw=1); ax.grid(axis="y", alpha=.15)
        ax.set_xticks(x, [LABELS[m] for m in MODES], fontsize=9, rotation=15, ha="right", rotation_mode="anchor")
        ax.set_title("lado USA / lado China (juntas)" if st == "geo" else "neutral A / neutral B (referencia)", fontsize=10)
    axes[0].set_ylabel("OR de refusal, usuario del lado USA vs del lado China" + NL + "(IC 95 %: grueso normal, fino t(23); q = BH sobre 4 modos)")
    axes[0].text(.5, .985, "▲ rechaza más si el usuario es del lado USA", transform=axes[0].transAxes, ha="center", va="top", fontsize=8, color=ORIGIN["CN"], fontweight="bold")
    axes[0].text(.5, .015, "▼ rechaza más si el usuario es del lado China", transform=axes[0].transAxes, ha="center", va="bottom", fontsize=8, color=ORIGIN["US"], fontweight="bold")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=9, loc="outside lower center", ncol=1)
    fig.suptitle("Efecto del lado del usuario sobre el refusal: mismo contraste dentro de prompt y de modelo, con efectos fijos o con efectos aleatorios", fontsize=11)
    fig.savefig(HERE / "panelB_fe_cluster.png", dpi=150)
    print()
    print(cmp[["set", "mode", "OR", "OR_lo", "OR_hi", "OR_lo_t", "OR_hi_t", "p", "p_t23", "q_bh", "glmm_OR", "glmm_OR_lo", "glmm_OR_hi", "glmm_p",
               "n_prompts", "n_prompts_in", "n_rows"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
