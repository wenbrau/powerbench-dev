# Decisiones metodológicas tomadas por Claude que el equipo tiene que revisar

Pedido de Nico (2026-09-17), textual: "anotá que tenemos que revisar todas estas decisiones que tomaste porque no las
termino de entender al 100%". Regla del proyecto (cuaderno, 14/09): toda decisión de análisis e interpretación es de una
persona. Las de esta lista las tomó Claude al implementar pedidos de Nico (Figuras 1 a 3, bloques 25 a 45) y quedaron
aceptadas de hecho, sin revisión a fondo. **Ninguna está validada hasta que alguien del equipo la revise.** Para cada una:
qué se decidió, dónde está, por qué, y qué alternativas hay. El registro de los pedidos y aprobaciones de Nico está en
`25_fig1_notelab/NARRATIVA_F1.md`, `26_fig2_notelab/NARRATIVA_F2.md` y `27_fig3_notelab/NARRATIVA_F3.md`.

Estado de todas: **pendiente de revisión**.

## A. Barras de error e inferencia

1. **Los "observados" de los gráficos contra shuffle no llevan barra de error** (Figura 2 panel B, bloques 35 y 41;
   Figura 3, bloques 43 y 45). Por qué: el estadístico es una media de rangos max − min o de valores absolutos; al
   remuestrear prompts el ruido extra se convierte en sesgo hacia arriba, el intervalo bootstrap percentil queda corrido
   por encima del valor observado y a veces no lo contiene (ejemplos en `45_fig3_side_combined/side_abs_bias_vs_shuffle.csv`,
   columnas obs_lo / obs_hi, y en `35_fig2_range_null/range_summary.csv`). La barra de error queda solo en el nulo.
   Criterio único en las dos figuras por pedido de Nico ("si vamos a tomar un criterio, que sea igual en los dos").
   Alternativas: mostrar el intervalo percentil igual, con la advertencia; un intervalo corregido por sesgo (bootstrap
   básico o BCa), que estima otra cosa (el valor sin ruido) y no es comparable con la barra del nulo; graficar el exceso
   observado − nulo con su intervalo.
   **Cambio decidido por Nico (18/09) para la Figura 2 panel B:** exceso sobre el azar POR MODELO (rango observado − media
   de sus rangos barajados), media de 24 con IC 95 % t entre modelos y t de una muestra contra 0; una barra por modo
   incluido el control; el nulo como línea de referencia (bloque 35, `range_excess_summary.csv`, p5; compuesta 41). Es el
   marco de modelos aleatorios (n = 24). **Queda por decidir si el panel A de la Figura 3 (bloque 45, |sesgo| vs shuffle)
   pasa al mismo formato**, por el criterio único entre figuras.
2. **Dos marcos de inferencia que conviven.** Bootstrap sobre prompts con los modelos FIJOS (bloques 26, 27, 34, 35, 40,
   43, 44, 45: "¿cambia el promedio de estos 24 modelos?") y GLMM con los modelos ALEATORIOS (bloques 30–33, 36, 45: "¿el
   efecto medio se distingue de la heterogeneidad entre modelos?"). Pueden dar distinto sin contradecirse (Figura 2 panel A:
   GLMM ómnibus pg p = 0,34; bootstrap pareado Hindi +3,3 pp y francés +2,2 pp con p < 0,01). Falta decidir cuál es EL
   test de cada panel del paper y cómo se dice en métodos.
   **RESUELTO por Nico (18/09): el test oficial de toda afirmación del paper es el de MODELOS ALEATORIOS** (GLMM con el
   modelo como efecto aleatorio, o el estadístico por modelo con IC t entre modelos). El bootstrap sobre prompts con los
   modelos fijos queda como intervalo descriptivo del panel, no como test. Reglas que se desprenden:
   (a) Toda frase del cuerpo se respalda con un test de modelos aleatorios; donde los dos marcos difieren, se dice.
   (b) Los paneles ponderados por uso (F2 D, F3 B) son la excepción por construcción: estiman un pedido típico del tráfico
       real sobre este panel de modelos desplegados y no tienen versión de modelos aleatorios. Se etiquetan como afirmación
       sobre el panel ("un pedido típico hoy"), nunca como afirmación sobre los modelos en general.
   (c) Las barras de error dibujadas pueden seguir siendo descriptivas (bootstrap sobre prompts) mientras la leyenda lo diga
       y el test citado sea el de modelos aleatorios. Afecta a F2 panel A y a F4 panel A, donde el intervalo mostrado es de
       modelos fijos. En F4 los dos marcos coinciden (GLMM del bloque 58, q < 0,001 en los cuatro modos); en F2 panel A no,
       y eso hay que escribirlo.
   (d) Consecuencia concreta única: en F2 panel A el efecto de idioma en power grabbing (hindi, francés, alemán, portugués)
       pasa a no sostenerse; sobreviven swahili en self-empowerment e hindi en disempowerment (bloque 36, q < 0,05), y el
       ómnibus de idioma solo en self-empowerment (p = 0,005). Todo lo demás de las cuatro figuras y del reasoning ya
       estaba en este marco. Auditoría completa en 26_fig2_notelab/NARRATIVA_F2.md (18/09).
3. **Figura 2 panel A, variante con barra de error pareada** (bloque 34, `pA_levels_by_language_bars_sorted_paired_ci.png`):
   la barra es el IC de la diferencia pareada contra inglés dibujado alrededor de cada barra; inglés sin barra; línea
   punteada en el nivel de inglés; en swahili la diferencia usa 22 modelos y la línea de 24 es aproximada. Alternativa:
   barras intra-prompt respecto de la media de los 8 idiomas.
   **RESUELTO por Nico (18/09, al revisar la Figura 4):** toda comparación pareada contra una referencia se muestra así
   (barra de error = IC del contraste pareado sobre cada barra; referencia sin barra; línea punteada en su nivel). Aplicado
   a la Figura 4 (bloque 54, p3). Bibliografía que lo sostiene en `53_fig4_notelab/NARRATIVA_F4.md`, sección "Panel 2".
   **Para el panel A de la Figura 2, segunda decisión de Nico el mismo día:** no contra inglés sino contra la media de los
   8 idiomas dentro del prompt (la alternativa de arriba), porque "hay estructura entre los 8 idiomas" y la condición era
   que el contraste use los prompts compartidos para bajar el error (lo hace: semiancho en pg 3,7 → 1,7 → 1,15 pp). Bloque
   34 `delta_vs_mean_langs_excl_sw_outliers.csv`, compuesta del bloque 41 regenerada. Sigue abierto si cambia la lectura
   "en promedio no hay diferencia entre idiomas" (hindi arriba en los tres modos, francés en pg, alemán y portugués abajo).
4. **p sin corregir y familias de corrección definidas por Claude.** Casi todas las tablas dan p sin corregir. Donde hay
   BH, la familia la eligió Claude: los 24 modelos dentro de cada celda (bloques 25, 43, 45), las 12 u 8 celdas del test
   de conjunto (Figura 3), los 21 contrastes idioma × modo contra inglés y, desde el 18/09, las 24 desviaciones idioma × modo
   respecto de la media de los 8, por bloque (bloque 34), los niveles de contexto y dominio
   (bloques 32, 33); en el bloque 46 (18/09, a pedido de Nico) las familias son: 6 tests principales del cuerpo, 6 interacciones,
   12 efectos por origen, 24 tests por díada del apéndice (BH y Holm). Falta una política única de comparaciones múltiples para el paper.
   **Parcialmente RESUELTO por Nico (18/09):** "Usemos siempre BH, no Holm". Benjamini-Hochberg en todo el paper; las columnas
   de Holm que existen (bloques 46, 52, 58, 64) quedan en las tablas como registro y no se citan. **Pendiente de Nico:** el
   alcance de la familia. Dos lecturas de "dentro de cada panel" que dan distinto en la afirmación central de la Figura 3:
   **RESUELTO por Nico (18/09): familia = por pregunta** ("confirmo familia por pregunta, creo que hacer las cosas de la
   manera habitual es una ventaja"). Regla del paper: Benjamini-Hochberg dentro de cada familia, y una familia es el conjunto
   de tests que contestan la misma pregunta dentro de un panel. Es lo aplicado hasta hoy: no hay nada que regenerar. En
   métodos hay que listar las familias de cada panel.
   (a) familia = los tests que contestan la misma pregunta dentro del panel (lo aplicado hasta hoy): en F3 panel C, los 8
       tests "24 modelos" son una familia y los 16 por origen otra; power grabbing hacia USA queda en q = 0,048;
   (b) familia = todos los tests dibujados en el panel (24 en F3 C): power grabbing hacia USA queda en q = 0,096.
   La lectura (a) es la usual (familias definidas por pregunta, no por el diseño de la figura) y es la recomendada. La
   opción "hipótesis primarias preespecificadas sin corregir" se descartó como recomendación: las preguntas del cuaderno
   del 8/09 (anteriores a las corridas de 24 modelos del 10–12/09) son ambiguas justo donde importa (F2 lista dos
   métricas, diferencia contra inglés y rango; F3 no dice qué modo) y resolver esa ambigüedad después de ver los números
   sería post hoc. Se describen en métodos como las preguntas de diseño del estudio, sin llamarlas preregistradas.
5. **Detalles del bootstrap:** B = 2000 o 5000 según el bloque; intervalo percentil; p bilateral = 2 · min(cola); en los
   bloques 43–45 el remuestreo se hace con pesos multinomiales por prompt (equivalente a la clase Boot del resto).

## B. Nulos de permutación

6. **Shuffle independiente por (modelo, prompt)** en la Figura 2 B (idiomas barajados dentro de cada prompt y modelo) y
   en la Figura 3 (intercambio de los dos veredictos de cada par; con las díadas juntas, independiente también entre las
   dos díadas del mismo prompt). Eso vuelve exacto el nulo por modelo (binomial, equivale a McNemar exacto). Alternativa
   más conservadora: el mismo intercambio para los 24 modelos de un prompt (conserva la correlación entre modelos).
7. **Juntar las dos díadas geopolíticas** (bloque 45): los pares discordantes de USA / China y de aliado de USA / aliado
   de China se suman por modelo; el bootstrap remuestrea prompts con sus dos díadas; en el GLMM entra `dyad` como efecto
   fijo y el prompt como intercepto aleatorio común a las dos díadas. La referencia neutral tiene una sola díada (la mitad
   de pares, menos potencia): la comparación geo contra neutral no es a igual potencia.
8. **La díada neutral A / neutral B como referencia en todos los paneles de la Figura 3**: la agregó Claude (es el
   control que pide el cuaderno); Nico aprobó los gráficos con ella pero no se discutió.

## C. GLMM (lme4::glmer)

9. **Regla de ajuste singular:** un ajuste singular (alguna varianza en 0) cuenta como convergido y se acepta antes que
   pasar a una estructura aleatoria más chica (`r/glmm_common.R`). Ya estaba marcada para Nico en NARRATIVA_F1.md.
10. **nAGQ = 0 en todos los modelos** fue decisión de Nico (16/09) por velocidad; el ómnibus de contexto cambió poco
    (χ² 6,8 → 4,7), pero no se comparó en los demás bloques.
11. **Estructura aleatoria:** `||` (sin correlación) primero; para factores de varios niveles, interceptos
    `(1 | model:factor)` en vez de 7 o más pendientes por modelo (bloques 32, 33, 36); contrastes suma-cero y ómnibus de
    Wald χ²; en el bloque 45 `side` está codificado ±0,5 (centrado) mientras que en la Figura 1 los contrastes binarios
    están en 0 / 1: con `||` la codificación cambia el modelo.
12. **Origen del modelo en el GLMM del lado:** dos parametrizaciones del mismo modelo (`side * cn` y `side * us`) para
    sacar el efecto en modelos US y en modelos CN con su error estándar.

12b. **(punto 21) GLMM de dirección por polo** (bloque 46, `r/glmm_direction.R`, pedido de Nico del 17/09): de las dos
    opciones que dio Nico se usó "dos modelos" (uno por polo); USA / China entra en los dos (con la dirección invertida en
    el de China); `toward` = ±0,5; origen del modelo centrado (±0,5) en UN solo ajuste por polo, y los efectos en modelos US
    y CN salen como combinaciones lineales de coeficientes con la matriz de covarianza (no tres ajustes, por el tope de 2
    minutos); `dyad` como efecto fijo y prompt como intercepto común a las díadas; el desglose díada por díada lo agregó
    Claude (Nico lo mandó a apéndice); primero solo power grabbing por pedido de Nico, después el control por sugerencia suya
    ("esto podría estar comparado con el control no?"): mismo modelo por separado, mostrado al lado, sin test de power
    grabbing contra control (queda como pregunta abierta para Nico).
12c. **Preferencia de Nico (17/09): "prefiero que no decidas por mí directamente".** Las bifurcaciones metodológicas se
    plantean antes de correr; lo que igual decida Claude se lista en el mensaje y acá.

12d. **(punto 22) Índice geopolítico 1D** (bloque 47, 18/09, pedido de Nico): curva principal (princurve, smooth.spline, df = 5, stretch = 2,
    arranque en PC1) sobre (axis_us, axis_cn); índice = longitud de arco reescalada linealmente a [−1, +1] entre los dos extremos observados,
    +1 del lado de USA, versión de la mañana del 18/09. Nico decidió centrar el cero en la MEDIANA de los países (extremos asimétricos);
    la implementación de Claude es (λ − mediana) / max |λ − mediana| (el extremo más lejano vale ±1, el otro llega a +0,57). Alternativas
    no elegidas: escala por rango; dejar la longitud de arco sin normalizar. El índice correlaciona 0,993 (ρ 0,998) con net_lean_us.

12e. **(punto 23) GLMM del índice 1D** (bloque 49, 18/09, Nico: "a ver, probemos ese GLMM"): refuse ~ índice × origen + (1 + índice || model) +
    (1 | prompt_id) + (1 | país); el país como intercepto aleatorio (propuesta de Claude aceptada para probar); en E, interceptos por país
    usuario y por país afectado; índice en la unidad del bloque 47; familias de corrección: 10 pendientes, 10 interacciones. Varios ajustes
    singulares con varianza de país = 0. No se probó sin los países extremos (índice < −0,6) ni el contraste power grabbing contra control.

## D. Métricas y estimadores

13. **Convención de signo del sesgo de díadas** (bloque 27 en adelante): > 0 = más rechazo cuando el lado A (USA o su
    aliado) es el usuario = a favor del lado China. Es el signo opuesto al del bloque 21 de Tomás.
14. **Sesgo por modelo como cociente (a − b) / (a + b)** sobre prompts discordantes y su promedio con peso igual: frágil
    con pocos discordantes (2 discordantes dan ±1). Por eso el panel pesado por uso terminó en OR de tasas (elección de
    Nico). La media de cocientes sigue en el panel de |sesgo| contra shuffle.
15. **Pesos de uso:** tokens de 30 días en OpenRouter sumando las variantes standard + free + batch de cada modelo
    (`inputs/openrouter_usage/`); en la media de cocientes los pesos se renormalizan sobre los modelos con sesgo definido.
    Un solo modelo (gpt-5.6-luna, 32 %) aporta 60–90 % de la varianza.
16. **Rango entre idiomas en OR** (Figura 2 B): logit suavizado (r·n + 0,5) / (n + 1) y media geométrica entre modelos.
17. **Acuerdo entre rankings de idiomas** (Figura 2 C): Spearman sobre 7 idiomas en los pares con un modelo excluido en
    swahili; IC bootstrap sobre prompts; tests por permutación de etiquetas de origen y de idiomas dentro de modelo (bloque 39).
18. **Índice de capability** usado solo para ordenar modelos en los gráficos y como covariable z en el bloque 30.

## E. Lecturas que dependen de lo anterior

19. Figura 2: "en promedio no hay diferencia entre idiomas" (Nico, 16/09) descansa en el GLMM con modelos aleatorios; con
    modelos fijos Hindi y francés sí difieren de inglés (punto 2).
20. Figura 3: "los modelos en general tienden a rechazar más sacarle poder a china (no así darle poder a USA, ya que
    self-empowerment no muestra diferencia)" (Nico, 17/09). En self-empowerment el resultado depende del estimador: el
    GLMM y el OR de tasas con peso igual dan un efecto chico en la dirección OPUESTA (OR 0,85, p = 0,043; OR 0,88,
    p = 0,005), mientras que el sesgo de discordantes y el pesado por uso no dan nada.

## F. pp vs OR, y OR por modelo vs OR de la media (pregunta de Nico, 18/09)

Nico (18/09): "qué es mejor, usar OR o usar diferencia de refusal directamente? cuándo decidiríamos usar uno u otro? [...]
cuando calculamos OR, entiendo que se puede calcular por modelo antes de hacer los promedios, y promediar sus ORs, o se
puede promediar primero y después hacer el OR de eso. Entiendo que lo segundo es peor porque eso sería equivalente a pp
(mentiroso) [...] quiero saber si estamos siendo consistentes con estas decisiones en todo el paper".

Inventario de lo que hace cada panel hoy (hecho, no decisión):

| panel | métrica | orden de promedio |
|---|---|---|
| F1 A–E | niveles en pp | no aplica |
| F2 A (bloque 34) | desviación en pp respecto de la media de los 8 idiomas, peso igual por modelo | pp: promediar antes o después da lo mismo (es colapsable) |
| F2 B (bloque 35) | rango entre idiomas en OR por modelo, exceso sobre su azar, media geométrica | OR POR MODELO primero |
| F2 D (bloque 40) | OR contra inglés de la tasa ponderada por uso | OR DESPUÉS (marginal): estimando "pedido típico", por diseño |
| F3 A (bloque 45) | (a − b)/(a + b) por modelo | por modelo |
| F3 B (bloque 45) | OR de lado de la tasa ponderada por uso | OR DESPUÉS (marginal), por diseño |
| F3 C (bloque 52) | GLMM: OR condicional (efectos aleatorios por modelo) | OR por modelo (condicional) |
| F4 (bloque 54) | niveles y Δ pareado en pp, peso igual por modelo | pp |
| `fig4_working` (Wendy) | pp; log-OR marginal (logística sobre filas apiladas = OR después); FE de prompt; forest por modelo = OR antes | mezcla, sin regla declarada |

Regla que se desprende y que el equipo tiene que confirmar: (1) "sesgo de un modelo" → calcular por modelo y promediar
después (pp o log-OR); (2) "pedido típico" → tasas agregadas con pesos de uso y recién ahí el OR, que es un OR marginal
(poblacional); (3) nunca comparar en magnitud un OR marginal (F2 D, F3 B) con uno condicional (F3 C, F2 B): por la
no-colapsabilidad del OR el marginal queda más cerca de 1 aun sin confusores (Greenland, Robins y Pearl 1999); (4) pp
para los contrastes pareados con la misma base en las dos ramas (F2 A, F4) y para hablar de impacto; OR o logit cuando se
comparan magnitudes entre modos o modelos con bases distintas (he 3,7 % vs pg 24 %); (5) donde haya ceros, la misma
suavización (+0,5) en todos los paneles.

Chequeo exploratorio (18/09, no es test oficial): exceso del rango sobre el azar del modo contra el del control, pareado
por modelo (t, 23 gl, en log): he 0,92 [0,68; 1,23] p = 0,55; de 1,24 [1,02; 1,52] p = 0,036; pg 1,02 [0,89; 1,16]
p = 0,82. Lo que en el panel B viejo parecía "he y de por encima del control" era el rango crudo sin corregir por el azar:
el rango barajado de he es 2,49 (base 3,7 %, conteos chicos y suavización) contra 1,51 del control.

**Aprobado por Nico (18/09):** la regla de la sección F ("ok lo del OR, me parece lógico lo que planteás, aprobado"). Los
paneles ponderados por uso (F2 D, F3 B) se quedan como OR marginal de un pedido típico, con esa etiqueta en la leyenda
y en métodos, sin comparar su magnitud con los OR por modelo. También aprobado el mismo día: panel A de la Figura 3 en el
formato de exceso por modelo (bloque 55), que cierra el punto 1 de la sección A para las dos figuras.

## G. Figura 4 (18/09): decisiones de Claude al implementar los pedidos de Nico

22. **Test de la frase "el sesgo es el mismo en los dos orígenes" (bloque 58):** elegido por analogía con la Figura 3
    (bloque 45): GLMM por modo refuse ~ ai × origen + (1 + ai || modelo) + (1 | prompt), ai = ±0,5, origen centrado
    (ajustes ai * cn y ai * us), Wald; familias BH: 4 principales, 4 interacciones, 8 por origen. Complemento: t de Welch
    entre orígenes sobre el sesgo de dirección por modelo (el estadístico del panel del apéndice). Alternativas: solo la
    Welch; permutación de las etiquetas de origen; el GLMM con la díada de dominio. Nico pidió "test estadístico" sin
    especificar cuál.
23. **Familias BH en la Figura 4:** 4 modos (bloques 56, 57-Welch, 58); en el bloque 59 (por dimensión) no hay corrección
    porque no hay tests, solo descriptivo. **DESACTUALIZADO (corregido el 20/09):** el bloque 59 sí testea cada celda (t entre
    modelos contra 0) y trae q = BH sobre todas las celdas de la dimensión (32 en contexto, 24 en dominio); los heatmaps D y E de
    la figura del agente IA marcan las celdas con q < 0,05 y el conteo de celdas significativas por modo sale de esa q.
24. **Panel 4 por dimensión (bloque 59):** el nivel se define por el prompt (escala, standing, contexto, dominio); el sesgo
    se calcula dentro del nivel por modelo y se promedian los modelos con al menos un discordante en ese nivel (los demás
    quedan fuera de esa celda). Alternativa: sumar los conteos discordantes de todos los modelos (pooled) o un GLMM con
    ai × nivel. Control sin dominio: no aparece en la figura de dominio.
25. **Test de la tendencia con la escala / standing (bloque 60):** GLMM por modo refuse ~ ai × nivel + (1 + ai || modelo) +
    (1 | prompt), nivel de referencia individual / low, contrastes por combinación lineal con vcov y ómnibus de Wald (χ², 2 gl),
    gemelo del test de escala de la Figura 1 (bloque 31); familias BH: 4 ómnibus por dimensión, 12 contrastes por dimensión.
    Complemento: t pareada por modelo del sesgo de dirección nivel 3 − nivel 1 (la "vieja y confiable" de Nico, como test).
    Alternativas: solo la t pareada; GLMM con los tres niveles como pendientes aleatorias por modelo.
26. **GLMM de capacidad (bloque 64):** refuse ~ ai × cap_z + (1 + ai || modelo) + (1 | prompt), cap_z estandarizado sobre los
    24 modelos; en la versión conjunta, `+ mode` como efecto fijo (sin ai × mode: una sola pendiente de capacidad para los
    tres modos de poder) y un modelo apilado ai × cap_z × ps para la diferencia de pendientes contra el control. Familia BH:
    las 4 interacciones por modo. Alternativas: ai × mode además; meta-regresión de los log-OR por modelo con sus SE;
    capacidad sin estandarizar.
27. **Recta del GLMM sobre los scatters de capacidad (bloque 64):** la predicción condicional del GLMM se dibuja marginalizada
    sobre el intercepto aleatorio de prompt con la aproximación de Zeger, Liang y Albert (1988), β_marginal ≈ β / √(1 + c² σ²),
    c² = (16√3 / 15π)² ≈ 0,346, σ² = varianza del intercepto de prompt (solo prompt, porque los puntos son por modelo).
    Los números anotados (razón de OR por SD, p) son los del GLMM en escala condicional. Alternativas: dibujar la recta
    condicional tal cual (queda por encima de los puntos); anclar la pendiente en la media de los puntos; puntos = BLUP
    por modelo (no sirve en ajustes singulares, colapsan sobre la recta).
28. **GLMM del reasoning ladder (bloque 68):** un solo ajuste con r1 y r2 (indicadoras de los dos niveles, OFF = referencia),
    modo y origen con contrastes suma-cero (los efectos de nivel son promedios sobre modos y orígenes), interacciones nivel ×
    modo y nivel × origen (sin la triple), intercepto aleatorio de prompt (aparea las tres ramas) y pendientes aleatorias de
    r1 y r2 por modelo (||). Los niveles se tratan como "primer nivel" y "segundo nivel" de cada proveedor aunque no sean
    comparables entre modelos. Familias BH: 8 efectos por modo (2 niveles × 4), 4 por origen, 6 contrastes modo − control,
    2 principales. Alternativas: nivel como ON / OFF (un solo término); nivel ordinal 0 / 1 / 2; tokens de razonamiento
    como covariable continua; ajustes separados por modo.
29. **Guard para las celdas con pocos modelos (bloque 69, sesgo de razonamiento por factor):** una celda se testea (t contra 0)
    solo si tiene al menos 4 modelos con discordantes y su SD entre modelos no es 0; si todos los sesgos son idénticos (por
    ejemplo −1 en 2 modelos) la t es infinita y daría p = 0 sin información. Las celdas no testeables se muestran sin
    asterisco. En los heatmaps de la Figura 4 (bloque 59) no había celdas con SD = 0 y las de menos de 4 modelos no
    salieron significativas, así que no cambian; el guard no está aplicado ahí (a unificar).

## H. Reglas de interpretación decididas por Nico (18/09)

30. **"Significativo en X y no en Y" se lee como "específico de X"**, aunque no haya test de la diferencia (Nico, 18/09, sobre
    capacidad: "me parece una interpretación razonable decir que si algo es significativo en un caso pero no en otro, es
    específico de ese primer caso, por más que no hagamos el test entre pendientes"). Aplica a F4 capacidad (power-shifting
    sí, control no; diferencia de pendientes p = 0,10, reportada como dato) y a F3 (díadas geopolíticas sí, neutral no). Se le
    señaló la crítica de Gelman y Stern (2006) y decidió mantener la lectura. Donde el test de la diferencia existe (F1 origen
    × power-shifting, reasoning modo × control, F4 escala) se reporta.
31. **Verificación de ajustes singulares en las afirmaciones del cuerpo (18/09, sobre el punto 9):** ningún test del cuerpo
    descansa solo en un ajuste singular. Los singulares significativos son (i) los efectos principales IA vs humano en
    self-empowerment y control (bloque 58) y los de capacidad media (bloque 64), que se confirman con un test independiente de
    modelos aleatorios sin GLMM (bloque 56, t entre modelos: q = 0,001 y 0,006); y (ii) la interacción IA × capacidad en power
    grabbing por modo (q = 0,005), que está en el apéndice con la advertencia, porque el cuerpo usa el ajuste conjunto de
    power-shifting, no singular. F3 panel C y F4 escala en power grabbing: no singulares.

32. **Test de "los modelos chinos se parecen más entre sí que los de USA" en el refusal medio (bloque 70, 18/09):** elegido por
    Claude: Brown-Forsythe (Levene centrado en la mediana, robusto a no normalidad) sobre los 12 + 12 promedios por modelo, con
    Fligner-Killeen y una permutación de etiquetas de origen sobre la razón de SD como chequeos. Resultado: no significativo
    (p = 0,15; 0,27; 0,054). Alternativas: comparar rangos intercuartiles con bootstrap sobre modelos; test sobre cada modo por
    separado (ninguno da); GLMM con varianza del intercepto de modelo distinta por origen y test de razón de verosimilitud.

33. **Bloque 72 (19/09): panel D de la Figura 2 con pesos por PEDIDOS, power shifting pooled y permutación al lado del
    bootstrap.** Pedido de Nico, textual: "pesar por pedidos me parece mejor"; "pooled de power shifting como análisis
    secundario me parece bien hacerlo también"; "test de permutación, no reemplaces lo otro por ahora pero hacelo así
    comparamos". Decisiones de Claude al implementarlo: (a) power_shifting = los 576 prompts he + de + pg con igual peso por
    prompt (equivale a la media de las tres tasas porque los modos están balanceados; alternativa: pesar los modos por su
    frecuencia en el tráfico, que no se conoce); (b) bootstrap estratificado por modo en el pooled, mismos índices para los
    24 modelos y para los dos juegos de pesos, misma semilla que el bloque 40 (los IC por tokens coinciden con los de ese
    bloque); (c) nulo de permutación = barajar los veredictos entre los idiomas presentes dentro de cada (modelo, prompt),
    independiente entre modelos, como en el bloque 35 (alternativa más conservadora: la misma permutación para los 24
    modelos de un prompt, que conserva la correlación entre modelos); (d) p bilateral de permutación
    (1 + #{|T*| ≥ |T|}) / (B + 1) con B = 5.000; p bilateral del bootstrap 2 · min(cola) como en el punto 5; (e) familia BH
    = los 7 idiomas de un mismo grupo (modo o pooled), aplicada por separado a cada p (alternativa: una familia de 35 con
    los cinco grupos); (f) los tokens quedan en una tabla de comparación, no en la figura. Sin test de power grabbing contra
    control (no pedido). Estado: RESUELTO por Nico (19/09): pesos por pedidos quedan; bootstrap para la barra, permutación para el test; la
    compuesta 41 se regeneró con el bloque 72.

34. **Bloques 73 y 74 (19/09): los otros dos paneles de "pedido típico" (Figura 3 B, Figura 4 panel 6) con pesos por PEDIDOS,
    power shifting pooled y permutación como test.** Decisión de Nico, textual: "la ponderación por pedido me parece mejor, queda
    eso"; "bootstrap para barra, permutación para test; hacé los tres que faltan". Decisiones de Claude al implementarlo:
    (a) mismo estimador que los bloques 44 / 45 y 63 (tasa pesada por uso en cada condición, un log-OR marginal); (b) nulos de
    permutación análogos al del bloque 72: en Figura 3, intercambio al azar de los dos veredictos de cada (modelo, prompt, díada),
    el nulo de los bloques 43 / 45 / 55; en Figura 4, intercambio del veredicto humano y el IA de cada (modelo, prompt); B = 5.000
    en los dos; (c) bootstrap sobre prompts con cada prompt arrastrando sus díadas (F3) o sus dos condiciones (F4), estratificado
    por modo en el pooled; en el 74 con la semilla y el orden de sorteos del bloque 63, así los IC por tokens de los 4 modos
    coinciden con ese bloque; (d) el pooled power_shifting se agregó también en F3 y F4 por simetría con el 72 (Nico lo aprobó
    para la Figura 2; acá es secundario y va sin corregir); (e) familias BH = los 4 modos de un mismo conjunto (F3: geo, neutral,
    USA / China, aliados; F4: 24 modelos, US, CN); (f) en el 74, el estimador por origen con los pesos renormalizados dentro de
    cada bloque, en OR y en pp, reemplaza con el estimador del paper la tabla "ponderando por uso" de fig4_working (Wen, 18/09),
    que usa una regresión pesada con errores agrupados por prompt y lee los pesos por tokens del bloque 40; ese script no se
    tocó (rutas de la máquina de Wen). Sin test de US contra CN ni de modo contra control (no pedidos). Estado: los bloques 44,
    45 y 63 quedan como registro; la compuesta 51 se regeneró con el 73 (Nico, 19/09); la 65 no incluye el panel de pedido típico.

35. **Panel B nuevo de la Figura 3 (19/09):** Nico pidió un panel con el efecto del lado sin pesar por uso. Claude eligió dibujar el
    OR del GLMM del lado del bloque 45 (`side_glmm.csv`, "lado (24 modelos)") con IC de Wald, igual que el panel D, para que B y D
    sean el mismo tipo de número (OR condicional de modelos aleatorios); alternativa: el OR con peso igual por modelo e IC bootstrap
    (`side_estimators.csv`, logOR_igual), que es descriptivo. Familia BH = los 4 modos del conjunto geo; neutral sin q (referencia;
    sus cuatro ajustes son singulares). Consecuencia: pg queda en q = 0,099 en B, mientras que en C (pesado por pedidos) da q = 0,011.

36. **Bloque 76 (19/09): test "power shifting tiene más sesgo de dirección hacia la IA que el control" (panel B de la figura del
    agente de IA).** Pedido de Nico. Decisiones de Claude: (a) el sesgo pooled de power shifting suma los discordantes de he, de y pg
    por modelo antes del cociente (cada prompt discordante pesa igual; alternativa: media de los tres sesgos por modo, que pesa igual
    a los modos); (b) test = t pareada entre los 24 modelos de sesgo(ps) − sesgo(control), Wilcoxon como chequeo (alternativa: GLMM
    ai × (ps vs control) con pendientes por modelo, no construido); (c) el test principal va sin corregir y los tres por modo forman
    una familia BH aparte. Resultado: +0,28 [0,18; 0,38], p < 0,001.

37. **Bloque 77 (19/09): familias BH para los bloques 30, 31 y 39.** Nico: "hay que correr lo de BH para los bloques que faltan, con las
    familias por pregunta como siempre hicimos". Familias elegidas por Claude según esa regla: Figura 1 modos, los 2 contrastes; origen,
    los 4 efectos CN − US por modo y, aparte, las 3 interacciones CN × (modo vs control); escala y standing, las 4 pendientes por modo y,
    aparte, las 3 interacciones; los pooled de power shifting como tests únicos (q = p). Idioma C (39): "dentro − mixto" por modo (4);
    "CN–CN − mixto" y "US–US − mixto" por modo (8); "todos los pares" por modo (4); "CN–CN", "US–US", "mixto" contra idiomas barajados por
    modo (12); sobre p_right unilateral, como los definió el bloque 39. Alternativas: una sola familia por panel (8 en escala, 24 en
    idioma C); los pooled dentro de la familia por modo (5). Consecuencia: escala en de q = 0,079 e interacción CN × (de vs control)
    q = 0,053 dejan de sostenerse; nada más cambia. Ninguna compuesta anota estos p, así que no hay figura que regenerar.

38. **Bloque 78 (19/09): Figura 1 rediseñada (candidata).** Pedido de Nico con siete paneles. Decisiones de Claude al implementarlo:
    (a) barras de error de los niveles = IC 95 % t entre los 24 modelos (o los 12 del origen), el marco de modelos aleatorios, y no
    bootstrap sobre prompts (alternativa descriptiva; en A el IC t es más ancho porque incluye la dispersión entre modelos); (b) power
    shifting medio por modelo = media de he, de y pg; (c) asteriscos de B = q del GLMM de origen del bloque 30 con la familia del 77;
    (d) "efecto general del origen" = GLMM nuevo refuse ~ cn + mode + (1 | prompt) + (1 | model) sobre los cuatro modos
    (r/glmm_fig1_v3.R), sin pendiente aleatoria de origen porque el origen es entre modelos; "si depende de power shifting" = el
    término cn × ps del ajuste E del bloque 30, no se refitó; (e) F y G: desviaciones por nivel con contrastes suma-cero sobre las
    filas de power shifting, refuse ~ nivel + mode + (1 | model) + (1 | model:nivel) + (1 | prompt), BH sobre los 8 niveles, análogo
    en modelos aleatorios del panel A de idioma (alternativa: bootstrap pareado dentro de modelo; o incluir el control en contexto);
    (f) en D y E solo curvas con banda; los tests siguen siendo los de los bloques 31 y 77; (g) C sin barras de error (media de
    cuatro tasas, como el bloque 70). Todo con nAGQ = 0.

39. **Bloque 79 (19/09): sesgo idioma contra idioma (heatmap triangular).** Pedido de Nico para la figura de idioma con Wendy.
    Decisiones de Claude: (a) sesgo por modelo y par = (solo A − solo B) / discordantes, sobre los prompts válidos en los dos
    idiomas; NaN si el modelo no tiene discordantes en ese par; (b) test = media entre modelos, IC t, t contra 0 (marco de modelos
    aleatorios, como los bloques 55, 56 y 76); (c) familia BH = los 28 pares de un mismo modo (alternativa: los 7 contrastes contra
    inglés, que sería el análogo del panel A; o una familia de 112 con los cuatro modos); (d) triángulo inferior con la fila contra la
    columna e idiomas en el orden del panel A (refusal medio creciente); (e) power_shifting pooled con los discordantes sumados por
    modelo, secundario; (f) swahili sin nemotron-3.5-lightning ni nova-2-lite (regla del 16/09), así los pares con swahili tienen 22
    modelos. Nota: en self-empowerment la mediana de discordantes por modelo es 5 a 8, así que los sesgos de ±0,3 a ±0,4 salen de
    pocos prompts; en pg son 26 a 42.
    **Actualización (Nico, 19/09): "quizás es intentar hacer demasiados tests y no es la mejor manera... y además es mucha información;
    creo que dejaría solo el de power-shifting, sin tests estadísticos, solo como descriptivo".** El bloque quedó con un solo panel,
    power shifting pooled, sin IC, p ni q; los puntos (b) y (c) ya no aplican. El heatmap de los cuatro modos con tests se borró de
    la carpeta; sus números están en la entrada del 19/09 de NARRATIVA_F2.md como registro.

40. **Bloque 80 (19/09): sesgo por par de idiomas contra la diferencia de prevalencia.** Pedido de Nico ("scatter y regresión entre
    esas dos cosas, no sé si será justo pero empecemos por ahí"). Decisiones de Claude: (a) prevalencia = participación de páginas
    en Common Crawl CC-MAIN-2026-34, el único proxy congelado en el repo (Wikipedia, mencionado en el cuaderno, nunca se bajó);
    (b) x = log10(share_A) − log10(share_B) con A la fila del heatmap del bloque 79, así una pendiente negativa = el idioma menos
    representado se rechaza más; (c) dos lecturas: recta de mínimos cuadrados sobre los 28 pares con el sesgo medio (su p es solo
    descriptiva porque los pares comparten idiomas) y pendiente por modelo con media e IC t entre modelos; (d) sin ponderar los
    pares por cantidad de discordantes (mediana 48 a 77 por modelo y par, alternativa: pesos 1/varianza). Advertencia de fondo:
    los 28 pares no son observaciones independientes; una regresión con efectos aleatorios cruzados por idioma A e idioma B sería
    lo formal, no construida.
    **Agregado (Nico, 19/09): la regresión formal quedó hecha** (`r/lmm_pair_prevalence.R`): LMM gaussiano sobre el sesgo por modelo
    y par, pendiente fija de dlog_share, pendiente e intercepto aleatorios por modelo (||), interceptos por idioma en el rol A y en
    el rol B; Wald z. Elecciones: gaussiano sobre un cociente acotado (alternativa: GLMM binomial sobre los conteos a y b); los dos
    roles del idioma como interceptos separados en vez de un efecto de idioma con signo ±1 (que lme4 no expresa directamente);
    sin la interacción con el origen del modelo (no pedida). Resultado: −0,013 [−0,075; 0,050], p = 0,70.

41. **Bloque 81 (20/09): concordancia del orden de idiomas entre modos.** Nico pidió "una manera de testear mejor" que las seis
    correlaciones. Decisiones de Claude: (a) W de Kendall por modelo con corrección por empates, rankings dentro de cada modo con
    rangos promedio; (b) Q2 como Spearman del ranking del control contra el rango medio de los tres modos de poder (alternativa:
    W de los 4 menos W de los 3, o W de los 4 solo); (c) nulo = idiomas barajados dentro de cada modo y modelo, independiente entre
    modos, B = 5.000, el del bloque 39; (d) test principal = exceso W − E0 por modelo con t entre los 24 (marco de modelos
    aleatorios); el p por modelo y el conteo de modelos con p < 0,05 son descriptivos; (e) dos preguntas, sin BH entre ellas;
    (f) los dos modelos sin swahili rankean 7 idiomas y entran igual; (g) la versión sobre las 8 medias (la pregunta original) queda
    como referencia con p de permutación (B = 20.000). Nada de esto está en la compuesta de Wendy.
    **Agregado (20/09):** los paneles para la figura. Bump chart: altura = posición 1..8 del rango medio de los rankings hechos dentro de cada
    modelo (Nico eligió la versión de posiciones sobre la de rango medio, que exagera diferencias chicas pero es la que quiere); barras B1/B2:
    media de los 24 del estadístico observado y media de su esperado bajo el nulo por modelo, ambas con IC t; el test sigue siendo la t del exceso
    por modelo. Los asteriscos por modelo del gráfico anterior eran descriptivos; con BH sobre 24, 14/18 en Q1 y 3/9 en Q2. Flag `--reuse`
    para redibujar sin repetir las permutaciones.

42. **Bloque 82 (20/09): GLMM de idioma sobre power shifting pooled.** Nico: "podría estar bueno, y dejar constancia". Decisiones de Claude:
    mismo modelo que el bloque 36 con las filas de los tres modos juntas y `mode` como efecto fijo (referencia pg), intercepto por modelo × idioma
    como perfil propio de cada modelo (variante mínima sin él si no converge; convergió la completa), BH sobre los 8 idiomas. Alternativas: pendiente
    aleatoria de idioma por modelo (8 pendientes, muy lento, descartado el 16/09 en el bloque 36), o interacción idioma × modo (otra pregunta).
    **Panel B1/B2 del bloque 81, tercera versión (20/09):** Nico objetó que el bigote del azar de un modelo se superpusiera con la media de 24 y el
    test diera igual; tenía razón, eran dos escalas. Ahora el panel es exceso sobre el azar por modelo con IC t y línea en cero, el formato del panel
    B de idioma y el A de países. La versión con dos barras (observado y azar) quedó descartada.
    **Definitiva (20/09):** B1 = Spearman medio entre los tres pares de órdenes por modelo (no la reescala del W, que con empates difiere
    hasta 0,05), t contra 0; B2 = rho contra el consenso, t contra 0; un solo panel en rho con línea en 0. El W de Kendall y su exceso quedan en
    la tabla como el estadístico original de Q1 (misma conclusión: 0,35 [0,27; 0,43]).

43. **Figura de idiomas, versión de página v2 (20/09): familias BH elegidas por Claude.** Nico pidió BH en todos los asteriscos.
    Familias: A = los 8 idiomas de cada modo (q del bloque 36; alternativas: 4 modos por idioma, los 32, los 24 de power shifting;
    ver NARRATIVA_F2, pendiente de Nico); D = los 4 modos dentro de cada ponderación (alternativa: los 8 tests del panel; no cambia
    ninguna estrella); F = los 3 tipos de par (alternativa: una familia con el corchete, 4). Consecuencia: en A quedan solo
    swahili-he y hindi-de; en F cae CN–CN (q 0,107). Tabla: `review_fig_languages/figure_paper_v2_bh_q_values.csv`.
    Implementación: argumento opcional `q=` en tres funciones de `figure_paper.py` de Wendy, sin cambiar su salida por defecto.

44. **Bloque 83 (20/09): BH para los dos tests del cuerpo que quedaban con p crudo.** Revisión de asteriscos pedida por Nico
    ("podés repasar las otras tres figuras a ver si alguna más está mostrando estrellas que no debería por no haber corregido
    por BH?"): las tres estaban corregidas salvo dos anotaciones. Familias elegidas por Claude: (a) Figura 3 (agente IA) F,
    la interacción IA × capacidad de los dos ajustes pooled, power shifting y control, como una familia de 2 (antes, dos tests
    únicos con p; power shifting pasa de p 0,006 a q 0,012, nada cambia de estado); la diferencia de pendientes del modelo
    apilado sigue como test único. (b) Figura 2 (países) B, el GLMM del lado del usuario, los 4 modos de cada set, geo y
    neutral, cada uno su familia; hasta hoy la BH de geo se calculaba dentro del script de la figura (misma q) y neutral no
    llevaba q; ahora la q está registrada en el bloque 83 y neutral la muestra también, como ya hacía el panel C (bloque 73).
    Alternativas: F como dos tests únicos (lo anterior); B con una sola familia de 8. Consumidores actualizados:
    paper_figures/figure3_aiagent_paper.py, analysis_65_fig4_composite.py, paper_figures/figure2_countries_paper.py,
    review_fig_countries/figure_full_split.py (+ SRC de analysis_51). Nico: "sí, hagamos las tres cosas".

45. **Resoluciones de Nico del 20/09 tras la auditoría de consistencia (RESULTADOS_CONSOLIDADOS.md, sección 9).** (a) Familia BH
    de los heatmaps de la Figura 3 (bloque 59) = las celdas dentro de cada modo ("esa es la pregunta"); recorrido, dos celdas de
    dominio cambian (he Legal pierde, de Attentional gana, q 0,050). (b) Familia BH del panel A de la Figura 2 (bloque 55) = los 4
    modos de cada set, como B y C; recorrido, nada cambia. (c) Las frases que los tests no sostienen no se dicen: "los modelos
    chinos se parecen más entre sí" (F1 C), "los modelos chinos ordenan parecido los idiomas" (F4 F, CN–CN q 0,107), "más marcado en
    modelos USA" (F2 D). (d) El pedido típico por idioma (bloque 72) va al apéndice. (e) Figura 3 F: la media simple de los tres
    log-OR por modo se abandona ("no me gusta que SE pese un montón y sea solo ruido"); candidato preferido = combinación por
    inversa de la varianza con el test del 64 sin cambios ("pareciera la mejor") → APROBADO ("ok, perfecto entonces aprobado"), bloque 84. Puntos 4, 23, 43 y 44
    quedan complementados por este.
