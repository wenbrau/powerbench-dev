#!/usr/bin/env python3
"""Apéndice de la figura de idiomas (pedido de Wendy 19/09): los paneles C y D finales SEPARADOS POR MODO.

En el cuerpo va figure_full_ps.png, con C y D sobre power shifting (he + de + pg juntos). Acá, para el apéndice, cada
panel por modo (he, de, pg, control), en una grilla 2 × 2, una figura por panel:

  figure_appendix_C_by_mode.png   acuerdo entre modelos en el ranking de idiomas    panelC/panelC_final_{he,de,pg,control}.png
  figure_appendix_D_by_mode.png   exceso sobre el azar por modelo (F6)              panelD/F6_exceso_{he,de,pg,control}.png

No calcula nada: junta los PNG ya producidos por panelC/panelC_with_tests.py (los cuatro modos en una corrida) y
panelD/F6_exceso_pg.py --mode <modo> (una corrida por modo). Los títulos internos de cada tile son los de sus scripts.
Ejecutar desde la raíz del repo:  python 4_analysis/review_fig_languages/figure_appendix_CD_by_mode.py
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

MODES = ("he", "de", "pg", "control")
LETTERS = ("a", "b", "c", "d")
FIGS = {
    "C": {m: HERE / "panelC" / f"panelC_final_{m}.png" for m in MODES},
    "D": {m: HERE / "panelD" / f"F6_exceso_{m}.png" for m in MODES},
}
GAP = 40          # px entre tiles
MARGIN = 30       # px borde
W = 3200          # px de ancho total (2 tiles por fila)


def assemble(panel: str) -> Path:
    imgs = {m: Image.open(FIGS[panel][m]).convert("RGB") for m in MODES}
    ar = {m: im.width / im.height for m, im in imgs.items()}
    inner = W - 2 * MARGIN
    rows = [MODES[:2], MODES[2:]]
    hs = [(inner - GAP) / (ar[a] + ar[b]) for a, b in rows]
    H = int(2 * MARGIN + sum(hs) + GAP)

    dpi = 200
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    fig.patch.set_facecolor("white")

    def place(m, let, x, y, h):
        w = ar[m] * h
        ax = fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])
        ax.imshow(imgs[m].resize((int(round(w)), int(round(h))), Image.LANCZOS)); ax.axis("off")
        fig.text((x - 4) / W, 1 - (y + 6) / H, let, fontsize=24, fontweight="bold", ha="left", va="top")
        return x + w + GAP

    y = MARGIN; k = 0
    for row, h in zip(rows, hs):
        x = MARGIN
        for m in row:
            x = place(m, LETTERS[k], x, y, h); k += 1
        y += h + GAP

    out = HERE / f"figure_appendix_{panel}_by_mode.png"
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}  ({W}x{H} px)")
    for m in MODES:
        print(f"  {m:8s} {FIGS[panel][m].relative_to(ROOT)}  {imgs[m].size}")
    return out


def main():
    missing = [p for d in FIGS.values() for p in d.values() if not p.exists()]
    if missing:
        raise SystemExit("faltan tiles:\n  " + "\n  ".join(str(p.relative_to(ROOT)) for p in missing))
    for panel in ("C", "D"):
        assemble(panel)


if __name__ == "__main__":
    main()
