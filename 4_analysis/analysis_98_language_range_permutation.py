#!/usr/bin/env python3
"""Bloque 98 — test de permutación para el panel D de la figura de idiomas (22 modelos), pedido de Nico (25/09).

Objeción del revisor: el bootstrap de un rango (estadístico tipo máximo) no es confiable para inferencia (el punto queda en el
borde superior del IC, p. ej. DE 1,99 [1,61; 2,11]). Acá la inferencia pasa a un test de permutación; el IC bootstrap queda
solo como descriptivo.

Estadístico (idéntico al de step3_panelD_bootstrap.py): por modo y modelo, rango = max − min del logit suavizado de R(idioma)
sobre la matriz 192 prompts × 8 idiomas (range_logodds); azar_m = media del rango con los idiomas barajados dentro de cada
prompt (shuffled, NPERM = 2.000, semilla SEED + 100·k, k = índice del modo; mismas llamadas que pb._obs_null);
exceso_m = rango_m − azar_m; panel = Σ w_m · exceso_m; OR = exp(panel).

Test (H0: dentro de cada prompt los 8 idiomas son intercambiables, en cada modelo):
- Un SEGUNDO juego de K = 10.000 barajados por modelo, independiente del que da el azar (semilla SEED + 100·k + 50; mismo
  shuffled, mismo range_logodds, barajado independiente por modelo como en el código existente). Cada barajado k es un
  pseudo-dato: pseudo-exceso_m,k = rango_m,k − azar_m, con el MISMO azar_m que usa el observado; nulo_k = Σ w_m · pseudo-exceso_m,k.
- p = (1 + #{nulo_k ≥ observado}) / (1 + K), una cola (más rango que el azar). Como azar_m es el mismo número para el
  observado y los K pseudo-datos, y bajo H0 el observado y los K barajados son intercambiables, el p es exacto (válido) y
  equivale al test de permutación de Σ w·rango. Se prefirió a la media leave-one-out (que usa K − 1 barajados en los
  pseudo-datos y K en el observado y rompe la simetría en O(1/K)).
- BH dentro de cada ponderación (familia = los 4 modos), como en el paper.
Ponderaciones: eq = 1/22; use = share_requests del bloque 72 renormalizada sobre los 22; use_noluna = la misma sin
gpt-5.6-luna, renormalizada sobre los 21. n efectivo = 1 / Σ w².

IC bootstrap descriptivo: se vuelve a correr pb.bootstrap_modes (B = 2.000, mismas semillas SEED + 100·k + 1 + c) con las tres
ponderaciones a la vez. Los sorteos no dependen de los pesos, así que las columnas eq y use reproducen las réplicas guardadas en
panelD_bootstrap_draws.npz (se verifica) y la columna use_noluna sale de las MISMAS réplicas.

Sin API. No modifica ningún archivo existente. Ejecutar desde cualquier lado:
    python 4_analysis/analysis_98_language_range_permutation.py        (≈ 4–6 min, 6 procesos)
Salida: results/98_language_range_permutation/{range_permutation.csv, README.md (a mano), provenance.json}
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D22 = ROOT / "4_analysis" / "review_fig_languages_22models"
if str(D22) not in sys.path:
    sys.path.insert(0, str(D22))
from _common import MODES, LANGS, WEIGHTS, load22  # noqa: E402  (pone 4_analysis, common y panelB en sys.path)
import panelB_bootstrap as pb  # noqa: E402
from panelB_weighted_requests import range_logodds, shuffled  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

OUT = ROOT / "4_analysis" / "results" / "98_language_range_permutation"
PANEL_D = D22 / "panelD_bootstrap.csv"
PANEL_D_DRAWS = D22 / "panelD_bootstrap_draws.npz"
LUNA = "gpt-5.6-luna"
K, CHUNK = 10_000, 2_000          # pseudo-datos por modelo, en bloques de 2.000 (memoria)
PERM_SEED_OFFSET = 50             # semilla del juego de pseudo-datos: SEED + 100·k + 50 (no choca con azar ni bootstrap)
LABEL = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT"}
FAMILY = {"eq": "4 modos, peso igual", "use": "4 modos, peso por uso", "use_noluna": "4 modos, peso por uso sin gpt-5.6-luna"}


def _perm_ranges(args):
    """K rangos por modelo con los idiomas barajados dentro de cada prompt (juego independiente del azar). Shape (K, n_modelos)."""
    mats, k_total, chunk, seed = args
    rng = np.random.default_rng(seed)
    out = np.empty((k_total, len(mats)))
    for i, M in enumerate(mats):
        out[:, i] = np.concatenate([range_logodds(shuffled(M, chunk, rng)) for _ in range(k_total // chunk)])
    return out


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    d, inputs = load22()
    meta = d.drop_duplicates("model").set_index("model").origin
    models = sorted(meta.index, key=lambda m: (meta[m] != "US", m))          # mismo orden que step3 (importa para las semillas)
    w_raw = pd.read_csv(WEIGHTS).set_index("model").share_requests.reindex(models)
    assert w_raw.notna().all(), "modelos sin peso"
    assert LUNA in models
    w_nl = w_raw.where(w_raw.index != LUNA, 0.0)
    weights = {"eq": np.full(len(models), 1 / len(models)), "use": (w_raw / w_raw.sum()).to_numpy(), "use_noluna": (w_nl / w_nl.sum()).to_numpy()}
    n_eff = {k: float(1 / np.sum(w ** 2)) for k, w in weights.items()}
    print(f"filas válidas {len(d):,} · modelos {len(models)} · n efectivo " + " · ".join(f"{k} {v:.2f}" for k, v in n_eff.items()), flush=True)

    mats = {}
    for mode in MODES:
        dm = d[d["mode"] == mode]
        for m in models:
            mats[(mode, m)] = dm[dm.model == m].pivot(index="prompt_id", columns="lang", values="refuse").reindex(columns=LANGS).to_numpy(float)
            assert mats[(mode, m)].shape == (192, 8)

    with ProcessPoolExecutor(max_workers=pb.MAX_WORKERS) as pool:
        f_perm = {mode: pool.submit(_perm_ranges, ([mats[(mode, m)] for m in models], K, CHUNK, pb.SEED + 100 * k + PERM_SEED_OFFSET))
                  for k, mode in enumerate(MODES)}
        res = pb.bootstrap_modes(mats, models, weights, pool)                  # (obs, azar, réplicas B × 3) por modo, semillas de step3
        perm = {mode: f.result() for mode, f in f_perm.items()}
    print(f"permutaciones y bootstrap listos · {time.time() - t0:.0f}s", flush=True)

    # verificaciones contra panelD (22 modelos, eq y use)
    ref = pd.read_csv(PANEL_D).set_index(["mode", "weights"])
    ref_draws = np.load(PANEL_D_DRAWS)
    checks = {"max_abs_diff_excess_logodds_vs_panelD": 0.0, "max_abs_diff_boot_draws_vs_panelD": 0.0}

    rows = []
    for mode in MODES:
        obs, null, boot = res[mode]
        exc = obs - null
        checks["max_abs_diff_boot_draws_vs_panelD"] = max(checks["max_abs_diff_boot_draws_vs_panelD"],
                                                          float(np.max(np.abs(boot[:, :2] - ref_draws[mode]))))
        pseudo = perm[mode] - null                                              # (K, 22): rango_k − azar del modelo
        for j, (wname, w) in enumerate(weights.items()):
            o = float(np.sum(w * exc))
            nul = np.sum(pseudo * w, axis=1)
            p_perm = (1 + int(np.sum(nul >= o))) / (1 + K)
            bt = boot[:, j]
            lo, hi = np.percentile(bt, [2.5, 97.5])
            r = dict(mode=mode, label=LABEL[mode], weighting=wname, n_models=int(np.sum(w > 0)), n_eff=n_eff[wname],
                     excess_logodds=o, observed_or=np.exp(o), boot_lo95_or=np.exp(lo), boot_hi95_or=np.exp(hi),
                     boot_source="panelD_bootstrap.csv (reproducido)" if wname in ("eq", "use") else "nuevo, mismas réplicas y semilla",
                     p_perm=p_perm, null_mean_or=float(np.exp(nul.mean())), null_p95_or=float(np.exp(np.percentile(nul, 95))),
                     null_max_or=float(np.exp(nul.max())), p_boot=pb.p_from_boot(bt), K=K, B=len(bt))
            if wname in ("eq", "use"):
                rr = ref.loc[(mode, wname)]
                checks["max_abs_diff_excess_logodds_vs_panelD"] = max(checks["max_abs_diff_excess_logodds_vs_panelD"], abs(o - rr.excess))
                assert abs(np.exp(lo) - rr.lo95_or) < 1e-9 and abs(np.exp(hi) - rr.hi95_or) < 1e-9, (mode, wname, "IC no reproduce panelD")
                r["q_boot_bh_current"] = float(rr.q_bh)
            rows.append(r)
    tab = pd.DataFrame(rows)
    tab["bh_family"] = tab.weighting.map(FAMILY)
    tab["q_perm_bh"] = tab.groupby("weighting").p_perm.transform(pb.bh)
    tab["q_boot_bh"] = tab.groupby("weighting").p_boot.transform(pb.bh)
    tab["stars_perm"] = tab.q_perm_bh.map(pb.stars_from_p)
    tab["stars_boot"] = tab.q_boot_bh.map(pb.stars_from_p)
    assert checks["max_abs_diff_excess_logodds_vs_panelD"] < 1e-12, checks
    assert checks["max_abs_diff_boot_draws_vs_panelD"] < 1e-9, checks
    ok = tab.dropna(subset=["q_boot_bh_current"])
    assert np.allclose(ok.q_boot_bh, ok.q_boot_bh_current), "q del bootstrap no reproduce panelD"

    order = {"eq": 0, "use": 1, "use_noluna": 2}
    tab = tab.sort_values(["weighting", "mode"], key=lambda s: s.map(order) if s.name == "weighting" else s.map({m: i for i, m in enumerate(MODES)}))
    cols = ["mode", "label", "weighting", "n_models", "n_eff", "excess_logodds", "observed_or", "boot_lo95_or", "boot_hi95_or", "boot_source",
            "p_perm", "q_perm_bh", "stars_perm", "p_boot", "q_boot_bh", "stars_boot", "q_boot_bh_current", "bh_family",
            "null_mean_or", "null_p95_or", "null_max_or", "K", "B"]
    tab[cols].to_csv(OUT / "range_permutation.csv", index=False)
    for _, r in tab.iterrows():
        print(f"{r.label} {r.weighting:10s} OR {r.observed_or:.2f} [{r.boot_lo95_or:.2f}; {r.boot_hi95_or:.2f}] · perm p {r.p_perm:.4f} q {r.q_perm_bh:.4f} "
              f"{r.stars_perm:3s} · boot p {r.p_boot:.4f} q {r.q_boot_bh:.4f} {r.stars_boot:3s} · nulo p95 {r.null_p95_or:.3f} max {r.null_max_or:.3f}", flush=True)

    rel = lambda p: str(Path(p).resolve().relative_to(ROOT)).replace("\\", "/") if str(Path(p).resolve()).startswith(str(ROOT)) else str(p)
    code = [__file__, D22 / "_common.py", Path(pb.__file__), ROOT / "4_analysis/review_fig_languages/panelB/panelB_weighted_requests.py",
            D22 / "step3_panelD_bootstrap.py"]
    prov = {"script": rel(__file__), "date": time.strftime("%Y-%m-%d %H:%M"), "api_calls": 0,
            "inputs": {rel(p): file_digest(p) for p in list(inputs) + [WEIGHTS, PANEL_D, PANEL_D_DRAWS] if Path(p).is_file()},
            "code": {rel(c): file_digest(c) for c in code},
            "models": models, "excluded_models_22_panel": ["nemotron-3.5-lightning", "nova-2-lite"], "excluded_use_noluna": LUNA,
            "n_eff": n_eff, "weights": {k: dict(zip(models, map(float, w))) for k, w in weights.items()},
            "params": {"K_pseudo_datasets": K, "chunk": CHUNK, "NPERM_chance": pb.NPERM, "B_boot": pb.B, "NPERM_BOOT": pb.NPERM_BOOT,
                       "N_CHUNKS_boot": pb.N_CHUNKS, "SEED": pb.SEED,
                       "seeds": {"chance (y observado)": "SEED + 100·k", "bootstrap": "SEED + 100·k + 1 + c", "pseudo-datos": f"SEED + 100·k + {PERM_SEED_OFFSET}",
                                 "k": {m: i for i, m in enumerate(MODES)}}},
            "checks": checks, "runtime_s": round(time.time() - t0)}
    (OUT / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"checks {checks} · {time.time() - t0:.0f}s · wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
