#!/usr/bin/env python3
"""Bloque 47 — Índice geopolítico en 1D: curva principal sobre los dos ejes (axis_us, axis_cn).
Pedido de Nico (18/09), textual: "nuestro índice geopolítico tiene 2 dimensiones. Pero hay una covarianza muy grande entre
ambas. Quiero que antes que nada vayas a buscar los datos y el gráfico en el que se basa ese índice, y veas si podés calcular
un subespacio 1D no lineal en el que proyectar los puntos para crear esta versión 1D del índice, que vaya de -1 a 1 entre los
extremos del subespacio. Si lo lográs, mostrámelo ese subespacio sobre el gráfico original, tendría que verse como una línea
que vive siguiendo la tendencia de los datos."

Datos: 1_create_dataset/nationality/geopolitics/alignment_axes.csv (186 países; axis_P = compromiso − hostilidad con la
potencia P; net_lean_us = axis_us − axis_cn es el índice 1D lineal que se usó para armar las bolsas de D2).
Método: curva principal de Hastie & Stuetzle (princurve::principal_curve en R, suavizador smooth.spline, arranque en la
primera componente principal; r/principal_curve.R). Cada país se proyecta sobre la curva; su posición en longitud de arco
(lambda) se reescala linealmente a [−1, +1] entre los dos extremos de la curva y se orienta con +1 del lado de USA.
Se ajusta con df = 4, 5 y 6; el índice principal usa df = 5 (el valor por defecto de princurve); los otros dos quedan
como sensibilidad. Decisiones de implementación de Claude (a revisar): el método (curva principal), df = 5, reescalado
lineal en longitud de arco entre los extremos observados, orientación.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_47_alignment_index_1d.py     (segundos; requiere Rscript + princurve)
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (str(HERE), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import TwoSlopeNorm  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "47_alignment_index_1d"
AXES_CSV = ROOT / "1_create_dataset" / "nationality" / "geopolitics" / "alignment_axes.csv"
POOLS_CSV = HERE / "results" / "27_fig3_notelab" / "country_pools.csv"
R_SCRIPT = HERE / "r" / "principal_curve.R"
R_LIB = Path.home() / "R" / "win-library" / "4.6"
DFS = (4, 5, 6)
DF_MAIN = 5
NL = chr(10)


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "savefig.facecolor": "white"})


def find_rscript() -> str:
    exe = shutil.which("Rscript")
    if exe:
        return exe
    cands = sorted(glob.glob("C:/Program Files/R/R-*/bin/Rscript.exe"))
    if not cands:
        sys.exit("Rscript no encontrado.")
    return cands[-1]


def main():
    style()
    a = pd.read_csv(AXES_CSV, encoding="utf-8-sig")
    pools = pd.read_csv(POOLS_CSV).drop_duplicates(["user_iso3", "geo_pool"])
    pool_of = {}
    for r in pools.itertuples():
        if r.geo_pool in ("ally_of_us", "ally_of_china", "neutral"):
            pool_of[r.user_iso3] = r.geo_pool
    a["d2_pool"] = a.iso3.map(pool_of).fillna("")

    rscript = find_rscript()
    with tempfile.TemporaryDirectory() as tmp:
        fin, fout = Path(tmp) / "axes.csv", Path(tmp) / "curve.csv"
        a[["iso3", "axis_us", "axis_cn"]].to_csv(fin, index=False)
        env = dict(os.environ)
        if R_LIB.is_dir():
            env["R_LIBS_USER"] = str(R_LIB)
        proc = subprocess.run([rscript, str(R_SCRIPT), str(fin), str(fout), ",".join(str(d) for d in DFS)], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=env)
        print(proc.stdout, flush=True)
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr); sys.exit(f"Rscript terminó con código {proc.returncode}")
        cv = pd.read_csv(fout)

    # reescalado a [−1, +1] entre los extremos y orientación (+1 del lado de USA)
    idx = {}
    for df, g in cv.groupby("df"):
        g = g.set_index("iso3").loc[a.iso3]
        lam = g["lambda"].to_numpy(float)
        if np.corrcoef(lam, a.axis_us.to_numpy(float))[0, 1] < 0:
            lam = -lam
        # Escala (decisión de Nico, 18/09): cero en la MEDIANA de los países, extremos asimétricos. Implementación de Claude
        # (a revisar): (lambda − mediana) / max |lambda − mediana|, así el extremo más lejano vale ±1 y el otro queda más cerca de 0.
        # La escala anterior (−1 y +1 en los dos extremos, cero en el medio de la curva) queda en index_1d_extremes_df*.
        cen = lam - np.median(lam)
        idx[df] = cen / np.abs(cen).max()
        a[f"index_1d_df{df}"] = idx[df]; a[f"dist_df{df}"] = g["dist_point"].to_numpy(float)
        a[f"index_1d_extremes_df{df}"] = 2 * (lam - lam.min()) / (lam.max() - lam.min()) - 1
        if df == DF_MAIN:
            a["s_us"], a["s_cn"], a["lambda"] = g["s_us"].to_numpy(float), g["s_cn"].to_numpy(float), lam
    a["index_1d"] = a[f"index_1d_df{DF_MAIN}"]
    a["dist_to_curve"] = a[f"dist_df{DF_MAIN}"]
    conv = cv.drop_duplicates("df").set_index("df")[["converged", "iterations", "total_dist"]]
    a["index_1d_extremes"] = a[f"index_1d_extremes_df{DF_MAIN}"]
    out_cols = ["iso3", "name", "axis_us", "axis_cn", "net_lean_us", "cuadrante", "d2_pool", "index_1d", "index_1d_extremes", "lambda", "s_us", "s_cn", "dist_to_curve"] + \
               [f"index_1d_df{d}" for d in DFS if d != DF_MAIN]
    table = a[out_cols].sort_values("index_1d", ascending=False).reset_index(drop=True)
    corr = {f"df{d}": float(np.corrcoef(idx[d], a.net_lean_us)[0, 1]) for d in DFS}
    corr_sp = {f"df{d}": float(pd.Series(idx[d]).corr(a.net_lean_us, method="spearman")) for d in DFS}
    corr_df = {f"df{d}_vs_df{DF_MAIN}": float(np.corrcoef(idx[d], idx[DF_MAIN])[0, 1]) for d in DFS if d != DF_MAIN}

    res = report.Result(
        NAME, "Índice geopolítico en 1D: curva principal sobre los dos ejes de alineamiento",
        "¿Se puede reemplazar el índice de dos ejes (compromiso con USA, compromiso con China; correlación −0,70) por una posición sobre una "
        "curva 1D que siga la tendencia de los datos, reescalada a [−1, +1] entre los extremos?",
        status="computado a pedido de Nico (18/09); método y parámetros a revisar")
    res.inputs([str(AXES_CSV), str(POOLS_CSV), str(R_SCRIPT)])
    res.data("186 países con los dos ejes completos (build_alignment_axes.py, datos 2022–2025); USA y China no tienen índice. d2_pool marca "
             "los países de las bolsas de D2 (aliados de USA, aliados de China, neutrales; 21 + 21 + 21 usados en el banco).")
    res.method(f"princurve::principal_curve (Hastie & Stuetzle), smooth.spline con df = {DFS}, stretch = 2, arranque en la primera componente "
               f"principal. Índice (decisión de Nico, 18/09: cero en la mediana, extremos asimétricos) = (lambda − mediana de lambda) / max |lambda − "
               f"mediana|, orientado con el lado USA positivo: el extremo más lejano de la mediana vale ±1 y el otro queda más cerca de 0. La escala "
               f"anterior (−1 y +1 en los dos extremos) queda en index_1d_extremes. Principal: df = {DF_MAIN}; los otros df quedan como sensibilidad. Convergencia: " +
               "; ".join(f"df {d}: {'sí' if bool(conv.loc[d, 'converged']) else 'NO'} en {int(conv.loc[d, 'iterations'])} iteraciones" for d in DFS) + ".")
    res.table("alignment_index_1d", table, "Índice 1D por país (df = 5; cero en la mediana), la versión con cero en el medio de la curva (index_1d_extremes), los dos ejes, el índice lineal net_lean_us, el cuadrante, la bolsa "
              "de D2, la proyección sobre la curva (s_us, s_cn), la distancia a la curva y los índices con df = 4 y 6.", show=False)
    for k, v in corr.items():
        res.stat(f"pearson_index1d_{k}_vs_net_lean", v, unit="r")
    for k, v in corr_sp.items():
        res.stat(f"spearman_index1d_{k}_vs_net_lean", v, unit="rho")
    for k, v in corr_df.items():
        res.stat(f"pearson_{k}", v, unit="r")

    # ------------------------------------------------------------------ figura 1: la curva sobre el gráfico original
    norm = TwoSlopeNorm(vmin=float(a.index_1d.min()), vcenter=0, vmax=float(a.index_1d.max()))
    fig, ax = plt.subplots(figsize=(11, 8.2), layout="constrained")
    curve = a.sort_values("lambda")
    for r in a.itertuples():
        ax.plot([r.axis_us, r.s_us], [r.axis_cn, r.s_cn], color="#999999", lw=.5, alpha=.5, zorder=1)
    ax.plot(curve.s_us, curve.s_cn, color="#111111", lw=2.6, zorder=3, label=f"curva principal (df = {DF_MAIN})")
    edge = np.where(a.d2_pool != "", "black", "#666666")
    sc = ax.scatter(a.axis_us, a.axis_cn, c=a.index_1d, cmap="RdBu", norm=norm, s=46, edgecolors=edge, linewidths=np.where(a.d2_pool != "", 1.2, .4), zorder=4)
    lab = a[(a.index_1d_extremes.abs() > .55) | a.iso3.isin(["IND", "TUR", "BRA", "ZAF", "IDN", "PAK", "THA", "KHM", "VNM", "UKR", "HUN", "SAU", "MEX", "ARG"])]
    for r in lab.itertuples():
        ax.annotate(r.iso3, (r.axis_us, r.axis_cn), xytext=(4, 3), textcoords="offset points", fontsize=7, color="#333")
    ax.axhline(0, color="#bbb", lw=.8); ax.axvline(0, color="#bbb", lw=.8)
    ax.set_xlabel("Eje EEUU = compromiso (votos ONU + seguridad + comercio) − hostilidad")
    ax.set_ylabel("Eje China = compromiso (votos ONU + seguridad + comercio) − hostilidad")
    cb = fig.colorbar(sc, ax=ax, shrink=.7, pad=.02); cb.set_label("índice 1D: posición sobre la curva, 0 = mediana de países; −1 = extremo China; lado USA hasta %+.2f" % a.index_1d.max())
    ax.legend(frameon=False, loc="upper right")
    ax.text(.01, .01, "borde negro = país de una bolsa de D2 (aliado de USA, aliado de China o neutral) · segmentos grises = proyección de cada país sobre la curva",
            transform=ax.transAxes, fontsize=8, color="#555", va="bottom")
    ax.set_title("Alineamiento con EEUU y con China, 186 países · subespacio 1D: curva principal que sigue la tendencia", fontsize=11)
    res.figure("p1_principal_curve_on_scatter", fig,
               "El gráfico original de los dos ejes (build_alignment_axes.py) con la curva principal encima (línea negra) y la proyección de cada "
               "país sobre ella (segmento gris). El color es el índice 1D nuevo: la posición sobre la curva reescalada a [−1, +1] entre los dos "
               "extremos (versión de la mañana del 18/09); desde la tarde del 18/09, por decisión de Nico, el cero está en la mediana de los "
               "países y los extremos son asimétricos (el más lejano, Corea del Norte, vale −1). Borde negro: países de las bolsas de D2.")

    # ------------------------------------------------------------------ figura 2: diagnóstico (sensibilidad a df; índice nuevo contra el lineal; bolsas)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2), layout="constrained")
    ax = axes[0]
    ax.scatter(a.axis_us, a.axis_cn, s=14, color="#BBBBBB", zorder=1)
    for df, col in zip(DFS, ("#E08A2E", "#111111", "#2E7DE0")):
        g = cv[cv.df == df].sort_values("lambda")
        ax.plot(g.s_us, g.s_cn, color=col, lw=2 if df == DF_MAIN else 1.4, label=f"df = {df}" + (" (principal)" if df == DF_MAIN else ""), zorder=2)
    ax.legend(frameon=False, fontsize=9); ax.set_xlabel("eje EEUU"); ax.set_ylabel("eje China"); ax.set_title("Sensibilidad al suavizado", fontsize=10.5)
    ax = axes[1]
    ax.scatter(a.net_lean_us, a.index_1d, s=18, c=np.where(a.d2_pool == "ally_of_us", "#326CA0", np.where(a.d2_pool == "ally_of_china", "#B44941",
               np.where(a.d2_pool == "neutral", "#777C83", "#CCCCCC"))), zorder=2)
    ax.set_xlabel("índice lineal usado para las bolsas: net_lean_us = eje EEUU − eje China"); ax.set_ylabel("índice 1D nuevo (curva principal)")
    ax.set_title(f"Nuevo contra lineal · r = {corr[f'df{DF_MAIN}']:.3f}, ρ = {corr_sp[f'df{DF_MAIN}']:.3f}", fontsize=10.5); ax.grid(alpha=.15)
    ax = axes[2]
    rng = np.random.default_rng(47)
    for k, (pool, col, lab_) in enumerate((("ally_of_china", "#B44941", "aliados de China"), ("neutral", "#777C83", "neutrales"), ("ally_of_us", "#326CA0", "aliados de USA"))):
        v = a[a.d2_pool == pool].index_1d
        ax.scatter(v, k + rng.uniform(-.18, .18, len(v)), s=22, color=col, zorder=2)
        ax.text(v.mean(), k + .38, f"media {v.mean():+.2f}  [{v.min():+.2f}; {v.max():+.2f}]", ha="center", fontsize=8.5, color=col)
    ax.set_yticks(range(3), ["aliados de China", "neutrales", "aliados de USA"]); ax.set_xlim(-1.05, 1.05); ax.axvline(0, color="#bbb", lw=.8)
    ax.text(.02, .97, "0 = mediana de los 186 países", transform=ax.transAxes, fontsize=8.5, color="#555", va="top")
    ax.set_xlabel("índice 1D nuevo"); ax.set_title("Las tres bolsas de D2 sobre el índice nuevo", fontsize=10.5)
    res.figure("p2_diagnostics", fig, "Izquierda: curvas con df = 4, 5, 6. Centro: índice nuevo contra el lineal (colores = bolsas de D2). Derecha: "
               "posición de los países de las tres bolsas de D2 sobre el índice nuevo.")
    res.note("Registro: 4_analysis/results/27_fig3_notelab/NARRATIVA_F3.md; decisiones a revisar: 4_analysis/results/DECISIONES_A_REVISAR.md.")
    res.conclusion("Índice 1D calculado; método y parámetros pendientes de decisión de Nico.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("correlación índice 1D vs net_lean_us:", {k: round(v, 3) for k, v in corr.items()}, {k: round(v, 3) for k, v in corr_sp.items()})
    print("correlación entre df:", {k: round(v, 4) for k, v in corr_df.items()})
    print(table.head(8)[["iso3", "name", "axis_us", "axis_cn", "net_lean_us", "index_1d", "dist_to_curve"]].round(3).to_string(index=False))
    print(table.tail(8)[["iso3", "name", "axis_us", "axis_cn", "net_lean_us", "index_1d", "dist_to_curve"]].round(3).to_string(index=False))
    print("wrote", out)


if __name__ == "__main__":
    main()
