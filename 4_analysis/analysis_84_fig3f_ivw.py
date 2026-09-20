#!/usr/bin/env python3
"""Bloque 84 — Figura 3 (agente IA), panel F: el punto de cada modelo para "power shifting" pasa de la MEDIA SIMPLE de sus tres
log-OR por modo (bloque 64, `power_shifting_mean_of_modes`) a la combinación por INVERSA DE LA VARIANZA de esos tres log-OR
(Mantel-Haenszel entre modos): cada modo pesa por su información, y self-empowerment (5–8 rechazos en 168 prompts) deja de valer 1/3.

Nico (20/09): "no me gusta que SE pese un montón y sea solo ruido" → "esta nueva versión pareciera la mejor" → "ok, perfecto entonces
aprobado". Regla para métodos (misma conversación): power shifting junta los tres modos de poder; las tasas se calculan sobre todos
sus prompts (mismo n por modo); los efectos como un efecto común estratificado por modo (el GLMM con `mode` como efecto fijo; por
modelo, esta combinación; para la dirección pareada, los discordantes sumados). Los efectos por modo quedan en el apéndice como
chequeo de homogeneidad (OR 1,97 / 2,19 / 2,09).

Sin cálculos nuevos de test: la recta y el recuadro de F siguen siendo el GLMM pooled del bloque 64 con la q del bloque 83. Este
bloque solo re-pondera los log-OR por modo que ya están en `64/capability_per_model_log_or.csv` y escribe la tabla que consumen
`analysis_65_fig4_composite.py` y `paper_figures/figure3_aiagent_paper.py`.

Ejecutar desde la raíz del repo:  python 4_analysis/analysis_84_fig3f_ivw.py     (segundos; sin API)
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
from matplotlib.lines import Line2D  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pbanalysis import report  # noqa: E402
from pbanalysis.final_panel import file_digest  # noqa: E402

NAME = "84_fig3f_ivw"
SRC = {"pm": HERE / "results" / "64_fig4_capability_glmm" / "capability_per_model_log_or.csv",
       "glmm": HERE / "results" / "64_fig4_capability_glmm" / "capability_glmm.csv",
       "cap": HERE / "results" / "30_fig1_glmm" / "capability_index.csv",
       "bh83": HERE / "results" / "83_bh_fig3f_fig2b" / "bh_families.csv"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
MODES_PS = ["he", "de", "pg"]


def main():
    pm = pd.read_csv(SRC["pm"]); g = pd.read_csv(SRC["glmm"]); g = g[g.run == "pooled"]
    cap = pd.read_csv(SRC["cap"]).set_index("model")["index"]; mu, sd = cap.mean(), cap.std(ddof=1)
    q83 = pd.read_csv(SRC["bh83"]); q83 = q83[(q83.block == 64) & (q83.n_family == 2)].set_index("test").q_bh
    m = pm[pm.set.isin(MODES_PS)].copy(); m["w"] = 1 / m.se ** 2
    rows = []
    for model, s in m.groupby("model"):
        s = s.set_index("set").loc[MODES_PS]; W = s.w.sum()
        rows.append(dict(model=model, origin=s.origin.iloc[0], capability=float(s.capability.iloc[0]), cap_z=float(s.cap_z.iloc[0]), set="power_shifting_ivw",
                         log_or=float((s.w * s.log_or).sum() / W), se=float(np.sqrt(1 / W)),
                         w_he=float(s.loc["he", "w"] / W), w_de=float(s.loc["de", "w"] / W), w_pg=float(s.loc["pg", "w"] / W),
                         log_or_mean3=float(s.log_or.mean())))
    ivw = pd.DataFrame(rows)
    ctl = pm[pm.set == "control"][["model", "origin", "capability", "cap_z", "set", "log_or", "se"]].copy()
    tab = pd.concat([ivw, ctl], ignore_index=True)
    old = pm[pm.set == "power_shifting_mean_of_modes"].set_index("model")
    print(ivw.sort_values("capability")[["model", "origin", "capability", "log_or_mean3", "log_or", "se", "w_he"]].round(3).to_string(index=False))
    print(f"peso de self-empowerment: mediana {ivw.w_he.median():.3f}, min {ivw.w_he.min():.3f}, max {ivw.w_he.max():.3f}; SE mediana {old.se.median():.3f} -> {ivw.se.median():.3f}")

    res = report.Result(
        NAME, "Figura 3, panel F: log-OR IA vs humano por modelo, los tres modos de poder combinados por inversa de la varianza",
        "¿Cómo queda el punto de 'power shifting' de cada modelo si los tres log-OR por modo se combinan por su información en vez de "
        "promediarlos con peso igual? Sin cambios en el GLMM ni en el test (bloques 64 y 83).",
        status="APROBADO por Nico (20/09): reemplaza a power_shifting_mean_of_modes del bloque 64 en la Figura 3 F")
    res.inputs([str(v.relative_to(ROOT)) for v in SRC.values()])
    res.data("Los log-OR por modo y modelo del bloque 64 (Haldane +0,5, sobre las tasas IA y humano de cada modo; 168 prompts por modo), 24 modelos.")
    res.method("Por modelo: log-OR_ps = Σ w_m · log-OR_m / Σ w_m con w_m = 1/SE_m², SE_ps = 1/√Σ w_m (combinación de efectos fijos entre estratos, "
               "como Mantel-Haenszel). Control: sin cambios. Recta y recuadro de la figura: GLMM pooled del bloque 64 (refuse ~ ai × cap_z + mode + "
               "(1 + ai || model) + (1 | prompt)), marginalizada sobre prompts como en el 64; q del bloque 83 (familia = power shifting y control).")
    res.table("capability_per_model_log_or_ivw", tab, "Por modelo: log-OR de power shifting combinado por inversa de la varianza (con el peso de cada modo y la media simple anterior) y el del control.")
    res.stat("w_he_median", float(ivw.w_he.median()), unit="peso de self-empowerment en el punto", note=f"min {ivw.w_he.min():.3f}, max {ivw.w_he.max():.3f}; antes 1/3")
    res.stat("se_median_ivw", float(ivw.se.median()), unit="SE por punto", note=f"media simple: {old.se.median():.3f}")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left"})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), layout="constrained", sharey=True)
    for ax, st, key, title in zip(axes, ("power_shifting_ivw", "control"), ("power_shifting", "control"), ("Capacidad · power shifting (he + de + pg)", "Capacidad · control")):
        d = tab[tab.set == st]
        for org in ("US", "CN"):
            s = d[d.origin == org]
            ax.errorbar(s.capability, s.log_or, yerr=1.96 * s.se, fmt="o", color=ORIGIN[org], ecolor=ORIGIN[org], elinewidth=.8, alpha=.75, ms=5, capsize=2, zorder=3)
        fr = g[g.set == key].set_index("quantity"); ai, it = fr.loc["ai (capacidad media)"], fr.loc["ai x capacidad (por 1 SD)"]
        att = float(np.sqrt(1 + (16 * np.sqrt(3) / (15 * np.pi)) ** 2 * ai.sd_prompt ** 2))
        xs = np.linspace(d.capability.min() - 1, d.capability.max() + 1, 50); zs = (xs - mu) / sd
        ax.plot(xs, (ai.estimate + it.estimate * zs) / att, color="#222222", lw=1.8, zorder=4)
        ax.axhline(0, color="black", lw=.8, ls=":", zorder=1); ax.grid(alpha=.15); ax.set_title(title, fontsize=10)
        ax.text(.03, .03, (f"GLMM: razón de OR por SD {it.OR_or_ratio:.2f} [{it.lo:.2f}; {it.hi:.2f}]\nq = {float(q83[key]):.3f}" + ("  ·  ajuste singular" if bool(it.singular) else "")).replace(".", ","),
                transform=ax.transAxes, ha="left", va="bottom", fontsize=8, bbox=dict(boxstyle="round,pad=.3", fc="white", ec="#CCCCCC"))
        ax.set_xlabel("índice de capacidad (GPQA-D + MMLU-Pro, %)")
    axes[0].set_ylabel("log-OR de refusal IA vs humano por modelo (IC 95 %)")
    axes[1].legend(handles=[Line2D([], [], marker="o", ls="", color=ORIGIN["US"], label="modelo US"), Line2D([], [], marker="o", ls="", color=ORIGIN["CN"], label="modelo CN"),
                            Line2D([], [], color="#222222", lw=1.8, label="recta del GLMM (bloque 64, marginalizada)")], frameon=False, fontsize=8, loc="upper left")
    res.figure("pF_capability_ivw", fig, "Panel F: puntos = log-OR por modelo con los tres modos de poder combinados por inversa de la varianza (izquierda) y control (derecha); "
               "recta = GLMM pooled del bloque 64 marginalizada sobre prompts; recuadro = razón de OR por SD y q (bloque 83).")
    res.note("Registro: 53_fig4_notelab/NARRATIVA_F4.md (20/09); DECISIONES punto 45 (e); RESULTADOS_CONSOLIDADOS.md flag 3.")
    res.conclusion("Con pesos por información, self-empowerment pesa una décima parte del punto y la recta del GLMM queda dentro de la nube; nada cambia en el test.")
    out = res.write()
    prov = {"inputs": {p: file_digest(ROOT / p) for p in res._inputs}, "code": {str(Path(__file__).relative_to(ROOT)): file_digest(__file__)}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
