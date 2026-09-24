# Tests entre modelos (DC, capacidad) con referencia t de grados de libertad between-within

*pedido de Nico (24/09); estimaciones nAGQ = 1 de la rama nagq1-rerun; lectura pendiente · 2026-09-24 · commit `17ae987` · `95_between_model_small_sample`*

## Question

¿Cambian los p de los efectos que solo se estiman entre los 24 modelos si se reemplaza la referencia normal del z de Wald por una t con df = modelos − parámetros a nivel de modelo?

Input files:

- `4_analysis/results/30_fig1_glmm_nagq1/glmm_origin.csv`
- `4_analysis/results/30_fig1_glmm_nagq1/glmm_interaction_ps_vs_control.csv`
- `4_analysis/results/78_fig1_v3_nagq1/origin_overall_glmm.csv`
- `4_analysis/results/45_fig3_side_combined_nagq1/side_glmm.csv`
- `4_analysis/results/46_fig3_direction_glmm_nagq1/direction_glmm.csv`
- `4_analysis/results/58_fig4_ai_origin_glmm_nagq1/ai_origin_glmm.csv`
- `4_analysis/results/64_fig4_capability_glmm_nagq1/capability_glmm.csv`
- `4_analysis/results/68_reasoning_glmm_nagq1/reasoning_glmm.csv`

## Method

- p_t = 2 · P(T_df > |z|), df = 24 − 2 = 22 (8 − 2 = 6 en razonamiento), con la misma estimación y el mismo SE de Wald; IC con el cuantil t. BH en las familias del paper (columna family). El ómnibus nivel × DC de razonamiento: F(2, 6) = χ²/2.

## Tables

### between_model_tests  (`between_model_tests.csv`)

Un test por fila: p y q con la referencia z (como en el paper, ahora con nAGQ = 1) y con la referencia t.

| panel | test | family | estimate | se | ratio | z | p_wald_z | df | p_t | ratio_lo_z | ratio_hi_z | ratio_lo_t | ratio_hi_t | paper | q_z | q_t | n_family | flips_at_05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fig 1B | DC (CN/US), SE | Fig 1B: DC by request type (4) | 0.6 | 0.4 | 1.8 | 1.4 | 0.2 | 22 | 0.2 | 0.8 | 4.4 | 0.7 | 4.6 |  | 0.2 | 0.2 | 4 | False |
| Fig 1B | DC (CN/US), DE | Fig 1B: DC by request type (4) | 1.1 | 0.5 | 2.9 | 2.0 | 0.0 | 22 | 0.1 | 1.0 | 8.4 | 1.0 | 8.9 |  | 0.2 | 0.2 | 4 | False |
| Fig 1B | DC (CN/US), PG | Fig 1B: DC by request type (4) | 0.7 | 0.5 | 1.9 | 1.4 | 0.2 | 22 | 0.2 | 0.8 | 4.9 | 0.7 | 5.2 |  | 0.2 | 0.2 | 4 | False |
| Fig 1B | DC (CN/US), CT | Fig 1B: DC by request type (4) | 0.2 | 0.4 | 1.2 | 0.5 | 0.6 | 22 | 0.6 | 0.5 | 2.8 | 0.5 | 3.0 |  | 0.6 | 0.6 | 4 | False |
| Fig 1B | DC (CN/US), PS pooled | single: DC, PS pooled | 0.8 | 0.5 | 2.3 | 1.8 | 0.1 | 22 | 0.1 | 0.9 | 5.7 | 0.9 | 6.0 |  | 0.1 | 0.1 | 1 | False |
| Fig 1B | DC (CN/US), four types | single: DC, four types | 0.6 | 0.4 | 1.9 | 1.5 | 0.1 | 22 | 0.2 | 0.8 | 4.4 | 0.8 | 4.6 |  | 0.1 | 0.2 | 1 | False |
| Fig 1B | DC × (PS vs CT) | single: DC × (PS vs CT) | 0.7 | 0.3 | 1.9 | 2.4 | 0.0 | 22 | 0.0 | 1.1 | 3.3 | 1.1 | 3.4 |  | 0.0 | 0.0 | 1 | False |
| Fig 1B (block 77) | DC × (SE vs CT) | DC × (type vs CT) (3) | 0.6 | 0.3 | 1.8 | 1.8 | 0.1 | 22 | 0.1 | 0.9 | 3.5 | 0.9 | 3.7 |  | 0.1 | 0.1 | 3 | False |
| Fig 1B (block 77) | DC × (DE vs CT) | DC × (type vs CT) (3) | 0.9 | 0.4 | 2.6 | 2.5 | 0.0 | 22 | 0.0 | 1.2 | 5.3 | 1.2 | 5.5 |  | 0.0 | 0.1 | 3 | True |
| Fig 1B (block 77) | DC × (PG vs CT) | DC × (type vs CT) (3) | 0.5 | 0.3 | 1.6 | 1.7 | 0.1 | 22 | 0.1 | 0.9 | 2.8 | 0.9 | 2.9 |  | 0.1 | 0.1 | 3 | False |
| Fig A2 (DC) | side × DC, SE | side × DC, geo set (4) | 0.1 | 0.2 | 1.1 | 0.5 | 0.6 | 22 | 0.6 | 0.8 | 1.5 | 0.8 | 1.5 |  | 0.8 | 0.8 | 4 | False |
| Fig A2 (DC) | side × DC, DE | side × DC, geo set (4) | -0.1 | 0.1 | 0.9 | -0.8 | 0.4 | 22 | 0.4 | 0.7 | 1.2 | 0.7 | 1.2 |  | 0.8 | 0.8 | 4 | False |
| Fig A2 (DC) | side × DC, PG | side × DC, geo set (4) | -0.1 | 0.1 | 0.9 | -0.6 | 0.5 | 22 | 0.5 | 0.7 | 1.2 | 0.7 | 1.2 |  | 0.8 | 0.8 | 4 | False |
| Fig A2 (DC) | side × DC, CT | side × DC, geo set (4) | 0.0 | 0.1 | 1.0 | 0.2 | 0.8 | 22 | 0.8 | 0.8 | 1.2 | 0.8 | 1.3 |  | 0.8 | 0.8 | 4 | False |
| Fig 2E | direction × DC, usa, SE | direction × DC, usa (4) | 0.0 | 0.1 | 1.0 | 0.1 | 0.9 | 22 | 0.9 | 0.8 | 1.2 | 0.8 | 1.3 |  | 0.9 | 0.9 | 4 | False |
| Fig 2E | direction × DC, china, SE | direction × DC, china (4) | -0.2 | 0.2 | 0.8 | -1.1 | 0.3 | 22 | 0.3 | 0.6 | 1.2 | 0.6 | 1.2 |  | 0.5 | 0.6 | 4 | False |
| Fig 2E | direction × DC, usa, DE | direction × DC, usa (4) | -0.2 | 0.1 | 0.9 | -1.5 | 0.1 | 22 | 0.2 | 0.7 | 1.1 | 0.7 | 1.1 |  | 0.6 | 0.6 | 4 | False |
| Fig 2E | direction × DC, china, DE | direction × DC, china (4) | -0.1 | 0.2 | 0.9 | -0.7 | 0.5 | 22 | 0.5 | 0.6 | 1.3 | 0.6 | 1.3 |  | 0.6 | 0.7 | 4 | False |
| Fig 2E | direction × DC, usa, PG | direction × DC, usa (4) | -0.1 | 0.1 | 0.9 | -1.0 | 0.3 | 22 | 0.3 | 0.8 | 1.1 | 0.8 | 1.1 |  | 0.6 | 0.6 | 4 | False |
| Fig 2E | direction × DC, china, PG | direction × DC, china (4) | -0.0 | 0.1 | 1.0 | -0.3 | 0.8 | 22 | 0.8 | 0.7 | 1.2 | 0.7 | 1.3 |  | 0.8 | 0.8 | 4 | False |
| Fig 2E | direction × DC, usa, CT | direction × DC, usa (4) | -0.0 | 0.1 | 1.0 | -0.3 | 0.7 | 22 | 0.7 | 0.9 | 1.1 | 0.8 | 1.1 |  | 0.9 | 0.9 | 4 | False |
| Fig 2E | direction × DC, china, CT | direction × DC, china (4) | -0.1 | 0.1 | 0.9 | -1.1 | 0.3 | 22 | 0.3 | 0.7 | 1.1 | 0.7 | 1.1 |  | 0.5 | 0.6 | 4 | False |
| Fig 3 (DC) | AI × DC, SE | AI × DC (4) | -0.1 | 0.3 | 0.9 | -0.5 | 0.6 | 22 | 0.6 | 0.5 | 1.5 | 0.5 | 1.6 |  | 0.9 | 0.9 | 4 | False |
| Fig 3 (DC) | AI × DC, DE | AI × DC (4) | -0.1 | 0.2 | 0.9 | -0.6 | 0.6 | 22 | 0.6 | 0.6 | 1.3 | 0.6 | 1.3 |  | 0.9 | 0.9 | 4 | False |
| Fig 3 (DC) | AI × DC, PG | AI × DC (4) | 0.0 | 0.2 | 1.0 | 0.1 | 0.9 | 22 | 0.9 | 0.7 | 1.4 | 0.7 | 1.4 |  | 0.9 | 0.9 | 4 | False |
| Fig 3 (DC) | AI × DC, CT | AI × DC (4) | 0.0 | 0.1 | 1.0 | 0.3 | 0.8 | 22 | 0.8 | 0.8 | 1.4 | 0.8 | 1.4 |  | 0.9 | 0.9 | 4 | False |
| Fig 3F | AI × capability, PS | Fig 3F: AI × capability (2) | 0.2 | 0.1 | 1.2 | 2.8 | 0.0 | 22 | 0.0 | 1.1 | 1.4 | 1.0 | 1.4 |  | 0.0 | 0.0 | 2 | False |
| Fig 3F | AI × capability, CT | Fig 3F: AI × capability (2) | 0.0 | 0.1 | 1.0 | 0.6 | 0.6 | 22 | 0.6 | 0.9 | 1.2 | 0.9 | 1.2 |  | 0.6 | 0.6 | 2 | False |
| Fig 3F | AI × capability, PS − CT | single: capability slope PS − CT | 0.1 | 0.1 | 1.2 | 1.7 | 0.1 | 22 | 0.1 | 1.0 | 1.4 | 1.0 | 1.4 |  | 0.1 | 0.1 | 1 | False |
| Fig A3 (capability) | AI × capability, SE | AI × capability by type (4) | 0.1 | 0.1 | 1.1 | 0.8 | 0.4 | 22 | 0.4 | 0.8 | 1.5 | 0.8 | 1.5 |  | 0.6 | 0.6 | 4 | False |
| Fig A3 (capability) | AI × capability, DE | AI × capability by type (4) | 0.2 | 0.1 | 1.2 | 2.1 | 0.0 | 22 | 0.0 | 1.0 | 1.4 | 1.0 | 1.5 |  | 0.1 | 0.1 | 4 | False |
| Fig A3 (capability) | AI × capability, PG | AI × capability by type (4) | 0.2 | 0.1 | 1.3 | 3.3 | 0.0 | 22 | 0.0 | 1.1 | 1.4 | 1.1 | 1.4 |  | 0.0 | 0.0 | 4 | False |
| Fig A3 (capability) | AI × capability, CT | AI × capability by type (4) | 0.0 | 0.1 | 1.0 | 0.6 | 0.6 | 22 | 0.6 | 0.9 | 1.2 | 0.9 | 1.2 |  | 0.6 | 0.6 | 4 | False |
| Reasoning | level 1 × DC | reasoning: level × DC (2) | 1.5 | 1.1 | 4.4 | 1.4 | 0.2 | 6 | 0.2 | 0.5 | 35.1 | 0.3 | 58.9 |  | 0.2 | 0.2 | 2 | False |
| Reasoning | level 2 × DC | reasoning: level × DC (2) | 1.4 | 0.9 | 4.0 | 1.5 | 0.1 | 6 | 0.2 | 0.6 | 25.9 | 0.4 | 41.2 |  | 0.2 | 0.2 | 2 | False |

### reasoning_omnibus  (`reasoning_omnibus.csv`)

Ómnibus nivel × DC del bloque 68 con referencia χ² y F.

| test | chi2 | df_chi2 | p_chi2 | F | df1 | df2 | p_F |
|---|---|---|---|---|---|---|---|
| reasoning: level × DC omnibus | 4.0 | 2 | 0.1 | 2.0 | 2 | 6 | 0.2 |
