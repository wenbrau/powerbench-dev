#!/usr/bin/env python3
"""Panel B, receta de solo permutación (20/09, pedido de Wendy): estrellas y banda salen del MISMO test, sin t ni bootstrap.

Por modo (he, de, pg, control) y juego de pesos (igual = 1/24; uso = share_requests de OpenRouter, bloque 72):
1. Por modelo, rango observado = max − min del logit suavizado de R(idioma) sobre la matriz 192 prompts × idiomas
   (nemotron-3.5-lightning y nova-2-lite sin swahili). Igual que el bloque 35.
2. Por modelo, NPERM rangos de azar: se barajan los idiomas dentro de cada prompt y se recalcula el rango. La varianza de
   cada modelo (refusal bajo → rango de azar disperso) queda en esos NPERM números.
3. Se combinan los 24 modelos: observado = Σ w·rango_m; y para cada permutación k, nulo_k = Σ w·rango_m,k.
4. De los NPERM valores nulo_k: azar = media; barra = exp(observado − azar) (OR); banda = exp(percentil 2.5 − azar),
   exp(percentil 97.5 − azar), alrededor de 1; p = (1 + #{nulo_k ≥ observado}) / (NPERM + 1). Estrellas * .05 ** .01 *** .001.
Sin API. Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_languages/panelB/panelB_permutation.py  (--plot-only rehace la figura)
"""
from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for p in (str(ROOT / "4_analysis"), str(ROOT / "common"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis.final_panel import load_d1_multilingual, MODES  # noqa: E402
from panelB_weighted_requests import range_logodds, shuffled, stars, LANGS, EXCL_SW, LABELS, MODE_COLORS, WEIGHTS  # noqa: E402

NPERM, SEED = 2000, 35
OUT_CSV = HERE / "panelB_permutation.csv"
OUT_PNG = HERE / "panelB_permutation.png"


def main():
    t0 = time.time()
    df = load_d1_multilingual()
    d = df[df.valid].copy(); d["refuse"] = d.refuse.astype(float)
    meta = d.drop_duplicates("model").set_index("model").origin
    models = sorted(meta.index, key=lambda m: (meta[m] != "US", m))
    w_use = pd.read_csv(WEIGHTS).set_index("model").share_requests.reindex(models)
    assert w_use.notna().all(), "modelos sin peso"
    weights = {"eq": np.full(len(models), 1 / len(models)), "use": (w_use / w_use.sum()).to_numpy()}
    rng = np.random.default_rng(SEED)

    rows, per_model = [], []
    for mode in MODES:
        dm = d[d["mode"] == mode]
        obs, perm = [], []
        for m in models:
            langs = [l for l in LANGS if not (l == "sw" and m in EXCL_SW)]
            M = dm[dm.model == m].pivot(index="prompt_id", columns="lang", values="refuse").reindex(columns=langs).to_numpy(float)
            assert M.shape[0] == 192
            obs.append(range_logodds(M)); perm.append(range_logodds(shuffled(M, NPERM, rng)))
            per_model.append(dict(mode=mode, model=m, origin=meta[m], share_requests=weights["use"][len(obs) - 1], n_langs=M.shape[1],
                                  range_or=np.exp(obs[-1]), null_or=np.exp(perm[-1].mean()), null_sd_logodds=perm[-1].std(),
                                  excess_or=np.exp(obs[-1] - perm[-1].mean())))
        obs = np.array(obs); perm = np.stack(perm, axis=1)                                   # (NPERM, 24)
        for wname, w in weights.items():
            o = float(np.sum(w * obs)); null = np.sum(perm * w, axis=1)                        # 2000 valores del estadístico bajo H0
            az = float(null.mean()); lo, hi, p95 = np.percentile(null, [2.5, 97.5, 95])
            p = (1 + int(np.sum(null >= o))) / (NPERM + 1)
            rows.append(dict(mode=mode, weights=wname, n_models=len(models), n_perm=NPERM, observed=o, null_mean=az, null_sd=float(null.std()),
                             null_p2_5=lo, null_p97_5=hi, null_p95=p95, null_max=float(null.max()), half95=p95 - az, excess=o - az, band_lo=lo - az, band_hi=hi - az, p_perm=p,
                             stars=stars(p), excess_or=np.exp(o - az), band_lo_or=np.exp(lo - az), band_hi_or=np.exp(hi - az),
                             bar_lo_or=np.exp(o - az - (p95 - az)), bar_hi_or=np.exp(o - az + (p95 - az))))
            r = rows[-1]
            print(f"{mode:8s} {wname:4s} OR {r['excess_or']:.2f} banda [{r['band_lo_or']:.3f}, {r['band_hi_or']:.3f}] p {p:.4f} {r['stars']:3s} · "
                  f"obs {o:.3f} azar {az:.3f} max nulo {r['null_max']:.3f} · {time.time() - t0:.0f}s", flush=True)

    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)
    pd.DataFrame(per_model).to_csv(HERE / "panelB_permutation_per_model.csv", index=False)
    plot()


def plot():
    tab = pd.read_csv(OUT_CSV).set_index(["mode", "weights"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "axes.titlelocation": "left", "savefig.facecolor": "white"})
    x = np.arange(len(MODES)); wb = .38
    fig, ax = plt.subplots(figsize=(9.5, 6), layout="constrained")
    for wname, off, alpha, lab in (("eq", -wb / 2, .4, "peso igual por modelo"), ("use", wb / 2, 1.0, "peso por uso (requests)")):
        t = tab.xs(wname, level="weights").loc[list(MODES)]
        col = [MODE_COLORS[m] for m in MODES]
        ax.bar(x + off, t.excess_or - 1, bottom=1, width=wb, color=col, alpha=alpha, label=lab, zorder=2)
        for xi, m in zip(x, MODES):
            r = t.loc[m]
            ax.text(xi + off, r.excess_or * 1.03, r.stars if isinstance(r.stars, str) else "", ha="center", va="bottom", fontsize=13)
    ax.axhline(1, color="k", lw=.9, ls="--", zorder=1)
    ax.set_yscale("log"); ax.set_yticks([.5, .7, 1, 1.5, 2, 3, 4]); ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_ylim(min(.85, tab.excess_or.min() * .92), tab.excess_or.max() * 1.3)
    ax.set_ylabel("exceso del rango entre idiomas sobre el azar, OR\n(rango observado / rango con idiomas barajados)")
    ax.set_xticks(x, [LABELS[m] for m in MODES], fontsize=10); ax.grid(axis="y", alpha=.15)
    ax.legend(fontsize=9, frameon=False, loc="upper right")
    ax.set_title(f"Panel B, solo permutación · 24 modelos · {NPERM} permutaciones de idiomas dentro del prompt\n"
                 "barra = observado / azar · estrellas: permutación · * p < 0.05  ** p < 0.01  *** p < 0.001",
                 fontsize=9.5)
    fig.savefig(OUT_PNG, dpi=170)
    print("wrote", OUT_PNG)


if __name__ == "__main__":
    plot() if "--plot-only" in sys.argv[1:] else main()
