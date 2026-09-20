# Figuras del cuerpo en versión de PÁGINA (20/09)

Pedido de Wendy (20/09): "que todas las figuras sean legibles en una página tipo paper". Las figuras aprobadas se
armaron a 17–22 in de ancho y al ancho de texto de ICLR 2027 (5,5 in) sus textos quedan en 2–3 pt. Cada script de
esta carpeta redibuja **los mismos paneles, con los mismos números** (lee solo las tablas guardadas por los bloques;
no corre ningún GLMM ni permutación) en 5,5 in de ancho, tipografía uniforme de 4,7–7,2 pt, letras de panel, notas
metodológicas en el caption. Salida por figura: `<stem>_{en,es}.pdf` (vectorial), `<stem>_{en,es}.png` (300 dpi) y
`<stem>_caption_{en,es}.md`. Estilo compartido en `_paperstyle.py` (copiado de la primera que se hizo así, la de idiomas).

| figura | versión de página (acá) | figura aprobada de la que sale | tablas que lee |
|---|---|---|---|
| 1 · D1 inglés | `figure1_paper.py` → `figure1_paper_{en,es}.*` (5,5 × 7,3 in) | `results/78_fig1_v3/figure1_full.png` | bloques 78, 70, 77 |
| 2 · países (D2) | `figure2_countries_paper.py` → `figure2_countries_paper_{en,es}.*` (5,5 × 7,4 in) | `review_fig_countries/figure_full_split.png` | bloques 55, 45, 73, 46 |
|   | 20/09 (tarde): panel C con IC y q del mismo bootstrap sobre prompts (`boot_q` del bloque 73, BH en los 4 modos) en vez de q de permutación; ninguna estrella cambia. Misma regla que el panel B de idiomas. **Versión final vigente.** | | |
| 3 · agente IA (D3 vs D1) | `figure3_aiagent_paper.py` → `figure3_aiagent_paper_{en,es}.*` (5,5 × 7,6 in) | `results/65_fig4_composite/figure4_full.png` | bloques 54, 56, 59, 60, 64, 76, 30 |
| 4 · idiomas | **no está acá**: desde el 20/09 (tarde) la vigente es `review_fig_languages/figure_paper_v2.py` → `figure_paper_v2_ps_en.*` (5,5 × 7,9 in, paneles A–F, BH en todos, solo inglés; Nico) | preview `review_fig_languages/figure_full_v2_ps.png` | bloques 36, 81 + paneles B (bootstrap único + BH), C, D de esa carpeta. La disposición anterior (`figure_paper.py` → `figure_paper_ps_{en,es}.*`, `figure_full_ps.png`) sigue actualizada pero ya no es la referencia |

Cambios de forma respecto de las figuras aprobadas (ningún cambio de contenido):
- Fig 1: tres filas (A | B | C; D | E; F | G) en vez de dos; el recuadro de B en seis líneas cortas; el p del ómnibus
  de F y G dentro del panel.
- Fig 2: A, B y C con títulos cortos y sus subpaneles geo | neutral con subtítulos "lado USA / China" y "neutral (ref.)";
  D en dos filas (USA arriba, China abajo) en vez de lado a lado.
- Fig 3: los Δ de A y C y las q de B rotados 90°; el título de E sin el paréntesis "el control no tiene dominio" (va en
  el caption); F en dos subpaneles apilados a la derecha de D y E, con el eje x "índice de capacidad (%)".

Ejecutar desde la raíz del repo:  `python 4_analysis/paper_figures/figure1_paper.py [--lang es|en|both]` (ídem las otras).
