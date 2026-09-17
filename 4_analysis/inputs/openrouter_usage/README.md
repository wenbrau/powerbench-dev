# Uso de los 24 modelos del panel en OpenRouter (foto del 2026-09-17)

`usage_30d_2026-08-18_2026-09-16.csv`: tokens procesados por OpenRouter para cada uno de los 24 modelos del panel
final en los 30 días UTC completos del 2026-08-18 al 2026-09-16 (el día 17, en curso, queda afuera).

- **Fuente:** OpenRouter (openrouter.ai/rankings), datos de actividad diaria por modelo, los mismos que alimentan el
  gráfico "Activity" de la página pública de cada modelo (`/api/frontend/v1/stats/model-activity?permaslug=…&variant=…`).
  Leídos el 2026-09-17T14:12:11Z con el navegador, sin clave de API. Los datos de rankings de OpenRouter se publican
  bajo CC BY 4.0. Cita: "Source: OpenRouter (openrouter.ai/rankings), as of 2026-09-17T14:12:11Z."
- **Qué es un token acá:** `total_prompt_tokens + total_completion_tokens`, contados con el tokenizador de cada
  proveedor (no son estrictamente comparables entre proveedores, advertencia de OpenRouter).
- **Variantes:** OpenRouter rankea por separado las variantes de un mismo modelo (`standard`, `free`, `batch`). Acá
  `tokens_30d` SUMA todas las variantes del mismo permaslug; las columnas `tokens_standard`, `tokens_free` y
  `tokens_batch` las separan (nemotron-3-ultra, nemotron-3.5-lightning e inkling son casi todo tráfico `free`).
- `n_days` = días con actividad dentro de la ventana (qwen3.8-flash salió el 2026-08-26: 22 días).
- `requests_30d` = cantidad de pedidos en la misma ventana.
- **Qué mide y qué no:** uso por API a través de un ruteador, cargado hacia programación y agentes; no incluye las apps
  propias de cada laboratorio ni su API directo; es uso global, no por idioma. Cambia cada semana: esta es una foto.

Pedido de Nico (2026-09-17) para pesar el sesgo por idioma de cada modelo por su uso (bloque 40).
