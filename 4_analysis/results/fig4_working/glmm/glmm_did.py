#!/usr/bin/env python3
"""Figura 4 -- DiD (parte especifica de poder) con GLMM, subcarpeta glmm/, para robustez.

DiD = (sesgo agente-IA en un modo de power shifting) - (sesgo agente-IA en el control). Aisla la
parte del sesgo que es especifica de poder. Hoy fig4 lo estima con logistica marginal + cluster-
robust two-way (fig4_did_logodds.py, termino ai:esModo). Aca se recomputa el MISMO DiD (termino
ai:ps) con un GLMM (efectos aleatorios por prompt y por modelo + pendiente aleatoria de ai:ps por
modelo, para no pseudorreplicar el termino que se testea) y se ponen los dos lado a lado.

El GLMM lo corre el harness del script padre ../glmm_ai_bias.R (E_ai_ps pooled he+de+pg vs control;
F_<modo>_vs_ctl por modo), el mismo que fig4_glmm.py. El cluster-robust se calcula aca sobre las
MISMAS filas d0 (logistica apilando modo + control, refuse ~ ai * esModo). NO decide nada: recomputa
un panel existente con otro estimador y grafica ambos.

Ejecutar desde la raiz:  python 4_analysis/results/fig4_working/glmm/glmm_did.py
Requiere Rscript con lme4.
"""
from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent  # fig4_working/
A4 = HERE.parent.parent.parent  # 4_analysis/
ROOT = A4.parent
for p in (str(A4), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import statsmodels.api as sm  # noqa: E402

import analysis_16_d3_panel24_control as a16  # noqa: E402

warnings.filterwarnings("ignore")

R_SCRIPT = PARENT / "glmm_ai_bias.R"  # el harness del DiD ya existente (E/F, ai:ps)
OUT_PNG = HERE / "glmm_did.png"
OUT_CSV = HERE / "glmm_did_compare.csv"
MODES = ["he", "de", "pg"]
MNAME = {"he": "Self-emp", "de": "Disemp", "pg": "Power grab", "pooled": "Pooled\n(he+de+pg)"}
COL = {"glmm": "#2a6f4e", "cr": "#8a6d3b"}
FILL = {"glmm": "#a7d3ba", "cr": "#e3cfa3"}


def find_rscript() -> str:
    exe = shutil.which("Rscript")
    if exe:
        return exe
    cands = sorted(glob.glob("C:/Program Files/R/R-*/bin/Rscript.exe"))
    if not cands:
        sys.exit("Rscript no encontrado: instalar R y lme4.")
    return cands[-1]


def logit_twoway(y, X, clp, clm):
    try:
        res = sm.Logit(y, X).fit(disp=0, method="newton", maxiter=100)
    except Exception:
        try:
            res = sm.Logit(y, X).fit(disp=0, method="bfgs", maxiter=500)
        except Exception:
            return None, None, False
    beta = res.params.to_numpy()
    p = res.predict()
    k = X.shape[1]
    A = X.T.to_numpy() @ (X.to_numpy() * (p * (1 - p))[:, None])
    try:
        A_inv = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        A_inv = np.linalg.pinv(A)
    s = (y - p)[:, None] * X.to_numpy()

    def meat(cl):
        cl = np.asarray(cl)
        M = np.zeros((k, k))
        for c in pd.unique(cl):
            g = s[cl == c].sum(0)
            M += np.outer(g, g)
        return M, len(pd.unique(cl))

    Mp, Gp = meat(clp)
    Mm, Gm = meat(clm)
    cell = pd.factorize(pd.Series(list(zip(clp, clm))))[0]
    Mc, Gc = meat(cell)
    V = A_inv @ (Gp / (Gp - 1) * Mp + Gm / (Gm - 1) * Mm - Gc / (Gc - 1) * Mc) @ A_inv
    return beta, np.sqrt(np.diag(V)), True


def cr_did(d0, modes):
    """DiD cluster-robust (log-OR): apila filas de `modes` + control, refuse ~ ai*ps. Devuelve ai:ps."""
    d = d0[d0["mode"].isin(list(modes) + ["ctl"])].copy()
    d["ps"] = (d["mode"] != "ctl").astype(float)
    X = pd.DataFrame({"const": 1.0, "ai": d["ai"].to_numpy(float), "ps": d["ps"].to_numpy(),
                      "ai_ps": (d["ai"].to_numpy() * d["ps"].to_numpy()).astype(float)})
    beta, se, ok = logit_twoway(d["refuse"].to_numpy(float), X, d["prompt_id"].to_numpy(),
                                d["model"].to_numpy())
    if not ok:
        return None
    j = list(X.columns).index("ai_ps")
    return float(beta[j]), float(se[j])


def run_glmm(d0):
    df = d0.copy()
    df["ps"] = (df["mode"] != "ctl").astype(int)
    df["cn"] = (df.origin == "CN").astype(int)
    df["mode_he"] = (df["mode"] == "he").astype(int)
    df["mode_de"] = (df["mode"] == "de").astype(int)
    rscript = find_rscript()
    with tempfile.TemporaryDirectory() as tmp:
        fin, fout = Path(tmp) / "in.csv", Path(tmp) / "out.csv"
        df[["refuse", "ai", "ps", "cn", "mode_he", "mode_de", "prompt_id", "model"]].to_csv(fin, index=False)
        proc = subprocess.run([rscript, str(R_SCRIPT), str(fin), str(fout)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(proc.stdout, flush=True)
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            sys.exit(f"Rscript termino con codigo {proc.returncode}")
        return pd.read_csv(fout)


def main():
    df = a16.load()
    d0 = df[df.valid].copy()
    d0["refuse"] = d0.refuse.astype(int)
    d0["ai"] = (d0.dataset == "D3").astype(int)
    print(f"rows {len(df):,}  valid {len(d0):,}", flush=True)

    o = run_glmm(d0)
    for c in ("messages",):
        o[c] = o[c].fillna("").astype(str)

    # GLMM ai:ps por fit (E pooled, F por modo) + cluster-robust equivalente
    plan = [("pooled", "E_ai_ps", MODES)] + [(m, f"F_{m}_vs_ctl", [m]) for m in MODES]
    recs = []
    for label, key, modes in plan:
        g = o[(o.fit == key) & (o.term == "ai:ps")]
        gb, gse, sing = (np.nan, np.nan, False)
        if not g.empty:
            r = g.iloc[0]
            gb, gse = float(r.estimate), float(r.se)
            sing = bool(r.singular) if not pd.isna(r.singular) else False
        cr = cr_did(d0, modes)
        cb, cse = (np.nan, np.nan) if cr is None else cr
        recs.append(dict(fit=label, glmm_logOR=gb, glmm_se=gse, glmm_lo=gb - 1.96 * gse,
                         glmm_hi=gb + 1.96 * gse, glmm_singular=sing,
                         cr_logOR=cb, cr_se=cse, cr_lo=cb - 1.96 * cse, cr_hi=cb + 1.96 * cse,
                         diff=gb - cb))
    comp = pd.DataFrame(recs)
    comp.to_csv(OUT_CSV, index=False)

    print("\n== DiD fig4 (parte especifica de poder): log-OR ai:ps = modo-vs-control ==")
    print(f"{'fit':8s}{'GLMM logOR':>12s}{'  IC95%':>16s}{'CLUSTER logOR':>15s}{'  IC95%':>16s}{'  Δ':>7s}")
    for _, x in comp.iterrows():
        print(f"{x['fit']:8s}{x['glmm_logOR']:>+12.3f}  [{x['glmm_lo']:+.2f},{x['glmm_hi']:+.2f}]"
              f"{x['cr_logOR']:>+13.3f}  [{x['cr_lo']:+.2f},{x['cr_hi']:+.2f}]{x['diff']:>+7.3f}"
              f"{'  (singular)' if x['glmm_singular'] else ''}")
    print(f"\nmax |Δ log-OR| = {comp['diff'].abs().max():.3f}")

    # ---- figura
    order = ["pooled", "he", "de", "pg"]
    comp = comp.set_index("fit").loc[order].reset_index()
    fig, ax = plt.subplots(figsize=(10.5, 6))
    xs = np.arange(len(order))
    w = 0.36
    for i, which in enumerate(["glmm", "cr"]):
        off = (-0.5 + i) * w
        b = comp[f"{which}_logOR"].to_numpy()
        lo = comp[f"{which}_lo"].to_numpy()
        hi = comp[f"{which}_hi"].to_numpy()
        ax.bar(xs + off, b, width=w, facecolor=FILL[which], edgecolor=COL[which], lw=1.6,
               alpha=0.9, zorder=2,
               label="GLMM (efectos aleatorios)" if which == "glmm" else "Cluster-robust (actual)")
        ax.errorbar(xs + off, b, yerr=[b - lo, hi - b], fmt="none", ecolor=COL[which],
                    elinewidth=1.9, capsize=4, zorder=5)
    ax.axhline(0, color="#333", lw=1.1)
    ax.set_xticks(xs)
    ax.set_xticklabels([MNAME[m] for m in order], fontsize=10.5, fontweight="bold")
    ax.set_ylabel("DiD  ·  log-OR (modo − control) del sesgo agente-IA", fontsize=11.5)
    ax.grid(axis="y", ls=":", alpha=0.4)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    sec = ax.secondary_yaxis("right", functions=(np.exp, np.log))
    sec.set_ylabel("ratio de OR", fontsize=11)
    sec.set_yticks([1, 1.25, 1.5, 2])
    ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    fig.suptitle("Figura 4 · DiD (parte específica de poder) — GLMM vs cluster-robust (IC95%)",
                 fontsize=12.5, y=0.97)
    fig.text(0.02, 0.01, "ai:ps > 0 ⇒ el sesgo agente-IA es mayor en el modo de poder que en el control · "
             "misma muestra en ambos · GLMM: refuse ~ ai*ps + (1+ai+ai:ps||model) + (1|prompt_id)",
             ha="left", fontsize=8.0, color="#555")
    fig.subplots_adjust(top=0.9, bottom=0.12)
    fig.savefig(OUT_PNG, dpi=140, bbox_inches="tight")
    print(f"\nsaved {OUT_PNG}\nsaved {OUT_CSV}")


if __name__ == "__main__":
    main()
