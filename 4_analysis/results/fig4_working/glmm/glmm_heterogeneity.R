#!/usr/bin/env Rscript
# glmm_heterogeneity.R -- version GLMM de la heterogeneidad de Figura 4, en DiD (parte especifica de
# poder). Por cada NIVEL de una dimension (columna `lev`) ajusta la logistica mixta
#     refuse ~ ai * ps + (1 + ai + ai:ps || model) + (1 | prompt_id)
# sobre las filas de ESE nivel (modo con ps=1 + control con ps=0, ya armadas en Python) y reporta el
# termino ai:ps = DiD (sesgo agente-IA del modo en ese nivel - sesgo en el control). Es el gemelo por
# efectos aleatorios de fig4_did_by_dimension (que usa el DiD por modelo con t de Student).
#
# La pendiente aleatoria de ai:ps por modelo es la que hace que el termino que se testea no
# pseudorreplique (mismo argumento que en glmm_ai_bias.R). Cadena de respaldo si no converge:
# baja a (1+ai:ps||model), (1+ai||model), (1|model). Harness 4_analysis/r/glmm_common.R (lme4::glmer,
# nAGQ = 0, || primero, bobyqa/nlminbwrap, Wald, singular = convergido).
#
# Uso:  Rscript glmm_heterogeneity.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), ai (0/1), ps (0/1), lev, prompt_id, model.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_heterogeneity.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "..", "..", "..", "r", "glmm_common.R"))

d <- read_input(args[1])
d$ai <- as.integer(d$ai)
d$ps <- as.integer(d$ps)
d$lev <- as.character(d$lev)

formulas <- list(
  as.formula("refuse ~ ai * ps + (1 + ai + ai:ps || model) + (1 | prompt_id)"),
  as.formula("refuse ~ ai * ps + (1 + ai:ps || model) + (1 | prompt_id)"),
  as.formula("refuse ~ ai * ps + (1 + ai || model) + (1 | prompt_id)"),
  as.formula("refuse ~ ai * ps + (1 | model) + (1 | prompt_id)")
)

fits <- list()
for (L in sort(unique(d$lev))) {
  dd <- droplevels(d[d$lev == L, ])
  fits[[L]] <- one(L, dd, formulas, "ai:ps", slope = "ai:ps")
}
finish(fits, args[2])
