#!/usr/bin/env Rscript
# glmm_side_ps.R — Figura de países, panel C: efecto del LADO del usuario sobre power shifting AGRUPADO (he + de + pg),
# versión pooled del GLMM del bloque 45 (que ajusta modo por modo). Columna violeta pedida por Wendy (2026-09-20, oficial desde ese día): "una columna violeta
# de power shifting general" en los paneles de la izquierda. Misma receta que el bloque 82 (idiomas pooled): las filas de los
# tres modos juntas y `mode` como efecto fijo de diseño.
#
# Por set (geo, neutral):  refuse ~ side + dyad + mode + (1 + side || model) + (1 | prompt_id)   (neutral sin dyad)
#   side = +0,5 usuario lado USA, −0,5 lado China. Un solo test por set (pooled): q = p.
# Protocolo de glmm_common.R: nAGQ = 1, || primero y correlacionada si no converge, bobyqa y nlminbwrap, Wald, singular aceptado.
#
# Uso:  Rscript glmm_side_ps.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode (he/de/pg), set, dyad, side (+0.5/-0.5), prompt_id, model.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_side_ps.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
d$mode <- factor(d$mode, levels = c("he", "de", "pg"))
out <- data.frame()
for (st in c("geo", "neutral")) {
  dd <- droplevels(d[d$set == st, ])
  dy <- if (st == "geo") "+ dyad" else ""
  if (st == "geo") dd$dyad <- factor(dd$dyad)
  f <- function(corr) as.formula(paste("refuse ~ side", dy, "+ mode", if (corr) "+ (1 + side | model)" else "+ (1 + side || model)", "+ (1 | prompt_id)"))
  f1 <- fit_any(list(f(FALSE), f(TRUE)), dd); m <- f1$m
  b <- fixef(m); se <- sqrt(diag(as.matrix(vcov(m))))
  est <- unname(b["side"]); s <- unname(se["side"]); p <- 2 * pnorm(-abs(est / s))
  out <- rbind(out, data.frame(set = st, mode = "power_shifting", quantity = "lado (24 modelos)", estimate = est, se = s, z = est / s, p = p,
                               OR = exp(est), OR_lo = exp(est - 1.96 * s), OR_hi = exp(est + 1.96 * s), q_bh = p,
                               sd_model_slope = vc_sd(m, "model", "side"), sd_model = vc_sd(m, "model", "(Intercept)"),
                               sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), singular = isSingular(m), optimizer = f1$optimizer,
                               variant = f1$variant, formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m),
                               lme4_version = as.character(packageVersion("lme4")), r_version = R.version.string, stringsAsFactors = FALSE))
  cat(sprintf("%-8s OR %.3f [%.3f, %.3f] p %.3g | sd_slope %.2f%s [%s, v%d]\n", st, exp(est), exp(est - 1.96 * s), exp(est + 1.96 * s), p,
              vc_sd(m, "model", "side"), if (isSingular(m)) " SINGULAR" else "", f1$optimizer, f1$variant)); flush(stdout())
}
write.csv(out, args[2], row.names = FALSE)
