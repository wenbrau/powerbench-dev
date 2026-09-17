#!/usr/bin/env Rscript
# glmm_context.R — Figura 1, panel 4: ¿hay contextos donde el refusal de power shifting es
# especialmente alto o bajo respecto al control?  (bloque 32; lo llama analysis_32_fig1_context_glmm.py)
#
# Sugerencia 1 elegida por Nico (16/09): interacción contexto × (power shifting vs control), test ómnibus
# de 7 gl sobre los términos de interacción, y después contrastes por contexto sobre la interacción.
#
# Contexto con contrastes suma-cero (contr.sum): el coeficiente ctxk:ps es la desviación de la brecha
# (power shifting − control) del contexto k respecto de la brecha media sobre los 8 contextos; el 8º se
# deriva como −(suma de los otros 7) con su varianza desde vcov. Ómnibus: Wald conjunto b' V⁻¹ b sobre
# los 7 términos, χ² con 7 gl. Por contexto: z de Wald y p, con BH sobre los 8.
#
# Efectos aleatorios (formulación estándar y barata, 16/09 19:05, tras una versión con 8–16 pendientes
# por modelo que tardaba horas): intercepto por prompt; por modelo, intercepto y pendiente de ps (||);
# intercepto por modelo × contexto (perfil de contexto propio de cada modelo) e intercepto por modelo ×
# contexto × ps (desviación propia de cada modelo en la interacción, que es lo que protege el test de
# ctx:ps de pseudorreplicar). Equivale a pendientes por contexto sin correlación y con varianza común.
#   E  los cuatro modos:   refuse ~ ctx * ps + mode_he + mode_de + (1 + ps || model) + (1 | model:ctx) + (1 | model:ctx:ps) + (1 | prompt_id)
#   F  modo m + control:   refuse ~ ctx * ps + (1 + ps || model) + (1 | model:ctx) + (1 | model:ctx:ps) + (1 | prompt_id)
#   Variante 2 si la primera no converge: sin los dos interceptos por modelo × contexto.
#   Protocolo del 16/09 (glmm_common.R): bobyqa y nlminbwrap con maxfun por defecto; Wald; un ajuste
#   singular cuenta como convergido.
#
# Uso:  Rscript glmm_context.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, prompt_id, model, ctx (entero 1..8 en el orden del cuaderno).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_context.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
d$ps <- as.integer(d$mode != "control")
d$mode_he <- as.integer(d$mode == "he")
d$mode_de <- as.integer(d$mode == "de")
K <- 8
d$ctx <- factor(d$ctx, levels = 1:K)
contrasts(d$ctx) <- contr.sum(K)
d$model_ctx <- factor(paste(d$model, d$ctx, sep = ":"))
d$model_ctx_ps <- factor(paste(d$model, d$ctx, d$ps, sep = ":"))
re_full <- "(1 + ps || model) + (1 | model_ctx) + (1 | model_ctx_ps) + (1 | prompt_id)"
re_min  <- "(1 + ps || model) + (1 | prompt_id)"
forms <- function(fixed) lapply(c(re_full, re_min), function(re) as.formula(paste(fixed, "+", re)))

L <- rbind(diag(K - 1), rep(-1, K - 1))   # 8 desviaciones desde los 7 coeficientes suma-cero

one_ctx <- function(key, dd) {
  fixed <- if (key == "E_ps_vs_control") "refuse ~ ctx * ps + mode_he + mode_de" else "refuse ~ ctx * ps"
  fulls <- forms(fixed)
  res <- tryCatch({
    t0 <- Sys.time()
    f1 <- fit_any(fulls, dd); m <- f1$m
    secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
    s <- summary(m)$coefficients
    V <- as.matrix(vcov(m))
    idx <- grep("^ctx[0-9]+:ps$", rownames(s))
    b <- s[idx, "Estimate"]; Vb <- V[idx, idx]
    W <- as.numeric(t(b) %*% solve(Vb) %*% b)
    dev <- as.numeric(L %*% b); dse <- sqrt(diag(L %*% Vb %*% t(L)))
    dz <- dev / dse; dp <- 2 * pnorm(-abs(dz)); dbh <- p.adjust(dp, method = "BH")
    meta <- data.frame(fit = key,
                       sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
                       sd_model_ps = vc_sd(m, "model", "ps"),
                       sd_model_ctx = vc_sd(m, "model_ctx", "(Intercept)"), sd_model_ctx_ps = vc_sd(m, "model_ctx_ps", "(Intercept)"),
                       singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "),
                       optimizer = f1$optimizer, formula_used = paste(deparse(fulls[[f1$variant]]), collapse = ""),
                       variant = f1$variant, fit_seconds = round(secs, 1), loglik = as.numeric(logLik(m)), nobs = nobs(m),
                       n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
                       error = "", stringsAsFactors = FALSE)
    rbind(
      cbind(data.frame(kind = "coef", term = rownames(s), ctx = NA, estimate = s[, "Estimate"], se = s[, "Std. Error"],
                       z = s[, "z value"], p = s[, "Pr(>|z|)"], p_bh = NA, df = NA, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "omnibus", term = "ctx:ps", ctx = NA, estimate = W, se = NA, z = NA,
                       p = pchisq(W, df = K - 1, lower.tail = FALSE), p_bh = NA, df = K - 1, stringsAsFactors = FALSE), meta, row.names = NULL),
      cbind(data.frame(kind = "ctx_dev", term = "ctx:ps", ctx = 1:K, estimate = dev, se = dse, z = dz, p = dp, p_bh = dbh, df = NA,
                       stringsAsFactors = FALSE), meta, row.names = NULL))
  }, error = function(e) {
    data.frame(kind = "error", term = NA, ctx = NA, estimate = NA, se = NA, z = NA, p = NA, p_bh = NA, df = NA,
               fit = key, sd_prompt = NA, sd_model = NA, sd_model_ps = NA, sd_model_ctx = NA, sd_model_ctx_ps = NA,
               singular = NA, messages = "", optimizer = NA, formula_used = NA, variant = NA, fit_seconds = NA,
               loglik = NA, nobs = nrow(dd), n_prompts = nlevels(droplevels(dd$prompt_id)),
               n_models = nlevels(droplevels(dd$model)), error = conditionMessage(e), stringsAsFactors = FALSE)
  })
  om <- res[res$kind == "omnibus", ]
  cat(sprintf("%-22s %s\n", key, if (nrow(om) == 0) paste("ERROR", res$error[1]) else
              sprintf("omnibus chi2(7) = %.2f p = %.3g  sd_prompt %.2f sd_model %.2f sd_ps %.2f sd_mctx %.2f sd_mctxps %.2f  [%s, v%d, %.0fs]%s%s",
                      om$estimate, om$p, om$sd_prompt, om$sd_model, om$sd_model_ps, om$sd_model_ctx, om$sd_model_ctx_ps,
                      om$optimizer, om$variant, om$fit_seconds,
                      if (isTRUE(om$singular)) "  SINGULAR" else "",
                      if (nzchar(om$messages)) paste0("  [", om$messages, "]") else "")))
  flush(stdout())
  res
}

fits <- list()
fits[["E_ps_vs_control"]] <- one_ctx("E_ps_vs_control", d)
for (md in c("he", "de", "pg")) {
  dd <- droplevels(d[d$mode %in% c(md, "control"), ])
  dd$ctx <- factor(dd$ctx, levels = 1:K); contrasts(dd$ctx) <- contr.sum(K)
  fits[[paste0("F_", md, "_vs_control")]] <- one_ctx(paste0("F_", md, "_vs_control"), dd)
}
finish(fits, args[2])
