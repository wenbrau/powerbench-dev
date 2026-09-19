#!/usr/bin/env python3
"""Bloque 78 — Figura 1 rediseñada, CANDIDATA (no reemplaza a la compuesta del bloque 71 hasta que Nico la apruebe).

Pedido de Nico (19/09), textual y en orden:
  "falta un panel A bien descriptivo al principio que sea promedio de refusal por modo, promediando 24 modelos, con barras de
   error, similar a las barras del resto del paper, con los mismos colores, y agregando control en gris y power shifting medio en
   violeta."                                                                                                        -> A
  "el A actual puede ser un B, mucho más angosto y sin boxplots [...] barras con su error, para cada modo, incluyendo
   power-shifting medio, [...] en cada uno US vs China, y asterisco si difieren significativamente (aprovechando en cada uno todo
   el dato con GLMM o el test que corresponda a nuestro criterio del paper, no 12 puntos contra 12 puntos). Y la estadística
   además tiene que decir si hay un efecto general del origen del modelo en tasa de refusal media en general, y si eso depende
   de si es power shifting o no."                                                                                    -> B
  "B es demasiado ancho, podrían ser barras horizontales en vez de verticales, pero el panel con la misma altura, o sea barras
   mucho más finas."                                                                                                 -> C
  "C podría ser un solo panel en vez de 3, no separando por origen del modelo, promedio de 24 modelos en tres curvas con banda
   de error, para self empowerment, disempowerment, power grabbing y control. D podría ser exactamente lo mismo."     -> D, E
  "falta describir contexto y dominio aunque sea con algo chiquito, quizás tasa de refusal media para cada dominio y para cada
   contexto, como dos gráficos de barras horizontales con sus errores, y tests para ver cuáles son significativamente distintos
   de la media, como hicimos con los idiomas en la figura 4"                                                        -> F, G

Estadísticos (elecciones de Claude, anotadas en DECISIONES punto 38):
  - Niveles (A, B, D, E, F, G): tasa por modelo, media de los 24 (o de los 12 del origen), IC 95 % t entre modelos: el marco de
    modelos aleatorios, el mismo de las barras del resto del paper. Power shifting medio por modelo = media de he, de y pg (los
    modos están balanceados: equivale a la tasa sobre los 576 prompts).
  - B, asteriscos: GLMM de origen del bloque 30 (refuse ~ cn + (1 | prompt) + (1 | model) por modo; + mode en el pooled), con
    las q de BH del bloque 77 (familia = los 4 modos; pooled solo). Efecto general del origen sobre los cuatro modos: ajuste
    nuevo refuse ~ cn + mode + (1 | prompt) + (1 | model) (r/glmm_fig1_v3.R). Si depende de power shifting: el término cn × ps
    del ajuste E del bloque 30.
  - F, G: sobre las filas de power shifting, GLMM con contexto (dominio) en contrastes suma-cero: la desviación de cada nivel
    respecto de la media de los 8, Wald, BH sobre los 8 (r/glmm_fig1_v3.R). Es el análogo, en modelos aleatorios, del panel A
    de idioma (desviación respecto de la media de los 8 idiomas).
  - D, E: solo curvas con banda; los tests son los de los bloques 31 y 77.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_78_fig1_v3.py   [--reuse-glmm]   (≈ 2–4 min; requiere Rscript + lme4)
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
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import load_d1_english, file_digest  # noqa: E402

NAME = "78_fig1_v3"
R = HERE / "results"
SRC = {"origin": R / "30_fig1_glmm" / "glmm_origin.csv", "origin_x": R / "30_fig1_glmm" / "glmm_interaction_ps_vs_control.csv",
       "bh": R / "77_bh_fig1_fig2c" / "bh_families.csv", "model_mean": R / "70_fig1_model_mean_refusal" / "model_mean_refusal.csv"}
R_SCRIPT = HERE / "r" / "glmm_fig1_v3.R"
R_LIB = Path.home() / "R" / "win-library" / "4.6"
MODES = ["he", "de", "pg", "control"]
POWER = ["he", "de", "pg"]
PS = "power_shifting"
GROUPS = ["he", "de", "pg", "control", PS]
LABELS = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control", PS: "Power shifting\n(he + de + pg)"}
SHORT = {"he": "Self-emp.", "de": "Disemp.", "pg": "Power grab.", "control": "Control", PS: "Power shift.\n(mean)"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83", PS: "#5B3F8C"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
FACTORS = {"scale": ["individual", "group", "society"], "standing": ["low", "med", "high"]}
FACTOR_TITLE = {"scale": "escala del afectado", "standing": "standing del usuario"}
NL = chr(10)


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "axes.titlelocation": "left", "savefig.facecolor": "white"})


def letter(ax, s, dx=-40):
    ax.annotate(s, xy=(0, 1), xycoords="axes fraction", xytext=(dx, 10), textcoords="offset points", fontsize=15, fontweight="bold", va="bottom")


def find_rscript() -> str:
    exe = shutil.which("Rscript")
    if exe:
        return exe
    cands = sorted(glob.glob("C:/Program Files/R/R-*/bin/Rscript.exe"))
    if not cands:
        sys.exit("Rscript no encontrado: instalar R (winget install RProject.R) y lme4.")
    return cands[-1]


def tci(v):
    """media de los modelos e IC 95 % t entre modelos."""
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    half = stats.t.ppf(.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v))
    return float(v.mean()), float(v.mean() - half), float(v.mean() + half), int(len(v))


def fmt(x):
    return f"{x:.3f}".replace(".", ",")


def main():
    style()
    df = load_d1_english()
    d = df[df.valid].copy()
    need = {"model", "origin", "mode", "prompt_id", "refuse", "scale", "standing", "context", "domain"}
    assert need <= set(d.columns), f"faltan columnas: {need - set(d.columns)}"
    d["refuse"] = d.refuse.astype(float)
    models = sorted(d.model.unique()); origin = d.drop_duplicates("model").set_index("model").loc[models, "origin"]

    # ---- tasas por modelo y modo, + power shifting medio
    rm = d.groupby(["model", "mode"]).refuse.mean().unstack("mode").reindex(models)[MODES] * 100
    rm[PS] = rm[POWER].mean(axis=1)
    rm["origin"] = origin.values

    # ---- A: media de 24 por grupo
    A = pd.DataFrame([dict(group=g, **dict(zip(["mean", "lo", "hi", "n_models"], tci(rm[g])))) for g in GROUPS])
    # ---- B: por origen, con los tests de origen del bloque 30 (q del 77) y el ajuste general nuevo
    B = pd.DataFrame([dict(group=g, origin=o, **dict(zip(["mean", "lo", "hi", "n_models"], tci(rm[rm.origin == o][g])))) for g in GROUPS for o in ("US", "CN")])
    og = pd.read_csv(SRC["origin"]).set_index("fit"); bh = pd.read_csv(SRC["bh"])
    key = {"he": "A_he", "de": "A_de", "pg": "A_pg", "control": "A_control", PS: "B_power_shifting"}
    qmap = {}
    for g, k in key.items():
        lab = {"he": "he", "de": "de", "pg": "pg", "control": "control", PS: "power shifting (pooled)"}[g]
        row = bh[(bh.panel == "Figura 1 · origen") & bh.family.str.startswith("efecto CN − US") & (bh.test == lab)].iloc[0]
        qmap[g] = dict(cn_logodds=float(og.loc[k, "cn_logodds"]), cn_or=float(og.loc[k, "cn_odds_ratio"]), p=float(row.p), q=float(row.q_bh))
    Btest = pd.DataFrame([dict(group=g, **v) for g, v in qmap.items()])
    ox = pd.read_csv(SRC["origin_x"]).set_index("fit").loc["E_ps_vs_control"]

    # ---- C: refusal medio por modelo (bloque 70)
    C = pd.read_csv(SRC["model_mean"])

    # ---- D, E: tasa por modelo × nivel × modo; media de 24 con IC t
    lev_rows = []
    for fac, levels in FACTORS.items():
        g = d.groupby(["model", "mode", fac]).refuse.mean() * 100
        for mode in MODES:
            for lv in levels:
                v = g.xs((mode, lv), level=("mode", fac)).reindex(models)
                m, lo, hi, n = tci(v); lev_rows.append(dict(factor=fac, mode=mode, level=lv, mean=m, lo=lo, hi=hi, n_models=n))
    LV = pd.DataFrame(lev_rows)

    # ---- F, G: contexto y dominio, tasa de power shifting por modelo × nivel; media de 24 con IC t; GLMM de desviaciones
    dps = d[d["mode"].isin(POWER)]
    ctxs = sorted(d.context.unique()); doms = sorted(dps.domain.unique())
    cd_rows = []
    for fac, levels in (("context", ctxs), ("domain", doms)):
        g = dps.groupby(["model", fac]).refuse.mean() * 100
        for lv in levels:
            m, lo, hi, n = tci(g.xs(lv, level=fac).reindex(models)); cd_rows.append(dict(factor=fac, level=lv, mean=m, lo=lo, hi=hi, n_models=n))
    CD = pd.DataFrame(cd_rows)
    # GLMM en R: origen general (4 modos) + desviaciones por contexto y por dominio (power shifting)
    x = d[["refuse", "mode", "prompt_id", "model", "origin", "context", "domain"]].copy()
    x["refuse"] = x.refuse.astype(int); x["cn"] = (x.origin == "CN").astype(int)
    x["ctx"] = x.context.map({c: i + 1 for i, c in enumerate(ctxs)}); x["dom"] = x.domain.map({c: i + 1 for i, c in enumerate(doms)})
    x["dom"] = x.dom.fillna(0).astype(int)   # control no tiene dominio; solo se usa en las filas de power shifting
    raw = R / NAME / "glmm_fig1_v3_raw.csv"; raw_dev = R / NAME / "glmm_fig1_v3_raw.csv.dev.csv"
    if "--reuse-glmm" in sys.argv and raw.is_file() and raw_dev.is_file():
        o = pd.read_csv(raw); odev = pd.read_csv(raw_dev); print("GLMM: reusando", raw, flush=True)
    else:
        rscript = find_rscript()
        with tempfile.TemporaryDirectory() as tmp:
            fin, fout = Path(tmp) / "glmm_input.csv", Path(tmp) / "glmm_out.csv"
            x[["refuse", "mode", "prompt_id", "model", "cn", "ctx", "dom"]].to_csv(fin, index=False)
            env = dict(os.environ)
            if R_LIB.is_dir():
                env["R_LIBS_USER"] = str(R_LIB)
            proc = subprocess.run([rscript, str(R_SCRIPT), str(fin), str(fout)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
            print(proc.stdout, flush=True)
            if proc.returncode != 0:
                print(proc.stderr, file=sys.stderr); sys.exit(f"Rscript terminó con código {proc.returncode}")
            o = pd.read_csv(fout); odev = pd.read_csv(str(fout) + ".dev.csv")
        raw.parent.mkdir(parents=True, exist_ok=True); o.to_csv(raw, index=False); odev.to_csv(raw_dev, index=False)
    oa = o[(o.fit == "origin_all") & (o.term == "cn")].iloc[0]
    origin_all = dict(cn_logodds=float(oa.estimate), se=float(oa.se), p=float(oa.p), OR=float(np.exp(oa.estimate)),
                      OR_lo=float(np.exp(oa.estimate - 1.96 * oa.se)), OR_hi=float(np.exp(oa.estimate + 1.96 * oa.se)), singular=bool(oa.singular))
    for fac, levels, key_ in (("context", ctxs, "ctx_ps"), ("domain", doms, "dom_ps")):
        dv = odev[(odev.fit == key_) & (odev.kind == "dev")].set_index("level")
        for i, lv in enumerate(levels):
            r = dv.loc[i + 1]
            CD.loc[(CD.factor == fac) & (CD.level == lv), ["dev_logodds", "dev_se", "dev_p", "dev_q_bh", "glmm_singular"]] = [r.estimate, r.se, r.p, r.p_bh, bool(r.singular)]
    omni = odev[odev.kind == "omnibus"].set_index("fit")
    print(A.round(2).to_string(index=False)); print(B.round(2).to_string(index=False)); print(Btest.round(3).to_string(index=False))
    print("origen general:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in origin_all.items()}, "| cn × ps (bloque 30 E): p =", round(float(ox.cnxps_p), 3))
    print(CD.round(3).to_string(index=False), flush=True)

    res = report.Result(
        NAME, "Figura 1 rediseñada (candidata): medias por modo, origen por modo, modelos, escala y standing como curvas, contexto y dominio",
        "Rediseño pedido por Nico (19/09): A media de refusal por modo (24 modelos); B US vs CN por modo con el test de origen; C refusal "
        "medio por modelo en barras horizontales; D y E escala y standing como curvas con banda; F y G contexto y dominio con desviaciones "
        "respecto de la media. ¿Hay un efecto general del origen y depende de power shifting?",
        status="CANDIDATA a pedido de Nico (19/09); no reemplaza a la compuesta 71 hasta que la apruebe")
    res.inputs(list(df.attrs["inputs"]) + [str(v.relative_to(ROOT)) for v in SRC.values()] + [str(R_SCRIPT.relative_to(ROOT)), str((HERE / "r" / "glmm_common.R").relative_to(ROOT))])
    res.data(f"D1 inglés + control, 24 modelos, {len(d):,} filas válidas. Power shifting medio por modelo = media de he, de y pg.")
    res.method("Niveles: tasa por modelo, media de los modelos e IC 95 % t entre modelos (A, B, D, E, F, G). B: asterisco si el GLMM de origen del "
               "bloque 30 da q < 0,05 (BH del bloque 77, familia = 4 modos; pooled solo). Efecto general del origen: GLMM nuevo refuse ~ cn + mode + "
               "(1 | prompt) + (1 | model) sobre los cuatro modos; dependencia de power shifting: cn × ps del ajuste E del bloque 30.")
    res.method("F, G: sobre las filas de power shifting, GLMM refuse ~ nivel (contrastes suma-cero) + mode + (1 | model) + (1 | model:nivel) + (1 | prompt); "
               "desviación de cada nivel respecto de la media de los 8 en log-odds, Wald, BH sobre los 8; ómnibus χ²(7). nAGQ = 0 como el resto.")
    res.table("pA_mean_by_mode", A, "A: media de refusal por grupo, IC t entre 24 modelos.")
    res.table("pB_by_origin", B.merge(Btest, on="group", how="left"), "B: media por origen y grupo con IC t entre 12 modelos; efecto CN − US del GLMM del bloque 30 con su p y q.")
    res.table("origin_overall_glmm", pd.DataFrame([dict(**origin_all, cn_x_ps_logodds=float(ox.cnxps_logodds), cn_x_ps_p=float(ox.cnxps_p), cn_x_ps_source="bloque 30, ajuste E")]),
              "Efecto general del origen (CN − US) sobre los cuatro modos, y su dependencia de power shifting (interacción del bloque 30).")
    res.table("pDE_levels", LV, "D, E: media de 24 por modo y nivel de escala / standing, IC t.")
    res.table("pFG_context_domain", CD, "F, G: media de power shifting por contexto y por dominio (IC t entre modelos) y desviación GLMM respecto de la media de los 8 con p y q.")
    res.table("glmm_omnibus", omni.reset_index()[["fit", "estimate", "df", "p", "singular", "variant"]].rename(columns={"estimate": "wald_chi2"}), "Ómnibus χ²(7) de contexto y de dominio.")
    res.table("rates_per_model", rm.reset_index(), "Tasas por modelo y grupo (%).", show=False)
    res.stat("origin_overall_OR", origin_all["OR"], origin_all["OR_lo"], origin_all["OR_hi"], origin_all["p"], unit="OR CN / US",
             note=f"cuatro modos; cn × ps (bloque 30 E) p = {float(ox.cnxps_p):.3f}")

    # ================================================================== figura
    # Segunda vuelta (Nico, 19/09): "en A no tiene sentido la barra de power shifting, eliminemosla"; "C puede ser MUCHÍSIMO menos alta,
    # misma altura que A y B, las barras más juntas"; "D y E [...] si power grabbing y disempowerment dan significativos en su subida en
    # escala, mostremos eso"; "F y G más angostos para estar en la segunda fila de paneles al lado de D y E, 4 paneles en esa fila".
    def fq(q):
        return "q < 0,001" if q < .001 else f"q = {fmt(q)}"

    bhq = {}
    for fac, pan in (("scale", "Figura 1 · C escala"), ("standing", "Figura 1 · D standing")):
        sub = bh[(bh.panel == pan) & bh.family.str.startswith(f"pendiente de {fac} por modo")]
        bhq[fac] = dict(zip(sub.test, sub.q_bh))
    # Tercera vuelta (Nico, 19/09): "C puede ser menos ancha [...] aprox 2/3 de su ancho actual"; "menos espacio entre F y G y quizás ambas menos anchas".
    fig = plt.figure(figsize=(17, 10.5), layout="constrained")
    fig.get_layout_engine().set(hspace=.04, wspace=.0, w_pad=.04, h_pad=.04)
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.05])
    gs1 = gs[0].subgridspec(1, 3, width_ratios=[1, 1.2, 1.6], wspace=.05)
    gs2 = gs[1].subgridspec(1, 4, width_ratios=[1.15, 1.15, .85, .85], wspace=.06)
    # ---- A (sin power shifting)
    ax = fig.add_subplot(gs1[0, 0]); xa = np.arange(len(MODES)); Aa = A.set_index("group").loc[MODES]
    ax.bar(xa, Aa["mean"], width=.62, color=[MODE_COLORS[g] for g in MODES], zorder=2)
    ax.errorbar(xa, Aa["mean"], yerr=[Aa["mean"] - Aa.lo, Aa.hi - Aa["mean"]], fmt="none", ecolor="#222", elinewidth=1.2, capsize=3, zorder=3)
    ax.set_xticks(xa, [SHORT[g] for g in MODES], fontsize=9); ax.set_ylabel("Refusal (%) · media de 24 modelos"); ax.grid(axis="y", alpha=.15)
    ax.set_title("Refusal por modo", fontsize=10); letter(ax, "A")
    # ---- B
    ax = fig.add_subplot(gs1[0, 1]); x = np.arange(len(GROUPS)); wd = .38
    for k, o in enumerate(("US", "CN")):
        t = B[B.origin == o].set_index("group").loc[GROUPS]; xo = x + (k - .5) * wd
        ax.bar(xo, t["mean"], width=wd, color=[MODE_COLORS[g] for g in GROUPS], alpha=.5 if o == "US" else .95, edgecolor=[MODE_COLORS[g] for g in GROUPS], lw=1, zorder=2)
        ax.errorbar(xo, t["mean"], yerr=[t["mean"] - t.lo, t.hi - t["mean"]], fmt="none", ecolor="#222", elinewidth=1.1, capsize=3, zorder=3)
    for xi, g in zip(x, GROUPS):
        q = qmap[g]["q"]; top = float(B[B.group == g].hi.max())
        ax.text(xi, top + .8, ("*" if q < .05 else "") + fq(q), ha="center", va="bottom", fontsize=7)
    ax.legend(handles=[Patch(facecolor="#888", alpha=.5, edgecolor="#888", label="US (12)"), Patch(facecolor="#888", alpha=.95, label="CN (12)")], frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0, .82))
    ax.set_xticks(x, [SHORT[g] for g in GROUPS], fontsize=8.5); ax.set_ylabel("Refusal (%) · media de 12"); ax.grid(axis="y", alpha=.15)
    ax.set_title("US vs CN por modo", fontsize=10); letter(ax, "B")
    ax.set_ylim(0, float(B.hi.max()) * 1.95)
    ax.text(.99, .985, ("q = GLMM de origen por modo, BH" + NL + f"origen, cuatro modos: OR CN/US {origin_all['OR']:.2f} [{origin_all['OR_lo']:.2f}; {origin_all['OR_hi']:.2f}], p = {origin_all['p']:.3f}" + NL +
                        f"origen × power shifting: log-odds {float(ox.cnxps_logodds):+.2f}, p = {float(ox.cnxps_p):.3f}").replace(".", ","),
            transform=ax.transAxes, ha="right", va="top", fontsize=7, bbox=dict(boxstyle="round,pad=.25", fc="white", ec="#CCCCCC"))
    # ---- C: modelos, barras horizontales finas, misma altura que A y B
    ax = fig.add_subplot(gs1[0, 2])
    Cs = pd.concat([C[C.origin == "US"].sort_values("mean_all", ascending=False), C[C.origin == "CN"].sort_values("mean_all", ascending=False)])
    y = np.arange(len(Cs))[::-1]
    ax.barh(y, Cs.mean_all, height=.8, color=[ORIGIN[o] for o in Cs.origin], zorder=2)
    for yi, (_, r) in zip(y, Cs.iterrows()):
        ax.text(r.mean_all + .3, yi, f"{r.mean_all:.1f}".replace(".", ","), va="center", ha="left", fontsize=6.5)
    ax.set_yticks(y, Cs.model, fontsize=7); ax.tick_params(axis="y", length=0)
    for tk, o in zip(ax.get_yticklabels(), Cs.origin):
        tk.set_color(ORIGIN[o])
    ax.axhline(len(Cs) - 12.5, color="#999", lw=.8, ls=":"); ax.set_ylim(-.7, len(Cs) - .3)
    ax.set_xlabel("Refusal medio (%) · promedio de los cuatro modos", fontsize=9); ax.grid(axis="x", alpha=.15); ax.set_xlim(0, float(Cs.mean_all.max()) * 1.12)
    ax.set_title("Refusal medio por modelo", fontsize=10); letter(ax, "C", -80)
    # ---- D, E: curvas con banda y la q de la pendiente lineal por modo (bloque 31, BH del 77)
    for j, fac in enumerate(("scale", "standing")):
        ax = fig.add_subplot(gs2[0, j]); lv = LV[LV.factor == fac]; xs = np.arange(3)
        for mode in MODES:
            t = lv[lv["mode"] == mode].set_index("level").loc[FACTORS[fac]]
            q = bhq[fac].get(mode)
            ax.plot(xs, t["mean"], marker="o", color=MODE_COLORS[mode], lw=2, label=LABELS[mode] + (f" · pendiente {fq(q)}" if q is not None else ""), zorder=3)
            ax.fill_between(xs, t.lo, t.hi, color=MODE_COLORS[mode], alpha=.15, zorder=2)
        ax.set_xticks(xs, [s_.capitalize() for s_ in FACTORS[fac]]); ax.set_ylabel("Refusal (%) · media de 24 modelos" if j == 0 else "")
        ax.set_xlabel(FACTOR_TITLE[fac] + NL + "banda = IC 95 % t entre modelos · q = pendiente GLMM, BH", fontsize=8.5)
        ax.grid(axis="y", alpha=.15); ax.legend(frameon=False, fontsize=7.5, loc="upper left")
        ax.set_title(f"Refusal por {FACTOR_TITLE[fac]}", fontsize=10); letter(ax, "DE"[j])
    # ---- F, G: contexto y dominio, barras horizontales, asterisco = desviación GLMM q < 0,05
    for j, (fac, title) in enumerate((("context", "contexto"), ("domain", "dominio"))):
        ax = fig.add_subplot(gs2[0, 2 + j]); t = CD[CD.factor == fac].sort_values("mean", ascending=True); y = np.arange(len(t))
        ax.barh(y, t["mean"], height=.82, color=MODE_COLORS[PS], alpha=.85, zorder=2)
        ax.errorbar(t["mean"], y, xerr=[t["mean"] - t.lo, t.hi - t["mean"]], fmt="none", ecolor="#222", elinewidth=1.1, capsize=3, zorder=3)
        ax.set_ylim(-.6, len(t) - .4)
        gm = float(t["mean"].mean()); ax.axvline(gm, color="black", lw=.9, ls="--", zorder=1)
        for yi, (_, r) in zip(y, t.iterrows()):
            ax.text(r.hi + .4, yi, ("* " if r.dev_q_bh < .05 else "") + fq(r.dev_q_bh), va="center", ha="left", fontsize=7)
        ax.set_yticks(y, t.level, fontsize=8.5); ax.grid(axis="x", alpha=.15)
        ax.set_xlim(0, float(t.hi.max()) * 1.45)
        om = omni.loc["ctx_ps" if fac == "context" else "dom_ps"]
        ax.set_title(f"Power shifting por {title}", fontsize=10); letter(ax, "FG"[j], -70)
        ax.set_xlabel(("Refusal de power shifting (%) · media de 24" + NL + "q = desv. vs media (GLMM, BH)" + NL + f"ómnibus p = {float(om.p):.3f}").replace(".", ","), fontsize=7.5)
    fig.suptitle("Figura 1 (candidata) · D1 inglés · 24 modelos (12 US, 12 CN)", fontsize=12)
    res.figure("figure1_v3_candidate", fig,
               "A: media de refusal por modo, más el control (gris), IC t entre los 24 modelos. B: lo mismo por origen del modelo con power shifting "
               "medio (violeta), US claro y CN oscuro, con la q del GLMM de origen (bloque 30, BH del 77) y, en el recuadro, el efecto general del "
               "origen sobre los cuatro modos y su interacción con power shifting. C: refusal medio por modelo. D, E: escala y standing como curvas "
               "por modo con banda t y la q de la pendiente lineal (bloque 31, BH del 77). F, G: refusal de power shifting por contexto y dominio; "
               "q = desviación respecto de la media de los 8 (GLMM).")
    res.note("Fuente de verdad: notebooks/PowerBench.md. Registro: 4_analysis/results/25_fig1_notelab/NARRATIVA_F1.md. Compuesta vigente: bloque 71.")
    res.conclusion("Candidata; decisión de Nico pendiente.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) if (ROOT / p).is_file() else None for p in res._inputs},
            "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
