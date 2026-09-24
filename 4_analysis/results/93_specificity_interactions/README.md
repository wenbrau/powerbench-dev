# Tests directos de especificidad: interacciones que faltaban para las afirmaciones de 'específico'

*computado a pedido de Nico (24/09), rama nagq1-rerun (nAGQ = 1); lectura pendiente del equipo · 2026-09-24 · commit `17ae987` · `93_specificity_interactions`*

## Question

¿El efecto que el paper llama específico de un tipo de pedido difiere significativamente del mismo efecto en el tipo con el que se lo compara? (diferencia de pendientes en un mismo ajuste, no significativo contra no significativo)

## Data

- D1 inglés + control y D2 inglés (18 condiciones), 24 modelos, veredictos de deepseek-v4-flash-0731; filas válidas.

Input files:

- `common/models_panel.py`
- `current/banks/dataset2_control_dyads_geobloc.v1.1.jsonl`
- `current/banks/dataset2_dyads_geobloc.v2.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/control_d2_geobloc_A19_pinned_off.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/control_d2_geobloc_v1.1_6models_pinned_off.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/control_d2_geobloc_v1.1_6models_pinned_off.rejudge_trunc5000_deepseek-v4-flash-0731.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/control_d2_geobloc_v1.1_newconds_6models_pinned_off.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/d2_geobloc_A19_pinned_off.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/d2_geobloc_v2_6models_pinned_off.jsonl.gz`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/d2_geobloc_v2_6models_pinned_off.rejudge_deepseek-v4-flash-0731.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/d2_geobloc_v2_6models_pinned_off.rejudge_trunc5000_deepseek-v4-flash-0731.jsonl`
- `C:/Users/Nico/Documents/GitHub/powerbench-dev-nagq1/current/runs/d2_geobloc_v2_newconds_6models_pinned_off.jsonl`
- `4_analysis/r/glmm_specificity.R`
- `4_analysis/r/glmm_common.R`
- `4_analysis/inputs/openrouter_usage/usage_30d_2026-08-18_2026-09-16.csv`
- `4_analysis/review_fig_languages_22models/panelD_bootstrap_draws.npz`

## Method

- GLMM (glmm_specificity.R, protocolo de glmm_common.R, nAGQ = 1): refuse ~ m × t [+ díada × t] [+ tipo] + (1 + m + t + m·t || model) + (1 | prompt_id); m:t = log del cociente de OR (tipo de interés / referencia). Escala − standing: refuse ~ escala + standing + (1 + escala + standing || model) + (1 | prompt_id), combinación lineal. Contraparte: refuse ~ toward + toward·r + díada + (1 + toward + toward·r || model) + (1 | prompt_id).
- Pesado por uso (Figura 2D): el estimador del bloque 73 (pesos por pedidos) en el tipo menos el del control; bootstrap sobre prompts (B = 5.000, semilla 73). Idiomas (Figura 4D): extracciones guardadas del bootstrap del panel, tipo − control, IC pivotal.
- BH dentro de cada familia (columna family), como las familias del paper para el panel de origen.

## Tables

### specificity_tests  (`specificity_tests.csv`)

Un test por fila. ratio = exp(estimate): cociente de OR (tipo de interés / referencia) o, en escala − standing, OR por nivel de escala / OR por nivel de standing.

| family | test | method | estimate | lo | hi | ratio | ratio_lo | ratio_hi | p | q_bh | n_family | OR_slope_reference | OR_slope_target | OR_slope_m | OR_slope_m2 | OR_slope_common | or_target | or_control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dirección × (tipo vs CT), china, 4 contrapartes | direction__china__all__he_vs_control | GLMM, Wald | 0.0 | -0.1 | 0.2 | 1.0 | 0.9 | 1.2 | 0.546 | 0.5 | 3 | 1.0 | 1.0 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__rival__de_vs_control | GLMM, Wald | -0.1 | -0.2 | 0.1 | 0.9 | 0.8 | 1.1 | 0.583 | 0.6 | 12 | 1.0 | 1.0 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__ally__pg_vs_control | GLMM, Wald | 0.2 | 0.1 | 0.4 | 1.3 | 1.1 | 1.5 | 0.009 | 0.1 | 12 | 1.0 | 1.3 | nan | nan | nan | nan | nan |
| lado × (PS vs CT), GLMM | side__ps_vs_control | GLMM, Wald | 0.2 | 0.0 | 0.3 | 1.2 | 1.0 | 1.3 | 0.017 | 0.0 | 1 | 0.9 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__ally__he_vs_control | GLMM, Wald | -0.1 | -0.3 | 0.1 | 0.9 | 0.7 | 1.1 | 0.225 | 0.3 | 12 | 1.0 | 0.9 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__ally__pg_vs_control | GLMM, Wald | 0.1 | -0.1 | 0.3 | 1.1 | 0.9 | 1.4 | 0.198 | 0.2 | 12 | 1.0 | 1.2 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, 4 contrapartes | direction__usa__all__he_vs_control | GLMM, Wald | -0.1 | -0.3 | -0.0 | 0.9 | 0.8 | 1.0 | 0.031 | 0.0 | 3 | 1.0 | 0.9 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__neutral__he_vs_control | GLMM, Wald | 0.2 | -0.0 | 0.5 | 1.2 | 1.0 | 1.6 | 0.097 | 0.2 | 12 | 0.9 | 1.2 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__neutral__pg_vs_control | GLMM, Wald | 0.2 | -0.0 | 0.3 | 1.2 | 1.0 | 1.4 | 0.089 | 0.2 | 12 | 1.1 | 1.3 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, 4 contrapartes | direction__usa__all__de_vs_control | GLMM, Wald | 0.2 | 0.1 | 0.3 | 1.3 | 1.1 | 1.4 | 0.000 | 0.0 | 3 | 1.0 | 1.3 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__neutral__de_vs_control | GLMM, Wald | 0.2 | 0.0 | 0.4 | 1.3 | 1.0 | 1.6 | 0.019 | 0.1 | 12 | 1.1 | 1.4 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__neutral__pg_vs_control | GLMM, Wald | 0.3 | 0.1 | 0.5 | 1.4 | 1.1 | 1.6 | 0.001 | 0.0 | 12 | 0.9 | 1.3 | nan | nan | nan | nan | nan |
| escala × (tipo vs SE) | scale__de_vs_he | GLMM, Wald | 0.1 | -0.6 | 0.8 | 1.1 | 0.5 | 2.2 | 0.830 | 0.8 | 2 | 1.6 | 1.7 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, 4 contrapartes | direction__china__all__de_vs_control | GLMM, Wald | 0.0 | -0.1 | 0.2 | 1.1 | 0.9 | 1.2 | 0.470 | 0.5 | 3 | 1.0 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__neutral__he_vs_control | GLMM, Wald | -0.1 | -0.3 | 0.2 | 0.9 | 0.7 | 1.2 | 0.672 | 0.7 | 12 | 1.1 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__neutral__de_vs_control | GLMM, Wald | 0.2 | 0.0 | 0.4 | 1.2 | 1.0 | 1.5 | 0.047 | 0.1 | 12 | 0.9 | 1.1 | nan | nan | nan | nan | nan |
| escala × (tipo vs SE) | scale__pg_vs_he | GLMM, Wald | 0.9 | 0.2 | 1.7 | 2.6 | 1.3 | 5.3 | 0.009 | 0.0 | 2 | 1.6 | 4.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, 4 contrapartes | direction__china__all__pg_vs_control | GLMM, Wald | 0.1 | -0.0 | 0.2 | 1.1 | 1.0 | 1.2 | 0.123 | 0.4 | 3 | 1.0 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__rival__he_vs_control | GLMM, Wald | -0.3 | -0.5 | -0.0 | 0.8 | 0.6 | 1.0 | 0.042 | 0.1 | 12 | 0.9 | 0.7 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__power__pg_vs_control | GLMM, Wald | 0.2 | -0.0 | 0.4 | 1.2 | 1.0 | 1.4 | 0.092 | 0.2 | 12 | 1.0 | 1.1 | nan | nan | nan | nan | nan |
| escala − standing (PS) | scale_minus_standing__ps | GLMM, Wald | 0.5 | 0.2 | 0.9 | 1.7 | 1.2 | 2.6 | 0.006 | 0.0 | 1 | nan | nan | 2.4 | 1.4 | nan | nan | nan |
| dirección × (tipo vs CT), usa, 4 contrapartes | direction__usa__all__pg_vs_control | GLMM, Wald | 0.2 | 0.1 | 0.3 | 1.2 | 1.1 | 1.3 | 0.002 | 0.0 | 3 | 1.0 | 1.2 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__ally__he_vs_control | GLMM, Wald | 0.0 | -0.2 | 0.3 | 1.0 | 0.8 | 1.3 | 0.811 | 0.8 | 12 | 1.0 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__rival__de_vs_control | GLMM, Wald | 0.4 | 0.1 | 0.6 | 1.4 | 1.2 | 1.8 | 0.001 | 0.0 | 12 | 0.9 | 1.3 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__ally__de_vs_control | GLMM, Wald | 0.2 | 0.0 | 0.4 | 1.2 | 1.0 | 1.4 | 0.047 | 0.1 | 12 | 1.0 | 1.2 | nan | nan | nan | nan | nan |
| lado × (tipo vs CT), GLMM | side__he_vs_control | GLMM, Wald | -0.1 | -0.3 | 0.1 | 0.9 | 0.8 | 1.1 | 0.272 | 0.3 | 3 | 0.9 | 0.9 | nan | nan | nan | nan | nan |
| dirección × contraparte, USA, SE | counterpart__usa__he__rival_vs_ally_neutral | GLMM, Wald | -0.4 | -0.6 | -0.1 | 0.7 | 0.5 | 0.9 | 0.003 | 0.0 | 2 | nan | nan | nan | nan | 0.9 | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__rival__he_vs_control | GLMM, Wald | 0.1 | -0.2 | 0.4 | 1.1 | 0.8 | 1.4 | 0.687 | 0.7 | 12 | 1.0 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__ally__de_vs_control | GLMM, Wald | 0.2 | -0.0 | 0.4 | 1.2 | 1.0 | 1.5 | 0.068 | 0.2 | 12 | 1.0 | 1.2 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__rival__pg_vs_control | GLMM, Wald | 0.2 | 0.0 | 0.4 | 1.3 | 1.0 | 1.5 | 0.015 | 0.1 | 12 | 0.9 | 1.1 | nan | nan | nan | nan | nan |
| dirección × contraparte, USA, SE | counterpart__usa__he__rival_and_china_vs_ally_neutral | GLMM, Wald | -0.3 | -0.6 | -0.1 | 0.7 | 0.6 | 0.9 | 0.018 | 0.0 | 2 | nan | nan | nan | nan | 0.9 | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__power__he_vs_control | GLMM, Wald | -0.2 | -0.4 | 0.1 | 0.9 | 0.7 | 1.1 | 0.183 | 0.2 | 12 | 1.0 | 0.8 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__power__he_vs_control | GLMM, Wald | 0.2 | -0.1 | 0.4 | 1.2 | 0.9 | 1.5 | 0.183 | 0.3 | 12 | 1.0 | 1.2 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__power__de_vs_control | GLMM, Wald | -0.1 | -0.3 | 0.0 | 0.9 | 0.7 | 1.0 | 0.138 | 0.2 | 12 | 1.0 | 0.9 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__rival__pg_vs_control | GLMM, Wald | -0.1 | -0.3 | 0.1 | 0.9 | 0.8 | 1.1 | 0.391 | 0.5 | 12 | 1.0 | 0.9 | nan | nan | nan | nan | nan |
| lado × (tipo vs CT), GLMM | side__de_vs_control | GLMM, Wald | 0.2 | 0.1 | 0.4 | 1.3 | 1.1 | 1.5 | 0.000 | 0.0 | 3 | 0.9 | 1.2 | nan | nan | nan | nan | nan |
| lado × (tipo vs CT), GLMM | side__pg_vs_control | GLMM, Wald | 0.2 | 0.0 | 0.4 | 1.2 | 1.0 | 1.4 | 0.019 | 0.0 | 3 | 0.9 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), usa, por contraparte | direction__usa__power__de_vs_control | GLMM, Wald | 0.1 | -0.0 | 0.3 | 1.2 | 1.0 | 1.4 | 0.138 | 0.2 | 12 | 1.0 | 1.1 | nan | nan | nan | nan | nan |
| dirección × (tipo vs CT), china, por contraparte | direction__china__power__pg_vs_control | GLMM, Wald | -0.2 | -0.4 | 0.0 | 0.8 | 0.7 | 1.0 | 0.092 | 0.2 | 12 | 1.0 | 0.9 | nan | nan | nan | nan | nan |
| escala − standing (PG) | scale_minus_standing__pg | GLMM, Wald | 0.9 | 0.3 | 1.5 | 2.4 | 1.3 | 4.4 | 0.005 | 0.0 | 1 | nan | nan | 4.1 | 1.7 | nan | nan | nan |

*(50 rows; first 40 shown)*

### glmm_specificity_fits  (`glmm_specificity_fits.csv`)

Salida completa de R (todas las cantidades, diagnósticos del ajuste).
