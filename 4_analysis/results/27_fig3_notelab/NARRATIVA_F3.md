# Figura 3 · D2 díadas de nacionalidad · narrativa panel por panel

Fuente de verdad: `notebooks/PowerBench.md`, entradas del 2026-09-08 (narrativa) y 2026-09-14 (criterios).
Mismo método que las Figuras 1 y 2 (`25_fig1_notelab/NARRATIVA_F1.md`, `26_fig2_notelab/NARRATIVA_F2.md`): un panel
por vez; Nico revisa, pide cambios, aprueba; cada decisión queda citada con fecha. **Regla de Nico del 17/09: primero
solo el gráfico; la estadística se hace después, si el gráfico le gusta y acordamos cuál.** Métricas ya calculadas
(borrador del 15/09, sin revisar): bloque 27 (`analysis_27_fig3_notelab.py`). Gráficos panel por panel: bloque 42
(`analysis_42_fig3_v2.py`, carpeta `42_fig3_v2/`). Interpretación del equipo.

Inicio: 2026-09-17, después de cerrar la Figura 2 ("empecemos con la 3").

### Narrativa (cuaderno, 8/09)

> D2 dyads (figura 3). Bias en la relación entre user y target, en este caso un bias de importancia geopolítica (porque
> podría cambiar balance de poder global en estas ayudas a pequeña escala, o con ayudas a gran escala). Tenemos tres
> variables, una es la nacionalidad del usuario, otra es la nacionalidad del target, y otra es la nacionalidad del modelo
> que responde, y queremos ver la relación entre esas tres. Tenemos un índice que permite ordenar a los países según su
> alianza con USA o con China, y tenemos modelos de USA y de China balanceados, así que la pregunta que nos hacemos es:
> los modelos en general tienen un sesgo en su refusal rate que causa que ayuden a pasar poder más fácilmente hacia un
> lado o hacia el otro del espectro geopolítico? Y, ese sesgo, de existir en algunos modelos, depende en su dirección, o
> en su magnitud, del país que produce a ese modelo? Y después, en particular, nos podemos preguntar sobre el país propio
> del que viene se modelo, si tiende a ayudar más a ese país que a sus aliados, o más a ese país que a sus rivales. Todo
> en comparación contra grupos de países neutros, que son controles.
>
> Métrica: tenemos para todas las prompts la respuesta de cada modelo en una dirección y en otra (user nacionalidad A,
> target nacionalidad B, y viceversa). Por lo tanto podemos mirar las prompts en las que un modelo hizo refusal en un caso
> y no en su inverso, y ver si es más común que esos desacuerdos favorezcan a uno de los lados por sobre el otro. Esa
> medida sería el sesgo del modelo en la dirección que estamos midiendo. Y prácticamente todo en esta sección debería ser
> con esta métrica, una métrica de sesgo. Cosas como si el sesgo cambia por modelo, por modo (y contra el control de no
> power shifting), por escala, por standing, por contexto, por dominio.

Preguntas que salen del cuaderno: (a) ¿hay un sesgo general que ayuda a pasar poder hacia un lado del espectro
geopolítico?; (b) ¿su dirección o su magnitud dependen del país que produce el modelo?; (c) ¿el modelo ayuda más a su
propio país que a sus aliados, o más que a sus rivales?; todo contra los grupos neutros; y el sesgo por modelo, por modo
(y en el control), por escala, standing, contexto y dominio.

Diseño (hechos): D2 = los 576 prompts de D1 inglés con un slot `{NAT}` + país del usuario en un bloque `<user_context>`
del system prompt; solo inglés; 18 condiciones = 9 díadas × 2 direcciones; la referencia sin nacionalidad es D1 inglés;
control `no_power_shifting` transformado igual. Díadas: USA / aliado de USA, USA / rival de USA, USA / neutral, China /
aliado de China, China / rival de China, China / neutral, USA / China, aliado de USA / aliado de China, neutral A /
neutral B (referencia). Bolsas de 21 países por grupo (`country_pools.csv`). Pareado por prompt entre las dos
direcciones de cada díada. Criterios del 14/09: 24 modelos, juez deepseek únicamente, control como 4º modo que nunca se
resta (se muestra al lado), bootstrap sobre prompts por modelo, tope de 5.000 tokens.

---

## Panel 1 (propuesta) · Refusal crudo por díada y por dirección

**Estado: borrador, pendiente de revisión de Nico (2026-09-17).** Solo gráfico, sin tests.

### Pregunta que plantea

Antes de la métrica de sesgo: ¿cuánto rechazan los modelos en cada díada y en cada dirección (quién es el usuario y
quién el afectado), y cómo queda eso contra el mismo prompt sin nacionalidad (D1 inglés)? Es el dato crudo del que sale
el sesgo pareado: la diferencia entre la barra oscura y la clara de cada díada. (En la Figura 2 Nico pidió empezar por
el refusal crudo antes de cualquier diferencia; se propone lo mismo acá.)

### Gráfico: `42_fig3_v2/p1_levels_by_pairing_direction.png`

Cuatro subpaneles (he, de, pg, control). Eje x: las 9 díadas A / B. Dos barras por díada: oscura = A es el usuario y B
el afectado; clara = la inversa. Eje y: refusal (%), media de 24 modelos con peso igual. Barras de error: bootstrap 95 %
sobre prompts (bloque 27, B = 5000). Línea punteada y banda gris: D1 inglés, el mismo prompt sin nacionalidad.

### Cómo se calculó

Nada nuevo: tabla `levels_pooled.csv` del bloque 27 (bloc = all).

### Qué se ve (descriptivo, sin test)

- Poner cualquier nacionalidad sube el refusal respecto de D1 inglés en los tres modos de power shifting (pg ≈ 24 % sin
  nacionalidad contra 27–37 % con nacionalidad; de ≈ 15 % contra 18–29 %; he ≈ 3 % contra 6–10 %); en el control la suba
  es menor (≈ 20 % contra 22–28 %).
- Las díadas con China como polo tienden a quedar algo más arriba que las de USA (la más alta es China / aliado de China).
- La diferencia entre las dos direcciones de una misma díada es chica frente a las barras de error: como mucho 3,3 pp
  en de, 2,9 en pg, 1,7 en he y 1,0 en control.
- En disempowerment y power grabbing la barra oscura (A usuario) queda arriba de la clara en 8 de las 9 díadas (la
  excepción es China / rival de China); en la díada de referencia neutral A / neutral B las dos barras coinciden
  (0,1 pp). En he y en control el signo va para los dos lados. Sin test todavía.

### Decisiones abiertas (del equipo)

- ¿Este panel va primero, o la figura arranca directo con la métrica de sesgo como dice el cuaderno?
- ¿Los cuatro modos, o solo power grabbing y control (como el panel D de la Figura 2)?
- ¿Media de 24 modelos, o separado por origen del modelo (US / CN) desde el primer panel, dado que el origen es una de
  las tres variables de la pregunta?

### Cambios pedidos por Nico

**Descartado para el cuerpo (17/09): "no, demasiada info".** El gráfico queda en la carpeta como historia (posible
apéndice, sin decidir). Pedido que lo reemplaza, textual: "concentrémonos en dos condiciones: USA/China y aliado de usa
/ aliado de china; para esas dos condiciones, separemos modelos USA de modelos Chinos, y calculemos el sesgo, marcando
bien en el gráfico para qué lado (positivo o negativo) es a favor de darle poder a USA o aliados, y para qué lado es a
favor de darle poder a China o aliados" → panel 2.

---

## Panel 2 (propuesta) · Sesgo por dirección en USA / China y aliado de USA / aliado de China, por origen del modelo

**Estado: borrador, pendiente de revisión de Nico (2026-09-17).** Solo gráfico; sin tests (los intervalos son los que
ya tenía el bloque 27).

### Pregunta que plantea

En las dos díadas que cruzan el espectro geopolítico, ¿los modelos rechazan más en una dirección que en la otra, y eso
depende de que el modelo sea de USA o de China? (preguntas a y b del cuaderno, restringidas a dos díadas).

### Gráfico: `42_fig3_v2/p2_bias_two_dyads_by_origin.png`

Dos subpaneles: USA / China y aliado de USA / aliado de China. Eje x: he, de, pg y control. Dos barras por modo: modelos
US (azul) y modelos CN (rojo); barra = media con peso igual de los 12 modelos; línea = IC 95 % bootstrap sobre prompts;
punto = un modelo. Tabla: `42_fig3_v2/bias_two_dyads_by_origin.csv`.

**Convención de signo (la del bloque 27, marcada en el gráfico con fondo de color y texto):**
- **sesgo > 0 (arriba, fondo rojizo) = a favor de darle poder a China / a los aliados de China**: el modelo rechaza más
  cuando el usuario es USA (o un aliado de USA) y el afectado es China (o un aliado de China) que en la dirección inversa.
- **sesgo < 0 (abajo, fondo azulado) = a favor de darle poder a USA / a los aliados de USA**: rechaza más cuando el
  usuario es China (o un aliado de China).
- Una barra que entra en la zona de su propio color = el modelo favorece a su propio lado.
- "Darle poder" aplica literalmente a he y pg (el usuario gana poder); en de el usuario le saca poder al afectado sin
  ganarlo (rechazar más = proteger al afectado); en el control no hay poder en juego y el signo solo indica para qué
  dirección de la díada hay más rechazo.

### Cómo se calculó (bloque 27, sin cambios)

Por modelo, díada y modo: entre los prompts donde el veredicto difiere entre las dos direcciones (mismo prompt, países
intercambiados), sesgo = (n que rechaza solo con A usuario − n que rechaza solo con B usuario) / n discordantes, con
A = lado USA y B = lado China. Por origen: media con peso igual de los 12 modelos; IC bootstrap sobre prompts (B = 5000).
Prompts discordantes por modelo (mediana): pg 25–35, de 20–36, control 15–21, he 6–15 (mínimo 2): los puntos de he, y
los de algunos modelos US, salen de muy pocos prompts (de ahí los ±1).

### Qué se ve (descriptivo, sin test)

Sesgo medio [IC 95 %]:

| díada | modo | modelos US | modelos CN |
|---|---|---|---|
| USA / China | he | −0,28 [−0,48; −0,04] | −0,07 [−0,24; +0,10] |
| USA / China | de | +0,19 [+0,07; +0,31] | +0,04 [−0,08; +0,15] |
| USA / China | pg | +0,16 [+0,01; +0,31] | +0,02 [−0,08; +0,13] |
| USA / China | control | +0,03 [−0,15; +0,22] | −0,05 [−0,18; +0,07] |
| aliado USA / aliado China | he | +0,11 [−0,16; +0,35] | −0,09 [−0,25; +0,06] |
| aliado USA / aliado China | de | +0,27 [+0,10; +0,42] | +0,17 [+0,05; +0,28] |
| aliado USA / aliado China | pg | +0,13 [−0,01; +0,26] | +0,05 [−0,06; +0,17] |
| aliado USA / aliado China | control | −0,13 [−0,32; +0,06] | −0,03 [−0,17; +0,11] |

- En disempowerment y power grabbing los modelos US quedan del lado positivo en las dos díadas (rechazan más cuando el
  usuario es del lado USA), con intervalos que excluyen o rozan el cero; los modelos CN quedan cerca de cero salvo en
  disempowerment entre aliados (+0,17).
- En self-empowerment, USA / China, los modelos US quedan del lado negativo (−0,28), pero con pocos prompts discordantes.
- En el control todos los intervalos incluyen el cero.
- Los modelos individuales se dispersan mucho, sobre todo los US.

Interpretación pendiente de Nico.

### Decisiones abiertas (del equipo)

- ¿Los cuatro modos, o menos (por ejemplo solo pg y control)?
- ¿Se dejan los puntos por modelo, o solo las barras con su intervalo?
- ¿El signo queda así (arriba = a favor del lado China) o se invierte (arriba = a favor del lado USA)?
- La referencia neutral A / neutral B no está en este gráfico; el cuaderno pide comparar todo contra los neutros.
- Estadística: a acordar después de aprobar el gráfico.

### Cambios pedidos por Nico

Reacción de Nico (17/09), textual: "esa figura no me parece mal, pero quizás esto de promediar todos los modelos entre
sí está diluyendo un efecto que existe. Además, no sé cómo calculás barras de error, pero son bastante grandes y me suena
a que es porque tomás un n=12 para cada barra, eso es injusto, con la cantidad de datos que tenemos... podríamos tener
muchísima más potencia. Me pregunto también eso para las barras de error de gráficos anteriores (e.g. figura 2), no
estamos sobreestimando muchísimo las barras de error? Se me ocurre probar: 1) qué pasa si medimos el sesgo dentro de
cada modelo, lo comparamos contra un shuffle de lados, y vemos si da consistente eso? o sea si, más allá de la
direccionalidad del sesgo, nos da que los modelos sí tienen más sesgo que el azar en general? 2) revisar barras de error
y quizás proponer una manera de visualizar/testear mejor estas diferencias" → panel 3 y la revisión de intervalos.

---

## Panel 3 (pedido de Nico) · ¿Más sesgo de dirección que el azar, sin importar para qué lado? (bloque 43)

**Estado: computado a pedido de Nico (2026-09-17), pendiente de su revisión.** `analysis_43_fig3_bias_vs_shuffle.py` →
`43_fig3_bias_vs_shuffle/`.

### Pregunta que plantea

Si el promedio entre modelos diluye el efecto porque los modelos tiran para lados distintos: ¿el tamaño del sesgo de
cada modelo, sin mirar el signo, es mayor que el que daría el azar? Es la misma lógica del panel B de la Figura 2.

### Gráficos

- `pA_abs_bias_vs_shuffle.png`: media de |sesgo| de los 24 modelos (barra de color) contra lados barajados (gris: mediana
  e intervalo 95 % del nulo), por modo, en USA / China, aliado de USA / aliado de China y neutral A / neutral B. La díada
  neutral la agregué yo como referencia sin polo (es el control que pide el cuaderno); Nico decide si queda.
- `pB_per_model_bias_<modo>.png`: cada modelo con su sesgo y la banda nula exacta del 95 % para su cantidad de prompts
  discordantes; punto lleno = p exacto < 0,05; izquierda = a favor del lado USA, derecha = a favor del lado China.

### Cómo se calculó

Sesgo por modelo = (a − b) / (a + b) entre prompts discordantes (a = rechaza solo con A usuario, b = solo con B usuario;
A = lado USA). Shuffle de lados: en cada (modelo, prompt) se intercambian al azar los dos veredictos, independiente por
prompt y modelo (igual que el shuffle de idiomas de la Figura 2); eso equivale a a ~ Binomial(a + b, 1/2), así que el
nulo por modelo es exacto (test binomial bilateral = McNemar exacto; BH entre los 24) y el de la media de |sesgo| sale de
20.000 sorteos; p = P(nulo ≥ observado). Tablas: `abs_bias_vs_shuffle.csv`, `per_model_bias_test.csv`.

### Qué dicen los datos

Media de |sesgo| de los 24 modelos, observado contra shuffle [intervalo 95 % del nulo]:

| díada | modo | observado | shuffle | p | modelos con p < 0,05 (→ lado China / → lado USA) | signo: + / − |
|---|---|---|---|---|---|---|
| USA / China | he | 0,33 | 0,27 [0,18; 0,37] | 0,12 | 2 (0 / 2) | 8 / 13 |
| USA / China | de | 0,34 | 0,17 [0,12; 0,23] | < 0,001 | 6 (4 / 2) | 15 / 7 |
| USA / China | pg | 0,29 | 0,17 [0,12; 0,22] | < 0,001 | 5 (2 / 3) | 17 / 6 |
| USA / China | control | 0,22 | 0,20 [0,13; 0,27] | 0,26 | 3 (2 / 1) | 9 / 13 |
| aliados | he | 0,25 | 0,25 [0,17; 0,34] | 0,50 | 2 (0 / 2) | 10 / 13 |
| aliados | de | 0,26 | 0,17 [0,12; 0,23] | 0,003 | 5 (5 / 0) | 18 / 3 |
| aliados | pg | 0,24 | 0,17 [0,11; 0,22] | 0,004 | 4 (3 / 1) | 15 / 9 |
| aliados | control | 0,16 | 0,20 [0,14; 0,27] | 0,87 | 0 | 7 / 13 |
| neutral A / B | he | 0,23 | 0,29 [0,22; 0,38] | 0,96 | 0 | 7 / 12 |
| neutral A / B | de | 0,24 | 0,18 [0,13; 0,24] | 0,022 | 2 (1 / 1) | 11 / 10 |
| neutral A / B | pg | 0,17 | 0,18 [0,13; 0,24] | 0,65 | 1 | 10 / 13 |
| neutral A / B | control | 0,22 | 0,23 [0,16; 0,30] | 0,59 | 1 | 14 / 7 |

- En disempowerment y power grabbing, en las dos díadas geopolíticas, los modelos tienen más sesgo de dirección que el
  azar; en self-empowerment y en el control no. En la referencia neutral no hay exceso en pg, he ni control; en de hay un
  exceso marginal (p = 0,022).
- Modelos significativos por separado (p exacto < 0,05, sin corregir; por azar se esperan ≈ 1,2 de 24): USA / China de:
  sonnet-5, gpt-5.6-sol, gemma-4-31b, gpt-5.6-terra (→ lado China), gemini-3.1-flash-lite, nova-2-lite (→ lado USA);
  USA / China pg: ling-3.0-flash, gpt-5.6-sol (→ lado China), mimo-v2.5-pro, qwen3.8-27b, nova-2-lite (→ lado USA);
  aliados de: kimi-k2.6, seed-2-1-turbo, hy3, inkling, gpt-5.6-luna (los 5 → lado China); aliados pg: gpt-5.6-sol,
  gpt-5.6-terra, grok-4.3 (→ lado China), nova-2-lite (→ lado USA). Tras BH quedan: USA / China pg 3 (ling-3.0-flash,
  qwen3.8-27b, nova-2-lite), aliados de 1 (inkling), aliados pg 1 (gpt-5.6-sol), USA / China de 0–1 (nova-2-lite q = 0,050).
- En de y pg la mayoría de los modelos cae del lado positivo (más rechazo cuando el usuario es del lado USA: 15–18 de 24),
  con pocos modelos fuertes en contra (nova-2-lite en las dos díadas; mimo-v2.5-pro y qwen3.8-27b en USA / China pg). En
  he y control el reparto es al revés o parejo. Sin test de signos (no pedido).

Interpretación pendiente de Nico.

---

## Revisión de las barras de error (pedido de Nico, 17/09)

**Cómo se calculan hoy (Figuras 2 y 3):** bootstrap sobre PROMPTS con los modelos fijos (criterio del cuaderno, 14/09):
se remuestrean los 192 prompts de cada modo, cada prompt trae todas sus condiciones y sus 24 modelos, y la media entre
modelos se recalcula en cada réplica. **No es un n = 12**: la incertidumbre es la del muestreo de prompts, no la de
modelos. (Los GLMM sí tratan a los modelos como aleatorios: ahí origen es 12 contra 12, y el efecto medio de un factor
intra-modelo se mide contra la heterogeneidad entre modelos.)

**Figura 3, por qué igual son anchas:** el sesgo usa solo los prompts discordantes, que son pocos: 25–35 de 192 por
modelo en pg y de, 6–15 en he; por origen son 240–390 eventos. Con todos independientes el error estándar sería
1/√n ≈ 0,05–0,065, o sea ± 0,10–0,13: es lo que hay. Diagnóstico (`interval_width_diagnostic.csv`, semiancho del IC 95 %):

| díada · modo · origen | media de cocientes por modelo (bloque 27) | conteos sumados entre modelos |
|---|---|---|
| USA / China · pg · US | +0,16 ± 0,15 | +0,17 ± 0,13 |
| USA / China · pg · CN | +0,02 ± 0,11 | +0,05 ± 0,11 |
| USA / China · de · US | +0,19 ± 0,12 | +0,12 ± 0,14 |
| aliados · pg · US | +0,13 ± 0,14 | +0,09 ± 0,11 |
| aliados · de · US | +0,27 ± 0,16 | +0,21 ± 0,16 |
| aliados · he · US | +0,11 ± 0,24 | −0,09 ± 0,18 |

Sumar conteos (cada discordancia pesa igual, en vez de cada modelo) cambia poco el intervalo (entre 25 % más angosto
y 15 % más ancho) y cambia el estimando; además muestra que la media de cocientes es frágil cuando hay modelos con 2–8 discordancias (en aliados · he ·
US cambia el signo). No hay "muchísima más potencia" escondida en el estimador: la potencia sale de juntar más eventos.

**Figura 2, panel A: ahí sí las barras exageran lo que importa.** Las barras son el IC del NIVEL de cada idioma
(± 3,7 pp en pg), dominado por la diferencia entre prompts (unos se rechazan casi siempre, otros nunca). Pero los idiomas
comparten prompts: el IC de la DIFERENCIA pareada contra inglés es la mitad (± 1,7 pp en pg, ± 1,6 en de, ± 0,8 en he;
bloque 26, `delta_vs_english_pooled.csv`, media de 24 modelos). Con ese intervalo, en pg Hindi +3,3 pp [±1,7] y francés
+2,2 [±1,5] excluyen el cero (swahili +3,0 [±2,2], pero ese número del bloque 26 incluye a los dos outliers); en de Hindi
+3,3 [±2,0]; en he Hindi +2,1 [±0,9]. El GLMM del bloque 36 (ómnibus pg p = 0,34) no contradice esto: contesta otra
pregunta, porque trata modelo × idioma como aleatorio (¿el efecto medio se distingue de la heterogeneidad entre
modelos?), mientras que el bootstrap con modelos fijos pregunta si el promedio de ESTOS 24 modelos cambia con el idioma.
Coincide con el panel D (pesado por uso: Hindi 1,27, francés 1,22). **A decidir por Nico: si esto cambia la lectura de
la Figura 2 ("en promedio no hay diferencia entre idiomas") y si el panel A lleva otro tipo de barra.**

**Propuestas para visualizar / testear mejor (sin hacer, a decidir):**
1. Por modelo contra su propio nulo (el bosque `pB`): no promedia nada y cada modelo tiene su test exacto.
2. Juntar eventos que miden el mismo eje: las dos díadas (USA / China + aliados) y/o de + pg; duplica o cuadruplica las
   discordancias y achica el intervalo ≈ 30–50 %.
3. Conteos sumados por origen en vez de media de cocientes (menos frágil; pesa más a los modelos con más discordancias).
4. GLMM del protocolo: refuse ~ dirección × origen + (1 | prompt) + (1 + dirección || modelo), por díada y modo: da el
   efecto de dirección como OR por origen y la interacción; pero el contraste US vs CN es 12 contra 12 y no hay forma de
   darle más potencia.
5. Figura 2, panel A: barras de error intra-prompt (del desvío de cada idioma respecto de la media del mismo prompt) o
   marcar sobre cada barra la diferencia pareada contra inglés con su intervalo.

### Cambios pedidos por Nico

(pendiente)
