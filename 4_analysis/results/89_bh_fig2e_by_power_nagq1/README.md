# Figura 2 E: BH por potencia para los OR de dirección (bloque 46)

*pedido de Nico (22/09, #25-#26): familias por potencia en lugar de juntar EE.UU. y China · 2026-09-24 · commit `17ae987` · `89_bh_fig2e_by_power_nagq1`*

## Question

Con la familia definida por la pregunta de cada subpanel (una potencia), ¿qué contrastes de dirección sobreviven la corrección?

## Data

- Las p de Wald de los GLMM de dirección del bloque 46 (refuse ~ direction × DC + pairing + (1 + direction || model) + (1 | prompt)), 24 modelos: 8 tests agrupados (2 potencias × 4 tipos) y 32 por contraparte (2 × 4 × 4).

Input files:

- `4_analysis/results/46_fig3_direction_glmm_nagq1/direction_glmm.csv`
- `4_analysis/results/46_fig3_direction_glmm_nagq1/direction_glmm_by_dyad.csv`

## Method

- BH dentro de cada potencia: familia de 4 para los OR agrupados sobre los cuatro contrapartes y de 16 para los OR por contraparte. Antes: 8 y 32 juntando las dos potencias. Ninguna p cambia; solo la corrección.

## Tables

### bh_by_power  (`bh_by_power.csv`)

Cada test con su p, la q anterior (familias de 8 / 32) y la q por potencia (familias de 4 / 16).

| level | power | mode | dyad | estimate | OR | OR_lo | OR_hi | p | q_bh_old | q_bh_power | family | n_family | sig_q05_old | sig_q05_power |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pooled | china | he | todas | 0.0 | 1.0 | 0.9 | 1.2 | 0.598 | 0.8 | 0.8 | direction, china, pooled (4 tests) | 4 | False | False |
| pooled | china | de | todas | 0.1 | 1.1 | 0.9 | 1.3 | 0.513 | 0.8 | 0.8 | direction, china, pooled (4 tests) | 4 | False | False |
| pooled | china | pg | todas | 0.1 | 1.1 | 0.9 | 1.2 | 0.238 | 0.5 | 0.8 | direction, china, pooled (4 tests) | 4 | False | False |
| pooled | china | control | todas | 0.0 | 1.0 | 0.9 | 1.1 | 0.912 | 1.0 | 0.9 | direction, china, pooled (4 tests) | 4 | False | False |
| pooled | usa | he | todas | -0.1 | 0.9 | 0.8 | 1.0 | 0.010 | 0.0 | 0.0 | direction, usa, pooled (4 tests) | 4 | True | True |
| pooled | usa | de | todas | 0.2 | 1.3 | 1.1 | 1.4 | 0.000 | 0.0 | 0.0 | direction, usa, pooled (4 tests) | 4 | True | True |
| pooled | usa | pg | todas | 0.2 | 1.2 | 1.1 | 1.3 | 0.000 | 0.0 | 0.0 | direction, usa, pooled (4 tests) | 4 | True | True |
| pooled | usa | control | todas | 0.0 | 1.0 | 0.9 | 1.1 | 0.970 | 1.0 | 1.0 | direction, usa, pooled (4 tests) | 4 | False | False |
| by_dyad | china | he | cn_ally | -0.1 | 0.9 | 0.7 | 1.1 | 0.245 | 0.4 | 0.4 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | he | cn_rival | 0.1 | 1.1 | 0.8 | 1.5 | 0.450 | 0.6 | 0.7 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | he | cn_neutral | 0.2 | 1.2 | 0.9 | 1.5 | 0.177 | 0.3 | 0.4 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | he | cn_us | 0.2 | 1.3 | 1.0 | 1.6 | 0.023 | 0.1 | 0.1 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | de | cn_ally | 0.2 | 1.2 | 1.1 | 1.5 | 0.007 | 0.0 | 0.0 | direction, china, by_dyad (16 tests) | 16 | True | True |
| by_dyad | china | de | cn_rival | -0.0 | 1.0 | 0.8 | 1.2 | 0.970 | 1.0 | 1.0 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | de | cn_neutral | 0.1 | 1.1 | 0.9 | 1.4 | 0.235 | 0.4 | 0.4 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | de | cn_us | -0.1 | 0.9 | 0.7 | 1.1 | 0.226 | 0.4 | 0.4 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | pg | cn_ally | 0.2 | 1.3 | 1.1 | 1.5 | 0.000 | 0.0 | 0.0 | direction, china, by_dyad (16 tests) | 16 | True | True |
| by_dyad | china | pg | cn_rival | -0.0 | 1.0 | 0.8 | 1.1 | 0.636 | 0.7 | 0.7 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | pg | cn_neutral | 0.2 | 1.3 | 1.1 | 1.5 | 0.002 | 0.0 | 0.0 | direction, china, by_dyad (16 tests) | 16 | True | True |
| by_dyad | china | pg | cn_us | -0.1 | 0.9 | 0.7 | 1.0 | 0.110 | 0.2 | 0.4 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | control | cn_ally | 0.0 | 1.0 | 0.9 | 1.2 | 0.700 | 0.7 | 0.7 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | control | cn_rival | 0.0 | 1.0 | 0.9 | 1.2 | 0.503 | 0.7 | 0.7 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | control | cn_neutral | -0.1 | 0.9 | 0.8 | 1.1 | 0.398 | 0.6 | 0.6 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | china | control | cn_us | 0.0 | 1.0 | 0.9 | 1.2 | 0.601 | 0.7 | 0.7 | direction, china, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | he | us_ally | 0.1 | 1.1 | 0.9 | 1.3 | 0.586 | 0.7 | 0.6 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | he | us_rival | -0.4 | 0.7 | 0.6 | 0.9 | 0.001 | 0.0 | 0.0 | direction, usa, by_dyad (16 tests) | 16 | True | True |
| by_dyad | usa | he | us_neutral | 0.1 | 1.1 | 0.9 | 1.3 | 0.511 | 0.7 | 0.6 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | he | us_cn | -0.2 | 0.8 | 0.6 | 1.0 | 0.023 | 0.1 | 0.1 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | de | us_ally | 0.2 | 1.2 | 1.1 | 1.4 | 0.004 | 0.0 | 0.0 | direction, usa, by_dyad (16 tests) | 16 | True | True |
| by_dyad | usa | de | us_rival | 0.3 | 1.3 | 1.1 | 1.5 | 0.001 | 0.0 | 0.0 | direction, usa, by_dyad (16 tests) | 16 | True | True |
| by_dyad | usa | de | us_neutral | 0.4 | 1.5 | 1.3 | 1.7 | 0.000 | 0.0 | 0.0 | direction, usa, by_dyad (16 tests) | 16 | True | True |
| by_dyad | usa | de | us_cn | 0.1 | 1.1 | 0.9 | 1.4 | 0.226 | 0.4 | 0.3 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | pg | us_ally | 0.1 | 1.2 | 1.0 | 1.3 | 0.023 | 0.1 | 0.1 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | pg | us_rival | 0.1 | 1.1 | 1.0 | 1.3 | 0.026 | 0.1 | 0.1 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | pg | us_neutral | 0.3 | 1.3 | 1.2 | 1.5 | 0.000 | 0.0 | 0.0 | direction, usa, by_dyad (16 tests) | 16 | True | True |
| by_dyad | usa | pg | us_cn | 0.1 | 1.1 | 1.0 | 1.4 | 0.110 | 0.2 | 0.2 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | control | us_ally | 0.0 | 1.0 | 0.9 | 1.2 | 0.747 | 0.8 | 0.7 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | control | us_rival | -0.1 | 0.9 | 0.8 | 1.0 | 0.183 | 0.3 | 0.3 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | control | us_neutral | 0.1 | 1.1 | 1.0 | 1.3 | 0.089 | 0.2 | 0.2 | direction, usa, by_dyad (16 tests) | 16 | False | False |
| by_dyad | usa | control | us_cn | -0.0 | 1.0 | 0.8 | 1.1 | 0.601 | 0.7 | 0.6 | direction, usa, by_dyad (16 tests) | 16 | False | False |

*(48 rows; first 40 shown)*

## Conclusion (preliminary)

0 de 48 tests cambian de lado de q = 0.05 al corregir por potencia.
