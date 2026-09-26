# Bloque 99: resultados pesados por uso, sin gpt-5.6-luna

**Pedido (25/09).** Un revisor sostiene que los resultados pesados por uso reflejan sobre todo a un modelo:
gpt-5.6-luna tiene el 40,0 % de los pedidos del panel y el número efectivo de modelos es 5,3. Se volvió a correr
**cada resultado pesado por uso que aparece en el paper** sin luna: los mismos pesos por pedidos con el de luna en 0,
renormalizados sobre los otros 23 modelos, con los mismos datos, B, semillas y familias de BH que los originales.

Script: `4_analysis/analysis_99_usage_weighted_without_luna.py` (sin API; unos 3 min). No toca ningún archivo existente.

## Cómo se hizo

- **Mismo código.** Se importan de los scripts originales los estimadores, la permutación y BH
  (`analysis_72_*`, `analysis_73_*`, `analysis_74_*`, `analysis_93_*`). El lazo principal de cada uno está copiado sin
  cambios en el bloque 99. Lo único que cambia es el juego de pesos, que pasa de {pedidos, tokens} a {con luna, sin luna}.
  En el 93 se copió `side_usage_interactions()` con el vector de pesos como argumento, porque la función original
  lee los pesos de la tabla de uso.
- **Sin luna = peso 0.** Los cuatro estimadores renormalizan los pesos sobre los modelos que entran, así que poner en 0
  el peso de luna da el mismo resultado que sacarlo. Hacerlo así deja idénticos los cubos de datos y las secuencias
  aleatorias. El bootstrap y la permutación sortean **los mismos índices** con luna y sin luna, de modo que la única
  diferencia es el peso de luna.
- **Control de reproducción.** Los números con luna coinciden con las tablas guardadas de los bloques 72, 73, 74 y 93
  hasta la precisión de máquina: diferencia máxima 4·10⁻¹⁵, con IC, p y q idénticos (`sanity_reproduction.csv`).
- **No se re-corrió** el rango entre idiomas pesado por uso (Figura 4D, columna "Usage-weighted" de `est_fig4` y sus filas
  "Language range ... usage weights" de `checks_interactions`), porque de eso se encarga otro agente (bloque 98).
- **`conclusion_changes`** usa un criterio mecánico, no una lectura. Vale "yes" si q cruza 0,05 (es decir, si el paper
  gana o pierde la estrella) o si, siendo significativo con y sin luna, el OR cambia de lado de 1. En cualquier otro caso
  vale "no". La nota trae el OR y la q de los dos lados. La lectura de estos resultados le corresponde al equipo.

## Número efectivo de modelos (1 / Σw²)

| pesos | todos | bloque US | bloque CN | mayor peso | 3 mayores |
|---|---:|---:|---:|---|---:|
| con luna (paper) | 5,3 (24) | 3,0 (12) | 6,5 (12) | luna 40,0 % | 57 % |
| sin luna | 12,4 (23) | 6,1 (11) | 6,5 (12) | gemini-3.1-flash-lite 15,1 % | 39 % |

## Afirmaciones del paper, con y sin luna

OR de un pedido típico pesado por uso, IC 95 % bootstrap sobre prompts. La q es la del mismo bootstrap (la que usa el paper).

| afirmación (dónde) | con luna | sin luna | ¿cambia? |
|---|---|---|---|
| **Fig. 2D** geo, DE, lado USA / lado China (results.tex) | 1,19 [1,07; 1,32], q = 0,003 | 1,11 [1,04; 1,19], q = 0,003 | no |
| Fig. 2D geo, PG (results.tex) | 1,11 [1,04; 1,21], q = 0,007 | 1,10 [1,04; 1,16], q = 0,003 | no |
| Fig. 2D geo, control (results.tex) | 1,01 [0,92; 1,12], q = 0,76 | 0,98 [0,93; 1,03], q = 0,66 | no |
| Fig. 2D geo, SE / PS agrupado (est_fig2) | 0,93, q = 0,43 / 1,11, q < 0,001 | 0,99, q = 0,92 / 1,08, q < 0,001 | no |
| Fig. 2D neutral, los 5 grupos (est_fig2) | todos q ≥ 0,29 | todos q ≥ 0,47 | no |
| **Fig. A2 C** aliados, DE (appendix.tex) | 1,26 [1,10; 1,45], q = 0,003 | 1,15 [1,05; 1,27], q = 0,006 | no |
| Fig. A2 C USA–China, PG | 1,13 [1,01; 1,26], q = 0,12 | 1,11 [1,03; 1,19], q = 0,021 | **sí: gana la estrella** |
| Fig. A2 C, resto de las celdas (USA–China SE/DE/CT, aliados SE/PG/CT, neutral) | sin estrella | sin estrella (aliados PG q = 0,054) | no |
| **Tabla checks_interactions**, lado × (DE vs control) | 1,17 [1,02; 1,34], q = 0,088 | 1,13 [1,04; 1,24], q = 0,010 | **sí: pasa a significativo** |
| checks_interactions, lado × (PG vs control) | 1,10 [0,97; 1,25], q = 0,20 | 1,12 [1,04; 1,21], q = 0,005 | **sí: pasa a significativo** |
| checks_interactions, lado × (PS vs control) | 1,09 [0,97; 1,22], q = 0,13 | 1,10 [1,03; 1,18], q = 0,003 | **sí: pasa a significativo** |
| checks_interactions, lado × (SE vs control) | 0,91, q = 0,32 | 1,01, q = 0,90 | no |
| **Fig. A3 B** IA vs humano, SE (appendix.tex) | 1,43 [1,07; 2,04], q = 0,012 | 1,61 [1,27; 2,17], q < 0,001 | no |
| Fig. A3 B IA vs humano, DE | 1,67 [1,45; 1,96], q < 0,001 | 1,49 [1,31; 1,69], q < 0,001 | no |
| Fig. A3 B IA vs humano, PG | 1,50 [1,30; 1,74], q < 0,001 | 1,42 [1,26; 1,61], q < 0,001 | no |
| Fig. A3 B IA vs humano, control | 1,21 [1,04; 1,44], q = 0,012 | 1,17 [1,06; 1,29], q = 0,002 | no |
| Fig. A3 B IA vs humano, PS agrupado | 1,51 [1,38; 1,67], q < 0,001 | 1,44 [1,33; 1,55], q < 0,001 | no |
| **Idiomas**, PG hindi vs inglés (results.tex, intro, discussion; abstract hasta el 25/09) | 1,31 [1,12; 1,54], q = 0,007 | 1,06 [0,96; 1,18], q = 0,32 | **sí: pierde la estrella** |
| Idiomas, PG francés vs inglés (ídem) | 1,29 [1,14; 1,48], q < 0,001 | 1,10 [1,01; 1,21], q = 0,028 | no (el OR baja de 1,29 a 1,10) |
| Idiomas, DE hindi (appendix.tex, Fig. A4 B) | 1,65 [1,37; 1,99], q < 0,001 | 1,05 [0,90; 1,23], q = 0,56 | **sí: pierde la estrella** |
| Idiomas, PS agrupado hindi (ídem) | 1,40 [1,25; 1,57], q < 0,001 | 1,08 [1,00; 1,17], q = 0,064 | **sí: pierde la estrella** |
| Idiomas, PS agrupado francés (ídem) | 1,16 [1,06; 1,28], q = 0,014 | 1,06 [0,99; 1,13], q = 0,11 | **sí: pierde la estrella** |
| Idiomas, "ningún idioma difiere del inglés en SE ni en el control" (appendix.tex) | cierto: ninguna q < 0,05 | SE: hindi 1,42, q = 0,014; control: 6 de 7 idiomas por debajo del inglés, q ≤ 0,035 (todos menos hindi) | **sí** |

Figura A4 B completa: sin luna, 21 de las 35 celdas cambian de significación. Cuatro la pierden (hindi en DE y en PG;
hindi y francés en PS agrupado) y 17 la ganan. De las 17 que la ganan, 16 tienen OR < 1, es decir, son idiomas que se
rechazan **menos** que el inglés: alemán, portugués y español en DE; alemán, español y swahili en PG; seis de los siete
idiomas (todos menos el hindi) en el control; y alemán, portugués, español y swahili en PS agrupado. La restante es hindi en SE
(OR 1,42). La única celda significativa con y sin luna es francés en PG. Detalle en
`compare_72_language_vs_english.csv`.

## Qué se sostiene y qué cambia

**Se sostiene.**
- **Nacionalidad (Fig. 2D y texto de results.tex).** Sin luna, el sesgo contra el usuario del lado USA sigue siendo
  significativo en DE (1,11, q = 0,003), en PG (1,10, q = 0,003) y en PS agrupado, y sigue sin detectarse en el control
  (q = 0,66) ni en el conjunto neutral. En DE el OR baja de 1,19 a 1,11, pero en PG casi no se mueve.
- **Aliados en DE (Fig. A2).** Se sostiene: baja de 1,26 a 1,15, con q = 0,006.
- **Agente de IA (Fig. A3 B).** Los cinco OR siguen significativos, con valores entre 1,17 y 1,61. Sin embargo, la frase
  de appendix.tex "the ordering of the equal-weight panel holds with these weights, with the largest bias in DE and PG
  and the smallest in the control" se sostiene solo a medias: sin luna el mayor OR es el de SE (1,61), seguido por DE
  (1,49) y PG (1,42). El control sigue siendo el menor (1,17). Esto no es un cambio de significación, pero sí del orden
  que afirma el texto.
- **Número efectivo.** Pasa de 5,3 a 12,4 modelos, y de 3,0 a 6,1 dentro del bloque US. El bloque CN no cambia (6,5).

**Cambia.**
- **Idiomas.** La afirmación de la introducción, results.tex y la discusión ("weighted by real-world usage,
  power-grabbing requests in Hindi and French are refused more often than in English"; el abstract la tenía al
  empezar este bloque y la versión editada el 25/09 ya no la incluye) depende de luna en la parte del hindi. Sin luna, el
  hindi en PG queda en OR 1,06 (q = 0,32). El francés en PG sigue significativo, pero con OR 1,10 (q = 0,028) en vez de
  1,29. También dependen de luna las frases del apéndice sobre hindi en DE (1,65), hindi en PS agrupado (1,40) y francés
  en PS agrupado (1,16): las tres pierden la significación. Como dato de contexto, sin análisis nuevo: en `est_fig4_models`
  luna rechaza 7,6 % en inglés y 15,3 % en hindi en power shifting. Además, sin luna aparecen contrastes que el paper no
  tiene: el inglés se rechaza más que alemán, español y swahili en PG, más que seis de los siete idiomas en el
  control y más que alemán, portugués, español y swahili en PS agrupado, y el hindi se rechaza más que el inglés en SE. Con eso deja de ser cierta la frase "no language differs from English in SE or in the control".
- **Especificidad del lado (tabla checks_interactions y su frase en appendix.tex, "the usage-weighted side effects do not
  differ from the control after correction").** Sin luna, lado × (tipo vs control) pasa a ser significativo en DE
  (q = 0,010), en PG (q = 0,005) y en PS agrupado (q = 0,003). Con luna los intervalos eran más anchos: luna aumentaba la
  varianza del contraste pesado.
- **Fig. A2 C, USA–China en PG.** Pasa a significativo (1,11, q = 0,021). Hoy la celda no lleva estrella.

## Archivos

| archivo | contenido |
|---|---|
| `compare_72_language_vs_english.csv` | idioma vs inglés, 5 grupos × 7 idiomas (Fig. A4 B y textos) |
| `compare_73_nationality_side.csv` | lado USA vs lado China: geo y neutral (Fig. 2D) y díadas USA–China y aliados (Fig. A2 C). Las filas de PS agrupado por díada no están en el paper |
| `compare_74_ai_agent.csv` | IA vs humano, 24 modelos (Fig. A3 B), más la versión por origen del bloque 74 (US / CN, que no está en el paper) |
| `compare_93_side_vs_control.csv` | lado × (tipo vs control) pesado por uso (tabla checks_interactions) |
| `effective_n_models.csv` | n efectivo, mayor peso y suma de los 3 mayores, en total, US y CN, con y sin luna |
| `weights_with_and_without_luna.csv` | participación de cada modelo en los pedidos, con y sin luna |
| `sanity_reproduction.csv` | diferencia entre los números con luna y las tablas originales de los bloques 72, 73, 74 y 93 |
| `full_tables/` | tablas completas con las mismas columnas que los originales (tasas, IC, p y q del bootstrap y de la permutación) para los dos juegos de pesos |
| `provenance.json` | hashes del código y de la tabla de uso, B y semillas |

Columnas de las tablas `compare_*`: `analysis, contrast, estimate_with_luna, ci_with_luna, q_with_luna,
estimate_without_luna, ci_without_luna, q_without_luna, conclusion_changes`, más `in_paper` (dónde aparece), `n_models_*`,
`perm_q_*` (la q de permutación que los bloques originales guardan como referencia; no es la del paper) y las claves.
