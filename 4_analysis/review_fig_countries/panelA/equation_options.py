#!/usr/bin/env python3
"""Revisión de la Figura 3 (19/09): tarjeta con las opciones de ecuaciones para el efecto de lado del panel A, con su
nivel de datos y qué problema resuelve cada una. Solo tipografía, sin datos.
Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_countries/panelA/equation_options.py
"""
from __future__ import annotations
import os, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans"})

# (letra, color, título, nivel, ecuaciones [líneas mathtext], qué resuelve)
BLOCKS = [
    ("A", "#777C83", "Exceso de |sesgo| sobre el azar  (el panel A de hoy)", "nivel modelo",
     [r"$\mathrm{excess}_m = |\mathrm{sesgo}_m| - E_0(n_m)$",
      r"$E_0(n) = \mathbb{E}\,|2a-n|/n,\quad a\sim\mathrm{Bin}(n,\frac{1}{2})\qquad\hat\theta=\frac{1}{24}\sum_m \mathrm{excess}_m$"],
     "peso IGUAL a cada modelo · sin signo · IC t entre modelos. No pondera por n ni por prompt."),
    ("B", "#2E7D5B", "Promedio ponderado con signo  (agrupar discordantes)", "nivel modelo",
     [r"$\mathrm{sesgo}_m=\dfrac{a_m-b_m}{n_m},\quad \mathrm{Var}(\mathrm{sesgo}_m)\approx 1/n_m$",
      r"$\hat\theta=\dfrac{\sum_m n_m\,\mathrm{sesgo}_m}{\sum_m n_m}=\dfrac{\sum_m a_m-\sum_m b_m}{\sum_m n_m}$"],
     "peso por n (inverso-varianza) · con signo · IC por bootstrap de prompts. Los modelos con más discordantes pesan más."),
    ("C", "#B68534", "Logit condicional / McNemar  (efecto fijo de prompt)", "nivel par",
     [r"$\mathrm{logit}\,P(\mathrm{refuse})=\alpha_{m,p}+\beta\cdot\mathrm{side}$",
      r"$\hat\beta=\log\dfrac{\sum_m a_m}{\sum_m b_m}\qquad \hat\beta_m=\log\dfrac{a_m}{b_m}$"],
     "el $\\alpha$ por prompt$\\times$modelo se CANCELA: es el FE de prompt exacto. Pesa por discordantes. Modelos fijos."),
    ("D", "#A44255", "GLMM  (el del bloque 45 / panel C)", "nivel fila",
     [r"$\mathrm{logit}\,P(\mathrm{refuse}_{m,p,c})=\beta_0+\beta_{\mathrm{side}}\,\mathrm{side}+\beta_{\mathrm{dyad}}\,\mathrm{dyad}+u_m+s_m\,\mathrm{side}+v_p$",
      r"$u_m,\,s_m\sim\mathcal{N}(0,\sigma^2)\ \text{(modelo)}\qquad v_p\sim\mathcal{N}(0,\sigma_v^2)\ \text{(prompt)}$"],
     "ataca los tres a la vez: n desigual (por precisión), prompt ($v_p$), heterogeneidad entre modelos ($s_m$). $+\\,\\beta_{\\mathrm{side}}\\times$origen para US/CN."),
    ("E", "#326CA0", "Meta-análisis de efectos aleatorios", "nivel modelo",
     [r"$\mathrm{sesgo}_m=\theta+\delta_m+\varepsilon_m$",
      r"$\delta_m\sim\mathcal{N}(0,\tau^2)\ \text{(heterogeneidad)}\qquad \varepsilon_m\sim\mathcal{N}(0,\,1/n_m)\ \text{(azar)}$"],
     "estima el efecto medio $\\theta$ y la heterogeneidad $\\tau^2$ pesando por precisión. No captura dependencia por prompts."),
]

fig = plt.figure(figsize=(13.5, 15))
fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.text(0.035, 0.975, "Opciones de ecuación para el efecto de lado (panel A, Figura 3)", fontsize=17, fontweight="bold")
ax.text(0.035, 0.957, "sesgo del modelo $m$:  $a_m$ = rechaza solo con usuario del lado USA,  $b_m$ = solo lado China,  "
        r"$n_m=a_m+b_m$ = pares discordantes", fontsize=10.5, color="#444")

y = 0.925
h = 0.172
for letra, color, titulo, nivel, eqs, resuelve in BLOCKS:
    ax.add_patch(plt.Rectangle((0.035, y - h + 0.012), 0.93, h - 0.02, facecolor=color, alpha=0.06,
                               edgecolor=color, lw=1.4, transform=ax.transAxes, zorder=0))
    ax.add_patch(plt.Circle((0.075, y - 0.018), 0.019, color=color, transform=ax.transAxes, zorder=2))
    ax.text(0.075, y - 0.018, letra, ha="center", va="center", color="white", fontsize=15, fontweight="bold", zorder=3)
    ax.text(0.105, y - 0.010, titulo, fontsize=13, fontweight="bold", va="center")
    ax.text(0.945, y - 0.010, nivel, fontsize=10.5, style="italic", color=color, ha="right", va="center")
    yy = y - 0.052
    for eq in eqs:
        ax.text(0.11, yy, eq, fontsize=13.5, va="center")
        yy -= 0.038
    ax.text(0.105, y - h + 0.036, "resuelve:  " + resuelve, fontsize=10, color="#333", va="center", wrap=True)
    y -= h

fig.savefig(HERE / "equation_options.png", dpi=150, bbox_inches="tight")
print("wrote", HERE / "equation_options.png")
