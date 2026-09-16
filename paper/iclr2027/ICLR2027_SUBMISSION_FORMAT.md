# ICLR 2027 — requisitos de formato y submission

Verificado el 16 de septiembre de 2026 contra las fuentes oficiales y contra el **paquete de estilo
descargado** (`iclr-2027-style-files.zip`, 7 archivos: `iclr2027_conference.{sty,bst,bib,tex}`,
`fancyhdr.sty`, `natbib.sty`, `math_commands.tex`).

Fuentes: [Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines) ·
[Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers) ·
[AI Policy for Authors](https://iclr.cc/Conferences/2027/AIPolicyForAuthors) ·
[style files](https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip) ·
[OpenReview ICLR 2027](https://openreview.net/group?id=ICLR.cc/2027/Conference)

## 1. Fechas (AoE = UTC−12)

| Hito | Fecha |
|---|---|
| **Abstract** (obligatorio, con título y lista de autores) | **18 sep 2026, 23:59 AoE** |
| **Paper completo** | **25 sep 2026, 23:59 AoE** — no se permiten ediciones después |
| Reviews publicadas | 5 nov 2026 |
| Discusión autor–reviewer | 5–18 nov 2026 |
| Decisiones finales | 16 dic 2026 |

El abstract se registra primero: **el título y la lista de autores quedan fijados el 18**.
Todos los autores necesitan perfil de OpenReview antes de esa fecha. Tope de 20 coautorías por
persona. Si un autor tiene 3+ submissions, hay obligación recíproca de revisar.

## 2. Límite de páginas

- **9 páginas** de texto principal en la submission inicial (límite estricto).
- Sube a **10 páginas** para rebuttal y camera-ready.
- **No cuentan**: referencias (ilimitadas), apéndices (ilimitados, después de la bibliografía),
  agradecimientos, y los tres statements de abajo.
- Los reviewers no están obligados a leer apéndices ni material suplementario. Todo lo que sostiene
  una afirmación central tiene que estar en las 9 páginas.

## 3. Statements al final del texto principal, antes de las referencias

| Statement | Estado | Tope |
|---|---|---|
| **AI use statement** | **OBLIGATORIO** | 1 página |
| Ethics statement | recomendado | 1 página |
| Reproducibility statement | recomendado | un párrafo |

Ninguno cuenta contra las 9 páginas. Para PowerBench los tres corresponden: el AI use statement es
obligatorio y además nuestro pipeline usa LLMs en construcción de prompts, traducción, judging y
código; el de ética aplica por ser un benchmark sobre asistencia a pedidos de poder; el de
reproducibilidad aplica porque liberamos banks y runs.

### AI use statement — qué exige la política

Hay que declararlo **en el paper y también en el formulario de submission**. Divide en dos niveles:

- **Disclosure requerida**: generar datasets sintéticos, ayudar a desarrollar modelos teóricos o
  marcos conceptuales, formular afirmaciones matemáticas, asistencia en demostraciones, refinamiento
  de hipótesis, diseño de metodología, implementación, limpieza de datos e **interpretación de
  resultados**.
- **Disclosure recomendada**: formular preguntas de encuestas/entrevistas, crear o modificar figuras
  científicas, sugerir parámetros experimentales, edición de código, análisis de literatura,
  brainstorming, edición y formato del paper.

Texto de la plantilla, tal cual viene en `iclr2027_conference.tex`:

> In this work, we used generative AI tools for [tasks with required disclosure]. We have not used
> generative AI tools for [other tasks with required disclosure], and [the rest of the required
> disclosure tasks] are not applicable to this work. Additionally, we used generative AI tools for
> [tasks with recommended disclosure]. We have reviewed all AI-assisted work. [Elaborate. For
> example, "we checked LLM-generated research ideas for potential plagiarism through a manual
> literature survey", "LLM-generated code was verified and tested for correctness by 2 authors",
> etc.]. We take responsibility for the final content of this work, including text, claims or
> artifacts produced with the aid of generative AI.

La política es explícita: *"Ultimately the paper's authors are responsible for the contents of their
submissions"*, y cualquier falsedad sustancial, plagio o tergiversación producida por un LLM viola
el Code of Ethics y puede causar desk rejection. **No se puede declarar revisión humana que no
ocurrió.**

## 4. Formato tipográfico exacto (medido en el `.sty`)

Nada de esto es opcional: *"Tweaking the style files may be grounds for rejection."*

```latex
\documentclass{article}
\usepackage{iclr2027_conference,times}
%\iclrfinalcopy   % COMENTADO en la submission; solo para camera-ready
```

| Parámetro | Valor |
|---|---|
| Caja de texto | 5.5 in (33 picas) de ancho × 9.0 in (54 picas) de alto |
| Margen izquierdo | 1.5 in (9 picas); todas las páginas empiezan a 1 in del borde superior |
| Papel | 8.5 × 11 in, una sola columna |
| Cuerpo | 10 pt con interlineado de 11 pt, **Times New Roman** |
| Párrafos | separados por 1/2 línea, **sin sangría** |
| Título | 17 pt, versalitas, alineado a la izquierda |
| Abstract | indentado 1/2 in a ambos lados, 10 pt/11 pt, la palabra ABSTRACT centrada en versalitas 12 pt, **un solo párrafo** |
| Heading nivel 1 | versalitas 12 pt, flush left |
| Headings niveles 2 y 3 | versalitas 10 pt, flush left |
| Citas | `natbib`: `\citet{}` dentro de la oración, `\citep{}` entre paréntesis |
| Referencias | orden alfabético por autor; el estilo interno da igual mientras sea consistente |
| Números de línea | los genera el `.sty` automáticamente para los reviewers; **no referirse a ellos en el texto** |

El `.sty` inserta solo un bloque **"Anonymous authors / Paper under double-blind review"** mientras
`\iclrfinalcopy` esté comentado. Hay que dejar el `\author{...}` real fuera del archivo o comentado.

## 5. Doble ciego

- *"Any paper where author identity is revealed in either the main text or the supplementary material
  will be desk rejected."*
- Consecuencia directa para nosotros: **todos los links a `4_analysis/results/...`, al repo y a
  cualquier cosa con el nombre del grupo tienen que salir del PDF y del suplementario.** El
  `WORKING_DRAFT.md` está lleno de links internos (`../../4_analysis/...`) que son evidencia para
  autores, no para la submission.
- Los trabajos propios relacionados se citan en tercera persona.
- El código/artefacto va como link anónimo (p. ej. anonymous.4open.science) o como archivo adjunto.

## 6. Preprints, dual submission, suplementario

- arXiv está permitido y **no** viola la política de dual submission; se puede subir durante el
  período de review.
- Sí está prohibido enviar algo idéntico o sustancialmente similar a lo publicado, aceptado o en
  revisión paralela en otra venue. Los workshops están exentos.
- Se recomienda **un solo archivo** (paper + suplementario). Se acepta y se alienta subir código.

## 7. Checklist de packaging para PowerBench

- [ ] Registrar abstract + autores en OpenReview antes del **18 sep 23:59 AoE**; perfiles creados.
- [ ] Migrar la prosa a la plantilla `iclr2027_conference.tex` sin tocar el `.sty`.
- [ ] Anonimizar: quitar nombres, agradecimientos, links internos del repo y rutas locales.
- [ ] Comprobar que el cuerpo entra en 9 páginas **con las cuatro figuras a tamaño de impresión**.
- [ ] AI use statement (obligatorio) redactado sobre el registro real del proyecto.
- [ ] Ethics + Reproducibility statements.
- [ ] Link anónimo al repo/banks + declaración del canario de `CANARY.md`.
- [ ] Apéndices A–H según el mapa de `PAPER_PLAN.md`.
