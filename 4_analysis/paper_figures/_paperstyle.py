"""Estilo común de las figuras de PÁGINA del paper (20/09, pedido de Wendy: "que todas las figuras sean legibles en una
página tipo paper"). Copia las constantes de 4_analysis/review_fig_languages/figure_paper.py (la primera que se hizo así)
para que las cuatro figuras del cuerpo compartan tipografía, colores, letras de panel y formato de salida.

Ancho de texto de ICLR 2027: 5,5 in. Tipografía 4,7–7,2 pt. Salida: PDF vectorial + PNG 300 dpi + caption en .md.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = ROOT / "4_analysis" / "results"
for p in (str(ROOT / "4_analysis"), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import warnings  # noqa: E402
warnings.filterwarnings("ignore")
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402

WIDTH = 5.5                                   # in, ancho de texto
F_TITLE, F_BASE, F_TICK, F_SMALL, F_TINY, F_LETTER = 7.2, 6.5, 6.0, 5.2, 4.7, 9.5

MODES = ["he", "de", "pg", "control"]
PS = "power_shifting"
MODE_LABEL = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT"}
MODE_SHORT = {"he": "SE", "de": "DE", "pg": "PG", "control": "CT", PS: "Power shift.\n(mean)"}
MODE_COLORS = {"he": "#456B91", "de": "#B68534", "pg": "#A44255", "control": "#777C83", PS: "#5B3F8C"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
ORIGIN_LIGHT = {"US": "#B9CDE0", "CN": "#E6BDB9"}


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": F_BASE, "axes.titlesize": F_TITLE, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 4, "axes.labelsize": F_BASE, "xtick.labelsize": F_TICK, "ytick.labelsize": F_TICK,
        "legend.fontsize": F_SMALL, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6,
        "xtick.major.width": .5, "ytick.major.width": .5, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "xtick.major.pad": 2, "ytick.major.pad": 2, "axes.labelpad": 2,
        "lines.linewidth": .8, "savefig.facecolor": "white", "pdf.fonttype": 42,
    })


def num(x, nd=3, lang="en", sign=False):
    """número con el separador decimal del idioma del texto (coma en español, punto en inglés)."""
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "es" else s


def fmt_q(q, lang="en", letter="q"):
    return f"{letter} < {num(.001, 3, lang)}" if q < .001 else f"{letter} = {num(q, 3, lang)}"


def stars(p, ns=""):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ns


def or_axis(ax, ticks, lo, hi):
    ax.set_yscale("log"); ax.set_yticks(ticks); ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter()); ax.set_ylim(lo, hi)
    ax.axhline(1, color="black", lw=.6); ax.grid(axis="y", alpha=.15)


def letters(fig, items, dx=.012, dy=.006):
    """letras de panel en coordenadas de figura, arriba a la izquierda de cada eje: items = [(ax, "A", x_override|None), ...].
    Llamar después de fig.canvas.draw() cuando el layout es 'constrained', para que get_position() sea la definitiva."""
    for ax, s, xo in items:
        x0, y0, w, h = ax.get_position().bounds
        fig.text((x0 - dx) if xo is None else xo, y0 + h + dy, s, fontsize=F_LETTER, fontweight="bold", ha="right" if xo is None else "left", va="bottom")


def save(fig, stem, lang, caption):
    for ext in ("pdf", "png"):
        out = HERE / f"{stem}_{lang}.{ext}"
        fig.savefig(out, dpi=300)
        print("escrito:", out.relative_to(ROOT))
    plt.close(fig)
    cap = HERE / f"{stem}_caption_{lang}.md"
    cap.write_text(caption + "\n", encoding="utf-8")
    print("escrito:", cap.relative_to(ROOT))


def which_langs(argv):
    which = argv[argv.index("--lang") + 1] if "--lang" in argv else "both"
    assert which in ("es", "en", "both"), which
    return ("es", "en") if which == "both" else (which,)
