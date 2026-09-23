#!/usr/bin/env Rscript
# glmm_context_within.R — Figura 1, panel F: ¿varía el refusal entre contextos DENTRO de cada tipo de pedido,
# el control incluido?  (bloque 90; lo llama analysis_90_fig1_context_within_type_glmm.py)
#
# Pedido de Nico (22/09, ronda 7, #8): el test de contexto del control no debe comparar con power shifting
# (eso hace el bloque 32) sino preguntar lo mismo que el panel F pregunta para power shifting: ¿gobierno
# se rechaza más que la media de los contextos, dentro del control? Es el gemelo de glmm_domain.R
# (bloque 33, dominios por tipo), con el contexto en lugar del dominio y el control incluido:
#   refuse ~ ctx + (1 | model) + (1 | model:ctx) + (1 | prompt_id)          por tipo (he, de, pg, control)
# ctx con contrastes suma-cero (contr.sum): cada coeficiente es la desviación del contexto k respecto de la
# media del tipo sobre los 8 contextos (log-odds); el 8º se deriva como −(suma) con su varianza.
# Ómnibus: Wald conjunto b' V⁻¹ b sobre los 7 términos, χ² con 7 gl. Por contexto: z de Wald, p, BH sobre 8.
# Variante 2 si no converge: solo (1 | model) + (1 | prompt_id). Protocolo de glmm_common.R (nAGQ = 0,
# bobyqa y nlminbwrap, Wald).
#
# Uso:  Rscript glmm_context_within.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, prompt_id, model, ctx (entero 1..8 en el orden del cuaderno).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_context_within.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
K <- 8
d$ctx <- factor(d$ctx, levels = 1:K)
contrasts(d$ctx) <- contr.sum(K)
d$model_ctx <- factor(paste(d$model, d$ctx, sep = ":"))
fulls <- list(refuse ~ ctx + (1 | model) + (1 | model_ctx) + (1 | prompt_id),
              refuse ~ ctx + (1 | model) + (1 | prompt_id))
L <- rbind(diag(K - 1), rep(-1, K - 1))

one_ctx <- function(key, dd) {
  res <- tryCatch({
    t0 <- Sys.time()
    f1 <- fit_any(fulls, dd); m <- f1$m
    secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
    s <- summary(m)$coefficients
    V <- as.matrix(vcov(m))
    idx <- grep("^ctx[0-9]+$", rownames(s))
    b <- s[idx, "Estimate"]; Vb <- V[idx, idx]
    W <- as.numeric(t(b) %*% solve(Vb) %*% b)
    dev <- as.numeric(L %*% b); dse <- sqrt(diag(L %*% Vb %*% t(L)))
    dz <- dev / dse; dp <- 2 * pnorm(-abs(dz)); dbh <- p.adjust(dp, method = "BH")
    meta <- data.frame(fit = key,
                       sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
                       sd_model_ctx = vc_sd(m, "model_ctx", "(Intercept)"),
                       singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "),
                       optimizer = f1$optimizer, formula_used = paste(deparse(fulls[[f1$variant]]), collapse = ""),
                       variant = f1$variant, fit_seconds = round(secs, 1), loglik = as.numeric(logLik(m)), nobs = nobs(m),
                       n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
                       error = "", stringsAsFactors = FALSE)
    rbind(
      cbind(data.frame(kind = "coef", term = rownames(s), ctx = NA, estimate = s[, "Estimate"], se = s[, "Std. Error"],
                       z = s[, "z value"], p = s[, "Pr(>|z|)"], p_bh = NA, df = NA, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "omnibus", term = "ctx", ctx = NA, estimate = W, se = NA, z = NA,
                       p = pchisq(W, df = K - 1, lower.tail = FALSE), p_bh = NA, df = K - 1, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "ctx_dev", term = "ctx", ctx = 1:K, estimate = dev, se = dse, z = dz, p = dp, p_bh = dbh, df = NA,
                       stringsAsFactors = FALSE), meta, row.names = NULL))
  }, error = function(e) {
    data.frame(kind = "error", term = NA, ctx = NA, estimate = NA, se = NA, z = NA, p = NA, p_bh = NA, df = NA,
               fit = key, sd_prompt = NA, sd_model = NA, sd_model_ctx = NA, singular = NA, messages = "",
               optimizer = NA, formula_used = NA, variant = NA, fit_seconds = NA, loglik = NA, nobs = nrow(dd),
               n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
               error = conditionMessage(e), stringsAsFactors = FALSE)
  })
  om <- res[res$kind == "omnibus", ]
  cat(sprintf("%-14s %s\n", key, if (nrow(om) == 0) paste("ERROR", res$error[1]) else
              sprintf("omnibus chi2(7) = %.2f p = %.3g  sd_prompt %.2f sd_model %.2f sd_model_ctx %.2f  [%s, v%d, %.0fs]%s%s",
                      om$estimate, om$p, om$sd_prompt, om$sd_model, om$sd_model_ctx, om$optimizer, om$variant, om$fit_seconds,
                      if (isTRUE(om$singular)) "  SINGULAR" else "",
                      if (nzchar(om$messages)) paste0("  [", om$messages, "]") else "")))
  flush(stdout())
  res
}

fits <- list()
for (md in c("control", "he", "de", "pg")) {
  if (!any(d$mode == md)) next
  dd <- droplevels(d[d$mode == md, ])
  dd$ctx <- factor(dd$ctx, levels = 1:K); contrasts(dd$ctx) <- contr.sum(K)
  dd$model_ctx <- factor(paste(dd$model, dd$ctx, sep = ":"))
  fits[[paste0("A_", md)]] <- one_ctx(paste0("A_", md), dd)
}
finish(fits, args[2])
