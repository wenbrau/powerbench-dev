#!/usr/bin/env python3
"""Figura 4 (idiomas), versión 2 del 20/09 sobre la compuesta de Wendy (figure_full.py --cd ps): los cambios que pidió Nico.

  A1  refusal por idioma y modo con el GLMM (Wendy, panelA_final_glmm)                  igual
  A2  ORDEN de los idiomas por modo, bump chart de posiciones (bloque 81)                REEMPLAZA al heatmap idioma × idioma del bloque 79
  B   B1/B2 en un panel: Spearman entre los órdenes de los modos de power shifting, y del control contra el consenso (bloque 81)   NUEVO
  C   exceso del rango sobre el azar, peso igual y por pedidos (Wendy, panelB)           antes B
  D   exceso sobre el azar por modelo, power shifting (Wendy, panelD F6_exceso_ps)       antes D
  E   acuerdo entre modelos en el ranking de idiomas, power shifting (Wendy, panelC)    antes C
Nico (20/09): "quizás A2 se va y en vez de eso tiene que quedar esto [el bump] y las barras que te digo como B1 y B2; y así desplazar a las
que sigan en su letra"; "La D tiene que ser la C porque también es magnitud del sesgo, solo que desglosado entre modelos"; "la D (que debería
ser la actual C)". Lectura de ese orden: C = rango (magnitud), D = exceso por modelo (magnitud desglosada), E = acuerdo entre modelos.

No calcula nada: junta PNG ya producidos (los tiles a 300 dpi de Wendy en _hires/ y los del bloque 81 en results/). Fila 1 = A1 | A2 | B;
fila 2 = C | D | E. Salida: figure_full_v2_ps.png en esta carpeta. No toca figure_full.py ni figure_full_ps.png.
Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_languages/figure_full_v2.py
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

R81 = ROOT / "4_analysis" / "results" / "81_fig2_mode_rank_concordance"
SRC = {"A1": HERE / "_hires" / "A1.png",
       "A2": R81 / "panel_bump_position_hires.png",
       "B": R81 / "panel_concordance_bars_hires.png",
       "C": HERE / "_hires" / "B.png",
       "D": HERE / "panelD" / "F6_exceso_ps.png",
       "E": HERE / "panelC" / "panelC_final_power_shifting.png"}
OUT = HERE / "figure_full_v2_ps.png"
GAP, MARGIN, W = 40, 30, 4200


def main():
    imgs = {k: Image.open(v).convert("RGB") for k, v in SRC.items()}
    ar = {k: im.width / im.height for k, im in imgs.items()}
    inner = W - 2 * MARGIN
    h1 = (inner - 2 * GAP) / (ar["A1"] + ar["A2"] + ar["B"])
    h2 = (inner - 2 * GAP) / (ar["C"] + ar["D"] + ar["E"])
    H = int(2 * MARGIN + h1 + GAP + h2)
    dpi = 200
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi); fig.patch.set_facecolor("white")

    def place(k, x, y, h):
        w = ar[k] * h
        ax = fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])
        ax.imshow(imgs[k].resize((int(round(w)), int(round(h))), Image.LANCZOS)); ax.axis("off")
        fig.text((x - 4) / W, 1 - (y + 6) / H, k, fontsize=26, fontweight="bold", ha="left", va="top")
        return x + w + GAP

    x, y = MARGIN, MARGIN
    for k in ("A1", "A2", "B"):
        x = place(k, x, y, h1)
    x, y = MARGIN, MARGIN + h1 + GAP
    for k in ("C", "D", "E"):
        x = place(k, x, y, h2)
    fig.savefig(OUT, dpi=dpi, facecolor="white")
    print(f"wrote {OUT}  ({W}x{H} px)")
    for k, v in SRC.items():
        print(f"  {k}: {v.relative_to(ROOT)}  {imgs[k].size}")


if __name__ == "__main__":
    main()
