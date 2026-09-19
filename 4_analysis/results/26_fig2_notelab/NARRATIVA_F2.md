# Figura 2 · D1 multilingüe · narrativa panel por panel

Fuente de verdad: `notebooks/PowerBench.md`, entradas del 2026-09-08 (narrativa) y 2026-09-14 (criterios).
Mismo método que la Figura 1 (`25_fig1_notelab/NARRATIVA_F1.md`): un panel por vez; Nico revisa, pide
cambios, aprueba; cada test queda copiado acá con sus números y su bloque; cada decisión citada con
fecha. Métricas: bloque 26 (`analysis_26_fig2_notelab.py`). Gráficos en el estilo aprobado para la
Figura 1: bloque 34 (`analysis_34_fig2_v2.py`, carpeta `34_fig2_v2/`). Interpretación del equipo.

### Narrativa (cuaderno, 8/09)

> Métrica: diferencia entre el refusal rate en un idioma y el refusal rate en inglés. Quizás otra
> métrica es rango de refusal (idioma con más refusal - idioma con menos refusal). Quizás esto en vez de
> hacerlo en pp hay que hacerlo en logits.
> La idea sería verlo en las mismas variables que antes para ver si detectamos sesgos distintos
> dependiendo del modelo, del modo, etc.
> si existe un idioma mas exploitable / si hay un idioma que aumenta el refusal / si hay modelos
> específicos que tienen comportamiento interesante para cierto idioma.
> los sesgos correlacionan con la cantidad de data del idioma, o algún proxy de eso?

Criterios del 14/09 que aplican: las versiones en otros idiomas son el mismo prompt traducido (pareado
por prompt); el sesgo se mide sobre prompts pareados; el mismo test en power shifting y, por separado,
en el control; proxy de representación del idioma pendiente de decisión (Wikipedia la vez pasada;
Common Crawl provisional en el bloque 26); reportar la proporción de respuestas truncadas por idioma y
modelo (5.000 tokens).

---

## Figura 2 completa (17/09) · `41_fig2_composite/figure2_full.png`

Pedido de Nico (17/09): "ahora mostrame la figura 2 completa". Bloque 41 (`analysis_41_fig2_composite.py`): solo ensambla,
lee las tablas de los bloques 34, 35, 38 y 40; ningún cálculo nuevo. **Estado: APROBADA como draft por Nico (17/09), con
el layout de dos filas: "así como draft me parece bien; cerramos figura 2". La Figura 2 queda cerrada; lo pendiente es
solo de apéndice (lista abajo).**

**Cambio del 17/09 en el panel B (criterio único con la Figura 3).** Nico: "si vamos a tomar un criterio, que sea igual en los
dos". Las barras de OBSERVADO (el modo y el control) ya no llevan barra de error; queda solo la del nulo (idiomas barajados).
Motivo: el rango max − min es un estadístico que el remuestreo de prompts infla, y su intervalo bootstrap queda corrido hacia
arriba con el valor observado pegado al borde inferior (control en OR: 2,84 con intervalo [2,70; 3,80]); ese intervalo no
describe la incertidumbre del observado. obs_lo / obs_hi siguen en `35_fig2_range_null/range_summary.csv`. Bloques 35 y 41
regenerados. Es una de las decisiones de Claude a revisar: `4_analysis/results/DECISIONES_A_REVISAR.md`, punto 1.

Cambio de layout pedido por Nico (17/09): "B necesita mucho menos espacio, y D necesita más" → la figura pasa de tres
filas a dos: arriba A (ancho) y B compacto (los mismos tres subpaneles he, de, pg con observado / idiomas barajados /
control, angostos, etiquetas verticales); abajo C (matriz + barras) y D, que pasa de ≈ 4,8 a ≈ 6,5 pulgadas de ancho y
con los idiomas sin rotar. Mismos datos y mismas barras; solo cambia el reparto del espacio (17 × 11,5 pulgadas).

| panel | qué muestra | gráfico aprobado | test acordado |
|---|---|---|---|
| A | refusal por idioma y modo (he, de, pg), media de 24 modelos, idiomas ordenados por refusal medio | `34_fig2_v2/pA_levels_by_language_bars_sorted.png` | bloque 36 (GLMM por modo, ómnibus de idioma + SD modelo × idioma) |
| B | rango entre idiomas por modelo en OR, media de 24: observado, idiomas barajados dentro del prompt, control; he, de, pg | `35_fig2_range_null/p4_range_vs_null_or.png` | permutación del bloque 35 |
| C | acuerdo entre rankings de idiomas: matriz 24 × 24 (CN, US por capability) y medias CN–CN, US–US, mixto; power grabbing | `38_fig2_language_order/pC_rank_agreement_pg.png` | bloque 39 (permutación de etiquetas de origen y de idiomas dentro de modelo) |
| D | OR de refusal contra inglés de un pedido típico, pesado por uso (OpenRouter, 18/08–16/09/2026); power grabbing y control | `40_fig2_usage_weighted/pD_usage_weighted_or.png` | ninguno de pg contra control, por decisión de Nico ("es una interpretación") |

Lectura de Nico hasta acá: "en promedio no hay diferencia entre idiomas (sesgo promedio no existe) pero para cada modelo en
particular sí existe sesgo, lo que pasa es que esos sesgos se cancelan" (A y B, 16/09); en D, efecto específico de power
grabbing en francés e hindi, que no aparece en el control (17/09, interpretación sin test).

A apéndice (decisiones del 17/09): C magnitud (bloque 37), refusal contra prevalencia del idioma (bloque 34, p1d y p2b),
dirección contra capability (bloque 38, gráfico de pares), self-empowerment y disempowerment del panel D y el estimador
alternativo (bloque 40), variables de la Figura 1 por idioma (no prioritario), tabla de truncado por idioma y modelo (más
adelante). Swahili (*) siempre sin nemotron-3.5-lightning ni nova-2-lite.

---

## Panel 1 → PANEL A de la Figura 2 · Refusal por idioma y modo, en barras

**Estado: APROBADO por Nico (2026-09-16) en su versión de barras, con dos cambios: idiomas ordenados por
refusal medio y siempre sin los outliers de swahili.** "siendo el A el de barras por idioma y por modo;
aunque en el A, preferiría si ordenamos idioma por refusal medio; acordate de siempre excluir los
outliers de swahili". Gráfico final: `34_fig2_v2/pA_levels_by_language_bars_sorted.png` (media de 24
modelos, 22 en swahili; he, de, pg; orden ascendente por la media de los tres modos; intervalo bootstrap
sobre prompts; tabla `levels_excl_sw_outliers.csv`). Las versiones de cajas con puntos (p1) y de barras
con outliers (p1c, eliminada) quedan como historia.

**Variante con la barra de error pareada (17/09). APROBADA por Nico el 18/09** al revisar la Figura 4 (registro y
bibliografía en `53_fig4_notelab/NARRATIVA_F4.md`, sección "Panel 2"): "me parece bien dejarlo así, pero hay otras figuras
en donde esto sea lo que hay que hacer y no lo estemos considerando? habría que hacerlo y mostrarlo así, incluyendo las
líneas punteadas del valor de referencia". Criterio general: comparación pareada contra una referencia → barra de error
del contraste pareado sobre cada barra, referencia sin barra, línea punteada en su nivel. La compuesta del bloque 41 se
regeneró con esta versión del panel A el 18/09 (inglés marcado "(referencia)", línea punteada por modo). Sigue pendiente
de Nico si cambia la lectura "en promedio no hay diferencia entre idiomas". Pedido original: "lo de figura 2 panel A,
podemos hacerlo de nuevo entonces con eso corregido?", después de la revisión de barras de error (registro completo en
`27_fig3_notelab/NARRATIVA_F3.md`). Gráfico: `34_fig2_v2/pA_levels_by_language_bars_sorted_paired_ci.png`; tabla:
`delta_vs_english_excl_sw_outliers.csv`. Mismas barras; lo que cambia es la barra de error: antes era el IC del NIVEL de
cada idioma (semiancho medio ± 3,7 pp en pg, ± 2,8 en de, ± 1,4 en he; lo domina la diferencia entre prompts), ahora es el
IC 95 % de la DIFERENCIA pareada contra inglés (mismos prompts, mismos modelos; ± 1,7 en pg, ± 1,6 en de, ± 0,8 en he),
dibujado alrededor de cada barra; una línea punteada marca el nivel de inglés en cada modo e inglés no lleva barra. Una
barra de error que no cruza la línea = idioma distinguible de inglés. (En swahili la diferencia usa los 22 modelos
incluidos, así que la línea de inglés de 24 modelos es una guía aproximada para esa barra.)

Diferencias que excluyen el cero (bootstrap sobre prompts, modelos fijos, B = 2000; p sin corregir, q = BH sobre las 21):
he Hindi +2,1 pp [+1,3; +3,1] (p < 0,001) y swahili +1,8 [+1,0; +2,7] (p < 0,001); de Hindi +3,3 [+1,3; +5,3] (p = 0,003,
q = 0,016); pg Hindi +3,3 [+1,6; +5,0] (p < 0,001) y francés +2,2 [+0,7; +3,7] (p = 0,005, q = 0,021). El resto cruza el
cero (los más cercanos: he chino +0,7 y francés +0,7, de alemán −1,4; p = 0,06–0,07). Sin los dos outliers, swahili en pg
queda en −1,6 [−3,9; +0,5].

Esto no contradice el test aprobado del panel A (bloque 36, ómnibus pg p = 0,34): ese GLMM trata modelo × idioma como
aleatorio (¿el efecto medio se distingue de la heterogeneidad entre modelos?); el bootstrap deja los modelos fijos (¿el
promedio de estos 24 modelos cambia con el idioma?). **A decidir por Nico: si esta variante reemplaza a la aprobada en
la figura compuesta (bloque 41) y si cambia la lectura "en promedio no hay diferencia entre idiomas".**

**Regla permanente desde el 16/09: nemotron-3.5-lightning y nova-2-lite se excluyen en swahili en todos
los paneles y tests de la Figura 2.**

**Corrección del 17/09 sobre el motivo de la exclusión.** Las proporciones de truncado estaban invertidas
en los mensajes del 16/09. Lo correcto (bloque 26, `truncation_by_language_model.csv`): nova-2-lite tiene
el 85,0 % de sus respuestas en swahili cortadas a 5.000 tokens; nemotron-3.5-lightning el 24,7 % en swahili
y el 9,4 % en hindi (resto < 1 %). Es decir: el swahili de nova-2-lite está dominado por el truncado; el de
nemotron-3.5-lightning (refusal 86 % en swahili, 51 % en hindi, 8 % en inglés) es un outlier de
comportamiento con truncado parcial, no un artefacto puro. La exclusión de ambos en swahili sigue siendo
decisión de Nico; este dato es para que la justifique como corresponde en el paper.

### Test del panel A (bloque 36, `analysis_36_fig2_language_glmm.py` + `r/glmm_language.R`) — APROBADO por Nico (16/09): "este test me parece bien, guardemos para A"

Propuesta de Claude aprobada por Nico (16/09, "dale, correlo"): por modo, GLMM
`refuse ~ idioma + (1 | prompt_id) + (1 | model) + (1 | model:idioma)`, idioma en contrastes suma-cero, sin
las filas de swahili de los dos outliers; nAGQ = 0. El intercepto por prompt aparea los idiomas; el de
modelo × idioma es el perfil propio de cada modelo y entra en el error del efecto promedio. Tres salidas:
ómnibus (¿hay efecto promedio?), desviación por idioma con BH (¿cuál?), y SD(modelo × idioma) contra la
SD de las 8 desviaciones fijas (¿cuánto es promedio y cuánto por modelo?). Ajustes de 11 a 22 s.

| modo | ómnibus χ²(7) | p | SD modelo × idioma | SD promedio por idioma | cociente |
|---|---|---|---|---|---|
| Self-empowerment | 20.2 | 0.00517 | 0.70 | 0.29 | 2.4 |
| Disempowerment | 9.4 | 0.222 | 0.68 | 0.16 | 4.1 |
| Power grabbing | 7.9 | 0.343 | 0.65 | 0.14 | 4.6 |
| Control | 8.9 | 0.259 | 0.57 | 0.14 | 4.1 |

Desviación de cada idioma respecto de la media del modo (log-odds; * p < 0,05; ** p < 0,05 tras BH):

| idioma | he | de | pg | control |
|---|---|---|---|---|
| English | -0.19 | -0.02 | +0.01 | +0.23 * |
| German | -0.39 * | -0.18 | -0.14 | +0.02 |
| French | +0.09 | -0.06 | +0.14 | +0.00 |
| Spanish | -0.08 | -0.05 | +0.00 | +0.00 |
| Portuguese | -0.33 | -0.05 | -0.11 | -0.08 |
| Chinese | +0.04 | -0.07 | -0.00 | -0.12 |
| Hindi | +0.36 * | +0.41 ** | +0.28 * | +0.16 |
| Swahili | +0.49 ** | +0.02 | -0.18 | -0.22 |

- El efecto promedio del idioma no se separa de 0 en power grabbing (p = 0,34), disempowerment (p = 0,22)
  ni control (p = 0,26); sí en self-empowerment (p = 0,005), donde hindi y swahili suben desde una base
  de 3 %.
- La variación del efecto del idioma entre modelos (SD modelo × idioma 0,57–0,70 log-odds) es 4 a 4,6
  veces la variación del efecto promedio entre idiomas (SD 0,14–0,16) en disempowerment, power grabbing y
  control, y 2,4 veces en self-empowerment (SD promedio 0,29, por hindi y swahili). Es la formalización de
  "el idioma importa por modelo, no en promedio", y coincide con el panel B.
- Contraste con el bootstrap del bloque 26 (modelos fijos): allí francés, hindi y swahili se separaban del
  inglés en pg; con el modelo × idioma como efecto aleatorio esa diferencia deja de sostenerse como
  promedio generalizable a otros modelos. Interpretación pendiente del equipo.


Nico (16/09), sobre la v1 (Δ vs inglés con cajas US/CN): "no sé si quiero seguir con cajas US/CN
[...] no me resulta muy intuitivo esto; creo que lo primero que hay que mostrar es refusal rate para
cada idioma (sin hacer la diferencia con inglés, refusal crudo)". La v1 queda como candidato p1b para
un panel posterior (la diferencia vs inglés es la métrica que pide el cuaderno).

### Preguntas que plantea

1. ¿Cuánto rechaza cada modelo en cada idioma, modo por modo? ¿Hay idiomas que suben o bajan el refusal
   respecto del resto?
2. ¿Se ve igual en power shifting y en control?

### Gráfico: `34_fig2_v2/p1_levels_by_language.png`

- Cuatro paneles (self-empowerment, disempowerment, power grabbing, control); eje x los 8 idiomas con
  inglés primero (línea punteada lo separa); eje y refusal %.
- Cada punto un modelo (192 prompts por idioma y modo); una sola caja por idioma = mediana y cuartiles
  entre los 24 modelos; sin desglose US/CN; eje hasta 80.

### Cómo se calculó (bloque 26)

- R(modo, idioma) por modelo sobre las 192 filas válidas; intervalos bootstrap sobre prompts
  (`levels_per_model.csv`); pooled = media con peso igual por modelo (`levels_pooled.csv`).

### Qué dicen los datos (media de 24 modelos, %)

| idioma | he | de | pg | control |
|---|---|---|---|---|
| English | 3,1 | 14,5 | 23,6 | 20,3 |
| German | 2,8 | 13,1 | 22,7 | 18,8 |
| French | 3,8 | 14,5 | 25,9 | 18,8 |
| Spanish | 3,3 | 14,0 | 24,4 | 18,5 |
| Portuguese | 2,7 | 13,9 | 23,1 | 17,5 |
| Chinese | 3,8 | 14,4 | 24,6 | 17,7 |
| Hindi | 5,2 | 17,8 | 26,9 | 20,1 |
| Swahili | 9,7 | 19,4 | 26,6 | 21,2 |

- Los niveles por idioma se mueven poco frente a la dispersión entre modelos (en pg, de 22,7 a 26,9 %
  contra un rango entre modelos de 3 a 53 %): el idioma es un efecto de segundo orden a nivel pooled.
- Hindi y swahili son los idiomas más altos en los tres modos de power shifting; en self-empowerment
  swahili triplica el inglés (9,7 vs 3,1 %). En control las diferencias entre idiomas son menores.
- Verificación (16/09, ante la duda de Nico: "antes veíamos tasas de refusal muy distintas entre
  idiomas"): recomputado desde los datos crudos (147.428 filas válidas, 24 modelos, 8 idiomas) da
  exactamente la tabla de arriba; coincide con el bloque 20 (Tomás) y el 17 (wen). Las diferencias
  grandes que se recuerdan son (a) de la era de 6 modelos con el juez viejo (bloque 02: hindi +9,9 pp,
  chino +7,5 pp pooled) y (b) por modelo: en pg el rango entre idiomas de un mismo modelo tiene mediana
  19 pp (deepseek-v4-pro 20 → 43 % en francés; haiku-4.5 27 → 52 % en chino; nova-2-lite 12 → 52 % en
  swahili; hy3 29 → 9 %; nemotron-3.5-lightning 4 → 86 %). Como el signo cambia de modelo a modelo y de
  bloque a bloque, el promedio de 24 se queda en 2–3 pp. Por eso este panel se ve plano y el sesgo por
  idioma hay que mostrarlo por modelo (Δ pareada o rango por modelo).
- Interpretación pendiente del equipo.

### Decisiones abiertas (del equipo)

- Si este panel va con los cuatro modos o solo con power shifting (control a apéndice, como en F1 v2).
- Puntos coloreados por origen (US/CN) o neutros como ahora.
- Escala pp o logit (para el panel de diferencias).

### Cambios pedidos por Nico

- 2026-09-16: v1 (Δ vs inglés, cajas US/CN) → v2 refusal crudo por idioma, una caja por idioma, sin US/CN.
- 2026-09-16: "a ver el mismo dato pero tipo gráfico de barras? solo 3 modos, sin control, con barras de
  error" → `p1c_levels_by_language_bars.png`: media de 24 modelos por idioma, tres barras por idioma
  (he, de, pg), barra de error = intervalo bootstrap 95 % sobre prompts (`levels_pooled.csv`). p1 (cajas
  con puntos) queda como alternativa hasta que Nico elija.

Lectura de Nico sobre las barras (16/09): "la figura de las barras de antes me gusta". Su duda "¿concluimos
entonces que idioma no afecta refusal?" quedó respondida así: barras solapadas no es "sin diferencia"
(la comparación correcta es pareada por prompt: fr +2,2 [+0,7; +3,8], hi +3,3 [+1,6; +5,0], sw +3,0
[+0,8; +5,2] pp en pg); el efecto promedio es chico y el efecto por modelo grande y de signo cambiante
(mediana del rango entre idiomas dentro de un modelo: 19 pp; 61 de 168 contrastes modelo × idioma en
pg pasan BH en el bloque 20). Conclusión sostenible: el idioma casi no cambia el promedio del panel pero
cambia mucho el de cada modelo. Pendiente de que Nico la haga suya.


### Verificación: ¿por qué difiere de lo que recordábamos con 6 modelos y el juez nano? (16/09)

Pregunta de Nico: "cómo dan los resultados con los 6 modelos que habíamos hecho al principio y el juez
nano? [...] no entiendo por qué es tan distinto a lo que recuerdo". Comparación entre el bloque 02
(nano, 6 modelos, 2/09) y el bloque 26 (deepseek, 24 modelos):

- **El juez no es la causa.** Para los mismos 5 modelos originales (sin solar-pro4), Δ R(pg) vs inglés
  con nano y con deepseek casi coincide: hindi +11,6 / +12,2; francés +9,4 / +10,2; chino +7,9 / +8,9;
  alemán +3,8 / +4,4; swahili +3,4 / +2,9 pp. deepseek es más estricto en nivel (+7 a +9 pp en todos
  los idiomas, bloque 10) pero no cambia el orden de los idiomas (ρ = 0,93).
- **La causa es el panel.** Los 5 originales suben en casi todos los idiomas; los 19 agregados después
  son otra mezcla. Media de Δ R(pg) vs inglés (pp):

| grupo | de | fr | es | pt | zh | hi | sw |
|---|---|---|---|---|---|---|---|
| 5 originales (haiku-4.5, minimax-m3, kimi-k2.6, deepseek-v4-pro, gpt-5.6-luna) | +4,4 | +10,2 | +2,6 | +1,0 | +8,9 | +12,2 | +2,9 |
| 19 nuevos | −2,3 | +0,1 | +0,3 | −1,0 | −1,1 | +1,0 | +3,0 |
| 19 nuevos, US (7) | +1,7 | +1,0 | +5,1 | +1,9 | −1,7 | +6,4 | +13,4 |
| 19 nuevos, CN (12) | −6,8 | −0,9 | −5,0 | −4,2 | −0,5 | −5,1 | −8,4 |

  Fracción de modelos con Δ > 0 en hindi: 5 de 5 originales, 8 de 19 nuevos; en francés 5 de 5 vs 9 de 19.
- Conclusión: lo que se recordaba (hindi +10, chino +7, francés +8) era cierto para esos 5 modelos y lo
  sigue siendo con el juez actual; con 24 modelos el promedio baja a 2–3 pp porque muchos de los nuevos,
  sobre todo los 12 CN (de los cuales solo minimax y kimi-k2.6 estaban en el panel original), se mueven
  poco o hacia abajo. Refuerza la lectura "el idioma es un efecto por modelo, no del panel".

---

## Panel 2 · Power grabbing por idioma y origen del modelo

**Estado: borrador, pendiente de revisión (2026-09-16).** Pedido de Nico: "un panel B, solo con power
grabbing, donde veamos dos barras por idioma, una para modelos US y otra para modelos CN".

### Pregunta que plantea

¿El efecto del idioma sobre el refusal de power grabbing es distinto en los modelos US y en los CN?

### Gráfico: `34_fig2_v2/p2_pg_by_language_origin_bars.png`

- Solo power grabbing. Por idioma dos barras: media de los 12 modelos US (azul) y de los 12 CN (roja);
  barra de error = intervalo bootstrap 95 % sobre prompts (modelos fijos). Inglés primero.

### Qué dicen los datos (power grabbing, %)

| idioma | US (12) | CN (12) |
|---|---|---|
| English | 21,7 | 25,6 |
| German | 23,2 | 22,2 |
| French | 23,5 | 28,3 |
| Spanish | 26,1 | 22,7 |
| Portuguese | 23,2 | 23,0 |
| Chinese | 21,8 | 27,3 |
| Hindi | 28,5 | 25,3 |
| Swahili | 32,4 | 20,8 |

- En inglés los CN rechazan más que los US (25,6 vs 21,7). El orden se invierte en los idiomas de menos
  recursos: en swahili los US suben a 32,4 y los CN bajan a 20,8; en hindi 28,5 vs 25,3. En chino y
  francés los CN quedan arriba (27,3 y 28,3).
- Diferencias pareadas vs inglés por bloque (bloque 26): US sube en swahili +10,8, hindi +6,9, español
  +4,4 (todas con IC fuera de 0); CN baja en swahili −4,8, alemán −3,4, español −2,9, portugués −2,6 y
  sube solo en francés +2,7.
- Advertencia: la barra de swahili US incluye a nova-2-lite (85 % de respuestas cortadas a 5.000 tokens,
  refusal 52 %) y nemotron-3.5-lightning (25 % cortadas, refusal 86 %); sin ellos la media US en swahili baja. Ver
  truncation_by_language_model.csv.
- Interpretación pendiente del equipo.

### Decisiones abiertas (del equipo)

- Test: interacción idioma × origen en el GLMM (con prompt pareado como intercepto aleatorio y modelo
  como intercepto y pendiente aleatoria), ómnibus de 7 gl; y el mismo en control.
- Qué hacer con los dos modelos con truncado masivo en swahili.

### Cambios pedidos por Nico

- 2026-09-16: "excluyamos a esos dos puntos en swahili que son outliers y recalculemos ambos gráficos,
  pero que el eje x sea lo que tenemos disponible para mostrar la prevalencia del idioma en la data;
  sería entonces más tipo scatterplot". → `p1d_levels_vs_share.png` (3 modos, media de 24; 22 en
  swahili) y `p2b_pg_by_origin_vs_share.png` (pg, US con 10 modelos en swahili y CN con 12): x = log10
  del % de páginas por idioma en Common Crawl CC-MAIN-2026-34 (proxy provisional del bloque 26; el
  cuaderno menciona Wikipedia como alternativa), y = media con intervalo bootstrap sobre prompts,
  recalculado sin nemotron-3.5-lightning ni nova-2-lite en swahili (solo en swahili). Tabla:
  `34_fig2_v2/levels_excl_sw_outliers.csv`.
  Efecto de la exclusión (solo swahili): pooled pg 26,6 → 22,8 %, de 19,4 → 15,0, he 9,7 → 4,9; US pg
  32,4 → 25,2 (10 modelos), CN sin cambio (20,8). El "swahili sube el refusal" de los paneles anteriores
  venía en buena parte de los dos modelos con truncado masivo; sin ellos, swahili queda en el nivel del
  inglés en pg (22,8 vs 23,6) y hindi es el idioma más alto en los tres modos (pg 26,9; de 17,8; he 5,2).
  En pg por bloque, sin outliers: US arriba en hindi (28,5 vs 25,3) y swahili (25,2 vs 20,8); CN arriba
  en inglés (25,6 vs 21,7), francés (28,3 vs 23,5) y chino (27,3 vs 21,8).

---

## Conclusión de Nico sobre A y B (16/09) y qué falta para cerrar la Figura 2

> Conclusión por ahora: en promedio no hay diferencia entre idiomas (sesgo promedio no existe) pero para
> cada modelo en particular sí existe sesgo, lo que pasa es que esos sesgos se cancelan; lo que faltaría
> mostrar es de qué depende ese sesgo que mostramos en B: ¿depende de si es CN vs US? ¿Depende de
> capabilities? Esas preguntas (de qué depende) valen tanto para la magnitud del sesgo (medido como el
> rango) como también para la dirección del sesgo (ahí no solamente mirando extremos, sino con alguna
> noción de orden). Eso para mí cerraría la narrativa de la figura 2.

### Panel C · propuestas (17/09)

- **Primera propuesta (bloque 37), rechazada en su mitad de dirección.** Magnitud = rango en OR por modelo contra
  origen y capability; dirección = pendiente del refusal contra la prevalencia del idioma. Nico: "no, eso no es lo
  que quiero; no es PARA NADA lo mismo que orden lo que calculaste". La pendiente impone un orden externo (la
  prevalencia); lo pedido es el orden propio de cada modelo. La mitad de magnitud del bloque 37 queda como
  candidata sin revisar (US 2,8 vs CN 2,9 en OR en pg; Spearman con capability −0,09).
- **Regla nueva de trabajo (Nico, 17/09): "desde ahora, no hagas más estadística primero, solo plots, y si me
  gustan y acordamos en la estadística, lo hacés."**
- **Segunda propuesta para la dirección (bloque 38, solo gráficos):** por modelo, el ranking de los 8 idiomas por
  refusal normalizado a 0–1 (0 = idioma con menos refusal para ese modelo, 1 = con más); sin swahili en los dos
  outliers. `38_fig2_language_order/pC_order_<modo>.png`: posición de cada idioma en el ranking de cada modelo,
  cajas US / CN y un punto por modelo, idiomas ordenados por posición media. `pC_order_matrix_<modo>.png`: lo
  mismo modelo por modelo (filas = modelos, US arriba, CN abajo, ordenados por capability; columnas = idiomas;
  color = posición en el ranking del modelo). Sin tests. Pendiente de revisión de Nico.
- **Tercera propuesta para la dirección (bloque 38 reescrito, solo gráficos).** Nico sobre la segunda: "no me
  convencen esos gráficos, no quiero mostrar cada idioma por separado, quiero alguna métrica de cuánto acuerdan los
  rankings entre ellos. Quizás matriz heatmap de 24x24, ordenada mitad CN y mitad US, que muestre correlación de
  rankings entre cada modelo y cada otro modelo? Y después promediamos correlación para todos los pares de modelos
  CN y todos los pares de modelos US y todos los pares mixtos, y mostramos eso como tres barras en un barplot con
  barras de error?" → `38_fig2_language_order/pC_rank_agreement_<modo>.png`: izquierda, matriz 24 × 24 de Spearman
  entre los rankings de idiomas de cada par de modelos (CN primero, después US; por capability dentro de bloque);
  derecha, media de los 66 pares CN–CN, 66 US–US y 144 mixtos con intervalo bootstrap 95 % sobre prompts. Pares con
  un modelo excluido: 7 idiomas. Sin tests. Valores descriptivos (Spearman medio): pg CN–CN +0,14, US–US +0,03,
  mixto −0,06; control +0,21 / +0,08 / −0,12; de +0,06 / +0,04 / −0,03; he +0,14 / +0,21 / +0,11. Las versiones
  idioma por idioma se eliminaron. Pendiente de revisión de Nico.
- **Dirección: gráfico APROBADO por Nico (17/09): "me parece que me gustan estos gráficos! podemos dejarlos y hacer la
  estadística correspondiente".** Estadística (bloque 39, `analysis_39_fig2_order_stats.py`), con los modelos como unidad:
  (1) origen: acuerdo dentro de bloque − mixto, nula por permutación de etiquetas de bloque entre los 24 modelos (10.000);
  (2) acuerdo distinto de cero: nula por permutación de los idiomas dentro de cada modelo (5.000).

  | modo | CN–CN | US–US | mixto | dentro − mixto | p origen | p CN–CN > 0 | p US–US > 0 | p mixto < 0 |
  |---|---|---|---|---|---|---|---|---|
  | self-empowerment | +0,14 | +0,21 | +0,11 | +0,07 | 0,056 | 0,009 | 0,001 | — (mixto > 0, p = 0,001) |
  | disempowerment | +0,06 | +0,04 | −0,03 | +0,07 | 0,073 | 0,11 | 0,20 | 0,18 |
  | power grabbing | +0,14 | +0,03 | −0,06 | +0,14 | 0,009 | 0,011 | 0,25 | 0,026 |
  | control | +0,21 | +0,08 | −0,12 | +0,27 | < 0,001 | 0,001 | 0,053 | < 0,001 |

  En power grabbing y en control el orden de idiomas depende del origen: los modelos de un mismo bloque acuerdan más entre
  sí que con los del otro (en pg por los CN: CN–CN − mixto +0,20, p = 0,003; US–US − mixto +0,09, p = 0,08), y los pares
  mixtos tienden a ordenar al revés. En self-empowerment todos acuerdan algo (también los mixtos) y el origen importa
  menos (p = 0,056); en disempowerment no hay acuerdo distinguible de cero. El acuerdo es bajo en valor absoluto (≤ 0,21).
  El efecto de origen es mayor en control que en power grabbing: no es específico de power shifting. Interpretación
  pendiente del equipo.
- **Magnitud: propuesta visual (bloque 37 reescrito, solo gráficos), pendiente de revisión.**
  `37_fig2_bias_dependence/pC_magnitude_<modo>.png`: por modelo, rango de refusal entre idiomas en OR (la métrica del
  panel B), izquierda por origen (cajas US / CN, un punto por modelo), derecha contra el índice de capability; eje
  logarítmico; sin tests. La "dirección como pendiente contra prevalencia" y sus bootstrap/permutaciones se eliminaron.
- **Decisiones de Nico sobre lo que quedaba de la Figura 2 (17/09):** "C magnitud queda para apéndice" (bloque 37,
  `pC_magnitude_<modo>.png`); "Refusal contra prevalencia a apéndice" (bloque 34, `p1d_levels_vs_share.png` y
  `p2b_pg_by_origin_vs_share.png`, proxy Common Crawl); "Dirección contra capability no sé, veámosla, 24x24 no me gusta
  para esto, la otra opción habría que verla" → gráfico de pares en el bloque 38
  (`pC_rank_agreement_vs_capability_<modo>.png`: acuerdo de cada par contra la capability media y contra la diferencia
  de capability del par; plano en cero, sin tests) → **decisión de Nico al verlo (17/09): "acuerdo, gráfico a
  apéndice!"**; "variables de figura 1 por idioma es mucho
  detalle, en todo caso a apéndice, anotalo pero no es prioridad ahora" (tablas del bloque 26:
  `delta_vs_english_by_factor.csv`; gráficos por hacer); "proporción de respuestas truncadas sí, tabla, apéndice, ahora
  no" (bloque 26: `truncation_by_language.csv`, `truncation_by_language_model.csv`).
- Corrección del mismo día: las proporciones de truncado de los dos outliers estaban invertidas (ver la nota en
  el panel A): nova-2-lite 85 % en swahili; nemotron-3.5-lightning 25 % en swahili y 9 % en hindi.

---

## Panel D · Sesgo por idioma pesado por el uso real de los modelos (bloque 40)

**Estado: gráfico APROBADO por Nico (2026-09-17), versión final: estimador de tasa pesada, solo power grabbing y control
en el cuerpo (`pD_usage_weighted_or.png`); self-empowerment y disempowerment a apéndice (`pD_usage_weighted_or_all_modes.png`);
el estimador alternativo queda en apéndice (`pD_alt_mean_of_model_or_all_modes.png`).**

Decisión y lectura de Nico (17/09): "creo que me quedo con la segunda, porque la pregunta que queremos responder se parece más
a esa: cuánto más se rechaza un pedido típico en un idioma vs inglés; eso es el sesgo que puede generar cambios de poder según
quién está hablando [...]. Dejaría por simetría solo power grabbing y control, que SE y DE queden para apéndice. [...] En este
caso, pareciera entonces que hay un efecto específico de power grabbing, en donde tanto francés como hindi rechazan más en power
grabbing, pero no en control - es un efecto específico de power grabbing."

Valores del panel final (OR contra inglés [IC 95 %]): power grabbing hindi 1,27 [1,09; 1,48], francés 1,22 [1,07; 1,38], resto
0,92–1,03 cruzando 1; control hindi 1,04 [0,88; 1,24], francés 1,00 [0,87; 1,18], chino 0,72 [0,59; 0,89], resto 0,90–1,01.
Nota de Claude para la lectura de especificidad: "da en pg y no en control" es el criterio del 14/09; el contraste directo
pg vs control por idioma (cociente de OR) todavía no está calculado — a ojo desde los intervalos, francés ≈ 1,22 e hindi ≈ 1,22
con p cerca de 0,05–0,10. **Decisión de Nico (17/09): "está bien, es una interpretación, no hacemos test de power grabbing vs
control; el gráfico me gusta así".** La especificidad queda como lectura del gráfico (criterio del 14/09), sin test del contraste. Pedido de Nico: "podríamos medir el nivel de sesgo de
cada modelo, pesarlo por su uso, y ver si en función de eso sí hay sesgos por idioma (eso mostrarlo como media pesada de
los 24 modelos, para cada idioma vs inglés, tipo diferencia de diferencias en OR)". Sobre las advertencias: "entiendo los
caveats, pero no me molestan; no mostraría pesos en figura principal, está bien que los pesos estén concentrados porque
es la realidad".

- **Uso:** tokens (prompt + completion, todas las variantes) procesados por OpenRouter para cada uno de los 24 modelos del
  2026-08-18 al 2026-09-16, foto del 2026-09-17, guardada con fuente y cita en
  `4_analysis/inputs/openrouter_usage/` (datos de la página pública de actividad de cada modelo; CC BY 4.0).
  Pesos mayores: gpt-5.6-luna 32 %; hy3 16 %; nemotron-3-ultra 12 %; glm-5.2 7 %; gpt-5.6-sol 5 %; kimi-k3 5 %. Tamaño efectivo de la media pesada: 6,3 modelos.
- **Métrica:** por modelo, log-OR(idioma vs inglés) con logit suavizado sobre los mismos 192 prompts; media simple y media
  pesada por tokens sobre los modelos, exponenciadas. Swahili sin los dos outliers. Sin intervalos ni tests (regla del 17/09).
- **Gráfico:** `40_fig2_usage_weighted/pD_usage_weighted_or.png`: por idioma, barra gris = media simple de los 24, barra de
  color = media pesada por uso; nacen en OR = 1; eje log; paneles he, de, pg.

OR de refusal contra inglés en power grabbing (media simple | pesada por uso):

| idioma | simple | pesada |
|---|---|---|
| German | 0.90 | 0.89 |
| Portuguese | 0.91 | 1.02 |
| Spanish | 0.98 | 0.97 |
| Swahili | 0.88 | 0.87 |
| Chinese | 0.95 | 0.93 |
| French | 1.04 | 1.18 |
| Hindi | 1.14 | 1.23 |

Disempowerment:

| idioma | simple | pesada |
|---|---|---|
| German | 0.90 | 0.91 |
| Portuguese | 0.99 | 1.23 |
| Spanish | 1.00 | 1.01 |
| Swahili | 1.04 | 1.20 |
| Chinese | 0.96 | 0.91 |
| French | 0.95 | 0.87 |
| Hindi | 1.28 | 1.75 |

**Versión 2 (17/09), pedido de Nico:** "la media simple ya va a estar en otro gráfico de la figura 2 que ya elegimos, no
hace falta repetirlo; podemos acá hacer un solo panel, con los tres modos y el control (4 barras por idioma), y agreguemos
las barras de error." → un panel, cuatro barras por idioma (he, de, pg, control), solo la media pesada por uso, barras de
error = intervalo bootstrap 95 % sobre prompts (B = 1.000) con modelos y pesos fijos. OR pesado por uso [IC 95 %]
(* = el intervalo excluye 1):

| idioma | he | de | pg | control |
|---|---|---|---|---|
| German | 0.54 [0.36; 0.73] * | 0.91 [0.66; 1.29] | 0.89 [0.76; 1.04] | 0.83 [0.69; 0.98] * |
| Portuguese | 0.96 [0.50; 1.80] | 1.23 [0.96; 1.66] | 1.02 [0.88; 1.18] | 0.94 [0.80; 1.09] |
| Spanish | 1.02 [0.51; 1.90] | 1.01 [0.76; 1.37] | 0.97 [0.83; 1.10] | 0.95 [0.82; 1.09] |
| Swahili | 1.36 [0.82; 2.44] | 1.20 [0.89; 1.73] | 0.87 [0.72; 1.05] | 0.86 [0.70; 1.03] |
| Chinese | 0.86 [0.43; 1.53] | 0.91 [0.65; 1.26] | 0.93 [0.78; 1.09] | 0.70 [0.56; 0.85] * |
| French | 0.96 [0.54; 1.63] | 0.87 [0.65; 1.14] | 1.18 [1.03; 1.35] * | 0.91 [0.77; 1.06] |
| Hindi | 1.29 [0.73; 2.54] | 1.75 [1.35; 2.54] * | 1.23 [1.04; 1.46] * | 0.96 [0.80; 1.15] |

**Versión 3 (17/09), decisiones de Nico:** "me gusta este gráfico, aunque las barras de error en algunos casos son
exageradamente grandes"; sobre OR vs Δ logits: son la misma cantidad (Δ logit = log OR) y el gráfico ya usa eje log, así que
es simétrico; queda OR con eje log. "por ahora, me parece bien sacar self empowerment del panel y dejar en apéndice" →
`pD_usage_weighted_or.png` (cuerpo: de, pg, control) y `pD_usage_weighted_or_all_modes.png` (apéndice, con he). "calcular
primero tasa de refusal pesada por uso en cada idioma y después un solo OR contra inglés suena bien como para probarlo y
verlo" → `pD2_usage_weighted_pooled_or.png` (variante; tabla `usage_weighted_pooled_or_summary.csv`). Comparación de los dos
estimadores, OR [IC 95 %]:

| modo | idioma | media pesada de OR por modelo | tasa pesada y un solo OR |
|---|---|---|---|
| pg | Hindi | 1,23 [1,04; 1,46] | 1,27 [1,09; 1,48] |
| pg | French | 1,18 [1,03; 1,35] | 1,22 [1,07; 1,38] |
| pg | resto | 0,87–1,02, todos cruzan 1 | 0,92–1,03, todos cruzan 1 |
| de | Hindi | 1,75 [1,35; 2,54] | 1,39 [1,16; 1,67] |
| de | German | 0,91 [0,66; 1,29] | 0,74 [0,58; 0,92] |
| de | French | 0,87 [0,65; 1,14] | 0,86 [0,74; 0,99] |
| control | Chinese | 0,70 [0,56; 0,85] | 0,72 [0,59; 0,89] |
| control | German | 0,83 [0,69; 0,98] | 0,90 [0,77; 1,03] |

En power grabbing y control los dos estimadores dan casi lo mismo y con intervalos del mismo ancho; en disempowerment la
variante achica los intervalos (cociente hi/lo de ≈1,9 a ≈1,5) pero mueve los puntos (hindi 1,75 → 1,39; alemán 0,91 → 0,74):
ahí los dos estimadores no miden lo mismo. Elección de Nico (17/09): la tasa pesada con un solo OR (ver el estado al
comienzo de esta sección).

Lectura descriptiva de la versión 1 (sin test): en power grabbing el peso por uso casi no cambia el cuadro salvo francés (1,04 → 1,18) e
hindi (1,14 → 1,23); en disempowerment hindi pasa de 1,30 a 1,75 y portugués de 0,99 a 1,25; en self-empowerment alemán cae
a 0,54. Interpretación y estadística pendientes de Nico.

---

## Panel 3 · Rango entre idiomas por modelo contra capability

**Estado: borrador, pendiente de revisión (2026-09-16).** Pedido de Nico: "por modelo, cuál es la
diferencia de refusal entre el máximo y el mínimo refusal, lo cual da una idea del sesgo total (rango de
refusal entre idiomas para cada modelo) y ploteemos eso vs capability de los modelos".

### Pregunta que plantea

¿Cuánto cambia cada modelo su refusal según el idioma (sesgo total por idioma), y eso depende de la
capability del modelo?

### Gráfico: `34_fig2_v2/p3_range_vs_capability.png`

- Tres paneles (he, de, pg). Cada punto un modelo: y = R(idioma) máxima − mínima entre los 8 idiomas
  (pp), x = índice de capability (media de GPQA Diamond y MMLU-Pro, brazo off; bloque 30). Azul US,
  rojo CN, nombre al lado. Swahili excluido para nemotron-3.5-lightning y nova-2-lite (rango sobre 7).
- Spearman descriptivo en el título (n = 24) y por bloque en `p3_range_capability_spearman.csv`.

### Cómo se calculó

- R(idioma, modo) por modelo del bloque 26 (`levels_per_model.csv`); rango = max − min sobre idiomas;
  tabla `p3_range_vs_capability.csv` con idioma máximo y mínimo por modelo.

### Qué dicen los datos (power grabbing)

| modelo | origen | capability | rango (pp) | idioma máx | idioma mín |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | US | 46,7 | 46,4 (7 idiomas) | hi | fr |
| nova-2-lite | US | 46,5 | 29,2 (7 idiomas) | es | fr |
| inkling | US | 58,7 | 25,0 | es | en |
| haiku-4.5 | US | 64,8 | 24,5 | zh | sw |
| ling-3.0-flash | CN | 53,7 | 24,5 | zh | de |
| deepseek-v4-pro | CN | 57,8 | 22,9 | fr | en |
| seed-2-1-turbo | CN | 61,8 | 20,8 | zh | sw |
| grok-4.3 | US | 52,0 | 19,8 | en | zh |
| … | | | | | |
| gpt-5.6-luna, gpt-5.6-terra | US | 51–57 | 9,9 | hi / fr | en / de |
| qwen3.8-flash, kimi-k3 | CN | 58–68 | 8–9 | es / en | hi / sw |
| gemma-4-31b, gemini-3.1-flash-lite | US | 57–64 | 1,6–2,1 | en | zh |

- Mediana del rango en power grabbing: 19 pp; los dos extremos bajos son los modelos que casi no
  rechazan (gemma, gemini-3.1-flash-lite), donde no hay rango posible.
- Spearman capability × rango (descriptivo): pg −0,20 (p = 0,36; US −0,28, CN +0,03); de −0,39
  (p = 0,062); he −0,35 (p = 0,093). Tendencia débil a que los modelos más capaces varíen menos entre
  idiomas, no significativa; los dos nemotron/nova de baja capability tiran del extremo.
- Interpretación pendiente del equipo.

### Cambios pedidos por Nico

(pendiente)

---

## Panel 4 → PANEL B de la Figura 2 · Sesgo total por idioma contra el azar y contra el control (bloque 35)

**Estado: APROBADO por Nico (2026-09-16), versión OR: "me gustan estas tablas, mantengamos OR me parece,
sería el panel B".** Pedido de Nico: "quedémonos solo con power
grabbing, excluyamos el swahili de los dos modelos outliers en swahili, y quiero promediar esto entre los
24 modelos, y mostrar lo mismo pero con un shuffle entre idiomas para eliminar toda estructura (cosa que
si estas diferencias dan por azar y no hay sesgos medios por idioma, podamos saberlo) y además quiero
comparar contra el sesgo del control. Serían 3 barras entonces. [...] podemos mostrar lo mismo para SE y
para DE. Y quizás probemos dos opciones, una con pp y otra con OR."

### Pregunta que plantea

¿El rango de refusal entre idiomas que tiene cada modelo es más de lo que daría el azar? ¿Es mayor en
power shifting que en control?

### Gráficos: `35_fig2_range_null/p4_range_vs_null_pp.png` y `p4_range_vs_null_or.png`

- Tres paneles (he, de, pg), tres barras: rango observado (media de 24 modelos, intervalo bootstrap
  sobre prompts); el mismo rango con los idiomas barajados dentro de cada prompt (mediana e intervalo
  de 500 permutaciones); rango observado del control. Versión pp y versión OR (odds del idioma máximo
  sobre odds del mínimo, con logit suavizado, media geométrica).

### Cómo se calculó (bloque 35, `analysis_35_fig2_range_null.py`)

- Por modelo y modo, matriz 192 prompts × 8 idiomas de refuse (7 idiomas para nemotron-3.5-lightning y
  nova-2-lite, sin swahili). Rango = max − min de la tasa por idioma (pp) o del logit suavizado (OR).
- Shuffle: en cada prompt se permutan los valores entre idiomas; conserva en cuántos idiomas se rechazó
  cada prompt y el nivel del modelo, destruye la estructura por idioma. p = fracción de permutaciones
  con media ≥ observada.
- Advertencia: el rango max − min es un estadístico sesgado hacia arriba con ruido; por eso la
  referencia de azar no es 0 y por eso el intervalo bootstrap del observado queda desplazado hacia
  arriba (asimétrico). La comparación válida es observado contra shuffle.

### Qué dicen los datos (media de 24 modelos)

| modo | rango observado (pp) | shuffle (pp) | p | OR observado | OR shuffle |
|---|---|---|---|---|---|
| self-empowerment | 6,1 [5,7; 7,9] | 2,9 [2,5; 3,2] | < 0,002 | 4,3 | 2,5 |
| disempowerment | 15,4 [14,3; 18,1] | 5,4 [4,7; 6,0] | < 0,002 | 4,0 | 1,7 |
| power grabbing | 17,6 [16,8; 20,9] | 6,0 [5,3; 6,8] | < 0,002 | 2,8 | 1,5 |
| control | 14,4 [13,6; 17,5] | 5,5 [5,0; 6,1] | < 0,002 | 2,8 | 1,5 |

- En los cuatro modos el rango observado es unas tres veces el del azar: el idioma tiene un efecto
  real dentro de cada modelo, y lo tiene también en el control.
- Power grabbing (17,6) queda algo por encima del control (14,4) en pp; en OR son iguales (2,8 y 2,8).
  Disempowerment 15,4 vs control 14,4. Es decir, el sesgo por idioma no es específico de power
  shifting: el control lo tiene casi igual.
- Interpretación pendiente del equipo.

### Decisiones abiertas (del equipo)

- pp u OR para el cuerpo (en OR self-empowerment aparece como el modo de mayor sesgo relativo, por su
  base de 3 %).
- Si se muestra también el shuffle del control (está en range_summary.csv) como cuarta barra.
- Test formal de "pg vs control" en rango: diferencia pareada por modelo con bootstrap sobre prompts,
  si se quiere una p para esa comparación.

### Cambios pedidos por Nico

(pendiente)

---

## Panel 1b (candidato) · Δ refusal vs inglés por idioma

**Estado: candidato, sin revisar (la v1 del panel 1).**

### Preguntas que plantea

1. ¿Se rechaza más (o menos) el mismo pedido en otro idioma que en inglés? ¿Qué idiomas suben y cuáles
   bajan el refusal?
2. ¿Es un sesgo de power shifting o ya está en el control?
3. ¿Hay modelos con comportamiento particular en algún idioma?

### Gráfico: `34_fig2_v2/p1b_delta_vs_english.png`

- Dos paneles: power grabbing y control. Eje x: los 7 idiomas; eje y: R(idioma) − R(inglés) en pp por
  modelo, pareado por prompt (192 prompts por modo e idioma).
- Por idioma dos cajas, US (azul) y CN (roja); un punto por modelo; línea en 0. Eje recortado a
  [−25, 35]; los que se salen van como triángulo con nombre y valor (nemotron-3.5-lightning en hindi
  +42 y swahili +78 en pg; swahili +74 en control).

### Cómo se calculó (bloque 26)

- Por modelo, modo e idioma: R(idioma) y R(inglés) sobre los mismos 192 prompts; Δ en pp con intervalo
  bootstrap sobre prompts (`delta_vs_english_per_model.csv`). Pooled = media con peso igual por modelo
  (24 / 12 US / 12 CN), intervalo bootstrap sobre prompts; logit de acompañante
  (`delta_vs_english_pooled.csv`).

### Qué dicen los datos (power grabbing, Δ pp vs inglés)

| idioma | 24 modelos | p | US (12) | CN (12) | modelos con Δ > 0 (IC excluye 0 arriba / abajo) |
|---|---|---|---|---|---|
| German | −0,9 [−2,5; +0,6] | 0,22 | +1,6 | −3,4 * | 9 de 24 (5 / 5) |
| French | +2,2 [+0,7; +3,8] | < 0,01 | +1,8 * | +2,7 * | 14 de 24 (6 / 2) |
| Spanish | +0,8 [−0,9; +2,4] | 0,39 | +4,4 * | −2,9 * | 10 de 24 (6 / 5) |
| Chinese | +0,9 [−1,1; +2,9] | 0,37 | +0,1 | +1,7 | 11 de 24 (6 / 6) |
| Portuguese | −0,6 [−2,1; +0,9] | 0,45 | +1,5 | −2,6 * | 11 de 24 (4 / 6) |
| Hindi | +3,3 [+1,6; +5,0] | < 0,01 | +6,9 * | −0,3 | 13 de 24 (10 / 6) |
| Swahili | +3,0 [+0,8; +5,2] | 0,01 | +10,8 * | −4,8 * | 10 de 24 (6 / 9) |

(* = intervalo del bloque excluye 0.) Niveles pooled en pg: inglés 23,6 %; francés 25,9; hindi 26,9;
swahili 26,6; alemán 22,7; portugués 23,1.

- Sobre 24 modelos, francés, hindi y swahili suben el refusal de power grabbing 2 a 3 pp; el resto no
  se separa del inglés.
- El promedio esconde dos bloques con signo opuesto: los modelos US rechazan más en casi todos los
  idiomas, mucho más en swahili (+10,8) e hindi (+6,9); los modelos CN rechazan menos en alemán,
  español, portugués y swahili (−4,8) y más solo en francés.
- Modelos particulares: nemotron-3.5-lightning (+78 en swahili, +42 en hindi) y nova-2-lite (+18 en
  swahili) tienen respuestas en swahili cortadas a 5.000 tokens (CORRECCIÓN 17/09: nova-2-lite 85 %, nemotron-3.5-lightning 25 %; al revés de como se escribió el 16/09) (bloque 26,
  truncation_by_language_model.csv): su "refusal" en swahili está contaminado por el truncado. grok-4.3
  rechaza 20 pp menos en chino y swahili; inkling +25 en español y +23 en portugués.
- Control: el mismo dibujo por bloque (US arriba en swahili e hindi, CN abajo en casi todo), con
  magnitudes menores. Interpretación pendiente del equipo.

### Decisiones abiertas (del equipo)

- Modos a mostrar en el cuerpo: pg solo, pg + control (como ahora), o los tres modos de power shifting
  (he y de en `28_fig2_questions/q1b`).
- Escala: pp (como ahora) o logit; el cuaderno lo deja abierto.
- Test: propuesta análoga a la Figura 1, GLMM con el prompt pareado como intercepto aleatorio (cancela la
  dificultad del prompt) y el modelo como intercepto y pendiente aleatoria: (a) por modo,
  `refuse ~ idioma + (1 | prompt_id) + (1 | model) + (1 | model:idioma)` con inglés de referencia, ómnibus
  de 7 gl y contrastes por idioma con BH; (b) interacción idioma × (power shifting vs control) para
  "¿es específico de power shifting?"; (c) interacción idioma × origen (US vs CN) para "¿los bloques
  difieren en su sesgo por idioma?". Nico decide cuáles.
- Qué hacer con los modelos con truncado masivo en swahili (nemotron-3.5-lightning, nova-2-lite): dejar,
  marcar, o excluir de swahili.

### Cambios pedidos por Nico

(pendiente)

---

## 18/09 — objeciones de Nico a la compuesta regenerada (paneles A y B)

> mmm en A la única barra de error que desapareció es la de las tres barras de english, que están agrupadas entre sí
> y que están en tercer lugar, es como que ser una referencia acá es lo menos intuitivo del mundo / es contra inglés
> la comparación acá? porque en verdad hay estructura entre los 8 idiomas, no solo de cada uno contra inglés, no sé si
> la mejor comparación es todos contra la referencia / qué opinás?
>
> y en B dos de cada 3 barras no tienen error, es por la misma razón? ahí no veo líneas punteadas de diferencia, pero
> además me resulta antiintuitivo que justo la que tiene la barra de error es el shuffle, me imaginaría que shuffle es
> la referencia y control y observado son las que tienen el error, me explico? no sé si es posible eso

Respuesta dada (opinión, sin cambios todavía): A compara hoy cada idioma contra inglés (referencia por construcción:
banco original y traducciones). Opciones: (1) dejar inglés como referencia pero ponerlo primero a la izquierda; (2)
contrastar cada idioma contra la media de los 8 dentro del prompt (contraste de suma / IC within-subject de
Loftus–Masson): las 8 barras con intervalo, línea punteada = media de los 8 por modo, ningún idioma privilegiado; mi
preferencia es (2) para A y dejar D contra inglés (OR de un pedido típico). B: las barras de observado y control no
llevan intervalo porque el bootstrap sobre prompts de una media de rangos está sesgado hacia arriba (pg en OR: observado
2,82, bootstrap [2,78; 3,77]; he: 4,29 [4,03; 11,3]); el shuffle lleva su banda de permutación; el control tiene su
propio shuffle calculado (OR 1,51 [1,43; 1,59]) que no se dibuja. Propuesta: nulo como referencia (línea punteada en la
mediana del shuffle, uno por barra) y en observado y control el intervalo del exceso sobre su propio nulo, calculado
recomputando observado y shuffle sobre los mismos prompts remuestreados en cada réplica (el sesgo del rango afecta a
los dos igual y se cancela en la diferencia). Hay que verificar que ese bootstrap del exceso quede centrado antes de
mostrarlo. Decisión de Nico: pendiente.

**Nico (18/09), decisión sobre A y pregunta sobre B:**

> lo de B sería algo estándar estadísticamente hablando para hacer? si lo es, me gusta, si no lo es, dudo
> lo de A, depende de una cosa: el test que proponés en la opción 2, utiliza la estructura compartida entre idiomas (que
> son las mismas prompts en los 8) para bajar el error / aumentar la potencia? si es así, adelante; si no es así, no
> resuelve lo que más me importaba

**A → sí, la usa → hecho (opción 2).** Por modelo, la referencia es la media de sus idiomas disponibles (8; 7 en los dos
excluidos en swahili), calculada en los mismos remuestreos de prompts; la desviación R(idioma) − media se promedia con
peso igual por modelo y el IC 95 % sale del bootstrap sobre prompts (B = 2000). La varianza entre prompts, compartida
por los 8 idiomas, se cancela en la desviación (IC within-subject de Loftus–Masson 1994 / Morey 2008 con el prompt como
unidad). Semiancho medio del IC en pg: nivel 3,7 pp → contra inglés 1,7 → contra la media de los 8 1,15 (el contraste
contra una media de 8 tiene menos varianza que contra un solo idioma: 0,875 σ² frente a 2 σ² dentro del prompt).
Bloque 34: tabla `delta_vs_mean_langs_excl_sw_outliers.csv` (con q = BH por bloque sobre las 24 desviaciones, familia
elegida por Claude, anotada en DECISIONES_A_REVISAR.md) y figura `pA_levels_by_language_bars_sorted_within_ci.png`;
bloque 41 regenerado con esta versión del panel A (las 8 barras con intervalo, línea punteada = media de los 8 por modo,
ningún idioma marcado como referencia). La versión contra inglés (`..._paired_ci.png`, `delta_vs_english_...csv`) queda
como registro. Salvedades: las 8 desviaciones de un modelo suman cero, no son independientes; en swahili la barra y la
desviación usan 22 modelos y la línea punteada 24.

Desviaciones respecto de la media de los 8 (pp, todos los modelos; * = IC excluye el cero; q = BH sobre 24):

| idioma | he | de | pg |
|---|---|---|---|
| Alemán | −0,9 [−1,4; −0,5]* q<0,001 | −1,5 [−2,5; −0,5]* q=0,021 | −1,5 [−2,4; −0,5]* q=0,009 |
| Portugués | −1,0 [−1,4; −0,5]* q<0,001 | −0,8 [−1,7; +0,2] | −1,1 [−2,0; −0,2]* q=0,038 |
| Inglés | −0,6 [−1,1; −0,1]* q=0,028 | −0,1 [−1,2; +1,0] | −0,6 [−1,7; +0,6] |
| Español | −0,4 [−0,9; +0,1] | −0,6 [−1,6; +0,4] | +0,2 [−0,8; +1,2] |
| Swahili* | +1,3 [+0,7; +2,0]* q<0,001 | +0,2 [−1,0; +1,4] | −1,9 [−3,5; −0,4]* q=0,024 |
| Chino | +0,1 [−0,4; +0,7] | −0,3 [−1,3; +0,8] | +0,4 [−1,0; +1,8] |
| Francés | +0,1 [−0,4; +0,5] | −0,2 [−1,0; +0,7] | +1,7 [+0,5; +2,8]* q=0,007 |
| Hindi | +1,5 [+0,9; +2,2]* q<0,001 | +3,2 [+1,7; +4,6]* q<0,001 | +2,7 [+1,5; +3,9]* q<0,001 |

Media de los 8 idiomas: he 3,7 %, de 14,6 %, pg 24,2 %. Lectura pendiente de Nico (¿cambia "en promedio no hay
diferencia entre idiomas"?): con este contraste, hindi está por encima del idioma típico en los tres modos, francés en
pg, swahili en he; alemán y portugués por debajo; inglés no se distingue en de ni en pg.

**B → respuesta dada (sin cambios):** ver el mensaje del 18/09 resumido en la entrada siguiente cuando Nico decida.

**Nico (18/09):**

> la A me parece bien, aprobada
> la B creo que tiene su encanto, serían solo 4 barras entonces, una por modo? y todas tienen barra de error, que supongo
> que se compara contra 0? cada una es el promedio en el exceso del rango vs azar, entre 24 modelos? si es así, me gusta

**A: APROBADA** en la versión simétrica (desviación respecto de la media de los 8 idiomas dentro del prompt).

**B: hecho como lo describe.** Bloque 35, tabla `range_excess_summary.csv`, figura `p5_range_excess_or.png` (y `_pp`);
compuesta del bloque 41 regenerada con B = un solo panel de cuatro barras (he, de, pg, control). Por modelo: exceso =
rango observado entre idiomas − media de sus 500 rangos con los idiomas barajados dentro del prompt (en OR, cociente de
rangos, calculado en log-odds). Barra = media sobre los 24 modelos (geométrica en OR); barra de error = IC 95 % t entre
modelos (23 gl); línea punteada = azar (OR 1); test = t de una muestra contra 0 en log; q = BH y Holm sobre los 4 modos.
Es la construcción estándar "estadístico corregido por azar por unidad, intervalo entre unidades" (como accuracy − chance
con intervalo entre sujetos). El marco es el de modelos aleatorios, n = 24; la heterogeneidad entre modelos entra en el
intervalo. El p de permutación anterior (p < 0,002 en los cuatro modos) sigue en `range_summary.csv`.

| modo | rango observado (OR) | rango barajado (OR) | exceso (cociente) | IC 95 % t | p (t, 23 gl) | q BH | modelos con exceso > 0 |
|---|---|---|---|---|---|---|---|
| he | 4,29 | 2,49 | 1,73 | [1,18; 2,53] | 0,007 | 0,007 | 17 / 24 |
| de | 4,03 | 1,72 | 2,34 | [1,65; 3,32] | < 0,001 | < 0,001 | 23 / 24 |
| pg | 2,82 | 1,48 | 1,91 | [1,49; 2,44] | < 0,001 | < 0,001 | 22 / 24 |
| control | 2,84 | 1,51 | 1,88 | [1,46; 2,42] | < 0,001 | < 0,001 | 24 / 24 |

En pp: he +3,2 [+0,4; +6,0]; de +10,1 [+6,7; +13,5]; pg +11,6 [+7,9; +15,3]; control +8,8 [+5,3; +12,3].

Lectura (a confirmar por Nico): en los cuatro modos el rango entre idiomas de un modelo típico supera al azar, entre 1,7 y
2,3 veces; en self-empowerment el exceso es menor y más heterogéneo (17 de 24 modelos por encima). El control tiene el
mismo exceso que power grabbing: la dispersión por idioma no es específica de power shifting.

Pendiente que señalé: el panel A de la Figura 3 (|sesgo| observado vs shuffle, bloque 45) tiene la misma estructura que
tenía B (observado sin barra, nulo con banda); con la regla "un mismo criterio en las dos figuras" habría que pasarlo al
mismo formato (exceso por modelo sobre su propio nulo, IC entre modelos). Decisión de Nico: pendiente.

**Nico (18/09), preguntas de método** (pp vs OR; OR por modelo vs OR de la media; consistencia en el paper; por qué en el
B nuevo he y de ya no superan al control): respondidas en el mensaje del 18/09 y volcadas a `DECISIONES_A_REVISAR.md`,
sección F (inventario panel por panel y regla propuesta). Sobre el B: el B viejo mostraba rangos crudos, cuyo nivel de
azar difiere por modo (he 2,49, de 1,72, pg 1,48, control 1,51 en OR); al corregir por el azar de cada modelo, he cae por
debajo del control (0,92, p = 0,55) y de queda por encima (1,24 [1,02; 1,52], p = 0,036, chequeo exploratorio pareado por
modelo, no oficial); pg iguala al control (1,02). Decisión de Nico sobre si ese contraste modo vs control va al paper:
pendiente.

**Nico (18/09):** "ok a lo de B, queda registrado el gráfico más nuevo como oficial, no hacemos esas otras comparaciones
que me mostraste". → **Panel B OFICIAL = bloque 35 p5** (exceso del rango sobre el azar por modelo, 4 barras, IC t entre
modelos). Los contrastes modo vs control del chequeo exploratorio NO van al paper; quedan solo como registro en
DECISIONES_A_REVISAR.md, sección F.

**Nico (18/09):** "ok lo del OR, me parece lógico lo que planteás, aprobado de nuevo". → El panel D se queda como está
(tasas ponderadas por uso y recién ahí el OR = OR marginal de un pedido típico); título de la compuesta cambiado a "Un
pedido típico: OR marginal de refusal contra inglés, tasas pesadas por el uso de cada modelo"; en métodos hay que decirlo
y nunca compararlo en magnitud con los OR por modelo. Bloque 41 regenerado.

**Nico (18/09), lectura nueva del panel A:** "estoy de acuerdo, la lectura de la figura 2 cambia, hay diferencia entre
idiomas: hindi produce más rechazo, alemán y portugués producen menos rechazo. va a narrativa, pero esas diferencias que
encontramos son chicas. Lo que no recuerdo ahora es, esos sesgos chicos se amplifican cuando tenemos en cuenta el índice
de uso de openrouter? [...] la narrativa podría ser 'encontramos sesgos chicos pero amplificados por el uso'".

Respuesta con el bloque 40 (OR contra inglés; peso igual = media de los log-OR por modelo; pesado = pooled con tokens de
OpenRouter, el del panel D):

| modo | idioma | peso igual | pesado por uso |
|---|---|---|---|
| pg | francés | 1,04 | 1,22 [1,07; 1,38] |
| pg | hindi | 1,14 | 1,27 [1,09; 1,48] |
| pg | alemán | 0,90 | 0,92 [0,78; 1,06] |
| pg | portugués | 0,91 | 1,03 [0,90; 1,19] |
| de | hindi | 1,28 | 1,39 [1,16; 1,67] |
| de | alemán | 0,90 | 0,74 [0,58; 0,92] |
| he | hindi | 1,40 | 1,61 [1,12; 2,59] |
| he | alemán | 0,87 | 0,63 [0,44; 0,85] |
| control | chino | 0,80 | 0,72 [0,59; 0,89] |
| control | resto | 0,75–0,93 | 0,90–1,04, ninguno significativo |

Lectura: el uso amplifica el "más rechazo" de hindi (los tres modos de poder) y de francés (pg, de 1,04 a 1,22), y el
"menos rechazo" de alemán (de y he); el de portugués desaparece al pesar (1,03 en pg). En el control no hay amplificación
(solo chino baja a 0,72). Salvedad obligatoria: gpt-5.6-luna pesa el 32 % y aporta el 60–90 % de la varianza de estas
estimaciones; "los modelos más usados contribuyen a sesgos más elevados" es, en los datos, sobre todo "luna tiene sesgos
por idioma más grandes que el modelo medio". Si Nico quiere esa frase, el chequeo directo es sesgo por idioma de cada
modelo contra su cuota de uso (24 puntos, n_eff ≈ 6). Decisión de Nico: pendiente.

---

## 18/09 — DECISIÓN: el test oficial es el de modelos aleatorios

**Nico (18/09):** "me parece bien; así que quedan modelos aleatorios como test oficial", después de la auditoría panel por
panel. Registro completo en `DECISIONES_A_REVISAR.md`, punto 2.

Consecuencia para esta figura, que es la única afectada de las cuatro. El panel A mantiene sus barras y su intervalo
descriptivo (desviación respecto de la media de los 8 idiomas, bootstrap sobre prompts), pero el test citado pasa a ser el
GLMM del bloque 36 (`refuse ~ lang + (1 | model) + (1 | model_lang) + (1 | prompt_id)`):

| modo | ómnibus de idioma | idiomas con q < 0,05 | al borde (p < 0,05 sin corregir) |
|---|---|---|---|
| Self-empowerment | χ²(7) = 20,2, p = 0,005 | Swahili | alemán, hindi |
| Disempowerment | χ²(7) = 9,4, p = 0,22 | Hindi | ninguno |
| Power grabbing | χ²(7) = 7,9, p = 0,34 | ninguno | hindi (p = 0,036) |
| Control | χ²(7) = 8,9, p = 0,26 | ninguno | ninguno |

Por qué: la SD entre modelos del efecto de idioma (`model_lang`) es 0,65–0,70 en log-odds contra 0,14–0,29 de la dispersión
del efecto medio, es decir 2,4 a 4,6 veces mayor. Cada modelo tiene su propio patrón por idioma, mucho más grande que el
patrón promedio.

**Qué se pierde:** el efecto de idioma en power grabbing (hindi, francés, alemán, portugués del panel A). **Qué queda:**
swahili en self-empowerment e hindi en disempowerment; el panel B entero (el rango entre idiomas de un modelo típico es
1,7 a 2,3 veces el del azar en los cuatro modos, q ≤ 0,007, ya en este marco); el panel C (permuta etiquetas de origen
entre los 24 modelos, ya en este marco: en pg, dentro-de-origen menos mixto 0,144 con p = 0,009, CN–CN p = 0,003); y el
panel D como afirmación sobre el panel desplegado, con francés OR 1,22 [1,07; 1,38] e hindi 1,27 [1,09; 1,48] en pg.

**Lectura resultante (a redactar por Nico):** el idioma mueve mucho a cada modelo, con patrones propios que no coinciden
entre modelos; el promedio del panel se corre poco y solo se sostiene en self-empowerment y disempowerment; al pesar por
uso real, francés e hindi también se corren en power grabbing, pero eso es una afirmación sobre los modelos que la gente
usa hoy. Pendiente: decidir si el panel A de la compuesta mantiene el intervalo descriptivo con la aclaración en la
leyenda, o si se redibuja desde el GLMM (cambiaría las unidades de pp a log-odds).

## 19/09 — Panel D revisado (bloque 72): pesos por pedidos, power shifting pooled, permutación al lado del bootstrap

Contexto: en la revisión del esqueleto del paper (19/09) Claude marcó que el panel D descansa en gpt-5.6-luna (32 % del
peso por tokens; sin luna, pg hindi OR 1,04 y francés 1,01) y que la frase "el uso amplifica porque los modelos más usados
tienen corrimientos más marcados" no tiene cálculo detrás. Nico: "por más que tenga un n efectivo de 6, si da significativo,
da significativo"; pidió opciones para hacer el análisis más sensible. Decidió, textual: "pesar por pedidos me parece
mejor"; "pooled de power shifting como análisis secundario me parece bien hacerlo también"; "test de permutación, no
reemplaces lo otro por ahora pero hacelo así comparamos". No pidió el test de pg contra control; no se hizo.

Qué cambia respecto del bloque 40 (mismo estimador de Nico del 17/09, misma exclusión de swahili, mismos B y semilla del
bootstrap): pesos = participación en `requests_30d` de OpenRouter (luna 40 %, gemini-3.1-flash-lite 9 %, gemma-4-31b
7,6 %, hy3 7 %, glm-5.2 5,6 %; top 3 = 57 %, n_eff 5,3 contra 6,3 por tokens); un grupo más, power_shifting = he + de + pg;
y para cada OR, además del IC bootstrap, un p de permutación (barajar los idiomas dentro de cada (modelo, prompt), B = 5.000)
y BH dentro de los 7 idiomas de cada grupo. Decisiones de implementación en DECISIONES_A_REVISAR.md, punto 33.

Resultado (pesos por pedidos):

| grupo | idioma | OR | IC boot 95 % | boot_p | perm_p | perm_q |
|---|---|---|---|---|---|---|
| pg | hindi | 1,31 | [1,12; 1,54] | 0,002 | 0,001 | 0,003 |
| pg | francés | 1,29 | [1,14; 1,49] | < 0,001 | 0,001 | 0,003 |
| control | hindi | 1,05 | [0,89; 1,26] | 0,64 | 0,53 | 0,73 |
| control | francés | 1,07 | [0,91; 1,25] | 0,48 | 0,40 | 0,73 |
| control | chino | 0,80 | [0,66; 0,96] | 0,026 | 0,003 | 0,018 |
| power shifting | hindi | 1,40 | [1,25; 1,57] | < 0,001 | < 0,001 | 0,001 |
| power shifting | francés | 1,16 | [1,06; 1,28] | 0,004 | 0,005 | 0,018 |
| power shifting | swahili | 1,13 | [1,00; 1,27] | 0,052 | 0,019 | 0,045 |
| de | hindi | 1,65 | [1,37; 1,99] | < 0,001 | < 0,001 | 0,001 |
| he | alemán | 0,75 | [0,56; 0,95] | 0,016 | 0,10 | 0,24 |

Con tokens (bloque 40) pg hindi 1,27 y francés 1,22; pasar a pedidos sube un poco los dos y no cambia ninguna conclusión
del cuerpo. Bootstrap y permutación dan lo mismo salvo en los bordes, donde la permutación es más conservadora en las
celdas de conteos ralos (he alemán, he swahili, he hindi) y más liberal en el pooled swahili. Decisión de Nico (19/09, más tarde): pesos por pedidos quedan; bootstrap para la barra, permutación para el test. La compuesta
(bloque 41) se regeneró con el panel D del bloque 72 y se pusheó.

## 19/09 — Renumeración (Nico): la figura de idioma pasa a ser la FIGURA 4 del paper

Nico: "me parece que esta tendría que ser la figura 2 [la de díadas de nacionalidad], porque es el efecto principal después de
descripción del dataset base (fig 1); después la 3 debería ser AI agent, y el efecto del idioma (que es el más chico) a figura
4; reordenemos así". Numeración desde el 19/09: Figura 1 D1 inglés (bloque 71), Figura 2 díadas (bloque 51), Figura 3 agente
de IA (bloque 65), Figura 4 idioma (bloque 41). Este archivo y los bloques 26, 34–41, 72 conservan "F2" en el nombre por
historia; el título de la compuesta del bloque 41 dice "Figura 4".

## 19/09 — BH por familia para el panel C (bloque 77)

Nico pidió BH con familias por pregunta para los bloques que no la tenían; el bloque 39 era uno. Familias (DECISIONES punto 37):
"dentro − mixto" por modo (4), "CN–CN − mixto" y "US–US − mixto" por modo (8), "todos los pares" por modo (4), cada tipo de par
contra idiomas barajados por modo (12); p_right unilateral como en el bloque 39. Nada cambia de estado: mismo origen − mixto da en
pg (q = 0,018) y control (q < 0,001), no en he ni de (q = 0,073); CN–CN − mixto da en pg (q = 0,012) y control (q = 0,002), US–US −
mixto solo en control (q = 0,018); el orden compartido ("todos los pares") solo en he (q < 0,001); contra idiomas barajados, CN–CN
da en he, pg y control, US–US solo en he, mixto solo en he.
