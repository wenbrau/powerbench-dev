# Figura 3 completa (D2 díadas): los paneles aprobados

*figura compuesta (draft); paneles aprobados por Nico el 17–18/09; panel B regenerado el 19/09 con el bloque 73 (pesos por pedidos, permutación como test) · 2026-09-19 · commit `c4c32f4` · `51_fig3_composite`*

## Question

Ensamblado de A (|sesgo| de lado contra lados barajados), B (pedido típico pesado por uso, OR) y C (dirección respecto de USA y de China con sus díadas de rivalidad). Sin cálculos nuevos.

## Data

- Tablas de los bloques 55 (A; el bloque 45 es su versión anterior), 73 (B; el bloque 45 pC es su versión anterior, por tokens) y 52 (C; la versión con cuatro díadas del bloque 46 va a apéndice).

Input files:

- `4_analysis/results/55_fig3_side_excess/side_abs_bias_excess_summary.csv`
- `4_analysis/results/73_fig3_usage_weighted_requests/side_or_requests.csv`
- `4_analysis/results/52_fig3_direction_rivalry/direction_glmm_rivalry.csv`

## Method

- A: exceso de |sesgo| por modelo sobre su nulo binomial exacto, IC t entre modelos, q BH sobre 8 (bloque 55; aprobado por Nico el 18/09). B: tasas pesadas por los PEDIDOS de cada modelo en OpenRouter; barra = IC bootstrap sobre prompts, modelos y pesos fijos; test = permutación de lados dentro de (modelo, prompt, díada), asterisco = q BH < 0,05 dentro de los 4 modos del conjunto (bloque 73; decisión de Nico, 19/09); es un OR marginal de un pedido típico, no comparable en magnitud con C. C: GLMM por país y modo (bloque 46), BH y Holm por familia en su tabla. Los intervalos de las figuras son los de cada bloque, sin corregir.

## Figures

### figure3_full

![figure3_full](figure3_full.png)

A: |sesgo| de lado por modelo (media de 24) contra lados barajados, lados juntos y referencia neutral, por modo. B: OR de refusal de un pedido típico según el lado del usuario, pesado por pedidos. C: OR de refusal con el país de usuario contra el país de afectado, todas las díadas de rivalidad de USA y de China, por grupo de modelos y modo. Ejes de OR en escala logarítmica.

## Notes and caveats

- Registro de decisiones y tests: 4_analysis/results/27_fig3_notelab/NARRATIVA_F3.md.

## Conclusion (preliminary)

Figura 3 compuesta con los paneles aprobados; interpretación del equipo en la narrativa.
