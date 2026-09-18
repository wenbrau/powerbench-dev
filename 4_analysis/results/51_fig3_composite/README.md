# Figura 3 completa (D2 díadas): los paneles aprobados

*figura compuesta (draft); paneles aprobados por Nico el 17–18/09 · 2026-09-18 · commit `86d611d` · `51_fig3_composite`*

## Question

Ensamblado de A (|sesgo| de lado contra lados barajados), B (pedido típico pesado por uso, OR) y C (dirección respecto de USA y de China con sus díadas de rivalidad). Sin cálculos nuevos.

## Data

- Tablas de los bloques 45 (A, B) y 52 (C; la versión con cuatro díadas del bloque 46 va a apéndice).

Input files:

- `4_analysis/results/45_fig3_side_combined/side_abs_bias_vs_shuffle.csv`
- `4_analysis/results/45_fig3_side_combined/side_estimators.csv`
- `4_analysis/results/52_fig3_direction_rivalry/direction_glmm_rivalry.csv`

## Method

- A: permutación (bloque 45). B: bootstrap sobre prompts, modelos y pesos fijos (bloque 45). C: GLMM por país y modo (bloque 46), BH y Holm por familia en su tabla. Los intervalos de las figuras son los de cada bloque, sin corregir.

## Figures

### figure3_full

![figure3_full](figure3_full.png)

A: |sesgo| de lado por modelo (media de 24) contra lados barajados, lados juntos y referencia neutral, por modo. B: OR de refusal de un pedido típico según el lado del usuario, pesado por uso. C: OR de refusal con el país de usuario contra el país de afectado, todas las díadas de rivalidad de USA y de China, por grupo de modelos y modo. Ejes de OR en escala logarítmica.

## Notes and caveats

- Registro de decisiones y tests: 4_analysis/results/27_fig3_notelab/NARRATIVA_F3.md.

## Conclusion (preliminary)

Figura 3 compuesta con los paneles aprobados; interpretación del equipo en la narrativa.
