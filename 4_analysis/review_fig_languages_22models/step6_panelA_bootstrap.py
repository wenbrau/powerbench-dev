#!/usr/bin/env python3
"""Paso 6 — panel A (24/09, Nico): intervalo bootstrap sobre prompts del desvío de cada idioma respecto de la media de los 8, en la
escala de las barras (pp), para los 22 modelos. La receta es figure_paper.deviation_bootstrap (review_fig_languages): barra = media
sobre los modelos de R(idioma, modo); desvío = barra − media de las 8 barras; Boot estratificado por modo con cada prompt arrastrando
sus 8 idiomas y sus modelos; IC percentil 95 %. Las estrellas del panel siguen siendo las del GLMM (paso 1, glmm_nagq1).
Salida: panelA_deviation_bootstrap.csv, que leen figure_22models.py y figure_22models_compact.py.   ≈ 1 min.
"""
from _common import HERE, load22, write_provenance
import figure_paper as fp


def main():
    d, inputs = load22()
    tab = fp.deviation_bootstrap(d)
    out = HERE / "panelA_deviation_bootstrap.csv"
    tab.to_csv(out, index=False)
    print(tab.round(2).to_string(index=False))
    write_provenance("step6_panelA_bootstrap", inputs, [__file__, fp.__file__], B=fp.B_A, seed=fp.SEED_A)


if __name__ == "__main__":
    main()
