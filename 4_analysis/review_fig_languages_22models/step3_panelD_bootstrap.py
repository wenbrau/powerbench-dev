#!/usr/bin/env python3
"""Paso 3 — panel D: la receta final del 20/09 (review_fig_languages/panelB/panelB_bootstrap.py) sobre los 22 modelos.
Por modo y ponderación (igual = 1/22; uso = share_requests del bloque 72 renormalizada sobre los 22): exceso del rango del logit de
R(idioma) sobre el azar (idiomas barajados dentro del prompt, 2.000 permutaciones); bootstrap sobre prompts (B = 4.000, pivotal), el
mismo para las dos barras; p por inversión del IC; BH dentro de cada ponderación (familia = 4 modos). Mismas funciones importadas.
Salida: panelD_bootstrap.csv (mismas columnas que panelB_bootstrap.csv), panelD_bootstrap_per_model.csv, panelD_bootstrap_draws.npz.
≈ 15 min.   --rescore: recalcula p, q y estrellas desde las réplicas guardadas."""
import sys
import time

import numpy as np
import pandas as pd

from _common import HERE, MODES, LANGS, WEIGHTS, load22, write_provenance
import panelB_bootstrap as pb                      # review_fig_languages/panelB (en sys.path por _common)
from panelB_weighted_requests import range_logodds, shuffled

B, NPERM, NPERM_BOOT, SEED, LEVELS = pb.B, pb.NPERM, pb.NPERM_BOOT, pb.SEED, pb.LEVELS
OUT_CSV, OUT_BOOT = HERE / "panelD_bootstrap.csv", HERE / "panelD_bootstrap_draws.npz"


def rescore():
    z = np.load(OUT_BOOT); draws = {m: z[m] for m in MODES}
    tab = pd.read_csv(OUT_CSV); tab = tab.drop(columns=[c for c in ("p_boot", "bh_family", "q_bh", "stars_raw", "stars") if c in tab.columns])
    tab = pb.score(tab, draws); tab.to_csv(OUT_CSV, index=False)
    for _, r in tab.iterrows():
        print(f"{r['mode']:8s} {r.weights:4s} OR {r.excess_bc_or:.2f} [{r.lo95_or:.2f}, {r.hi95_or:.2f}] p {r.p_boot:.4f} q {r.q_bh:.4f} {r.stars_raw:3s} -> {r.stars:3s}")


def main():
    t0 = time.time()
    d, inputs = load22()
    meta = d.drop_duplicates("model").set_index("model").origin
    models = sorted(meta.index, key=lambda m: (meta[m] != "US", m))
    w_use = pd.read_csv(WEIGHTS).set_index("model").share_requests.reindex(models)
    assert w_use.notna().all(), "modelos sin peso"
    weights = {"eq": np.full(len(models), 1 / len(models)), "use": (w_use / w_use.sum()).to_numpy()}
    print(f"filas válidas {len(d):,} · modelos {len(models)} · n efectivo pesos por uso {1 / np.sum(weights['use'] ** 2):.1f} · B {B}", flush=True)
    mats = {}
    for mode in MODES:
        dm = d[d["mode"] == mode]
        for m in models:
            mats[(mode, m)] = dm[dm.model == m].pivot(index="prompt_id", columns="lang", values="refuse").reindex(columns=LANGS).to_numpy(float)
            assert mats[(mode, m)].shape == (192, 8)
    rng = np.random.default_rng(SEED)
    rows, per_model, draws = [], [], {}
    for mode in MODES:
        obs = np.array([range_logodds(mats[(mode, m)]) for m in models])
        null = np.array([range_logodds(shuffled(mats[(mode, m)], NPERM, rng)).mean() for m in models])
        exc = obs - null
        for i, m in enumerate(models):
            per_model.append(dict(mode=mode, model=m, origin=meta[m], share_requests=weights["use"][i], n_langs=8,
                                  range_or=np.exp(obs[i]), null_or=np.exp(null[i]), excess_or=np.exp(exc[i])))
        boot = np.empty((B, len(weights)))
        for b in range(B):
            idx = rng.integers(0, 192, 192)
            eb = np.empty(len(models))
            for i, m in enumerate(models):
                Mb = mats[(mode, m)][idx]
                eb[i] = range_logodds(Mb) - range_logodds(shuffled(Mb, NPERM_BOOT, rng)).mean()
            boot[b] = [np.sum(w * eb) for w in weights.values()]
            if b % 500 == 0:
                print(f"  {mode} réplica {b}/{B} · {time.time() - t0:.0f}s", flush=True)
        draws[mode] = boot
        for j, (wname, w) in enumerate(weights.items()):
            o = float(np.sum(w * exc)); bt = boot[:, j]; bm = float(bt.mean())
            r = dict(mode=mode, weights=wname, n_models=len(models), B=B, n_perm=NPERM, n_perm_boot=NPERM_BOOT,
                     observed=float(np.sum(w * obs)), null=float(np.sum(w * null)), excess_raw=o, boot_mean=bm, shift=bm - o, excess_bc=2 * o - bm)
            for lvl, a in LEVELS.items():
                lo, hi = np.percentile(bt, [100 * a / 2, 100 * (1 - a / 2)])
                r[f"lo{lvl}"], r[f"hi{lvl}"] = 2 * o - hi, 2 * o - lo
            for c in ("excess_raw", "excess_bc", "lo95", "hi95", "lo99", "hi99", "lo999", "hi999"):
                r[c + "_or"] = np.exp(r[c])
            rows.append(r)
            print(f"{mode:8s} {wname:4s} OR {r['excess_bc_or']:.2f} [{r['lo95_or']:.2f}, {r['hi95_or']:.2f}] · {time.time() - t0:.0f}s", flush=True)
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)
    pd.DataFrame(per_model).to_csv(HERE / "panelD_bootstrap_per_model.csv", index=False)
    np.savez_compressed(OUT_BOOT, **{m: draws[m] for m in MODES}, weights=list(weights))
    rescore()
    write_provenance("step3_panelD_bootstrap", inputs + [WEIGHTS], [__file__, pb.__file__, HERE.parents[0] / "review_fig_languages/panelB/panelB_weighted_requests.py"],
                     B=B, n_perm=NPERM, n_perm_boot=NPERM_BOOT, seed=SEED)


if __name__ == "__main__":
    rescore() if "--rescore" in sys.argv[1:] else main()
