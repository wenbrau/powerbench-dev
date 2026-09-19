# Reasoning ladder (apéndice + un párrafo en el cuerpo) — registro panel por panel

Registro abierto el 18/09/2026, con la misma regla que las Figuras 1–4: cada gráfico que Nico ve, lo que pide, lo que decide
y cada número quedan acá. Las decisiones de análisis e interpretación son de Nico; lo que yo elija sin que él lo dicte va
a [DECISIONES_A_REVISAR.md](../DECISIONES_A_REVISAR.md).

---

## 0. Qué dice el cuaderno (texto de Nico, 14/09)

> 4 + 4 modelos (de China y USA en igual proporción) estudiados en dos niveles distintos de reasoning (+ reasoning off como
> nivel cero, que ya lo teníamos) en D1 inglés. Esto probablemente iría a apéndice y en el cuerpo le damos un párrafo como
> mucho.

> Otra decisión tomada: no correr el panel B de modelos (todos con reasoning). Era muy caro y no estaba justificado por
> nuestros objetivos. Estamos testeando un panel muy grande de modelos sin reasoning, evaluando sus capacidades, y además
> mostrando cómo cambian los sesgos cuando agregamos reasoning.

Nico (18/09): "más allá de eso, y de los apéndices que falta construir, faltaría también el análisis de reasoning, no?" →
"dale, vamos con panel a panel de reasoning".

(La pregunta 41 de la lista pegada del 1/09, "¿el razonamiento cambia el sesgo o solo el nivel?", es de un bloque de
Fable 5.1, no texto de Nico; se anota como contexto, no como pedido.)

---

## 1. Lo que hay: bloque 18 (`18_reasoning_ladder`, 12/09, preliminar)

**Diseño.** 8 modelos del estrato A, 4 US y 4 CN, corridos con reasoning ON en sus dos primeros niveles de esfuerzo
ofrecidos ("rung 1" y "rung 2"), sobre D1 inglés (576 prompts) y su control (192), contra el brazo OFF verificado que ya
teníamos (juez oficial en todo). Los niveles NO son comparables entre proveedores: low / medium para terra, grok, inkling,
gemini y qwen; low / high para deepseek y hy3; high / xhigh para glm-5.2 (no ofrece menos). Los tokens de razonamiento
entregados van de 84 (terra, low) a 3.427 (deepseek, high). glm-5.2 en xhigh perdió 26 / 576 filas de D1 y 9 / 192 del
control por agotar el presupuesto (excluidas). Filas ON con cero tokens de razonamiento: excluidas.

**Método del bloque 18.** Tasas por modelo × nivel × modo; bootstrap sobre prompts (B = 1.000, las tres ramas de un prompt
remuestreadas juntas → Δ vs OFF pareado por prompt); media de los 8 y por bloque. Figuras: `ladder_by_model.png` (un
panel por modelo, refusal por modo en OFF / rung 1 / rung 2, más el pooled Δ vs OFF) y `dpg_vs_tokens.png` (Δ pg vs
tokens de razonamiento). Tablas `levels.csv`, `pooled_delta_vs_off.csv`, `excess_by_rung.csv`.

**Niveles (refusal %, `levels.csv`):**

| modelo | origen | nivel (effort, tokens) | he | de | pg | control | Δ pg vs OFF | Δ control vs OFF |
|---|---|---|---|---|---|---|---|---|
| gpt-5.6-terra | US | OFF | 0,5 | 3,6 | 16,1 | 17,2 | | |
| | | low, 84 | 0,5 | 5,7 | 19,3 | 16,8 | +3,1 (p 0,2) | −0,4 |
| | | medium, 107 | 1,6 | 4,2 | 17,2 | 18,2 | +1,0 | +1,0 |
| grok-4.3 | US | OFF | 5,7 | 46,4 | 53,1 | 35,4 | | |
| | | low, 430 | 0,5 | 3,6 | 12,0 | 14,6 | **−41,1** | **−20,8** |
| | | medium, 766 | 0,5 | 2,1 | 12,0 | 13,0 | **−41,1** | **−22,4** |
| inkling | US | OFF | 2,6 | 14,1 | 24,5 | 21,9 | | |
| | | low, 239 | 5,7 | 22,9 | 36,5 | 25,5 | **+12,0** | +3,6 |
| | | medium, 708 | 2,1 | 16,1 | 24,5 | 22,4 | 0,0 | +0,5 |
| gemini-3.1-flash-lite | US | OFF | 0,0 | 0,5 | 2,6 | 2,1 | | |
| | | low, 125 | 0,0 | 1,0 | 2,6 | 4,2 | 0,0 | +2,1 |
| | | medium, 605 | 0,0 | 0,5 | 2,1 | 3,7 | −0,5 | +1,6 |
| deepseek-v4-pro | CN | OFF | 3,6 | 12,0 | 19,8 | 17,7 | | |
| | | low, 2.105 | 0,5 | 0,5 | 10,4 | 1,6 | **−9,4** | **−16,1** |
| | | high, 3.427 | 0,5 | 1,0 | 7,3 | 2,1 | **−12,5** | **−15,6** |
| hy3 | CN | OFF | 4,7 | 26,0 | 28,6 | 16,7 | | |
| | | low, 868 | 0,5 | 3,1 | 10,4 | 5,7 | **−18,2** | **−10,9** |
| | | high, 1.951 | 1,0 | 2,1 | 8,3 | 5,2 | **−20,3** | **−11,5** |
| qwen3.8-27b | CN | OFF | 3,6 | 16,7 | 28,6 | 28,6 | | |
| | | low, 625 | 8,3 | 11,5 | 30,7 | 21,4 | +2,1 | **−7,3** |
| | | medium, 846 | 2,6 | 8,9 | 24,0 | 9,9 | −4,7 | **−18,8** |
| glm-5.2 | CN | OFF | 3,1 | 24,5 | 34,9 | 25,0 | | |
| | | high, 251 | 2,1 | 2,1 | 9,4 | 14,1 | **−25,5** | **−10,9** |
| | | xhigh, 592 | 1,1 | 8,1 | 15,8 | 12,0 | **−19,0** | **−13,0** |

Negrita: p de bootstrap < 0,05 (sin corregir). Pooled de los 8, Δ vs OFF en pp: rung 1: he −0,7, de −11,7, pg −9,6,
control −7,6; rung 2: he −1,8, de −12,6, pg −12,2, control −9,8; en US los Δ son menores (pg −6,5 / −10,2; control −3,9 /
−4,8) que en CN (pg −12,8 / −14,1; control −11,3 / −14,7).

**Lo que se ve a ojo, para discutir:** con razonamiento la mayoría rechaza MENOS, en los modos de poder y también en el
control; los cuatro CN y grok bajan mucho; terra y gemini no se mueven (razonan poco: 84–605 tokens); inkling sube en
rung 1 y vuelve en rung 2. Es muy heterogéneo entre modelos, y el orden de los modos (pg > de > he) se conserva.

---

## 2. Mapa de paneles propuesto (Nico elige)

- P1 ¿cambia el refusal con el razonamiento, en cada modo y en el control? → por modo, x = OFF / rung 1 / rung 2, una
  línea por modelo coloreada por origen (bloque 67). Solo el gráfico.
- P2 ¿el cambio es específico de power-shifting o general? → Δ vs OFF por modo, media de los 8, con intervalo entre
  modelos (formato del 18/09), el control al lado.
- P3 ¿el razonamiento cambia el sesgo entre modos (pg − he, pg − de) o solo el nivel? → contraste de modos en OFF vs ON.
- P4 ¿depende de cuánto razona? → Δ vs tokens de razonamiento (ya existe en el bloque 18).
- Test, a acordar: GLMM refuse ~ nivel × modo + (1 + nivel || modelo) + (1 | prompt), con el prompt pareado entre ramas.

---

## Panel 1 (bloque 67) → rechazado; Panel A (bloque 68) + test

**Nico (18/09):** "creo que el panel A que me gustaría ver es tres curvas por modo (CN, USA y todos) para cada modo, sin las
curvas por modelo; y el test sí GLMM de refusal vs nivel, codificando toda la estructura posible para ganar potencia, y
quiero saber si depende de CN vs USA, y si depende del modo"

→ Bloque 67 (líneas por modelo) queda como registro. Bloque 68: panel A con tres curvas por modo (US, CN, todos; banda =
IC t entre modelos) y el GLMM único refuse ~ (r1 + r2) × (modo + origen) con contrastes suma-cero, (1 + r1 + r2 || modelo)
+ (1 | prompt) (`r/glmm_reasoning.R`). Resultados abajo.

**Bug encontrado y corregido (18/09) en el cargador del bloque 18:** los archivos `*_ladder_rung*_pinned_on.jsonl` se
comprimieron a `.jsonl.gz` después del 12/09 y el glob del loader (`*.jsonl`) no los veía: devolvía solo el brazo OFF
(6.144 filas) sin avisar, porque la aserción de cobertura no mira qué ramas hay. Corregido (`analysis_18_reasoning_ladder.py`,
glob `*.jsonl*` + `open_run`); los resultados del bloque 18 en disco son del 12/09, con los archivos planos, y siguen
valiendo. Ahora el loader devuelve 18.432 filas (8 × 3 × 768).

**Resultados del bloque 68** (`68_reasoning_glmm/reasoning_glmm.csv`; ajuste no singular, bobyqa, 41 s; SD entre modelos:
intercepto 1,68, pendiente de r1 1,47, de r2 1,31; SD de prompt 2,60). OR de refusal del nivel contra OFF:

| cantidad | nivel 1 (OR) | q BH | nivel 2 (OR) | q BH |
|---|---|---|---|---|
| promedio sobre modos y orígenes | 0,33 [0,12; 0,93] | 0,036 | 0,23 [0,09; 0,58] | 0,004 |
| modelos US | 0,67 [0,15; 2,93] | 0,59 | 0,44 [0,12; 1,67] | 0,31 |
| modelos CN | 0,16 [0,04; 0,70] | 0,029 | 0,11 [0,03; 0,42] | 0,005 |
| nivel × origen (razón US / CN) | 4,2 [0,5; 33] | p = 0,18 | 3,9 [0,6; 25] | p = 0,15 |
| en self-empowerment | 0,65 [0,20; 2,07] | 0,59 | 0,31 [0,10; 0,96] | 0,069 |
| en disempowerment | 0,16 [0,05; 0,47] | 0,004 | 0,14 [0,05; 0,38] | 0,001 |
| en power grabbing | 0,32 [0,11; 0,91] | 0,066 | 0,23 [0,09; 0,59] | 0,008 |
| en control | 0,35 [0,12; 1,02] | 0,075 | 0,25 [0,10; 0,66] | 0,014 |
| pg − control (razón de OR) | 0,90 [0,62; 1,32] | 0,59 | 0,90 [0,60; 1,33] | 0,59 |
| de − control | 0,45 [0,30; 0,69] | 0,001 | 0,56 [0,36; 0,86] | 0,020 |
| he − control | 1,85 [1,02; 3,36] | 0,069 | 1,23 [0,60; 2,51] | 0,59 |

Ómnibus de Wald: nivel (2 gl) χ² = 13,9, p = 0,001; nivel × origen (2 gl) χ² = 3,8, p = 0,15; nivel × modo (6 gl) χ² = 27,6,
p < 0,001.

Lectura provisoria (a confirmar por Nico): (1) con razonamiento el refusal baja, en promedio a un tercio de las chances en
el nivel 1 y a un cuarto en el nivel 2, con una heterogeneidad enorme entre modelos (SD de la pendiente ≈ 1,4 en log-OR:
grok baja 41 pp y terra no se mueve). (2) ¿Depende de US vs CN? La caída es significativa en los CN y no en los US, pero
la interacción no llega (p = 0,15) con 4 modelos por lado: no se puede afirmar que dependa del origen. (3) ¿Depende del
modo? Sí (p < 0,001): la caída es mayor en disempowerment que en el control (razón 0,45, q = 0,001); en power grabbing
es igual que en el control (0,90); en self-empowerment es menor, pero self-empowerment parte del piso. Es decir, el
razonamiento reduce el refusal de forma general, no específica de power-shifting, salvo el extra en disempowerment.
Decisión de Nico sobre el panel A y la lectura: pendiente.

**Nico (18/09):** "perfecto, este panel va! aunque lo arreglaría para que el eje y sea igual en todos; y el análisis es
este, conclusión: a mayor razonamiento, menor tasa de refusal, y eso parece ser así sea en control o en powershifting,
aunque disempowerment baja incluso más (llamativo). No depende de dónde viene el modelo, al menos en nuestros datos.
quizás podemos mostrar el sesgo de razonamiento, entre nivel máximo y nivel off, mismas prompts pareadas, vemos cuando
cambia el juicio, así construimos siempre el sesgo, no? pooleamos todos los 8 modelos, ya no separamos por US / CN, y
podemos ver cómo cambia ese sesgo (a rechazar menos cuando razonan) según factores como escala, standing, contexto o
dominio?"

→ **Panel A APROBADO** (bloque 68, con el eje y compartido entre modos; bandas se mantienen). **Test = el GLMM del bloque
68.** Conclusión aprobada (sus palabras): a mayor razonamiento, menor tasa de refusal, en el control y en power-shifting;
disempowerment baja incluso más; no depende del origen del modelo en nuestros datos. Siguiente: el sesgo de razonamiento
= la métrica de dirección de los desacuerdos (nivel 2 vs OFF, mismos prompts, por modelo), los 8 modelos juntos, por modo
y por escala, standing, contexto y dominio (bloque 69).

**Panel A regenerado con el eje y común** (`68_reasoning_glmm/pA_reasoning_by_mode_groups.png`, 0–60 %).

## Sesgo de razonamiento (bloque 69): nivel 2 vs OFF, dirección de los desacuerdos, 8 modelos juntos

`analysis_69_reasoning_bias.py` → `69_reasoning_bias/`: sesgo = (solo con razonamiento − solo sin) / discordantes por modelo
(convención del proyecto: positivo = más refusal con el tratamiento; acá negativo = rechaza menos al razonar); media de los
modelos con discordantes, IC 95 % t, q = BH (4 modos; las celdas de cada dimensión). Guard: una celda se testea solo con
≥ 4 modelos y SD > 0 (DECISIONES_A_REVISAR.md, punto 29). 6.115 pares OFF / nivel 2 válidos.

| modo | sesgo medio | IC 95 % t | q BH | modelos con sesgo < 0 | prompts que cambian de veredicto |
|---|---|---|---|---|---|
| he | −0,42 | [−1,09; +0,24] | 0,17 | 6 / 7 | 3 % |
| de | −0,56 | [−1,04; −0,09] | 0,055 | 5 / 7 | 17 % |
| pg | −0,52 | [−0,89; −0,14] | 0,055 | 6 / 8 | 18 % |
| control | −0,41 | [−0,88; +0,07] | 0,11 | 5 / 8 | 17 % |

Lectura: cuando el veredicto cambia entre OFF y el nivel 2, alrededor de tres de cada cuatro cambios van hacia rechazar
menos, en los cuatro modos; pero con 8 modelos y SD entre modelos de 0,45–0,72 (terra e inkling van al revés), ningún
modo pasa el q < 0,05 (de y pg quedan en 0,055). El GLMM del bloque 68, que usa todas las filas y las tres ramas, es el
que da la significación; este panel muestra la consistencia del cambio, no su tamaño.

Por factor (`bias_by_{scale,standing,context,domain}.csv`, figuras `p2_scale`, `p2_standing`, `p3_context`, `p3_domain`):
todas las celdas testeables son negativas o cerca de cero; con 8 modelos y una mediana de 3 discordantes por modelo en
las celdas de contexto y dominio (9–10 en escala y standing), la potencia es mínima. Celdas con q < 0,05: escala: he
individual −0,92, de group −0,65 y society −0,63, pg society −0,54, control group −0,63; standing: de low −0,63, pg low
−0,62; contexto: pg Academia −0,77, Fiction −0,86, Interpersonal −0,76, control Markets −0,67, Media −0,82; dominio: de
Legal −0,89, Wealth −0,79, he Legal −0,81, pg Epistemic −0,57, Physical −0,79, Wealth −0,76. No hay un patrón que
distinga power-shifting del control ni una dimensión que ordene el efecto; se ve "menos refusal al razonar, en todos
lados, con ruido". Decisión de Nico: pendiente (qué va al apéndice: mi lectura es panel A + GLMM + el sesgo por modo; los
heatmaps por factor no tienen potencia para decir nada más que eso).

---

## Reasoning ladder CERRADO (18/09)

**Nico (18/09):** "creo que el apéndice es solo el panel A, nada más vale la pena porque no tenemos potencia. Queda así"

→ **Apéndice = solo el panel A** (`68_reasoning_glmm/pA_reasoning_by_mode_groups.png`), con el GLMM del bloque 68 como
test y su conclusión aprobada: a mayor razonamiento, menor tasa de refusal, en el control y en power-shifting;
disempowerment baja incluso más; no depende del origen del modelo en nuestros datos (interacción p = 0,15 con 4 + 4).
El sesgo de razonamiento por modo y por factor (bloque 69) y las líneas por modelo (bloque 67) quedan como registro, no
van al paper: sin potencia con 8 modelos.

## Estado al 18/09

Cerrado. Un párrafo en el cuerpo (a redactar por Nico) + el panel A en el apéndice. Salvedades para métodos: niveles no
comparables entre proveedores; tokens de razonamiento de 84 a 3.400; glm-5.2 en xhigh con 35 filas excluidas por
presupuesto; loader del bloque 18 corregido el 18/09 (archivos .gz).
