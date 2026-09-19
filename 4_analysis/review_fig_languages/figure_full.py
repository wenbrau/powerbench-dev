#!/usr/bin/env python3
"""Revisión de la figura de idiomas (19/09, pedido de Wendy): la figura completa con los paneles revisados del día más el
heatmap idioma × idioma de Nico (bloque 79). Salida: figure_full_pg.png / figure_full_ps.png en esta carpeta (no toca results/).
FINAL POR AHORA (Wendy 19/09, notebooks/PowerBench.md): figure_full_ps.png — C y D sobre power shifting (he + de + pg), que es
más general. figure_full_pg.png es la variante con C y D solo sobre power grabbing. Los paneles C y D separados por modo (he, de,
pg, control) van a un apéndice: figure_appendix_CD_by_mode.py.

  A1  panel A final con IC del GLMM (modelos aleatorios)      panelA/panelA_final_glmm.py
  A2  sesgo idioma contra idioma, power shifting (bloque 79)   4_analysis/analysis_79_fig2_language_pairwise_bias.py
  B   exceso del rango, peso igual vs peso por requests        panelB/panelB_weighted_requests.py
  C   acuerdo entre modelos en el ranking de idiomas, pg       panelC/panelC_with_tests.py
  D   exceso sobre el azar por modelo, pg (F6)                 panelD/F6_exceso_pg.py

No calcula nada: junta las figuras ya producidas por esos scripts. Fila 1 = A1 | A2; fila 2 = B | C | D. A1 y B se
re-renderizan a 300 dpi corriendo el script original con `fig.savefig` redirigido a `_hires/` (mismo código, misma
tabla; el PNG original no se toca). A2, C y D entran desde su PNG existente (el bloque 79 reescribe provenance si se
corre; C y D tardan minutos por las permutaciones). `--no-rerender` usa los cinco PNG tal cual. Los títulos internos
de cada panel son los de sus scripts.

Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_languages/figure_full.py [--no-rerender] [--cd pg|ps]
  --cd ps   (pedido de Wendy 19/09) C y D sobre power shifting = he + de + pg juntos (panelC_final_power_shifting.png,
            F6_exceso_ps.png) en vez de power grabbing; salida figure_full_ps.png (la final por ahora). Default pg → figure_full_pg.png.
"""
from __future__ import annotations

import os
import runpy
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.figure as mfig  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

_argv = sys.argv[1:]
CD = _argv[_argv.index("--cd") + 1] if "--cd" in _argv else "pg"
assert CD in ("pg", "ps"), CD
SRC = {
    "A1": HERE / "panelA" / "panelA_final_glmm.png",
    "A2": ROOT / "4_analysis" / "results" / "79_fig2_language_pairwise_bias" / "pairwise_bias_power_shifting.png",
    "B": HERE / "panelB" / "panelB_weighted_requests.png",
    "C": HERE / "panelC" / ("panelC_final_pg.png" if CD == "pg" else "panelC_final_power_shifting.png"),
    "D": HERE / "panelD" / f"F6_exceso_{CD}.png",
}
RERENDER = {  # panel -> (script, argv) ; se re-renderizan a 300 dpi en HERE/_hires/
    "A1": (HERE / "panelA" / "panelA_final_glmm.py", []),
    "B": (HERE / "panelB" / "panelB_weighted_requests.py", ["--plot-only"]),
}
HIRES_DPI = 300
OUT = HERE / f"figure_full_{CD}.png"
GAP = 40          # px entre tiles
MARGIN = 30       # px borde
W = 4200          # px de ancho total


def rerender(panel: str) -> Path:
    """Corre el script original con savefig redirigido a HERE/_hires/<panel>.png a 300 dpi."""
    script, argv = RERENDER[panel]
    out_dir = HERE / "_hires"; out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{panel}.png"
    orig = mfig.Figure.savefig

    def redirected(self, fname, *a, **k):
        k["dpi"] = HIRES_DPI
        return orig(self, out, *a, **k)

    mfig.Figure.savefig = redirected
    old_argv, old_path = sys.argv, list(sys.path)
    try:
        sys.argv = [str(script), *argv]
        runpy.run_path(str(script), run_name="__main__")
    finally:
        mfig.Figure.savefig = orig
        sys.argv, sys.path[:] = old_argv, old_path
        plt.close("all")
    return out


def main():
    paths = dict(SRC)
    if "--no-rerender" not in sys.argv[1:]:
        for p in RERENDER:
            paths[p] = rerender(p)
    imgs = {k: Image.open(v).convert("RGB") for k, v in paths.items()}
    ar = {k: im.width / im.height for k, im in imgs.items()}

    # fila 1: A1 | A2 ; fila 2: B | C | D. Alto de cada fila = el que hace que los tiles llenen W.
    inner = W - 2 * MARGIN
    h1 = (inner - GAP) / (ar["A1"] + ar["A2"])
    h2 = (inner - 2 * GAP) / (ar["B"] + ar["C"] + ar["D"])
    H = int(2 * MARGIN + h1 + GAP + h2)

    dpi = 200
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    fig.patch.set_facecolor("white")

    def place(k, x, y, h):
        w = ar[k] * h
        ax = fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])
        im = imgs[k].resize((int(round(w)), int(round(h))), Image.LANCZOS)
        ax.imshow(im); ax.axis("off")
        fig.text((x - 4) / W, 1 - (y + 6) / H, k, fontsize=26, fontweight="bold", ha="left", va="top")
        return x + w + GAP

    x = MARGIN; y = MARGIN
    x = place("A1", x, y, h1); place("A2", x, y, h1)
    x = MARGIN; y = MARGIN + h1 + GAP
    x = place("B", x, y, h2); x = place("C", x, y, h2); place("D", x, y, h2)

    fig.savefig(OUT, dpi=dpi, facecolor="white")
    print(f"wrote {OUT}  ({W}x{H} px)")
    for k, v in paths.items():
        print(f"  {k}: {v.relative_to(ROOT)}  {imgs[k].size}")


if __name__ == "__main__":
    main()
