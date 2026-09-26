# Bloque 98 — test de permutación para el panel D de idiomas (Figura 4D, 22 modelos)

*pedido de Nico, 25/09, por la objeción del revisor al bootstrap de un rango · script: `4_analysis/analysis_98_language_range_permutation.py` (≈ 4 min, sin API)*

**Método.** Estadístico idéntico a `review_fig_languages_22models/step3_panelD_bootstrap.py`: por modelo, rango entre los 8 idiomas del logit
suavizado de R menos su azar (media de 2.000 barajados de idiomas dentro del prompt, misma semilla); media pesada sobre modelos; OR = exp.
H0: dentro de cada prompt los idiomas son intercambiables, en cada modelo. Nulo: un **segundo juego independiente** de K = 10.000 barajados
por modelo (mismas funciones `shuffled`/`range_logodds`, barajado independiente por modelo como en el código existente, semilla SEED + 100·k + 50);
cada barajado es un pseudo-dato cuyo exceso es rango_k − **el mismo azar del observado**, y se promedia con los mismos pesos. p = (1 + #{nulo ≥ observado}) / (1 + K),
una cola. Se eligió el juego independiente y no la media leave-one-out porque así el observado y los K pseudo-datos son intercambiables bajo H0
y el p es exacto (equivale al test de permutación de Σ w·rango); el leave-one-out rompe esa simetría. BH dentro de cada ponderación (familia = 4 tipos).
El IC bootstrap sobre prompts (B = 2.000) queda solo como **descriptivo**.

**Ponderaciones.** eq = 1/22 · use = requests de OpenRouter renormalizados sobre los 22 (n efectivo 1/Σw² = **5,13**; gpt-5.6-luna pesa 40,6 %)
· use_noluna = lo mismo sin gpt-5.6-luna, renormalizado sobre 21 (n efectivo **11,88**).

| tipo | ponderación | OR observado | IC 95 % bootstrap (descriptivo) | p permutación | q BH permutación | q BH bootstrap |
|---|---|---|---|---|---|---|
| SE | igual | 1,48 | [1,20; 1,76] | 0,0001 | 0,0001 *** | 0,0010 *** |
| DE | igual | 1,99 | [1,61; 2,11] | 0,0001 | 0,0001 *** | 0,0010 *** |
| PG | igual | 1,70 | [1,46; 1,80] | 0,0001 | 0,0001 *** | 0,0010 *** |
| CT | igual | 1,65 | [1,38; 1,73] | 0,0001 | 0,0001 *** | 0,0010 *** |
| SE | uso | 1,12 | [0,82; 1,50] | 0,286 | 0,286 n.s. | 0,225 n.s. |
| DE | uso | 2,13 | [1,51; 2,72] | 0,0001 | 0,00013 *** | 0,0013 ** |
| PG | uso | 1,39 | [1,15; 1,55] | 0,0001 | 0,00013 *** | 0,0013 ** |
| CT | uso | 1,60 | [1,26; 1,80] | 0,0001 | 0,00013 *** | 0,0013 ** |
| SE | uso sin luna | 1,41 | [1,10; 1,57] (nuevo) | 0,0002 | 0,0002 *** | 0,014 * |
| DE | uso sin luna | 1,73 | [1,36; 1,94] (nuevo) | 0,0001 | 0,00013 *** | 0,0013 ** |
| PG | uso sin luna | 1,47 | [1,22; 1,74] (nuevo) | 0,0001 | 0,00013 *** | 0,0013 ** |
| CT | uso sin luna | 1,61 | [1,30; 1,80] (nuevo) | 0,0001 | 0,00013 *** | 0,0013 ** |

p = 0,0001 es el mínimo posible con K = 10.000 (1/10.001: ningún pseudo-dato llegó al observado). El p del bootstrap por inversión del IC tiene
mínimo 2/2.001 ≈ 0,001, así que el paso de ** a *** en uso es resolución del test, no un cambio de conclusión. Ninguna significancia cambia con
respecto al bootstrap actual: SE con peso por uso sigue sin evidencia (p 0,29) y todo lo demás es significativo con los dos métodos. Sin gpt-5.6-luna,
SE con peso por uso pasa a ser significativo (OR 1,41; permutación q 0,0002; bootstrap q 0,014).

**Verificaciones** (`provenance.json`): el exceso observado reproduce `panelD_bootstrap.csv` (diferencia máx. 6e-17 log-odds); el bootstrap se
volvió a correr con las mismas semillas y las tres ponderaciones a la vez, y las réplicas de eq y use coinciden con `panelD_bootstrap_draws.npz`
(diferencia máx. 7e-16), con los mismos IC y q; la columna use_noluna sale de esas mismas réplicas. La media del nulo da OR ≈ 1,00 en las 12 filas.

**Decisión a revisar:** barajado independiente por modelo (heredado de step3). La alternativa sería una misma permutación de idiomas por prompt
para todos los modelos, que conserva la correlación entre modelos dentro de cada celda prompt × idioma y daría un nulo más ancho con peso por uso.

Archivos: `range_permutation.csv` (una fila por tipo × ponderación: OR, IC, p y q de permutación y de bootstrap, `q_boot_bh_current` = q actual
de panelD, percentil 95 y máximo del nulo, n efectivo), `provenance.json` (digests de datos y código, pesos, semillas, verificaciones).
