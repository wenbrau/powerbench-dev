#!/usr/bin/env Rscript
# glmm_specificity.R — bloque 93: tests directos de las afirmaciones de especificidad del paper (un efecto que es
# significativo en un tipo de pedido y no en otro). Lo llama analysis_93_specificity_interactions.py, que exporta los datos
# ya armados (una fila por veredicto, con la clave del test) y reparte los tests entre varios procesos de R.
#
# Tres clases de ajuste (columna kind):
#   inter        refuse ~ m * t [+ dyad * t] [+ mode_he + mode_de] + (1 + m + t + mt || model) + (1 | prompt_id)
#                m = la manipulación del panel (side ±0,5; toward ±0,5; escala 0/1/2), t = 1 en el tipo de interés y 0 en el
#                tipo de referencia, mt = m · t. Término m:t = diferencia de pendientes (log del cociente de OR), la misma
#                construcción que las interacciones con el control de los bloques 30 y 31. dyad * t cuando el panel junta díadas
#                (los niveles de cada díada pueden diferir entre los dos tipos); mode_he y mode_de cuando t = 1 es power shifting
#                agrupado (tipo como efecto fijo, como en los ajustes agrupados del paper).
#   diff2        refuse ~ m + m2 [+ mode_he + mode_de] + (1 + m + m2 || model) + (1 | prompt_id); cantidad m − m2
#                (escala menos standing, las dos 0/1/2, en el mismo ajuste).
#   counterpart  refuse ~ m + m2 + dyad + (1 + m + m2 || model) + (1 | prompt_id), m = toward, m2 = toward · r (r = ±0,5, un grupo
#                de contrapartes contra otro); término m2 = diferencia de la pendiente de dirección entre los dos grupos.
# Protocolo de glmm_common.R (nAGQ del entorno, || primero y correlacionada si no converge, bobyqa y nlminbwrap, Wald,
# singular aceptado). Además de m:t se reportan la pendiente en cada tipo (combinaciones lineales con vcov).
#
# Uso:  Rscript glmm_specificity.R <datos.csv> <salida.csv>
# datos.csv: test, kind, refuse, prompt_id, model, m, m2, t, dyad, mode_he, mode_de.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_specificity.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
d$mt <- d$m * d$t

fit_test <- function(key, dd) {
  t0 <- proc.time()[["elapsed"]]
  kind <- dd$kind[1]
  dd$dyad <- factor(dd$dyad)
  has_dyad <- nlevels(dd$dyad) > 1
  has_mode <- any(dd$mode_he != 0) || any(dd$mode_de != 0)
  md <- if (has_mode) "+ mode_he + mode_de" else ""
  if (kind == "inter") {
    fe <- paste("refuse ~ m * t", if (has_dyad) "+ dyad * t" else "", md)
    re <- c("+ (1 + m + t + mt || model) + (1 | prompt_id)", "+ (1 + m + t + mt | model) + (1 | prompt_id)")
    slope <- "mt"
  } else if (kind == "diff2") {
    fe <- paste("refuse ~ m + m2", md)
    re <- c("+ (1 + m + m2 || model) + (1 | prompt_id)", "+ (1 + m + m2 | model) + (1 | prompt_id)")
    slope <- "m"
  } else if (kind == "counterpart") {
    fe <- "refuse ~ m + m2 + dyad"
    re <- c("+ (1 + m + m2 || model) + (1 | prompt_id)", "+ (1 + m + m2 | model) + (1 | prompt_id)")
    slope <- "m2"
  } else stop("kind desconocido: ", kind)
  fl <- lapply(re, function(r) as.formula(paste(fe, r)))
  f1 <- fit_any(fl, dd); m <- f1$m
  b <- fixef(m); V <- as.matrix(vcov(m))
  lc <- function(w) {
    est <- sum(w * b[names(w)]); se <- sqrt(as.numeric(t(w) %*% V[names(w), names(w)] %*% w)); c(est, se)
  }
  q <- if (kind == "inter") rbind("interaction" = lc(c("m:t" = 1)), "slope_reference" = lc(c("m" = 1)),
                                  "slope_target" = lc(c("m" = 1, "m:t" = 1)))
       else if (kind == "diff2") rbind("difference" = lc(c("m" = 1, "m2" = -1)), "slope_m" = lc(c("m" = 1)), "slope_m2" = lc(c("m2" = 1)))
       else rbind("interaction" = lc(c("m2" = 1)), "slope_common" = lc(c("m" = 1)))
  el <- proc.time()[["elapsed"]] - t0
  out <- data.frame(test = key, kind = kind, quantity = rownames(q), estimate = q[, 1], se = q[, 2], z = q[, 1] / q[, 2],
                    p = 2 * pnorm(-abs(q[, 1] / q[, 2])),
                    sd_model_slope = vc_sd(m, "model", slope), sd_model = vc_sd(m, "model", "(Intercept)"),
                    sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), singular = isSingular(m),
                    messages = paste(msgs_of(m), collapse = " | "), optimizer = f1$optimizer, variant = f1$variant,
                    formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m),
                    n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
                    nagq = NAGQ, seconds = el, row.names = NULL, stringsAsFactors = FALSE)
  cat(sprintf("%-40s %s %+.3f (se %.3f, p %.3g)  [%s, v%d]%s  %.0f s\n", key, out$quantity[1], out$estimate[1], out$se[1], out$p[1],
              f1$optimizer, f1$variant, if (isTRUE(out$singular[1])) "  SINGULAR" else "", el))
  flush(stdout())
  out
}

fits <- list()
for (k in unique(as.character(d$test))) fits[[k]] <- fit_test(k, droplevels(d[d$test == k, ]))
finish(fits, args[2])
