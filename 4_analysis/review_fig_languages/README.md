# review_fig_languages — figura de idiomas, versión de 24 modelos (APÉNDICE desde el 21/09)

- **Cuerpo del paper (decisión de Wendy, 2026-09-21): `../review_fig_languages_22models/figure_22models_ps_en.*`**, 22 modelos
  (sin nemotron-3.5-lightning ni nova-2-lite en ningún idioma; fallan en swahili). Ver el README de esa carpeta.
- **Apéndice: `figure_paper_v2_ps_en.*`** (este directorio), 24 modelos con esos dos excluidos solo de swahili (swahili*). La genera
  `figure_paper_v2.py`, que a su vez presta sus funciones de dibujo a la de 22 modelos.
- Cambios de dibujo del 21/09, en las dos: panel B sin conexión al control (puntos sueltos) y chino en rosa; panel F sin recuadro de
  barras, con el resultado del test como nota al pie (contraste mismo origen > mixto en negrita).
- Apéndice por modo: `figure_appendix_C_by_mode.png` (acuerdo entre modelos, tiles de `panelC/panelC_with_tests.py --redraw`,
  también sin recuadro desde el 21/09) y `figure_appendix_D_by_mode.png` (exceso por modelo, `panelD/F6_exceso_pg.py --mode <modo>`).
  Los dos sobre 24 modelos.
- Historia: `figure_full_ps.png` / `figure_paper_ps_{en,es}.*` (versiones anteriores al 20/09), `panelA/`, `panelB/`, `panelC/`,
  `panelD/` con los README de cada panel.
