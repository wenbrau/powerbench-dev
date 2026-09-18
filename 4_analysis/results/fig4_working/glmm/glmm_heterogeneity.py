#!/usr/bin/env python3
"""Figura 4 -- HETEROGENEIDAD del DiD (parte especifica de poder) con GLMM, subcarpeta glmm/.

Pregunta (conclusiones #6/#7 de METHODS.md): la parte del sesgo agente-IA que es especifica de poder
-- DiD = (sesgo D3 vs D1 en el modo) - (sesgo en el control) -- se concentra en ciertos niveles?
Individual/Society segun el modo, standing Low, domain Legal/Physical, context Government/Academia.

Aca se recomputa el DiD DENTRO de cada nivel de scale/standing/context/domain con un GLMM
(refuse ~ ai*ps + (1+ai+ai:ps||model) + (1|prompt_id), termino ai:ps), para LOS TRES MODOS de poder
(he, de, pg). Gemelo por efectos aleatorios de fig4_did_by_dimension (que usa el DiD por modelo con
t de Student). Pooled US+CN.

El control tiene scale/standing/context pero NO domain -> en scale/standing/context el control se
matchea por nivel; en domain se usa el control GLOBAL (broadcast), igual que fig4_did_by_dimension.

NO decide nada: recomputa un corte existente con otro estimador. Ejecutar desde la raiz:
  python 4_analysis/results/fig4_working/glmm/glmm_heterogeneity.py [--mode all|pg|de|he]
Requiere Rscript con lme4.
"""
from __future__ import annotations

import argparse
import glob
import shutil
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
A4 = HERE.parent.parent.parent  # 4_analysis/
ROOT = A4.parent
for p in (str(A4), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

import analysis_16_d3_panel24_control as a16  # noqa: E402

warnings.filterwarnings("ignore")

R_SCRIPT = HERE / "glmm_heterogeneity.R"
# dimensiones con cobertura en el control (matcheo por nivel) vs sin cobertura (broadcast del control global)
DIMS_MATCHED = {
    "scale": ["individual", "group", "society"],
    "standing": ["low", "med", "high"],
    "context": ["Academia", "Diplomacy", "Fiction", "Government", "Interpersonal", "Markets", "Media", "Work"],
}
DIMS_BROADCAST = {
    "domain": ["Rank", "Wealth", "Legal", "Physical", "Epistemic", "Status", "Attentional"],
}
DIMS = {**DIMS_MATCHED, **DIMS_BROADCAST}
MLAB = {"pg": "power-grabbing", "de": "disempowerment", "he": "self-empowerment"}


def find_rscript() -> str:
    exe = shutil.which("Rscript")
    if exe:
        return exe
    cands = sorted(glob.glob("C:/Program Files/R/R-*/bin/Rscript.exe"))
    if not cands:
        sys.exit("Rscript no encontrado: instalar R y lme4.")
    return cands[-1]


def run_glmm(dlong):
    """dlong: refuse, ai, ps, lev, prompt_id, model. Devuelve dict lev -> (b, se, p, sing) del ai:ps."""
    rscript = find_rscript()
    with tempfile.TemporaryDirectory() as tmp:
        fin, fout = Path(tmp) / "in.csv", Path(tmp) / "out.csv"
        dlong[["refuse", "ai", "ps", "lev", "prompt_id", "model"]].to_csv(fin, index=False)
        proc = subprocess.run([rscript, str(R_SCRIPT), str(fin), str(fout)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
            sys.exit(f"Rscript termino con codigo {proc.returncode}")
        o = pd.read_csv(fout)
    out = {}
    for lev, g in o[o.term == "ai:ps"].groupby("fit"):
        r = g.iloc[0]
        out[str(lev)] = (float(r.estimate), float(r.se), float(r.p),
                         bool(r.singular) if not pd.isna(r.singular) else False)
    return out


def build_long(mode_rows, ctrl_rows, dim, matched):
    """Arma el df largo (una fila por observacion, con lev y ps) para una dimension."""
    if matched:
        a = mode_rows.assign(ps=1, lev=mode_rows[dim].astype(str))
        b = ctrl_rows.assign(ps=0, lev=ctrl_rows[dim].astype(str))
        return pd.concat([a, b], ignore_index=True)
    # broadcast: para cada nivel del modo, ese nivel del modo + TODO el control
    parts = []
    for L in sorted(mode_rows[dim].dropna().astype(str).unique()):
        parts.append(mode_rows[mode_rows[dim].astype(str) == L].assign(ps=1, lev=L))
        parts.append(ctrl_rows.assign(ps=0, lev=L))
    return pd.concat(parts, ignore_index=True)


def analyze_mode(d0, mode):
    mode_rows = d0[d0["mode"] == mode].copy()
    ctrl_rows = d0[d0["mode"] == "ctl"].copy()

    # DiD global del modo (linea de referencia): modo entero + control entero, un solo nivel
    glob_long = pd.concat([mode_rows.assign(ps=1, lev="all"),
                           ctrl_rows.assign(ps=0, lev="all")], ignore_index=True)
    gd = run_glmm(glob_long).get("all")
    gb = gd[0] if gd else np.nan
    print(f"\n=== modo {mode} ===  DiD global (ai:ps) = {gb:+.3f}  ROR {np.exp(gb):.2f}", flush=True)

    results, recs = {}, []
    for dim, order in DIMS.items():
        matched = dim in DIMS_MATCHED
        dlong = build_long(mode_rows, ctrl_rows, dim, matched)
        res = run_glmm(dlong)
        levels = [L for L in order if L in res] + [L for L in res if L not in order]
        results[dim] = (levels, res, matched)
        print(f"  [{dim}]{'' if matched else '  (control broadcast)'}")
        for L in levels:
            b, se, p, sing = res[L]
            recs.append(dict(mode=mode, dimension=dim, level=L, matched=matched,
                             did_logOR=b, se=se, lo=b - 1.96 * se, hi=b + 1.96 * se,
                             p=p, singular=sing))
            print(f"    {L:14s} DiD {b:+.3f}  ROR {np.exp(b):.2f}  [{b-1.96*se:+.2f},{b+1.96*se:+.2f}]"
                  f"  p={p:.3g}{'  (sing)' if sing else ''}")

    comp = pd.DataFrame(recs)
    comp.to_csv(HERE / f"glmm_heterogeneity_did_{mode}.csv", index=False)
    make_fig(mode, results, gb, comp)
    return comp, results, gb


def make_fig(mode, results, gb, comp):
    fig, axes = plt.subplots(1, 4, figsize=(16, 5.6),
                             gridspec_kw={"width_ratios": [3, 3, 8, 7]})
    BAR, EDGE = "#4a7ba6", "#2f5570"
    for ax, dim in zip(axes, DIMS):
        levels, res, matched = results[dim]
        b = np.array([res[L][0] for L in levels])
        lo = np.array([res[L][0] - 1.96 * res[L][1] for L in levels])
        hi = np.array([res[L][0] + 1.96 * res[L][1] for L in levels])
        sig = np.array([(res[L][0] - 1.96 * res[L][1]) > 0 or (res[L][0] + 1.96 * res[L][1]) < 0
                        for L in levels])
        xs = np.arange(len(levels))
        bars = ax.bar(xs, b, width=0.72, facecolor=BAR, edgecolor=EDGE, lw=1.4, zorder=2)
        for patch, s in zip(bars.patches, sig):
            patch.set_alpha(0.95 if s else 0.4)
        ax.errorbar(xs, b, yerr=[b - lo, hi - b], fmt="none", ecolor=EDGE, elinewidth=1.6,
                    capsize=3, zorder=5)
        if not np.isnan(gb):
            ax.axhline(gb, color="#b24747", lw=1.4, ls="--", zorder=1,
                       label=f"DiD global ({gb:+.2f})")
        ax.axhline(0, color="#333", lw=1.0)
        ax.set_xticks(xs)
        ax.set_xticklabels(levels, rotation=45, ha="right", fontsize=9)
        ax.set_title(dim + ("" if matched else " *"), fontsize=11.5, fontweight="bold")
        ax.grid(axis="y", ls=":", alpha=0.4)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.legend(loc="upper right", fontsize=8, frameon=False)
    axes[0].set_ylabel("DiD  ·  log-OR (modo − control) del sesgo agente-IA", fontsize=10.5)
    ymax = max(comp["hi"].max(), gb) + 0.15
    ymin = min(comp["lo"].min(), 0) - 0.1
    for ax in axes:
        ax.set_ylim(ymin, ymax)
    fig.suptitle(f"Figura 4 · heterogeneidad del DiD (parte específica de poder) en {MLAB[mode]} — "
                 f"GLMM (IC95%; barra tenue = cruza 0; * = control global)", fontsize=12, y=0.99)
    fig.text(0.01, 0.005, "refuse ~ ai*ps + (1+ai+ai:ps||model) + (1|prompt_id) por nivel · "
             "ai:ps > 0 ⇒ sesgo agente-IA mayor que en el control · línea = DiD global del modo",
             ha="left", fontsize=7.8, color="#555")
    fig.subplots_adjust(top=0.88, bottom=0.2, wspace=0.25, left=0.06, right=0.99)
    out = HERE / f"glmm_heterogeneity_did_{mode}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {out}")


def make_combined_fig(per_mode, order_modes):
    """per_mode[mode] = (results, gb). Grilla: una fila por modo, una columna por dimension."""
    nrow = len(order_modes)
    fig, axes = plt.subplots(nrow, 4, figsize=(16, 4.2 * nrow), squeeze=False,
                             gridspec_kw={"width_ratios": [3, 3, 8, 7]})
    BAR, EDGE = "#4a7ba6", "#2f5570"
    # rango y comun (min/max de todos los IC de todas las celdas)
    allv = []
    for results, _ in per_mode.values():
        for dim in DIMS:
            levels, res, _ = results[dim]
            for L in levels:
                b, se = res[L][0], res[L][1]
                allv += [b - 1.96 * se, b + 1.96 * se]
    ymax, ymin = max(allv) + 0.15, min(min(allv), 0) - 0.1
    for ri, mode in enumerate(order_modes):
        results, gb = per_mode[mode]
        for ci, dim in enumerate(DIMS):
            ax = axes[ri][ci]
            levels, res, matched = results[dim]
            b = np.array([res[L][0] for L in levels])
            lo = np.array([res[L][0] - 1.96 * res[L][1] for L in levels])
            hi = np.array([res[L][0] + 1.96 * res[L][1] for L in levels])
            sig = [(res[L][0] - 1.96 * res[L][1]) > 0 or (res[L][0] + 1.96 * res[L][1]) < 0 for L in levels]
            xs = np.arange(len(levels))
            bars = ax.bar(xs, b, width=0.72, facecolor=BAR, edgecolor=EDGE, lw=1.3, zorder=2)
            for patch, s in zip(bars.patches, sig):
                patch.set_alpha(0.95 if s else 0.4)
            ax.errorbar(xs, b, yerr=[b - lo, hi - b], fmt="none", ecolor=EDGE, elinewidth=1.5,
                        capsize=2.5, zorder=5)
            if not np.isnan(gb):
                ax.axhline(gb, color="#b24747", lw=1.3, ls="--", zorder=1)
            ax.axhline(0, color="#333", lw=1.0)
            ax.set_ylim(ymin, ymax)
            ax.set_xticks(xs)
            ax.grid(axis="y", ls=":", alpha=0.4)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            if ri == 0:
                ax.set_title(dim + ("" if matched else " *"), fontsize=12, fontweight="bold")
            if ri == nrow - 1:
                ax.set_xticklabels(levels, rotation=45, ha="right", fontsize=8.5)
            else:
                ax.set_xticklabels([])
            if ci == 0:
                ax.set_ylabel(f"{MLAB[mode]}\n(DiD global {gb:+.2f})", fontsize=10.5, fontweight="bold")
    fig.suptitle("Figura 4 · heterogeneidad del DiD (parte específica de poder) por modo — GLMM "
                 "(IC95%; barra tenue = cruza 0; línea roja = DiD global del modo; * = control global)",
                 fontsize=12.5, y=0.995)
    fig.text(0.005, 0.005, "refuse ~ ai*ps + (1+ai+ai:ps||model) + (1|prompt_id) por nivel · "
             "ai:ps > 0 ⇒ sesgo agente-IA mayor que en el control", ha="left", fontsize=7.8, color="#555")
    fig.subplots_adjust(top=1 - 0.5 / (4.2 * nrow) - 0.02, bottom=0.09, wspace=0.22, hspace=0.12,
                        left=0.07, right=0.99)
    out = HERE / "glmm_heterogeneity_did_combined.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"\nsaved {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="all", choices=["all", "pg", "de", "he"])
    args = ap.parse_args()

    df = a16.load()
    d0 = df[df.valid].copy()
    d0["refuse"] = d0.refuse.astype(int)
    d0["ai"] = (d0.dataset == "D3").astype(int)
    print(f"rows {len(df):,}  valid {len(d0):,}", flush=True)

    modes = ["he", "de", "pg"] if args.mode == "all" else [args.mode]
    per_mode = {}
    for m in modes:
        _, results, gb = analyze_mode(d0, m)
        per_mode[m] = (results, gb)
    if len(modes) > 1:
        make_combined_fig(per_mode, modes)


if __name__ == "__main__":
    main()
