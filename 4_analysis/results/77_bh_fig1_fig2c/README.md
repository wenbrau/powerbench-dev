# BH por familia para los tests de la Figura 1 (bloques 30, 31) y del panel C de idioma (bloque 39)

*pedido de Nico (19/09): BH con familias por pregunta para los bloques que no la tenían; sin recalcular ningún test · 2026-09-19 · commit `733ce59` · `77_bh_fig1_fig2c`*

## Question

¿Qué tests de la Figura 1 (modos, origen, escala, standing) y del acuerdo entre rankings de idiomas sobreviven la corrección de Benjamini-Hochberg con familia = los tests que contestan la misma pregunta dentro del panel?

## Data

- Tablas de p de los bloques 30, 31 y 39 (GLMM con nAGQ = 0 en 30 y 31; permutaciones en 39). No se recalcula nada: solo se agrega q.

Input files:

- `4_analysis/results/30_fig1_glmm/glmm_mode_contrasts.csv`
- `4_analysis/results/30_fig1_glmm/glmm_origin.csv`
- `4_analysis/results/30_fig1_glmm/glmm_interaction_ps_vs_control.csv`
- `4_analysis/results/31_fig1_glmm_scale/glmm_scale_trend.csv`
- `4_analysis/results/31_fig1_glmm_scale/glmm_scale_interaction_ps_vs_control.csv`
- `4_analysis/results/31_fig1_glmm_standing/glmm_standing_trend.csv`
- `4_analysis/results/31_fig1_glmm_standing/glmm_standing_interaction_ps_vs_control.csv`
- `4_analysis/results/39_fig2_order_stats/order_agreement_tests.csv`

## Method

- Familias en la docstring del script y en DECISIONES punto 37. BH dentro de cada familia; los tests únicos (pooled) llevan q = p. En el bloque 39 se corrige p_right (unilateral), tal como lo definió ese bloque.

## Tables

### bh_families  (`bh_families.csv`)

Todos los tests con su familia, p, q y si cambian de estado a q < 0,05.

| figure | block | panel | family | test | estimate | p | singular | n_family | q_bh | sig_p05 | sig_q05 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Figura 1 | 30 | Figura 1 · A modos | contrastes de modo (2) | de − he | 1.9 | 0.000 | False | 2 | 0.0 | True | True |
| Figura 1 | 30 | Figura 1 · A modos | contrastes de modo (2) | pg − de | 0.9 | 0.002 | False | 2 | 0.0 | True | True |
| Figura 1 | 30 | Figura 1 · origen | efecto CN − US por modo (4) | he | 0.6 | 0.225 | False | 4 | 0.3 | False | False |
| Figura 1 | 30 | Figura 1 · origen | efecto CN − US por modo (4) | de | 1.0 | 0.059 | False | 4 | 0.2 | False | False |
| Figura 1 | 30 | Figura 1 · origen | efecto CN − US por modo (4) | pg | 0.6 | 0.186 | False | 4 | 0.3 | False | False |
| Figura 1 | 30 | Figura 1 · origen | efecto CN − US por modo (4) | control | 0.2 | 0.663 | False | 4 | 0.7 | False | False |
| Figura 1 | 30 | Figura 1 · origen | efecto CN − US, pooled (1) | power shifting (pooled) | 0.8 | 0.094 | False | 1 | 0.1 | False | False |
| Figura 1 | 30 | Figura 1 · origen | interacción CN × (modo vs control) por modo (3) | he vs control | 0.6 | 0.091 | False | 3 | 0.1 | False | False |
| Figura 1 | 30 | Figura 1 · origen | interacción CN × (modo vs control) por modo (3) | de vs control | 0.9 | 0.018 | False | 3 | 0.1 | True | False |
| Figura 1 | 30 | Figura 1 · origen | interacción CN × (modo vs control) por modo (3) | pg vs control | 0.5 | 0.111 | False | 3 | 0.1 | False | False |
| Figura 1 | 30 | Figura 1 · origen | interacción CN × (power shifting vs control), pooled (1) | power shifting vs control (pooled) | 0.6 | 0.023 | False | 1 | 0.0 | True | True |
| Figura 1 | 31 | Figura 1 · C escala | pendiente de scale por modo (4) | he | 0.3 | 0.242 | False | 4 | 0.3 | False | False |
| Figura 1 | 31 | Figura 1 · C escala | pendiente de scale por modo (4) | de | 0.4 | 0.040 | False | 4 | 0.1 | True | False |
| Figura 1 | 31 | Figura 1 · C escala | pendiente de scale por modo (4) | pg | 1.2 | 0.000 | False | 4 | 0.0 | True | True |
| Figura 1 | 31 | Figura 1 · C escala | pendiente de scale por modo (4) | control | -0.1 | 0.678 | True | 4 | 0.7 | False | False |
| Figura 1 | 31 | Figura 1 · C escala | pendiente de scale, pooled (1) | power shifting (pooled) | 0.7 | 0.000 | False | 1 | 0.0 | True | True |
| Figura 1 | 31 | Figura 1 · C escala | interacción scale × (modo vs control) por modo (3) | he vs control | 0.4 | 0.265 | False | 3 | 0.3 | False | False |
| Figura 1 | 31 | Figura 1 · C escala | interacción scale × (modo vs control) por modo (3) | de vs control | 0.5 | 0.102 | True | 3 | 0.2 | False | False |
| Figura 1 | 31 | Figura 1 · C escala | interacción scale × (modo vs control) por modo (3) | pg vs control | 1.3 | 0.000 | False | 3 | 0.0 | True | True |
| Figura 1 | 31 | Figura 1 · C escala | interacción scale × (power shifting vs control), pooled (1) | power shifting vs control (pooled) | 0.8 | 0.002 | False | 1 | 0.0 | True | True |
| Figura 1 | 31 | Figura 1 · D standing | pendiente de standing por modo (4) | he | 0.5 | 0.097 | False | 4 | 0.2 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | pendiente de standing por modo (4) | de | -0.2 | 0.466 | False | 4 | 0.6 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | pendiente de standing por modo (4) | pg | 0.4 | 0.063 | False | 4 | 0.2 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | pendiente de standing por modo (4) | control | 0.1 | 0.766 | True | 4 | 0.8 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | pendiente de standing, pooled (1) | power shifting (pooled) | 0.2 | 0.076 | False | 1 | 0.1 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | interacción standing × (modo vs control) por modo (3) | he vs control | 0.4 | 0.322 | True | 3 | 0.5 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | interacción standing × (modo vs control) por modo (3) | de vs control | -0.2 | 0.464 | True | 3 | 0.5 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | interacción standing × (modo vs control) por modo (3) | pg vs control | 0.4 | 0.279 | False | 3 | 0.5 | False | False |
| Figura 1 | 31 | Figura 1 · D standing | interacción standing × (power shifting vs control), pooled (1) | power shifting vs control (pooled) | 0.2 | 0.507 | True | 1 | 0.5 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | mismo origen − mixto, por modo (4) | dentro − mixto · he | 0.1 | 0.057 | nan | 4 | 0.1 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | mismo origen − mixto, por modo (4) | dentro − mixto · de | 0.1 | 0.073 | nan | 4 | 0.1 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | mismo origen − mixto, por modo (4) | dentro − mixto · pg | 0.1 | 0.009 | nan | 4 | 0.0 | True | True |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | mismo origen − mixto, por modo (4) | dentro − mixto · control | 0.3 | 0.000 | nan | 4 | 0.0 | True | True |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | CN–CN − mixto · he | 0.0 | 0.296 | nan | 8 | 0.3 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | US–US − mixto · he | 0.1 | 0.097 | nan | 8 | 0.1 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | CN–CN − mixto · de | 0.1 | 0.077 | nan | 8 | 0.1 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | US–US − mixto · de | 0.1 | 0.129 | nan | 8 | 0.1 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | CN–CN − mixto · pg | 0.2 | 0.003 | nan | 8 | 0.0 | True | True |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | US–US − mixto · pg | 0.1 | 0.081 | nan | 8 | 0.1 | False | False |
| Figura de idioma (4 del paper) | 39 | idioma · C acuerdo entre rankings | cada bloque − mixto, por modo (8) | CN–CN − mixto · control | 0.3 | 0.000 | nan | 8 | 0.0 | True | True |

*(57 rows; first 40 shown)*

### changed_at_q05  (`changed_at_q05.csv`)

Tests cuyo estado (p < 0,05) cambia al pasar a q < 0,05.

| figure | block | panel | family | test | estimate | p | singular | n_family | q_bh | sig_p05 | sig_q05 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Figura 1 | 30 | Figura 1 · origen | interacción CN × (modo vs control) por modo (3) | de vs control | 0.9 | 0.018 | False | 3 | 0.1 | True | False |
| Figura 1 | 31 | Figura 1 · C escala | pendiente de scale por modo (4) | de | 0.4 | 0.040 | False | 4 | 0.1 | True | False |

## Key numbers  (`stats.json`)

- **changed_30_de vs control**: +0.9, p = 0.018 log-odds o Spearman — q = 0.053 (interacción CN × (modo vs control) por modo (3))
- **changed_31_de**: +0.4, p = 0.040 log-odds o Spearman — q = 0.079 (pendiente de scale por modo (4))

## Notes and caveats

- Registro: 25_fig1_notelab/NARRATIVA_F1.md (Figura 1) y 26_fig2_notelab/NARRATIVA_F2.md (panel C de idioma).

## Conclusion (preliminary)

Ver changed_at_q05. Las lecturas del cuerpo que dependan de un test que cambie de estado se revisan con Nico.
