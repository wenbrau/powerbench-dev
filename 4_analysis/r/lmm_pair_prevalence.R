#!/usr/bin/env Rscript
# lmm_pair_prevalence.R — bloque 80: regresión del sesgo por par de idiomas contra la diferencia de prevalencia, con efectos
# aleatorios cruzados por modelo y por idioma (lo llama analysis_80_fig2_pairwise_bias_vs_prevalence.py).
# Nico (19/09): "querés hacer la regresión ya que estamos para que quede registrado?".
#
#   bias_ij(m) ~ dlog_share_ij + (1 + dlog_share || model) + (1 | lang_a) + (1 | lang_b)
#
# Una fila por modelo y par (triángulo inferior, 28 pares × 24 modelos, 22 en swahili). Gaussiano (el sesgo es un cociente en
# [−1, 1]); lme4::lmer por máxima verosimilitud, bobyqa; Wald z sobre la pendiente fija (protocolo del paper: Wald, singular
# aceptado). Los interceptos por idioma en el rol A y en el rol B absorben que cada idioma aparezca en 7 pares; la pendiente
# aleatoria por modelo es la heterogeneidad de dirección entre modelos.
#
# Uso:  Rscript lmm_pair_prevalence.R <datos.csv> <salida.csv>
# datos.csv: columnas bias, dlog_share, model, lang_a, lang_b.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript lmm_pair_prevalence.R <datos.csv> <salida.csv>")
suppressPackageStartupMessages(library(lme4))
d <- read.csv(args[1], stringsAsFactors = FALSE)
d <- d[is.finite(d$bias), ]
d$model <- factor(d$model); d$lang_a <- factor(d$lang_a); d$lang_b <- factor(d$lang_b)
ctrl <- lmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
m <- lmer(bias ~ dlog_share + (1 + dlog_share || model) + (1 | lang_a) + (1 | lang_b), data = d, REML = FALSE, control = ctrl)
s <- summary(m)$coefficients
vc <- as.data.frame(VarCorr(m))
sd_of <- function(grp, var) { r <- vc[vc$grp == grp & vc$var1 == var & is.na(vc$var2), ]; if (nrow(r)) r$sdcor[1] else NA_real_ }
out <- data.frame(term = rownames(s), estimate = s[, "Estimate"], se = s[, "Std. Error"], z = s[, "Estimate"] / s[, "Std. Error"],
                  p = 2 * pnorm(-abs(s[, "Estimate"] / s[, "Std. Error"])),
                  sd_model_int = sd_of("model", "(Intercept)"), sd_model_slope = sd_of("model.1", "dlog_share"),
                  sd_lang_a = sd_of("lang_a", "(Intercept)"), sd_lang_b = sd_of("lang_b", "(Intercept)"), sd_resid = sigma(m),
                  singular = isSingular(m), messages = paste(unlist(m@optinfo$conv$lme4$messages), collapse = " | "),
                  nobs = nobs(m), n_models = nlevels(d$model), n_pairs = length(unique(paste(d$lang_a, d$lang_b))),
                  loglik = as.numeric(logLik(m)), lme4_version = as.character(packageVersion("lme4")), r_version = R.version.string,
                  stringsAsFactors = FALSE)
if (is.na(out$sd_model_slope[1])) out$sd_model_slope <- sd_of("model", "dlog_share")
write.csv(out, args[2], row.names = FALSE)
cat("wrote", args[2], "\n"); print(out[, c("term", "estimate", "se", "p", "sd_model_slope", "sd_lang_a", "sd_lang_b", "singular")])
