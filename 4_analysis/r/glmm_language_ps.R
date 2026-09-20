#!/usr/bin/env Rscript
# glmm_language_ps.R — bloque 82: efecto de idioma sobre las filas de POWER SHIFTING juntas (he + de + pg), desviación de cada
# idioma respecto de la media de los 8 (lo llama analysis_82_fig2_language_glmm_ps.py). Nico (20/09): "podría estar bueno, y
# dejar constancia" — la versión pooled del bloque 36, que ajusta modo por modo.
#
#   refuse ~ lang + mode + (1 | model) + (1 | model_lang) + (1 | prompt_id)
#   lang en contrastes suma-cero: cada coeficiente es la desviación del idioma respecto de la media de los 8; el 8º se deriva como
#   −(suma de los otros 7) con su varianza desde vcov; Wald por idioma, BH sobre los 8; ómnibus χ² con 7 gl. (1 | model_lang) es el
#   perfil de idioma propio de cada modelo (como en el bloque 36 y en glmm_fig1_v3.R). Variante mínima sin él si no converge.
#   Protocolo de glmm_common.R (nAGQ = 0, bobyqa y nlminbwrap, Wald, singular aceptado).
#
# Uso:  Rscript glmm_language_ps.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode (he/de/pg), prompt_id, model, lang (entero 1..8 en el orden que pasa el Python).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_language_ps.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
K <- 8
d$lang <- factor(d$lang, levels = 1:K)
contrasts(d$lang) <- contr.sum(K)
d$mode <- factor(d$mode, levels = c("pg", "he", "de"))
d$model_lang <- factor(paste(d$model, d$lang, sep = ":"))
fulls <- lapply(c("(1 | model) + (1 | model_lang) + (1 | prompt_id)", "(1 | model) + (1 | prompt_id)"),
                function(re) as.formula(paste("refuse ~ lang + mode +", re)))
t0 <- Sys.time()
f1 <- fit_any(fulls, d); m <- f1$m
secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
s <- summary(m)$coefficients; V <- as.matrix(vcov(m))
idx <- grep("^lang[0-9]+$", rownames(s))
b <- s[idx, "Estimate"]; Vb <- V[idx, idx]
L <- rbind(diag(K - 1), rep(-1, K - 1))
dev <- as.numeric(L %*% b); dse <- sqrt(diag(L %*% Vb %*% t(L)))
dz <- dev / dse; dp <- 2 * pnorm(-abs(dz)); dbh <- p.adjust(dp, method = "BH")
W <- as.numeric(t(b) %*% solve(Vb) %*% b)
out <- data.frame(kind = c(rep("dev", K), "omnibus"), lang = c(1:K, NA), estimate = c(dev, W), se = c(dse, NA), z = c(dz, NA),
                  p = c(dp, pchisq(W, df = K - 1, lower.tail = FALSE)), p_bh = c(dbh, NA), df = c(rep(NA, K), K - 1),
                  sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
                  sd_model_lang = if (f1$variant == 1) vc_sd(m, "model_lang", "(Intercept)") else NA_real_,
                  singular = isSingular(m), optimizer = f1$optimizer, variant = f1$variant,
                  formula_used = paste(deparse(fulls[[f1$variant]]), collapse = ""), messages = paste(msgs_of(m), collapse = " | "),
                  fit_seconds = round(secs, 1), nobs = nobs(m), lme4_version = as.character(packageVersion("lme4")), r_version = R.version.string,
                  stringsAsFactors = FALSE)
write.csv(out, args[2], row.names = FALSE)
cat("wrote", args[2], "\n"); print(out[, c("kind", "lang", "estimate", "se", "p", "p_bh", "singular")])
