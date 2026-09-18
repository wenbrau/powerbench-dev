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
    porque no hay tests, solo descriptivo.
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
