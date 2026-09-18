#!/usr/bin/env python3
"""Bloque 49 — Figura 3 (D2): GLMM del efecto del índice geopolítico 1D sobre el refusal (test de los gráficos del bloque 48).
Nico (18/09): "a ver, probemos ese GLMM". Modelo propuesto por Claude y aceptado por Nico para probar:
  refuse ~ índice × origen + (1 + índice || model) + (1 | prompt_id) + (1 | país)     (r/glmm_index.R, lme4, nAGQ = 0)
El país entra como intercepto aleatorio porque el índice es una variable del país: su efecto se mide contra la variación
entre países (63 en A–D), no contra las filas (24 modelos × ≈ 9 prompts por país pseudorreplicarían). En E (aliado contra
aliado) hay dos países por fila: intercepto por país usuario y por país afectado.
Variantes y modos como en el bloque 48: A USA usuario, B China usuario, C USA afectado, D China afectado, E aliados;
power grabbing y control. Índice del bloque 47 (cero en la mediana, lado USA positivo): la pendiente es el cambio en log-odds
de refusal por unidad de índice; también se reporta el OR entre las bolsas de aliados de China y de USA (0,79 unidades).
Corrección por comparaciones múltiples (pedido de Nico): BH y Holm sobre las 10 pendientes principales (5 variantes × 2 modos)
y, aparte, sobre las 10 interacciones.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_49_fig3_index_glmm.py [--refit]   (≈ 3 min; requiere Rscript + lme4)
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (str(HERE), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402
from pbanalysis.final_conditions import load_d2_final  # noqa: E402

NAME = "49_fig3_index_glmm"
INDEX_CSV = HERE / "results" / "47_alignment_index_1d" / "alignment_index_1d.csv"
R_SCRIPT = HERE / "r" / "glmm_index.R"
R_LIB = Path.home() / "R" / "win-library" / "4.6"
MODES = ("pg", "control")
POOL_SPAN = 0.79   # distancia entre las medias de las bolsas de D2: aliados de USA (+0,35) − aliados de China (−0,44)
VARIANTS = {
    "A_usa_user": ("USA es el usuario · x = índice del país afectado", ["us_ally", "us_rival", "us_neutral"], "affected"),
    "B_china_user": ("China es el usuario · x = índice del país afectado", ["cn_ally", "cn_rival", "cn_neutral"], "affected"),
    "C_usa_target": ("USA es el afectado · x = índice del país usuario", ["ally_us", "rival_us", "neutral_us"], "user"),
    "D_china_target": ("China es el afectado · x = índice del país usuario", ["ally_cn", "rival_cn", "neutral_cn"], "user"),
    "E_allies": ("aliado de USA contra aliado de China · x = índice(usuario) − índice(afectado)", ["allyus_allycn", "allycn_allyus"], "diff"),
}


def find_rscript() -> str:
    exe = shutil.which("Rscript")
    if exe:
        return exe
    cands = sorted(glob.glob("C:/Program Files/R/R-*/bin/Rscript.exe"))
    if not cands:
        sys.exit("Rscript no encontrado.")
    return cands[-1]


def bh(p):
    p = np.asarray(p, float); ok = np.isfinite(p); q = np.full(p.shape, np.nan)
    if ok.sum():
        v = p[ok]; o = np.argsort(v); m = len(v)
        adj = np.minimum.accumulate((v[o] * m / np.arange(1, m + 1))[::-1])[::-1]
        r = np.empty(m); r[o] = np.minimum(adj, 1); q[ok] = r
    return q


def holm(p):
    p = np.asarray(p, float); ok = np.isfinite(p); h = np.full(p.shape, np.nan)
    if ok.sum():
        v = p[ok]; o = np.argsort(v); m = len(v)
        adj = np.maximum.accumulate(v[o] * (m - np.arange(m)))
        r = np.empty(m); r[o] = np.minimum(adj, 1); h[ok] = r
    return h


def main():
    idx = pd.read_csv(INDEX_CSV).set_index("iso3")["index_1d"]
    d2 = load_d2_final()
    d2 = d2[d2["mode"].isin(MODES) & d2.valid].copy()
    d2["idx_user"] = d2.user_iso3.map(idx); d2["idx_aff"] = d2.affected_iso3.map(idx)
    rows = []
    for key, (title, conds, kind) in VARIANTS.items():
        sub = d2[d2.condition.isin(conds)].copy()
        if kind == "affected":
            sub["x"], sub["country1"], sub["country2"] = sub.idx_aff, sub.affected_iso3, ""
        elif kind == "user":
            sub["x"], sub["country1"], sub["country2"] = sub.idx_user, sub.user_iso3, ""
        else:
            sub["x"], sub["country1"], sub["country2"] = sub.idx_user - sub.idx_aff, sub.user_iso3, sub.affected_iso3
        sub = sub[sub.x.notna()]
        sub["variant"] = key
        rows.append(sub[["refuse", "variant", "mode", "x", "origin", "prompt_id", "model", "country1", "country2"]])
    g = pd.concat(rows, ignore_index=True)
    g["refuse"] = g.refuse.astype(int); g["origin_c"] = np.where(g.origin == "CN", .5, -.5)
    print("filas:", g.groupby(["variant", "mode"]).size().to_dict(), flush=True)

    raw = HERE / "results" / NAME / "glmm_index_raw.csv"
    if raw.is_file() and "--refit" not in sys.argv:
        o = pd.read_csv(raw); print("GLMM: reusando", raw.name, flush=True)
    else:
        rscript = find_rscript()
        with tempfile.TemporaryDirectory() as tmp:
            fin, fout = Path(tmp) / "glmm_input.csv", Path(tmp) / "glmm_out.csv"
            g[["refuse", "variant", "mode", "x", "origin_c", "prompt_id", "model", "country1", "country2"]].to_csv(fin, index=False)
            env = dict(os.environ)
            if R_LIB.is_dir():
                env["R_LIBS_USER"] = str(R_LIB)
            t0 = time.time()
            proc = subprocess.run([rscript, str(R_SCRIPT), str(fin), str(fout)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
            print(proc.stdout, flush=True); print(f"R: {time.time() - t0:.0f} s en total", flush=True)
            if proc.returncode != 0:
                print(proc.stderr, file=sys.stderr); sys.exit(f"Rscript terminó con código {proc.returncode}")
            o = pd.read_csv(fout)
        raw.parent.mkdir(parents=True, exist_ok=True); o.to_csv(raw, index=False)
    for col in ("messages", "formula_used", "optimizer"):
        o[col] = o[col].fillna("").astype(str)
    o["OR_per_unit"], o["OR_lo"], o["OR_hi"] = np.exp(o.estimate), np.exp(o.estimate - 1.96 * o.se), np.exp(o.estimate + 1.96 * o.se)
    o["OR_pool_span"] = np.exp(o.estimate * POOL_SPAN)
    o["family"] = np.where(o.quantity == "pendiente (24 modelos)", "pendientes", np.where(o.quantity == "pendiente x origen (CN - US)", "interacciones", "por_origen"))
    o["q_bh"] = np.nan; o["p_holm"] = np.nan
    for fam, ix in o.groupby("family").groups.items():
        o.loc[ix, "q_bh"] = bh(o.loc[ix, "p"].to_numpy()); o.loc[ix, "p_holm"] = holm(o.loc[ix, "p"].to_numpy())
    o["title"] = o.variant.map({k: v[0] for k, v in VARIANTS.items()})
    glmm = o[["variant", "title", "mode", "quantity", "estimate", "se", "z", "p", "q_bh", "p_holm", "OR_per_unit", "OR_lo", "OR_hi", "OR_pool_span",
              "sd_model_slope", "sd_model", "sd_prompt", "sd_country1", "sd_country2", "singular", "optimizer", "variant_formula", "formula_used",
              "messages", "nobs", "n_countries", "seconds", "lme4_version", "r_version"]]

    res = report.Result(
        NAME, "Figura 3: GLMM del índice geopolítico 1D sobre el refusal (test de los gráficos del bloque 48)",
        "¿El refusal cambia con el índice 1D del otro país (o del usuario), y eso depende del origen del modelo? Cinco variantes, power "
        "grabbing y control por separado.",
        status="computado a pedido de Nico (18/09); interpretación pendiente del equipo")
    res.inputs(list(d2.attrs["inputs"]) + [str(INDEX_CSV), str(R_SCRIPT), str(HERE / "r" / "glmm_common.R")])
    res.data("D2 inglés, power grabbing y control, 24 modelos, juez deepseek-v4-flash-0731; índice 1D del bloque 47. A–D: 3 condiciones × 192 "
             "prompts × 24 modelos (≈ 13.800 filas, 63 países); E: 2 condiciones (≈ 9.200 filas, 21 + 21 países).")
    res.method("GLMM (lme4::glmer, nAGQ = 0, || primero, bobyqa + nlminbwrap, Wald; r/glmm_index.R): refuse ~ x × origin_c + (1 + x || model) + "
               "(1 | prompt_id) + (1 | país) [+ (1 | país afectado) en E]; x = índice 1D (unidad = la escala del bloque 47: Corea del Norte −1, "
               "Japón +0,57), origin_c = ±0,5. La pendiente es el cambio en log-odds por unidad de índice; OR_pool_span = OR entre la media de "
               f"la bolsa de aliados de China y la de aliados de USA ({POOL_SPAN} unidades). BH y Holm sobre las 10 pendientes principales y, "
               "aparte, sobre las 10 interacciones (familias definidas por Claude, a revisar).")
    res.table("index_glmm", glmm, "Por variante y modo: pendiente del índice (log-odds por unidad) para los 24 modelos, para modelos US y CN, y la "
              "interacción con el origen; Wald; q (BH) y Holm; OR por unidad y OR entre bolsas; SD entre modelos de la pendiente y SD entre países.")
    for r in glmm[glmm.quantity == "pendiente (24 modelos)"].itertuples():
        res.stat(f"{r.variant}_{r.mode}_pendiente", r.estimate, r.estimate - 1.96 * r.se, r.estimate + 1.96 * r.se, r.p, unit="log-odds por unidad")
    res.note("Registro: 4_analysis/results/27_fig3_notelab/NARRATIVA_F3.md; decisiones de implementación a revisar: 4_analysis/results/DECISIONES_A_REVISAR.md.")
    res.conclusion("Computado a pedido de Nico; interpretación pendiente del equipo.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.set_option("display.width", 250)
    print(glmm[["variant", "mode", "quantity", "estimate", "se", "p", "q_bh", "OR_per_unit", "OR_pool_span", "sd_model_slope", "sd_country1", "singular", "seconds"]].round(3).to_string(index=False))
    print("wrote", out)


if __name__ == "__main__":
    main()
