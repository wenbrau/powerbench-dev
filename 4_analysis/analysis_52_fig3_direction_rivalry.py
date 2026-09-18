#!/usr/bin/env python3
"""Bloque 52 — Figura 3 (D2): el panel C (efecto de la dirección respecto de USA y de China) usando SOLO las díadas de
rivalidad. Pregunta de Nico (18/09), textual: "quizás mezclar USA/aliado y USA/neutral con los dos de rivalidad no es una
buena idea? cómo darían los gráficos, y los tests, en los que hacemos eso, si no lo hacemos y usamos solo los de rivalidad?"

Mismo modelo que el bloque 46 (r/glmm_direction.R, modelo conjunto por país y modo, lme4, nAGQ = 0):
  refuse ~ toward × origin_c + dyad + (1 + toward || model) + (1 | prompt_id)
pero con dos díadas por país en vez de cuatro:
  díadas de rivalidad con USA   : USA / rival de USA (aliado de China), USA / China
  díadas de rivalidad con China : China / rival de China (aliado de USA), China / USA (mismas filas que USA / China, al revés)
toward = +0,5 si el país es el usuario. Modos: he, de, pg, control. BH y Holm por familia (8 tests principales, 8 interacciones,
16 por origen). Salida: tabla `direction_glmm_rivalry.csv`, figura `pD_direction_body_rivalry.png` (mismo formato que la del
bloque 46) y una comparación contra la versión con las cuatro díadas.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_52_fig3_direction_rivalry.py [--refit]   (≈ 2–3 min de R)
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

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402
from pbanalysis.final_conditions import load_d2_final  # noqa: E402

NAME = "52_fig3_direction_rivalry"
MODES = ("he", "de", "pg", "control")
LABELS = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
POLES = {"usa": [("us_rival", "us_rival", "rival_us"), ("us_cn", "us_cn", "cn_us")],
         "china": [("cn_rival", "cn_rival", "rival_cn"), ("cn_us", "cn_us", "us_cn")]}
COUNTRY = {"usa": "USA", "china": "China"}
R_SCRIPT = HERE / "r" / "glmm_direction.R"
R_LIB = Path.home() / "R" / "win-library" / "4.6"
ALL_DYADS = HERE / "results" / "46_fig3_direction_glmm" / "direction_glmm.csv"
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


def or_axis(ax, lo=.6, hi=1.8):
    ax.set_yscale("log"); ax.set_yticks([.67, .8, 1, 1.25, 1.5]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter()); ax.set_ylim(lo, hi)
    ax.axhline(1, color="black", lw=1); ax.grid(axis="y", alpha=.15)


def body_fig(joint, modes, subtitle):
    gi = joint.set_index(["mode", "country", "quantity"])
    groups = (("direccion (24 modelos)", "todos los modelos" + NL + "(24)", "#222222"), ("direccion, modelos US", "modelos US" + NL + "(12)", ORIGIN["US"]),
              ("direccion, modelos CN", "modelos CN" + NL + "(12)", ORIGIN["CN"]))
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), sharey=True, layout="constrained")
    x = np.arange(len(groups)); wd = .8 / len(modes)
    for ax, pole in zip(axes, POLES):
        P = COUNTRY[pole]
        for k, mode in enumerate(modes):
            r = pd.DataFrame([gi.loc[(mode, pole, q[0])] for q in groups])
            xo = x + (k - (len(modes) - 1) / 2) * wd
            ax.bar(xo, r.OR.values - 1, bottom=1, width=wd, color=MODE_COLORS[mode], alpha=.9, zorder=2, label=LABELS[mode])
            ax.errorbar(xo, r.OR.values, yerr=[r.OR.values - r.OR_lo.values, r.OR_hi.values - r.OR.values], fmt="none", ecolor="#111", elinewidth=1.3, capsize=4, zorder=3)
        or_axis(ax, .47, 1.9); ax.set_yticks([.5, .67, .8, 1, 1.25, 1.5]); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.set_xticks(x, [q[1] for q in groups])
        for tk, q in zip(ax.get_xticklabels(), groups):
            tk.set_color(q[2])
        ax.set_title(f"Rivalidad con {P}: {P} / rival de {P} y {P} / {'China' if pole == 'usa' else 'USA'}", fontsize=10.5)
        ax.text(.5, .985, f"▲ rechaza más cuando {P} es el usuario" + NL + f"(en power shifting: {P} gana poder o se lo saca al otro)", transform=ax.transAxes,
                ha="center", va="top", fontsize=9, color="#333", fontweight="bold")
        ax.text(.5, .015, f"▼ rechaza más cuando {P} es el afectado" + NL + f"(en power shifting: {P} pierde poder)", transform=ax.transAxes,
                ha="center", va="bottom", fontsize=9, color="#333", fontweight="bold")
    axes[0].set_ylabel("OR de refusal: el país es el usuario / el país es el afectado" + NL + "(GLMM, IC 95 % de Wald)")
    axes[1].legend(frameon=False, fontsize=9.5, loc="upper right", bbox_to_anchor=(1, .86))
    fig.suptitle(subtitle, fontsize=12)
    return fig


def main():
    style()
    d2 = load_d2_final()
    base = d2[d2["mode"].isin(MODES) & d2.valid]
    rows = []
    for pole, dyads in POLES.items():
        for key, c_user, c_aff in dyads:
            for cond, toward in ((c_user, .5), (c_aff, -.5)):
                x = base[base.condition == cond][["refuse", "mode", "prompt_id", "model", "origin"]].copy()
                x["pole"], x["dyad"], x["toward"] = pole, key, toward
                rows.append(x)
    g = pd.concat(rows, ignore_index=True)
    g["refuse"] = g.refuse.astype(int); g["origin_c"] = np.where(g.origin == "CN", .5, -.5)
    print("filas:", g.groupby(["mode", "pole"]).size().to_dict(), flush=True)
    raw = HERE / "results" / NAME / "glmm_direction_rivalry_raw.csv"
    if raw.is_file() and "--refit" not in sys.argv:
        o = pd.read_csv(raw); print("GLMM: reusando", raw.name, flush=True)
    else:
        rscript = find_rscript()
        with tempfile.TemporaryDirectory() as tmp:
            fin, fout = Path(tmp) / "glmm_input.csv", Path(tmp) / "glmm_out.csv"
            g[["refuse", "mode", "pole", "dyad", "toward", "origin_c", "prompt_id", "model"]].to_csv(fin, index=False)
            env = dict(os.environ)
            if R_LIB.is_dir():
                env["R_LIBS_USER"] = str(R_LIB)
            t0 = time.time()
            proc = subprocess.run([rscript, str(R_SCRIPT), str(fin), str(fout), "joint"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
            print(proc.stdout, flush=True); print(f"R: {time.time() - t0:.0f} s en total", flush=True)
            if proc.returncode != 0:
                print(proc.stderr, file=sys.stderr); sys.exit(f"Rscript terminó con código {proc.returncode}")
            o = pd.read_csv(fout)
        raw.parent.mkdir(parents=True, exist_ok=True); o.to_csv(raw, index=False)
    for col in ("messages", "formula_used", "optimizer"):
        o[col] = o[col].fillna("").astype(str)
    o["OR"], o["OR_lo"], o["OR_hi"] = np.exp(o.estimate), np.exp(o.estimate - 1.96 * o.se), np.exp(o.estimate + 1.96 * o.se)
    what = np.select([o.quantity == "direccion (24 modelos)", o.quantity == "direccion x origen (CN - US)"], ["direccion", "interaccion"], "por_origen")
    o["family"] = what; o["q_bh"] = np.nan; o["p_holm"] = np.nan
    for fam, ix in o.groupby("family").groups.items():
        o.loc[ix, "q_bh"] = bh(o.loc[ix, "p"].to_numpy()); o.loc[ix, "p_holm"] = holm(o.loc[ix, "p"].to_numpy())
    o["n_family"] = o.groupby("family")["family"].transform("size")
    joint = o.rename(columns={"pole": "country"})[["mode", "country", "quantity", "estimate", "se", "z", "p", "q_bh", "p_holm", "n_family", "OR", "OR_lo", "OR_hi",
                                                    "sd_model_slope", "sd_model", "sd_prompt", "singular", "optimizer", "variant", "formula_used", "messages", "nobs",
                                                    "seconds", "lme4_version", "r_version"]]
    # comparación con las cuatro díadas (bloque 46)
    allv = pd.read_csv(ALL_DYADS)
    cmp = joint[["mode", "country", "quantity", "OR", "OR_lo", "OR_hi", "p", "q_bh"]].merge(
        allv[["mode", "country", "quantity", "OR", "OR_lo", "OR_hi", "p", "q_bh"]], on=["mode", "country", "quantity"], suffixes=("_rivalidad", "_4diadas"))

    res = report.Result(
        NAME, "Figura 3, panel C con solo las díadas de rivalidad",
        "¿Cambia el efecto de la dirección (el país es el usuario contra el afectado) si en vez de las cuatro díadas de cada país se usan solo "
        "las dos de rivalidad (contra un rival y contra la otra potencia)?",
        status="computado a pedido de Nico (18/09); a decidir si reemplaza a la versión con cuatro díadas")
    res.inputs(list(d2.attrs["inputs"]) + [str(R_SCRIPT), str(HERE / "r" / "glmm_common.R"), str(ALL_DYADS)])
    res.data("D2 inglés, he / de / pg / control, 24 modelos; por país dos díadas × 2 direcciones × 192 prompts × 24 modelos (≈ 18.400 filas por modo).")
    res.method("Idéntico al bloque 46 (GLMM conjunto por país y modo, toward ± 0,5, origen centrado, dyad como efecto fijo), con dos díadas en vez de "
               "cuatro. BH y Holm por familia: 8 tests principales, 8 interacciones, 16 efectos por origen.")
    res.table("direction_glmm_rivalry", joint, "Modelo conjunto por país y modo con solo las díadas de rivalidad.")
    res.table("comparison_rivalry_vs_4dyads", cmp, "Lado a lado: OR, IC, p y q con las dos díadas de rivalidad y con las cuatro díadas (bloque 46).")
    res.figure("pD_direction_body_rivalry", body_fig(joint, MODES, "Efecto de la dirección con SOLO las díadas de rivalidad · 24 modelos · he, de, pg, control"),
               "Mismo formato que el panel C aprobado (bloque 46) pero con dos díadas por país: contra un rival y contra la otra potencia. OR > 1 = más rechazo "
               "cuando el país es el usuario. IC 95 % de Wald, sin corregir.")
    res.note("Registro: 4_analysis/results/27_fig3_notelab/NARRATIVA_F3.md.")
    res.conclusion("Computado a pedido de Nico; a decidir si reemplaza a la versión con cuatro díadas.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.set_option("display.width", 250)
    print(cmp.round(3).to_string(index=False))
    print("wrote", out)


if __name__ == "__main__":
    main()
