#!/usr/bin/env python3
"""Bloque 74 — Figura 4, pedido típico revisado: OR marginal de refusal IA vs humano con pesos por PEDIDOS, power shifting
pooled, por origen del modelo, y permutación como test con el bootstrap como barra.

Decisión de Nico (19/09): "la ponderación por pedido me parece mejor, queda eso"; "bootstrap para barra, permutación para
test; hacé los tres que faltan". Gemelo de los bloques 72 (Figura 2 D) y 73 (Figura 3 B) para la Figura 4.

Mismo estimador que el bloque 63: por grupo, tasa de refusal de cada condición (humano = D1 inglés, IA = D3) por modelo,
media pesada por uso, UN log-OR = logit(tasa IA) − logit(tasa humano). Es un OR MARGINAL (sección F de DECISIONES), no
comparable en magnitud con los OR por modelo del GLMM (bloque 58).

Cambios respecto del 63: pesos = participación en los PEDIDOS de OpenRouter (tokens en una tabla de comparación; el
bootstrap por tokens reproduce los IC del bloque 63 porque usa su semilla y su orden de sorteos); un grupo más,
power_shifting = he + de + pg; el mismo estimador por origen del modelo (pesos renormalizados dentro de US y dentro de CN,
en OR y en pp), que reemplaza con el estimador del paper la tabla ponderada por uso de fig4_working; y para cada número,
además del IC bootstrap (B = 1.000, semilla 63, mismos índices para los 24 modelos, estratificado por modo en el pooled),
un p de permutación: intercambiar al azar el veredicto humano y el veredicto IA de cada (modelo, prompt), B = 5.000,
semilla 174, p bilateral = (1 + #{|T*| ≥ |T|}) / (B + 1). BH (regla del 18/09) dentro de cada familia = los 4 modos de un
mismo conjunto de modelos (24, US, CN); el pooled es un test solo (q = p).

Datos: filas válidas del bloque 22. Ejecutar desde la raíz:  python 4_analysis/analysis_74_fig4_usage_weighted_requests.py   (≈ 1 min)
"""
from __future__ import annotations

import json
import os
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
import matplotlib.ticker as mticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "74_fig4_usage_weighted_requests"
SRC = HERE / "results" / "22_d3_ai_final" / "analysis_rows.csv.gz"
USAGE = HERE / "inputs" / "openrouter_usage" / "usage_30d_2026-08-18_2026-09-16.csv"
B_BOOT, SEED_BOOT = 1000, 63          # los del bloque 63: por tokens, los IC de los 4 modos coinciden con ese bloque
B_PERM, SEED_PERM = 5000, 174
MODES = ["he", "de", "pg", "control"]
PS = "power_shifting"
GROUPS = MODES + [PS]
LABELS = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control", PS: "Power shifting\n(he + de + pg)"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83", PS: "#5B3F8C"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "axes.titlelocation": "left", "savefig.facecolor": "white"})


def logit(x):
    x = np.clip(x, 1e-6, 1 - 1e-6)
    return np.log(x / (1 - x))


def stat(cube, w):
    """cube: modelos × prompts × 2 (humano, IA); NaN = par inválido. Tasas por modelo, media pesada por uso sobre los modelos con
    peso > 0 y tasas definidas, log-OR IA vs humano y diferencia en pp."""
    n = np.sum(np.isfinite(cube), axis=1)
    with np.errstate(invalid="ignore"):
        r = np.nansum(cube, axis=1) / np.where(n > 0, n, np.nan)
    ok = np.isfinite(r[:, 0]) & np.isfinite(r[:, 1]) & (w > 0)
    ww = w[ok] / w[ok].sum()
    rh, ra = float((ww * r[ok, 0]).sum()), float((ww * r[ok, 1]).sum())
    return float(logit(ra) - logit(rh)), 100 * (ra - rh), rh, ra, int(ok.sum())


def bh(p):
    p = np.asarray(p, float); m = len(p); order = np.argsort(p)
    q = np.empty(m); prev = 1.0
    for rank, i in zip(range(m, 0, -1), order[::-1]):
        prev = min(prev, p[i] * m / rank); q[i] = prev
    return q


def main():
    style()
    d = pd.read_csv(SRC, low_memory=False)
    d = d[(d.valid == True) & d["mode"].isin(MODES)].copy(); d["refuse"] = d.refuse.astype(float)  # noqa: E712
    use = pd.read_csv(USAGE).set_index("model")
    models = sorted(use.index)
    assert set(models) == set(d.model.unique()), "la tabla de uso no coincide con el panel"
    origin = d.drop_duplicates("model").set_index("model").loc[models, "origin"].to_numpy()
    base = {"requests": use.loc[models, "requests_30d"].to_numpy(float), "tokens": use.loc[models, "tokens_30d"].to_numpy(float)}
    base = {k: v / v.sum() for k, v in base.items()}
    # juegos de pesos: (nombre de pesos, conjunto de modelos) -> vector; por origen, renormalizado dentro del bloque
    W = {}
    for k, v in base.items():
        W[(k, "all")] = v
        for o in ("US", "CN"):
            vo = v * (origin == o); W[(k, o)] = vo / vo.sum()
    neff = {key: float(1 / (v ** 2).sum()) for key, v in W.items()}
    print(f"filas válidas {len(d):,}  modelos {len(models)}  n_eff pedidos {neff[('requests', 'all')]:.1f} (US {neff[('requests', 'US')]:.1f}, "
          f"CN {neff[('requests', 'CN')]:.1f})  tokens {neff[('tokens', 'all')]:.1f}", flush=True)

    cubes, strata = {}, {}
    for mode in MODES:
        dm = d[d["mode"] == mode]
        prompts = sorted(dm.prompt_id.unique())
        cubes[mode] = np.stack([dm[dm.model == m].pivot(index="prompt_id", columns="condition", values="refuse")
                                .reindex(index=prompts, columns=["human", "ai"]).to_numpy(float) for m in models])
        strata[mode] = np.zeros(len(prompts), int)
    cubes[PS] = np.concatenate([cubes[m] for m in ("he", "de", "pg")], axis=1)
    strata[PS] = np.concatenate([np.full(cubes[m].shape[1], k) for k, m in enumerate(("he", "de", "pg"))])

    rng_boot = np.random.default_rng(SEED_BOOT)      # un solo generador, modos en el orden del bloque 63, después el pooled
    rows = []
    for g in GROUPS:
        cube, st = cubes[g], strata[g]
        obs = {key: stat(cube, w) for key, w in W.items()}
        blocks = [np.where(st == v)[0] for v in np.unique(st)]
        dr_or = {key: np.empty(B_BOOT) for key in W}; dr_pp = {key: np.empty(B_BOOT) for key in W}
        for b in range(B_BOOT):
            idx = rng_boot.integers(0, cube.shape[1], cube.shape[1]) if g in MODES else \
                np.concatenate([rng_boot.choice(blk, len(blk), replace=True) for blk in blocks])
            sub = cube[:, idx, :]
            for key, w in W.items():
                s = stat(sub, w); dr_or[key][b], dr_pp[key][b] = s[0], s[1]
        rng = np.random.default_rng(SEED_PERM)
        pm_or = {key: np.empty(B_PERM) for key in W}; pm_pp = {key: np.empty(B_PERM) for key in W}
        for b in range(B_PERM):
            S = rng.random(cube.shape[:2]) < .5
            sub = np.where(S[:, :, None], cube[:, :, ::-1], cube)
            for key, w in W.items():
                s = stat(sub, w); pm_or[key][b], pm_pp[key][b] = s[0], s[1]
        for (k, o), w in W.items():
            est, pp, rh, ra, nm = obs[(k, o)]
            lo, hi = np.percentile(dr_or[(k, o)], [2.5, 97.5]); plo, phi = np.percentile(dr_pp[(k, o)], [2.5, 97.5])
            pboot = min(1.0, 2 * min((dr_or[(k, o)] <= 0).mean(), (dr_or[(k, o)] >= 0).mean()))
            pperm = (1 + (np.abs(pm_or[(k, o)]) >= abs(est)).sum()) / (B_PERM + 1)
            pperm_pp = (1 + (np.abs(pm_pp[(k, o)]) >= abs(pp)).sum()) / (B_PERM + 1)
            rows.append(dict(weights=k, models=o, group=g, n_models=nm, n_prompts=int(cube.shape[1]),
                             rate_human=100 * rh, rate_ai=100 * ra, odds_ratio=float(np.exp(est)), boot_lo=float(np.exp(lo)), boot_hi=float(np.exp(hi)),
                             boot_p=float(pboot), perm_p=float(pperm), pp=float(pp), pp_boot_lo=float(plo), pp_boot_hi=float(phi), pp_perm_p=float(pperm_pp)))
        o = obs[("requests", "all")]
        print(f"{g:15s} pedidos OR {np.exp(o[0]):.3f} ({o[2] * 100:.1f} -> {o[3] * 100:.1f} %)  tokens OR {np.exp(obs[('tokens', 'all')][0]):.3f}", flush=True)
    tab = pd.DataFrame(rows)
    tab["boot_q"] = np.nan; tab["perm_q"] = np.nan; tab["pp_perm_q"] = np.nan
    for _, sub in tab.groupby(["weights", "models"]):
        m = sub.group.isin(MODES)
        for src, dst in (("boot_p", "boot_q"), ("perm_p", "perm_q"), ("pp_perm_p", "pp_perm_q")):
            tab.loc[sub.index[m], dst] = bh(sub.loc[m, src]); tab.loc[sub.index[~m], dst] = sub.loc[~m, src]
    req = tab[(tab.weights == "requests") & (tab.models == "all")].drop(columns=["weights", "models"])
    tok = tab[(tab.weights == "tokens") & (tab.models == "all")].drop(columns=["weights", "models"])
    byo = tab[(tab.weights == "requests") & (tab.models != "all")].drop(columns="weights").rename(columns={"models": "origin"})
    print(req.round(3).to_string(index=False), flush=True)
    print(byo[["origin", "group", "rate_human", "rate_ai", "pp", "pp_boot_lo", "pp_boot_hi", "pp_perm_q", "odds_ratio", "boot_lo", "boot_hi", "perm_q"]].round(3).to_string(index=False), flush=True)

    wt = use.reset_index()[["model", "origin", "tokens_30d", "requests_30d"]]
    wt["share_tokens"] = wt.tokens_30d / wt.tokens_30d.sum(); wt["share_requests"] = wt.requests_30d / wt.requests_30d.sum()
    wt = wt.sort_values("share_requests", ascending=False)

    res = report.Result(
        NAME, "Figura 4, pedido típico revisado: OR marginal IA vs humano, pesos por pedidos, power shifting pooled, por origen, bootstrap y permutación",
        "Para un pedido típico (tasas pesadas por la participación de cada modelo en los PEDIDOS de OpenRouter), ¿cuánto más se rechaza cuando "
        "el usuario es un agente de IA que cuando es humano? Por modo, para power shifting junto, y por origen del modelo; IC bootstrap sobre "
        "prompts como barra, permutación humano / IA como test.",
        status="decisión de Nico (19/09): pesos por pedidos quedan; bootstrap para la barra, permutación para el test; reemplaza al bloque 63 y a la tabla ponderada de fig4_working")
    res.inputs([str(SRC.relative_to(ROOT)), str(USAGE.relative_to(ROOT))])
    res.data(f"Filas válidas del bloque 22 (24 modelos, {len(d):,} filas; pares humano / IA por prompt y modelo). Pesos: pedidos y tokens por modelo en "
             f"OpenRouter del 2026-08-18 al 2026-09-16, foto del 2026-09-17; n_eff por pedidos {neff[('requests', 'all')]:.1f} (US "
             f"{neff[('requests', 'US')]:.1f}, CN {neff[('requests', 'CN')]:.1f}), por tokens {neff[('tokens', 'all')]:.1f}.")
    res.method("Estadístico (bloque 63): tasa de refusal por modelo con usuario humano y con usuario IA, media pesada por uso sobre los modelos, un "
               "log-OR IA vs humano (OR marginal) y la diferencia en pp. power_shifting = he + de + pg juntos (igual peso por prompt). Por origen: "
               "el mismo estimador con los pesos renormalizados dentro de US y dentro de CN.")
    res.method(f"Bootstrap sobre prompts: B = {B_BOOT}, semilla {SEED_BOOT} y orden de sorteos del bloque 63 (los IC por tokens de los 4 modos coinciden "
               "con ese bloque), mismos índices para los 24 modelos y para todos los juegos de pesos, estratificado por modo en el pooled; modelos y "
               "pesos fijos; IC percentil 95 % (la barra) y p bilateral 2 · min(cola) como referencia (boot_p).")
    res.method(f"Permutación (el test): intercambio al azar del veredicto humano y el veredicto IA de cada (modelo, prompt), independiente; B = {B_PERM:,}, "
               f"semilla {SEED_PERM}; p bilateral = (1 + #{{|T*| ≥ |T|}}) / (B + 1), para el log-OR (perm_p) y para la diferencia en pp (pp_perm_p).")
    res.method("BH dentro de cada familia = los 4 modos de un mismo conjunto de modelos (24, US, CN) y juego de pesos; el pooled es un test solo "
               "(q = p). Familia elegida por Claude; anotada en DECISIONES_A_REVISAR.md.")
    res.table("usage_weighted_or_requests", req, "PESOS POR PEDIDOS, 24 modelos. Por grupo: tasas pesadas humano e IA (%), OR marginal, IC y p del "
              "bootstrap, p de permutación, q de BH; y lo mismo en pp.")
    res.table("usage_weighted_or_tokens", tok, "PESOS POR TOKENS (bloque 63), mismas columnas, para comparar.", show=False)
    res.table("usage_weighted_by_origin", byo, "PESOS POR PEDIDOS renormalizados dentro de cada origen (12 US, 12 CN). Reemplaza con el estimador del "
              "paper la tabla 'ponderando por uso' de fig4_working (cuaderno, 18/09).")
    res.table("weights", wt, "Participación de cada modelo en tokens y en pedidos (30 días).", show=False)
    for _, r in req.iterrows():
        res.stat(f"typical_request_or_{r.group}", r.odds_ratio, r.boot_lo, r.boot_hi, p=r.perm_p, unit="OR",
                 note=f"pesos por pedidos; pp {r.pp:+.1f} [{r.pp_boot_lo:+.1f}, {r.pp_boot_hi:+.1f}]; perm_q {r.perm_q:.3f}")

    # ------------------------------------------------------------------ figuras
    def fmt_q(q):
        return ("q < 0,001" if q < .001 else f"q = {q:.3f}").replace(".", ",")

    fig, ax = plt.subplots(figsize=(8.4, 4.8), layout="constrained")
    x = np.arange(len(GROUPS)); t = req.set_index("group").loc[GROUPS]
    ax.bar(x, t.odds_ratio - 1, bottom=1, width=.6, color=[MODE_COLORS[g] for g in GROUPS], alpha=.9, zorder=2)
    ax.errorbar(x, t.odds_ratio, yerr=[t.odds_ratio - t.boot_lo, t.boot_hi - t.odds_ratio], fmt="none", ecolor="#222", elinewidth=1.2, capsize=4, zorder=3)
    for xi, (_, r) in zip(x, t.iterrows()):
        ax.text(xi, r.boot_hi * 1.03, fmt_q(r.perm_q), ha="center", va="bottom", fontsize=8.5)
    ax.axhline(1, color="black", lw=.9, ls="--", zorder=1)
    ax.set_yscale("log"); ax.set_yticks([1, 1.25, 1.5, 2, 2.5]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter()); ax.set_ylim(.92, float(t.boot_hi.max()) * 1.25)
    ax.set_xticks(x, [LABELS[g] for g in GROUPS], fontsize=9.5); ax.grid(axis="y", alpha=.15)
    ax.set_ylabel("OR marginal de refusal, usuario IA vs humano\n(tasas pesadas por pedidos)")
    ax.set_title("Figura 4 · Un pedido típico (pesos por pedidos): OR marginal IA vs humano, por modo y power shifting pooled", fontsize=9.5)
    fig.text(.01, -.02, "Barra = OR de las tasas pesadas por pedidos en OpenRouter (30 días) · barra de error = IC 95 % bootstrap sobre prompts, modelos y "
             "pesos fijos · q = BH sobre el p de permutación dentro de los 4 modos (pooled sin corregir)", fontsize=8.5, color="#555555", ha="left", va="top")
    res.figure("p6_requests_typical_or", fig, "El panel 6 de la Figura 4 (bloque 63) con pesos por pedidos y el pooled de power shifting; IC bootstrap "
               "como barra, permutación como test. OR marginal: no comparable en magnitud con los OR por modelo del GLMM (bloque 58).")

    fig, ax = plt.subplots(figsize=(9.6, 4.8), layout="constrained")
    wd = .38
    for k, o in enumerate(("US", "CN")):
        t = byo[byo.origin == o].set_index("group").loc[GROUPS]; xo = x + (k - .5) * wd
        ax.bar(xo, t.odds_ratio - 1, bottom=1, width=wd, color=ORIGIN[o], alpha=.85, zorder=2, label=f"modelos {o}")
        ax.errorbar(xo, t.odds_ratio, yerr=[t.odds_ratio - t.boot_lo, t.boot_hi - t.odds_ratio], fmt="none", ecolor="#222", elinewidth=1.2, capsize=3, zorder=3)
        for xi, (_, r) in zip(xo, t.iterrows()):
            if r.perm_q < .05:
                ax.text(xi, r.boot_hi * 1.03, "*", ha="center", va="bottom", fontsize=12)
    ax.axhline(1, color="black", lw=.9, ls="--", zorder=1)
    ax.set_yscale("log"); ax.set_yticks([.8, 1, 1.25, 1.5, 2, 2.5, 3]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter()); ax.set_ylim(.78, float(byo.boot_hi.max()) * 1.3)
    ax.set_xticks(x, [LABELS[g] for g in GROUPS], fontsize=9.5); ax.grid(axis="y", alpha=.15); ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.set_ylabel("OR marginal IA vs humano\n(tasas pesadas por pedidos dentro del origen)")
    ax.set_title("Figura 4 · Un pedido típico por origen del modelo (pesos por pedidos renormalizados dentro de US y de CN)", fontsize=9.5)
    res.figure("p6_requests_by_origin_or", fig, "El mismo estimador dentro de cada bloque de 12 modelos, con sus pesos renormalizados. Asterisco = "
               "q < 0,05 de BH sobre el p de permutación dentro de los 4 modos del origen (pooled sin corregir). La diferencia US − CN no se testea aquí.")

    res.note("Fuente de verdad: notebooks/PowerBench.md. Registro en 4_analysis/results/53_fig4_notelab/NARRATIVA_F4.md.")
    res.note("El bloque 63 queda como está (registro). La tabla 'ponderando por uso' de fig4_working (Wen, 18/09) usa un estimador distinto "
             "(regresión pesada con errores agrupados por prompt) y lee los pesos por tokens del bloque 40; no se tocó.")
    res.conclusion("OR marginal IA vs humano de un pedido típico con pesos por pedidos, por modo, pooled y por origen, con IC bootstrap y p de "
                   "permutación. Lectura de Nico pendiente.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)},
            "B_boot": B_BOOT, "seed_boot": SEED_BOOT, "B_perm": B_PERM, "seed_perm": SEED_PERM, "n_eff": {f"{k}_{o}": v for (k, o), v in neff.items()}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
