"""Robustness check de la figura de idiomas (Wendy, 2026-09-20): la MISMA figura (figure_paper_v2.py, paneles A–F) sin los dos
modelos que no funcionan en swahili — nemotron-3.5-lightning y nova-2-lite — eliminados de TODOS los idiomas, no solo de swahili.

En la figura de 24 modelos esos dos entran en 7 idiomas y quedan fuera de swahili (por eso el asterisco); acá salen del panel y
quedan 22 modelos (10 US / 12 CN), los 8 idiomas completos en todos, y swahili sin asterisco.

Este módulo carga los datos y fija las constantes; cada paso (step1..step5) recalcula la tabla de un panel con la receta de su
script original (bloque 36, bloque 81, panelB_bootstrap.py, F6_exceso_pg.py --mode ps, panelC_with_tests.py --only power_shifting)
y figure_22models.py arma la figura. Sin llamadas a ninguna API.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REF = ROOT / "4_analysis/review_fig_languages"          # la figura de 24 modelos (referencia)
for p in (str(ROOT / "4_analysis"), str(ROOT / "common"), str(REF), str(REF / "panelB"), str(REF / "panelC")):
    if p not in sys.path:
        sys.path.insert(0, p)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))

import pandas as pd  # noqa: E402

from pbanalysis.final_panel import load_d1_multilingual, MODES, file_digest  # noqa: E402

EXCLUDE = {"nemotron-3.5-lightning", "nova-2-lite"}       # los dos que no funcionan en swahili; acá salen de todo
N_MODELS = 22
LANGS = ["en", "de", "fr", "es", "pt", "zh", "hi", "sw"]
LANG_NAME = {"en": "English", "de": "German", "fr": "French", "es": "Spanish", "pt": "Portuguese", "zh": "Chinese", "hi": "Hindi", "sw": "Swahili"}
WEIGHTS = ROOT / "4_analysis/results/72_fig2_usage_weighted_requests/weights.csv"
CAPS = ROOT / "4_analysis/results/30_fig1_glmm/capability_index.csv"


def load22():
    """Filas válidas de D1 + control en 8 idiomas, sin los dos modelos excluidos. Devuelve (d, inputs)."""
    df = load_d1_multilingual()
    d = df[df.valid & ~df.model.isin(EXCLUDE)].copy()
    d["refuse"] = d.refuse.astype(float)
    models = sorted(d.model.unique())
    assert len(models) == N_MODELS, models
    origin = d.drop_duplicates("model").set_index("model").origin
    assert Counter(origin) == {"US": 10, "CN": 12}, Counter(origin)
    assert set(d.lang) == set(LANGS)
    assert (d.groupby("model").lang.nunique() == 8).all(), "algún modelo sin los 8 idiomas"
    return d, list(df.attrs["inputs"])


def write_provenance(name, inputs, code_files, **extra):
    prov = {"inputs": {str(Path(p).relative_to(ROOT)) if str(p).startswith(str(ROOT)) else str(p): file_digest(p) for p in inputs if Path(p).is_file()},
            "code": {str(Path(c).resolve().relative_to(ROOT)): file_digest(c) for c in code_files},
            "excluded_models": sorted(EXCLUDE), **extra}
    (HERE / f"{name}.provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
