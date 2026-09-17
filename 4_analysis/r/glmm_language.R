#!/usr/bin/env Rscript
# glmm_language.R — Figura 2, panel A: ¿el idioma tiene un efecto promedio sobre el refusal, y cuánto de su
# efecto es propio de cada modelo?  (bloque 36; lo llama analysis_36_fig2_language_glmm.py)
#
# Por modo (he, de, pg, control):
#   refuse ~ lang + (1 | model) + (1 | model:lang) + (1 | prompt_id)
# lang con contrastes suma-cero (8 idiomas → 7 coeficientes): cada coeficiente es la desviación del idioma k
# respecto de la media del modo sobre los 8 idiomas (log-odds); el 8º se deriva como −(suma) con su varianza.
# El intercepto por prompt aparea los idiomas (mismo prompt traducido); el intercepto por modelo × idioma es
# el perfil de idiomas propio de cada modelo y entra en el error del efecto fijo. Ómnibus: Wald conjunto
# b' V⁻¹ b, χ² con 7 gl. Por idioma: z de Wald, p, BH sobre 8. Se reportan las SD de los tres efectos
# aleatorios para la descomposición "promedio vs por modelo".
# Protocolo del 16/09 (glmm_common.R): nAGQ = 0, bobyqa y nlminbwrap, Wald, singular aceptado.
# Variante 2 si no converge: sin (1 | model:lang).
#
# Uso:  Rscript glmm_language.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, prompt_id, model, lang (entero 1..8).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_language.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
K <- 8
d$lang <- factor(d$lang, levels = 1:K)
contrasts(d$lang) <- contr.sum(K)
d$model_lang <- factor(paste(d$model, d$lang, sep = ":"))
fulls <- list(refuse ~ lang + (1 | model) + (1 | model_lang) + (1 | prompt_id),
              refuse ~ lang + (1 | model) + (1 | prompt_id))
L <- rbind(diag(K - 1), rep(-1, K - 1))

one_lang <- function(key, dd) {
  res <- tryCatch({
    t0 <- Sys.time()
    f1 <- fit_any(fulls, dd); m <- f1$m
    secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
    s <- summary(m)$coefficients
    V <- as.matrix(vcov(m))
    idx <- grep("^lang[0-9]+$", rownames(s))
    b <- s[idx, "Estimate"]; Vb <- V[idx, idx]
    W <- as.numeric(t(b) %*% solve(Vb) %*% b)
    dev <- as.numeric(L %*% b); dse <- sqrt(diag(L %*% Vb %*% t(L)))
    dz <- dev / dse; dp <- 2 * pnorm(-abs(dz)); dbh <- p.adjust(dp, method = "BH")
    meta <- data.frame(fit = key,
                       sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
                       sd_model_lang = vc_sd(m, "model_lang", "(Intercept)"),
                       singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "),
                       optimizer = f1$optimizer, formula_used = paste(deparse(fulls[[f1$variant]]), collapse = ""),
                       variant = f1$variant, fit_seconds = round(secs, 1), loglik = as.numeric(logLik(m)), nobs = nobs(m),
                       n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
                       error = "", stringsAsFactors = FALSE)
    rbind(
      cbind(data.frame(kind = "coef", term = rownames(s), lang = NA, estimate = s[, "Estimate"], se = s[, "Std. Error"],
                       z = s[, "z value"], p = s[, "Pr(>|z|)"], p_bh = NA, df = NA, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "omnibus", term = "lang", lang = NA, estimate = W, se = NA, z = NA,
                       p = pchisq(W, df = K - 1, lower.tail = FALSE), p_bh = NA, df = K - 1, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "lang_dev", term = "lang", lang = 1:K, estimate = dev, se = dse, z = dz, p = dp, p_bh = dbh, df = NA,
                       stringsAsFactors = FALSE), meta, row.names = NULL))
  }, error = function(e) {
    data.frame(kind = "error", term = NA, lang = NA, estimate = NA, se = NA, z = NA, p = NA, p_bh = NA, df = NA,
               fit = key, sd_prompt = NA, sd_model = NA, sd_model_lang = NA, singular = NA, messages = "",
               optimizer = NA, formula_used = NA, variant = NA, fit_seconds = NA, loglik = NA, nobs = nrow(dd),
               n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
               error = conditionMessage(e), stringsAsFactors = FALSE)
  })
  om <- res[res$kind == "omnibus", ]
  cat(sprintf("%-10s %s\n", key, if (nrow(om) == 0) paste("ERROR", res$error[1]) else
              sprintf("omnibus chi2(7) = %.2f p = %.3g  sd_prompt %.2f sd_model %.2f sd_model_lang %.2f  [%s, v%d, %.0fs]%s%s",
                      om$estimate, om$p, om$sd_prompt, om$sd_model, om$sd_model_lang, om$optimizer, om$variant, om$fit_seconds,
                      if (isTRUE(om$singular)) "  SINGULAR" else "",
                      if (nzchar(om$messages)) paste0("  [", om$messages, "]") else "")))
  flush(stdout())
  res
}

fits <- list()
for (md in c("he", "de", "pg", "control")) {
  dd <- droplevels(d[d$mode == md, ])
  dd$lang <- factor(dd$lang, levels = 1:K); contrasts(dd$lang) <- contr.sum(K)
  fits[[paste0("A_", md)]] <- one_lang(paste0("A_", md), dd)
}
finish(fits, args[2])
