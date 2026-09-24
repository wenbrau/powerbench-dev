#!/usr/bin/env Rscript
# glmm_index.R — Figura 3 (D2): efecto del índice geopolítico 1D del otro país (o del usuario) sobre el refusal, a nivel de
# fila, con el país como intercepto aleatorio. Pedido de Nico (18/09): "a ver, probemos ese GLMM". Lo llama
# analysis_49_fig3_index_glmm.py.
#
# Por variante (A–E del bloque 48) y modo:
#   refuse ~ x * origin_c + (1 + x || model) + (1 | prompt_id) + (1 | country1) [+ (1 | country2)]
#   x        = índice 1D (bloque 47; cero en la mediana de los países, lado USA positivo) del país afectado (A, B), del país
#              usuario (C, D) o la diferencia usuario − afectado (E)
#   origin_c = +0,5 modelo CN, −0,5 modelo US (centrado: 'x' es la pendiente media de los dos orígenes)
#   country1 = el país cuyo índice es x (A–D) o el país usuario (E); country2 = el país afectado (solo E)
#   pendiente en modelos US = x − 0,5 · x:origin_c; en modelos CN = x + 0,5 · x:origin_c (combinaciones lineales con su error estándar)
# Protocolo de glmm_common.R: lme4::glmer, nAGQ = 1, || primero, bobyqa y nlminbwrap, Wald, ajuste singular aceptado.
#
# Uso:  Rscript glmm_index.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), variant, mode, x, origin_c, prompt_id, model, country1, country2 ("" si no hay).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_index.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
d$country1 <- factor(d$country1)
d$country2 <- ifelse(is.na(d$country2) | d$country2 == "", NA, d$country2)

fit_idx <- function(key, dd) {
  t0 <- proc.time()[["elapsed"]]
  two <- !all(is.na(dd$country2))
  if (two) dd$country2 <- factor(dd$country2)
  c2 <- if (two) "+ (1 | country2)" else ""
  f <- function(corr) as.formula(paste("refuse ~ x * origin_c", if (corr) "+ (1 + x | model)" else "+ (1 + x || model)",
                                       "+ (1 | prompt_id) + (1 | country1)", c2))
  f1 <- fit_any(list(f(FALSE), f(TRUE)), dd); m <- f1$m
  b <- fixef(m); V <- as.matrix(vcov(m))
  lc <- function(w) { est <- sum(w * b[names(w)]); se <- sqrt(as.numeric(t(w) %*% V[names(w), names(w)] %*% w)); c(est, se) }
  q <- rbind("pendiente (24 modelos)" = lc(c("x" = 1)),
             "pendiente, modelos US" = lc(c("x" = 1, "x:origin_c" = -0.5)),
             "pendiente, modelos CN" = lc(c("x" = 1, "x:origin_c" = 0.5)),
             "pendiente x origen (CN - US)" = lc(c("x:origin_c" = 1)))
  el <- proc.time()[["elapsed"]] - t0
  out <- data.frame(fit = key, quantity = rownames(q), estimate = q[, 1], se = q[, 2], z = q[, 1] / q[, 2],
                    p = 2 * pnorm(-abs(q[, 1] / q[, 2])),
                    sd_model_slope = vc_sd(m, "model", "x"), sd_model = vc_sd(m, "model", "(Intercept)"),
                    sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_country1 = vc_sd(m, "country1", "(Intercept)"),
                    sd_country2 = if (two) vc_sd(m, "country2", "(Intercept)") else NA_real_,
                    singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "), optimizer = f1$optimizer,
                    variant_formula = f1$variant, formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m),
                    n_countries = nlevels(droplevels(dd$country1)), seconds = el, row.names = NULL, stringsAsFactors = FALSE)
  cat(sprintf("%-20s pendiente %+.3f (se %.3f, p %.3g) | CN-US %+.3f (p %.3g) | sd_slope %.2f sd_pais %.2f  [%s, v%d]%s  %.1f s\n", key,
              out$estimate[1], out$se[1], out$p[1], out$estimate[4], out$p[4], out$sd_model_slope[1], out$sd_country1[1],
              f1$optimizer, f1$variant, if (isTRUE(out$singular[1])) "  SINGULAR" else "", el))
  flush(stdout())
  out
}

fits <- list()
for (v in unique(d$variant)) for (md in unique(d$mode)) {
  dd <- droplevels(d[d$variant == v & d$mode == md, ])
  x <- fit_idx(paste(v, md, sep = "__"), dd); x$variant <- v; x$mode <- md
  fits[[paste(v, md)]] <- x
}
finish(fits, args[2])
