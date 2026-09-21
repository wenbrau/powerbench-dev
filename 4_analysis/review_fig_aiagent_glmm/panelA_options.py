#!/usr/bin/env python3
"""Cuatro formas de dibujar el panel A de la figura de IA una vez que el Δ viene del GLMM (pregunta de Wendy 2026-09-20:
"los Δ son con GLMM, pero los IC no, ¿cierto? ¿cómo graficás IC si el GLMM estima cambio, no promedio de refusal?").
Datos reales: barras observadas (54 levels_pooled), Δ GLMM (85), Δ bootstrap (22)."""
import sys; from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; import numpy as np, pandas as pd
R = ROOT / "4_analysis/results"
lv = pd.read_csv(R / "54_fig4_levels_box/levels_pooled.csv"); G = pd.read_csv(R / "85_fig3a_glmm/ai_glmm_main.csv").set_index("mode")
bt = pd.read_csv(R / "22_d3_ai_final/paired_pooled.csv"); bt = bt[(bt.bloc == "all") & (bt.contrast == "ai_minus_human")].set_index("mode")
MODES = ["he", "de", "pg", "control"]; LAB = {"he": "Self-emp.", "de": "Disemp.", "pg": "Power grab.", "control": "Control"}
COL = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83"}
hum = lv[lv.condition == "human"].set_index("mode").estimate; ai = lv[lv.condition == "ai"].set_index("mode").estimate
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left"})
fig, axes = plt.subplots(2, 2, figsize=(15, 10.5), sharey=True, layout="constrained"); axes = axes.ravel(); x = np.arange(4); w = .34
titles = ["1 · barras observadas; al lado de IA, un PUNTO en (humano + Δ del GLMM)\ncon el bigote del IC del Δ  (recomendada)",
          "2 · como está ahora: barras observadas; el bigote del IC del Δ GLMM\nva centrado en la barra IA (la brecha visual ≠ Δ)",
          "3 · barras = niveles marginales del GLMM (NO son las tasas observadas);\nbigote = IC del Δ; la brecha sí es el Δ",
          "4 · volver al bootstrap: barras observadas, Δ e IC del bootstrap\n(coinciden con la brecha), y decir que el test es el GLMM"]
for k, (ax, t) in enumerate(zip(axes, titles)):
    for i, m in enumerate(MODES):
        c = COL[m]; g = G.loc[m]; b = bt.loc[m]
        h, a = (g.p_human_pp, g.p_ai_pp) if k == 2 else (hum[m], ai[m])
        ax.bar(x[i] - w/2, h, w, color=c, alpha=.45, edgecolor=c); ax.bar(x[i] + w/2, a, w, color=c, alpha=.95, edgecolor=c)
        ax.plot([x[i] - w, x[i] + w], [h, h], ls="--", lw=.8, color="#555")
        if k == 0:
            y = hum[m] + g.delta_pp; ax.errorbar(x[i] + w/2 + .28, y, yerr=[[g.delta_pp - g.delta_lo], [g.delta_hi - g.delta_pp]], fmt="o", ms=5, color="#222", capsize=3, lw=1.3)
            ax.text(x[i] + w/2 + .36, y, f"Δ {g.delta_pp:+.1f}\n[{g.delta_lo:+.1f}; {g.delta_hi:+.1f}]".replace(".", ","), fontsize=8, va="center")
        elif k in (1, 2):
            ax.errorbar(x[i] + w/2, a, yerr=[[g.delta_pp - g.delta_lo], [g.delta_hi - g.delta_pp]], fmt="none", ecolor="#222", capsize=3, lw=1.3)
            ax.text(x[i] + w/2, a + (g.delta_hi - g.delta_pp) + 1, f"Δ {g.delta_pp:+.1f}\n[{g.delta_lo:+.1f}; {g.delta_hi:+.1f}]".replace(".", ","), fontsize=8, ha="center", va="bottom")
        else:
            ax.errorbar(x[i] + w/2, a, yerr=[[b.estimate - b.lo], [b.hi - b.estimate]], fmt="none", ecolor="#222", capsize=3, lw=1.3)
            ax.text(x[i] + w/2, a + (b.hi - b.estimate) + 1, f"Δ {b.estimate:+.1f}\n[{b.lo:+.1f}; {b.hi:+.1f}]".replace(".", ","), fontsize=8, ha="center", va="bottom")
    ax.set_xticks(x, [LAB[m] for m in MODES]); ax.set_title(t, fontsize=10.5); ax.grid(axis="y", alpha=.15); ax.set_ylim(0, 45)
axes[0].set_ylabel("Refusal (%) · claro = humano, oscuro = IA"); axes[2].set_ylabel("Refusal (%) · claro = humano, oscuro = IA")
fig.suptitle("Panel A de la figura de IA: cuatro formas de dibujar el Δ y su IC ahora que salen del GLMM · números reales", fontsize=12)
out = Path(__file__).with_name("panelA_options.png"); fig.savefig(out, dpi=150); print("wrote", out)
