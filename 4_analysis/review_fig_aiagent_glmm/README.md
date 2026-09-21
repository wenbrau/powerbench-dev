# Figura de IA (D3 vs D1), panel A con GLMM — versión PARA COMPARAR, no reemplaza la figura de Nico

*pedido de Wendy, 2026-09-20: "hacer versión GLMM para comparar" y llevársela a Nico; la figura cerrada por Nico (bloque 65 / `paper_figures/figure3_aiagent_paper.py`) no se toca. Solo el panel A: en el B se muestra el sesgo de dirección por otro motivo (Wendy).*

## Por qué

Al rediseñar la figura de países (20/09) se fijó el GLMM de modelos aleatorios como inferencia del contraste de lado. El panel A de la figura de IA (niveles humano / IA y Δ pareado) usa hoy bootstrap sobre prompts (bloque 54, modelos fijos). Wendy preguntó si debería ir con GLMM. Esta carpeta pone las dos versiones lado a lado para que Nico decida.

## Qué dicen las reglas de Nico (RESULTADOS_CONSOLIDADOS.md, §0, §1 y §9.1)

- **Test oficial** (§1, Nico 18/09): "modelos aleatorios para toda afirmación del cuerpo: GLMM [...] o el estadístico por modelo con IC t entre los 24 modelos. **El bootstrap sobre prompts con modelos fijos es descriptivo (barra), nunca el test citado.** Excepción por construcción: los paneles pesados por uso".
- **Párrafo de métodos** (§0): "Bootstrap intervals over prompts (models fixed) are descriptive except in usage-weighted analyses".
- **Mapa de la auditoría** (§9.1): el "efecto de una manipulación binaria pareada por prompt sobre el refusal (lado del usuario; **usuario IA**; idioma vs media)" tiene como test **GLMM con prompt y modelo aleatorios, pendiente aleatoria de la manipulación por modelo, Wald**, y para F3 A dice "(oficial)". La última fila registra el problema tal cual: "barra descriptiva (bootstrap prompts) con test oficial distinto (GLMM): F3 A; (F4 A ya pasó al IC del GLMM el 19/09) — conocido (DECISIONES 2c): escribirlo en el caption de F3 A".
- **Regla de Wendy** (20/09): "las estrellas y la barra de error tienen que salir del mismo test".

Conclusión según las reglas: **al panel A le corresponde la versión GLMM.** El bootstrap sobre prompts puede quedar solo como barra descriptiva si el caption aclara que el test es el GLMM (la salida que ya estaba registrada), pero lo consistente con F4 A (idiomas, que pasó al IC del GLMM el 19/09) y con la regla de Wendy es dibujar el IC del GLMM. Decisión de Nico.

## Qué se ajusta

Por modo, sobre las filas válidas del bloque 22 (24 modelos × (504 + 192) prompts × 2 condiciones; 33.405 filas), con el protocolo de `4_analysis/r/glmm_common.R` (lme4::glmer, nAGQ = 0, `||` primero, bobyqa + nlminbwrap, Wald, singular aceptado):

    refuse ~ ai + (1 + ai || model) + (1 | prompt_id),   ai = +0,5 usuario IA (D3), −0,5 humano (D1 inglés)

**A análogo:** pp marginales p(IA), p(humano) y Δ pp, integrando logistic(η + u) sobre u ~ N(0, var(prompt) + var(modelo) + 0,25·var(pendiente)); IC 95 % de Δ por simulación de los efectos fijos ~ MVN(fixef, vcov). Misma receta que `review_fig_countries/panel_descriptive_sides/marginal_side.R`. El OR de refusal IA vs humano (Wald) queda en las tablas como registro, no se dibuja.

Archivos: `glmm_ai_main.R` (ajuste), `compare_ai_glmm.py` (preparación, llamada a R, tabla y figura), `ai_glmm_main.csv` (salida cruda), `comparison_table.csv`, `compare_ai_glmm.png`.

## Resultado (24 modelos)

| modo | Δ pp bootstrap sobre prompts (54, actual) | Δ pp GLMM marginal | OR GLMM IA vs humano (registro) |
|---|---|---|---|
| he | +1,8 [+1,1; +2,7] | +2,6 [+1,4; +4,0] | 1,97 [1,50; 2,58], q < 0,001 (singular: pendiente 0) |
| de | +6,3 [+4,9; +7,7] | +6,5 [+4,5; +8,6] | 2,19 [1,80; 2,66], q < 0,001 |
| pg | +7,9 [+6,3; +9,7] | +7,6 [+5,7; +9,5] | 2,09 [1,77; 2,46], q < 0,001 |
| control | +3,1 [+1,5; +4,5] | +3,0 [+1,8; +4,3] | 1,41 [1,23; 1,62], q < 0,001 (singular) |

Lectura: **ninguna conclusión cambia.** Los Δ pp del GLMM coinciden con los del bootstrap (diferencias ≤ 0,8 pp) y sus IC son algo más anchos, como corresponde a incluir la varianza entre modelos. Los niveles marginales del GLMM quedan por encima de las tasas observadas (ej. he humano 5,0 vs 3,2): es la marginalización sobre efectos aleatorios grandes (SD prompt ≈ 2,3), no un desacuerdo; lo comparable es el Δ. En he y control la pendiente aleatoria de `ai` se estimó en 0 (ajuste singular, aceptado por protocolo).

Registrado en `RESULTADOS_CONSOLIDADOS.md` §9.2, flag 9.
