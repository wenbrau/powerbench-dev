#!/usr/bin/env Rscript
# glmm_direction_counterpart.R — Bloque 100: ¿el efecto de dirección respecto de EE.UU. es menor cuando la contraparte es China
# que cuando es un aliado, un rival o un país neutral? Pedido de Wendy (26/09). Lo llama analysis_100_us_counterpart_contrast.py.
#
# Un modelo por modo con las cuatro díadas de EE.UU. juntas y un efecto de dirección propio de cada díada (medias por celda):
#   refuse ~ 0 + dyad + dyad:toward + origin_c + toward:origin_c + (1 + toward || model) + (1 | prompt_id)
#   toward = +0,5 si EE.UU. es el USUARIO, −0,5 si es el AFECTADO; origin_c = +0,5 CN, −0,5 US (como en glmm_direction.R).
#   dyadX:toward = log-OR de dirección en la díada X (promedio de los dos orígenes, porque origin_c está centrado).
# Contrastes (Wald, combinación lineal con la matriz de covarianza): China − aliado, China − rival, China − neutral, y
# China − media de los otros tres. Negativo = el efecto de dirección es menor frente a China.
# Protocolo de glmm_common.R (|| primero, bobyqa y nlminbwrap, nAGQ de PB_NAGQ, Wald, singular aceptado).
#
# Uso:  Rscript glmm_direction_counterpart.R <datos.csv> <salida.csv>
# datos.csv: refuse (0/1), mode, dyad (us_ally / us_rival / us_neutral / us_cn), toward (±0.5), origin_c (±0.5), prompt_id, model.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("uso: Rscript glmm_direction_counterpart.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
DY <- c("us_ally", "us_rival", "us_neutral", "us_cn")

rows <- list()
for (md in unique(d$mode)) {
  t0 <- proc.time()[["elapsed"]]
  dd <- droplevels(d[d$mode == md, ]); dd$dyad <- factor(dd$dyad, levels = DY)
  f <- function(corr) as.formula(paste("refuse ~ 0 + dyad + dyad:toward + origin_c + toward:origin_c",
        if (corr) "+ (1 + toward | model)" else "+ (1 + toward || model)", "+ (1 | prompt_id)"))
  f1 <- fit_any(list(f(FALSE), f(TRUE)), dd); m <- f1$m
  b <- fixef(m); V <- as.matrix(vcov(m))
  tw <- function(k) paste0("dyad", k, ":toward")
  lc <- function(w) { est <- sum(w * b[names(w)]); se <- sqrt(as.numeric(t(w) %*% V[names(w), names(w)] %*% w)); c(est, se) }
  w_of <- function(pos, negs) { w <- c(1, rep(-1 / length(negs), length(negs))); names(w) <- tw(c(pos, negs)); w }
  q <- rbind(
    "direccion us_ally"               = lc(setNames(1, tw("us_ally"))),
    "direccion us_rival"              = lc(setNames(1, tw("us_rival"))),
    "direccion us_neutral"            = lc(setNames(1, tw("us_neutral"))),
    "direccion us_cn"                 = lc(setNames(1, tw("us_cn"))),
    "China - aliado"                  = lc(w_of("us_cn", "us_ally")),
    "China - rival"                   = lc(w_of("us_cn", "us_rival")),
    "China - neutral"                 = lc(w_of("us_cn", "us_neutral")),
    "China - media de los otros tres" = lc(w_of("us_cn", c("us_ally", "us_rival", "us_neutral"))))
  el <- proc.time()[["elapsed"]] - t0
  out <- data.frame(mode = md, quantity = rownames(q), estimate = q[, 1], se = q[, 2], z = q[, 1] / q[, 2],
                    p = 2 * pnorm(-abs(q[, 1] / q[, 2])),
                    sd_model_slope = vc_sd(m, "model", "toward"), sd_model = vc_sd(m, "model", "(Intercept)"),
                    sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), singular = isSingular(m),
                    messages = paste(msgs_of(m), collapse = " | "), optimizer = f1$optimizer, variant = f1$variant,
                    formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m), seconds = el,
                    row.names = NULL, stringsAsFactors = FALSE)
  cat(sprintf("%-8s China - otros tres %+.3f (se %.3f, p %.3g)  [%s, v%d]%s  %.1f s\n", md, out$estimate[8], out$se[8], out$p[8],
              f1$optimizer, f1$variant, if (isTRUE(out$singular[1])) "  SINGULAR" else "", el))
  flush(stdout())
  rows[[md]] <- out
}
finish(rows, args[2])
