#!/usr/bin/env Rscript
# glmm_main_panel.R -- version GLMM del PANEL PRINCIPAL de Figura 4 (D3 agente-IA vs D1 humano).
# Por cada celda (modo x bloque US/CN) ajusta una logistica mixta
#     refuse ~ ai + (1 + ai || model) + (1 | prompt_id)
# y reporta el coeficiente 'ai' (= log-OR de refutar al agente IA vs al humano) con IC de Wald.
# Es el gemelo por efectos aleatorios de fig4_panel_main_logodds (que usa el MISMO log-OR pero con
# errores cluster-robust two-way prompt x modelo en vez de efectos aleatorios). Sirve solo para ver
# si el resultado del panel cambia al pasar de cluster-robust a GLMM (robustez).
#
# Usa el harness compartido 4_analysis/r/glmm_common.R (bloques 30-33, glmm_ai_bias.R): lme4::glmer,
# nAGQ = 0, variante sin correlaciones (||) primero y (1|model) como respaldo, bobyqa/nlminbwrap,
# Wald, singular aceptado como convergido.
#
# Uso:  Rscript glmm_main_panel.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), ai (0/1), mode3 (he/de/pg/ctl), org (US/CN), prompt_id, model.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_main_panel.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "..", "..", "..", "r", "glmm_common.R"))

d <- read_input(args[1])
d$ai <- as.integer(d$ai)

permode_formulas <- list(
  as.formula("refuse ~ ai + (1 + ai || model) + (1 | prompt_id)"),
  as.formula("refuse ~ ai + (1 | model) + (1 | prompt_id)")
)

fits <- list()
for (m in c("he", "de", "pg", "ctl")) {
  for (org in c("US", "CN")) {
    key <- paste0(m, "_", org)
    dd <- droplevels(d[d$mode3 == m & d$org == org, ])
    fits[[key]] <- one(key, dd, permode_formulas, "ai", slope = "ai")
  }
}
finish(fits, args[2])
