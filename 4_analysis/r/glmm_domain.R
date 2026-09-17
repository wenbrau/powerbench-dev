#!/usr/bin/env Rscript
# glmm_domain.R — Figura 1, panel 5: ¿varía el refusal entre dominios de poder, dentro de cada modo?
# (bloque 33; lo llama analysis_33_fig1_domain_glmm.py). Sin control: el control no tiene dominio.
#
# Decisión de Nico (16/09): los tests equivalentes al panel de contexto que no involucren al control.
# Por modo (he, de, pg):
#   refuse ~ dom + (1 | model) + (1 | model:dom) + (1 | prompt_id)
# dom con contrastes suma-cero (contr.sum): cada coeficiente es la desviación del dominio k respecto de
# la media del modo sobre los 8 dominios (log-odds); el 8º se deriva como −(suma) con su varianza.
# Ómnibus: Wald conjunto b' V⁻¹ b sobre los 7 términos, χ² con 7 gl. Por dominio: z de Wald, p, BH sobre 8.
# El intercepto por modelo × dominio (perfil de dominio propio de cada modelo) es lo que evita
# pseudorreplicar el efecto del dominio sobre los 24 modelos; equivale a pendientes por dominio sin
# correlación y con varianza común, y es mucho más barato (16/09 19:05, tras la versión con 7 pendientes).
# Variante 2 si no converge: solo (1 | model) + (1 | prompt_id).
#
# Uso:  Rscript glmm_domain.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, prompt_id, model, dom (entero 1..8 en el orden del cuaderno).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_domain.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
K <- 8
d$dom <- factor(d$dom, levels = 1:K)
contrasts(d$dom) <- contr.sum(K)
d$model_dom <- factor(paste(d$model, d$dom, sep = ":"))
fulls <- list(refuse ~ dom + (1 | model) + (1 | model_dom) + (1 | prompt_id),
              refuse ~ dom + (1 | model) + (1 | prompt_id))
L <- rbind(diag(K - 1), rep(-1, K - 1))

one_dom <- function(key, dd) {
  res <- tryCatch({
    t0 <- Sys.time()
    f1 <- fit_any(fulls, dd); m <- f1$m
    secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
    s <- summary(m)$coefficients
    V <- as.matrix(vcov(m))
    idx <- grep("^dom[0-9]+$", rownames(s))
    b <- s[idx, "Estimate"]; Vb <- V[idx, idx]
    W <- as.numeric(t(b) %*% solve(Vb) %*% b)
    dev <- as.numeric(L %*% b); dse <- sqrt(diag(L %*% Vb %*% t(L)))
    dz <- dev / dse; dp <- 2 * pnorm(-abs(dz)); dbh <- p.adjust(dp, method = "BH")
    meta <- data.frame(fit = key,
                       sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
                       sd_model_dom = vc_sd(m, "model_dom", "(Intercept)"),
                       singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "),
                       optimizer = f1$optimizer, formula_used = paste(deparse(fulls[[f1$variant]]), collapse = ""),
                       variant = f1$variant, fit_seconds = round(secs, 1), loglik = as.numeric(logLik(m)), nobs = nobs(m),
                       n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
                       error = "", stringsAsFactors = FALSE)
    rbind(
      cbind(data.frame(kind = "coef", term = rownames(s), dom = NA, estimate = s[, "Estimate"], se = s[, "Std. Error"],
                       z = s[, "z value"], p = s[, "Pr(>|z|)"], p_bh = NA, df = NA, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "omnibus", term = "dom", dom = NA, estimate = W, se = NA, z = NA,
                       p = pchisq(W, df = K - 1, lower.tail = FALSE), p_bh = NA, df = K - 1, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "dom_dev", term = "dom", dom = 1:K, estimate = dev, se = dse, z = dz, p = dp, p_bh = dbh, df = NA,
                       stringsAsFactors = FALSE), meta, row.names = NULL))
  }, error = function(e) {
    data.frame(kind = "error", term = NA, dom = NA, estimate = NA, se = NA, z = NA, p = NA, p_bh = NA, df = NA,
               fit = key, sd_prompt = NA, sd_model = NA, sd_model_dom = NA, singular = NA, messages = "",
               optimizer = NA, formula_used = NA, variant = NA, fit_seconds = NA, loglik = NA, nobs = nrow(dd),
               n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
               error = conditionMessage(e), stringsAsFactors = FALSE)
  })
  om <- res[res$kind == "omnibus", ]
  cat(sprintf("%-14s %s\n", key, if (nrow(om) == 0) paste("ERROR", res$error[1]) else
              sprintf("omnibus chi2(7) = %.2f p = %.3g  sd_prompt %.2f sd_model %.2f sd_model_dom %.2f  [%s, v%d, %.0fs]%s%s",
                      om$estimate, om$p, om$sd_prompt, om$sd_model, om$sd_model_dom, om$optimizer, om$variant, om$fit_seconds,
                      if (isTRUE(om$singular)) "  SINGULAR" else "",
                      if (nzchar(om$messages)) paste0("  [", om$messages, "]") else "")))
  flush(stdout())
  res
}

fits <- list()
for (md in c("he", "de", "pg")) {
  dd <- droplevels(d[d$mode == md, ])
  dd$dom <- factor(dd$dom, levels = 1:K); contrasts(dd$dom) <- contr.sum(K)
  fits[[paste0("A_", md)]] <- one_dom(paste0("A_", md), dd)
}
finish(fits, args[2])
