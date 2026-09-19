#!/usr/bin/env Rscript
# glmm_side_sets.R — variante de glmm_side.R para conjuntos arbitrarios de díadas (una o varias por conjunto).
# Pedido de Nico (19/09): ver el efecto del lado con USA / China y aliado de USA / aliado de China POR SEPARADO (y la
# referencia neutral), en lugar de juntas como en el bloque 45. Lo llama analysis_75_fig3_dyads_separate.py.
#
# Por conjunto (los que traiga el archivo) y por modo, solo el ajuste de los 24 modelos:
#   side   refuse ~ side [+ dyad si el conjunto tiene más de una díada] + (1 + side || model) + (1 | prompt_id)
#          side = +0,5 si el usuario es del lado A (USA o su aliado), −0,5 si es del lado B; el coeficiente es el log-OR
#          de refusal usuario-lado-A contra usuario-lado-B. Misma codificación y protocolo que glmm_side.R (glmm_common.R:
#          lme4::glmer, nAGQ = 0, || primero y correlacionada si no converge, bobyqa y nlminbwrap, Wald, singular aceptado).
#
# Uso:  Rscript glmm_side_sets.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, set, dyad, side (+0.5 / -0.5), prompt_id, model.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_side_sets.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
fits <- list()
for (st in unique(d$set)) {
  for (md in c("he", "de", "pg", "control")) {
    dd <- droplevels(d[d$set == st & d$mode == md, ])
    dd$dyad <- factor(dd$dyad)
    dy <- if (nlevels(dd$dyad) > 1) "+ dyad" else ""
    f <- function(rhs, corr = FALSE)
      as.formula(paste("refuse ~", rhs, dy, if (corr) "+ (1 + side | model)" else "+ (1 + side || model)", "+ (1 | prompt_id)"))
    k <- paste(st, md, sep = "_")
    r1 <- one(paste0("side__", k), dd, list(f("side"), f("side", TRUE)), "side", slope = "side")
    r1$set <- st; r1$mode <- md
    fits[[k]] <- r1
    cat(k, "\n")
  }
}
finish(fits, args[2])
