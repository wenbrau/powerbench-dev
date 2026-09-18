#!/usr/bin/env Rscript
# glmm_ai_level.R — Figura 4 (D3 agente IA vs D1 humano): ¿el efecto del usuario IA cambia con el nivel de una dimensión
# del prompt (escala del afectado, standing del usuario)? Pregunta de Nico (18/09): "las tendencias de sesgo vs escala en PG
# y DE son significativas?". Gemelo del test de escala / standing de la Figura 1 (bloque 31) aplicado al efecto ai.
# Lo llama analysis_60_fig4_ai_level_glmm.py.
#
# Por modo:  refuse ~ ai * level + (1 + ai || model) + (1 | prompt_id)
#   ai = +0,5 usuario IA (D3), −0,5 humano (D1 inglés); level = factor con el primer nivel como referencia (individual / low).
#   Se reportan: el efecto ai en cada nivel (b_ai + b_ai:level, combinación lineal con vcov), los contrastes entre niveles del
#   efecto ai (= los términos ai:level y su diferencia), y el ómnibus de Wald b' V⁻¹ b sobre los dos términos ai:level (χ², 2 gl).
# Protocolo de glmm_common.R: lme4::glmer, nAGQ = 0, || primero y correlacionada si no converge, bobyqa y nlminbwrap, Wald,
# ajuste singular aceptado.
#
# Uso:  Rscript glmm_ai_level.R <datos.csv> <salida.csv> <nivel1,nivel2,nivel3>
# datos.csv: columnas refuse (0/1), mode, ai (+0.5 / -0.5), level, prompt_id, model.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) stop("uso: Rscript glmm_ai_level.R <datos.csv> <salida.csv> <niveles separados por coma>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
levels_ <- strsplit(args[3], ",")[[1]]
d$level <- factor(d$level, levels = levels_)
fits <- list()
for (md in c("he", "de", "pg", "control")) {
  dd <- droplevels(d[d$mode == md, ])
  t0 <- proc.time()[["elapsed"]]
  f <- function(corr) as.formula(paste("refuse ~ ai * level", if (corr) "+ (1 + ai | model)" else "+ (1 + ai || model)", "+ (1 | prompt_id)"))
  f1 <- fit_any(list(f(FALSE), f(TRUE)), dd); m <- f1$m
  b <- fixef(m); V <- as.matrix(vcov(m))
  lc <- function(w) {
    est <- sum(w * b[names(w)]); se <- sqrt(as.numeric(t(w) %*% V[names(w), names(w)] %*% w))
    c(est, se)
  }
  L2 <- paste0("ai:level", levels_[2]); L3 <- paste0("ai:level", levels_[3])
  q <- rbind(
    "ai en nivel 1" = lc(c("ai" = 1)),
    "ai en nivel 2" = lc(setNames(c(1, 1), c("ai", L2))),
    "ai en nivel 3" = lc(setNames(c(1, 1), c("ai", L3))),
    "nivel 2 - nivel 1" = lc(setNames(1, L2)),
    "nivel 3 - nivel 1" = lc(setNames(1, L3)),
    "nivel 3 - nivel 2" = lc(setNames(c(1, -1), c(L3, L2))))
  bb <- b[c(L2, L3)]; W <- as.numeric(t(bb) %*% solve(V[c(L2, L3), c(L2, L3)]) %*% bb)
  el <- proc.time()[["elapsed"]] - t0
  out <- data.frame(fit = paste0("ai_level__", md), mode = md, quantity = c(rownames(q), "omnibus ai x nivel"),
                    estimate = c(q[, 1], W), se = c(q[, 2], NA), z = c(q[, 1] / q[, 2], NA),
                    p = c(2 * pnorm(-abs(q[, 1] / q[, 2])), pchisq(W, df = 2, lower.tail = FALSE)), df = c(rep(NA, nrow(q)), 2),
                    sd_model_slope = vc_sd(m, "model", "ai"), sd_model = vc_sd(m, "model", "(Intercept)"),
                    sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), singular = isSingular(m),
                    messages = paste(msgs_of(m), collapse = " | "), optimizer = f1$optimizer, variant = f1$variant,
                    formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m), seconds = el,
                    level1 = levels_[1], level2 = levels_[2], level3 = levels_[3], row.names = NULL, stringsAsFactors = FALSE)
  cat(sprintf("%-12s ai@%s %+.3f | ai@%s %+.3f | ai@%s %+.3f | (3-1) %+.3f p %.3g | omnibus chi2(2) %.2f p %.3g | sd_slope %.2f [%s, v%d]%s %.0fs\n",
              md, levels_[1], q[1, 1], levels_[2], q[2, 1], levels_[3], q[3, 1], q[5, 1], out$p[5], W, out$p[7],
              out$sd_model_slope[1], f1$optimizer, f1$variant, if (isTRUE(out$singular[1])) " SINGULAR" else "", el))
  flush(stdout())
  fits[[md]] <- out
}
finish(fits, args[2])
