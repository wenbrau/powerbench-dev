# glmm_common.R — piezas compartidas por los scripts glmm_*.R (bloques 30, 31): ajuste con lme4::glmer,
# secuencia de optimizadores, extracción de SD de efectos aleatorios y salida en formato largo.
# Se carga con source() desde cada script; no se ejecuta solo.
#
# Protocolo (decisión de Nico, 16/09, para acelerar sin perder rigor): (1) cuando hay pendientes
# aleatorias, se ajusta PRIMERO la variante sin correlaciones (||) y solo si no converge la correlacionada;
# (2) dos optimizadores, bobyqa y nlminbwrap (el que rescató el ajuste de control en el bloque 30);
# (3) inferencia de Wald (z = coeficiente / SE), sin LRT. El bloque 30 (origen y modos) se calculó antes
# de esta decisión con la variante correlacionada primero, cuatro optimizadores y LRT; sus tablas
# conservan esas columnas.

suppressPackageStartupMessages(library(lme4))

# maxfun por defecto (10.000): hasta el 16/09 19:05 estaba en 2e5, y eso convertía un ajuste que no
# cierra en horas de optimizador en vez de un aviso rápido de no convergencia (señalado por Nico).
optimizers <- list(
  list(name = "bobyqa",     ctrl = glmerControl(optimizer = "bobyqa")),
  list(name = "nlminbwrap", ctrl = glmerControl(optimizer = "nlminbwrap"))
)
msgs_of <- function(m) unlist(m@optinfo$conv$lme4$messages)
is_sing_msg <- function(x) grepl("singular", x, fixed = TRUE)
clean <- function(m) { x <- msgs_of(m); length(x[!is_sing_msg(x)]) == 0 }

# formulas: lista de variantes en el orden en que se prueban (la estructura aleatoria más completa
# primero, en su versión ||). Se queda con el primer ajuste sin avisos de convergencia; un ajuste
# singular (alguna varianza en 0) CUENTA como convergido y se acepta, marcado singular, antes que pasar a
# una estructura aleatoria más chica: para testear efectos fijos es la opción conservadora (mantener las
# pendientes por modelo aunque alguna sea 0). Solo si ningún optimizador converge en una variante se
# prueba la siguiente; si ninguna converge, se devuelve el último ajuste con sus avisos.
# (Hasta las 17:55 del 16/09 la regla prefería una variante más chica no singular a la completa
# singular; se cambió porque el bloque 33 caía a "solo intercepto por modelo" en los tres modos.)
# nAGQ = 0 (decisión de Nico, 16/09 19:30: "nAGQ para todo desde ahora"): los efectos fijos se estiman
# dentro del paso interno (PIRLS) y el optimizador externo solo mueve las varianzas. Es la aproximación
# que glmer usa como primera etapa; con 18 efectos fijos el ajuste de contexto pasa de 240 s a 24 s y
# el estadístico ómnibus cambia poco (χ² 6,8 → 4,7, misma conclusión). Los bloques 30–33 se recorrieron
# todos con nAGQ = 0 para que la Figura 1 tenga un solo estimador; se declara en métodos.
NAGQ <- 0
fit_any <- function(formulas, dd) {
  for (fi in seq_along(formulas)) {
    for (o in optimizers) {
      m <- suppressWarnings(glmer(formulas[[fi]], data = dd, family = binomial, control = o$ctrl, nAGQ = NAGQ))
      if (clean(m)) return(list(m = m, optimizer = o$name, variant = fi))
    }
  }
  list(m = m, optimizer = o$name, variant = fi)
}

# SD (o correlación, si var2 se da) de un efecto aleatorio. grp se compara exacto o como grp.N, porque
# con || lme4 nombra los términos model, model.1, model.2, ... (y "model:ctx" NO debe confundirse con "model").
vc_sd <- function(m, grp, var1, var2 = NA) {
  vc <- as.data.frame(VarCorr(m))
  sel <- (vc$grp == grp | grepl(paste0("^", grp, ".[0-9]+$"), vc$grp)) & !is.na(vc$var1) & vc$var1 == var1 &
    (if (is.na(var2)) is.na(vc$var2) else !is.na(vc$var2) & vc$var2 == var2)
  if (any(sel, na.rm = TRUE)) vc$sdcor[which(sel)[1]] else NA_real_
}

# Un ajuste: fulls es la lista de variantes de fórmula; term es el efecto fijo de interés (Wald);
# slope, si se da, es el nombre del efecto aleatorio por modelo cuya SD se reporta.
one <- function(key, dd, fulls, term, slope = NULL) {
  res <- tryCatch({
    f1 <- fit_any(fulls, dd); m <- f1$m
    s <- summary(m)$coefficients
    data.frame(fit = key, term = rownames(s), estimate = s[, "Estimate"], se = s[, "Std. Error"],
               z = s[, "z value"], p = s[, "Pr(>|z|)"],
               sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
               sd_model_slope = if (is.null(slope)) NA_real_ else vc_sd(m, "model", slope),
               cor_model_int_slope = if (is.null(slope)) NA_real_ else vc_sd(m, "model", "(Intercept)", slope),
               slope_name = if (is.null(slope)) "" else slope,
               singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "),
               optimizer = f1$optimizer, formula_used = paste(deparse(fulls[[f1$variant]]), collapse = ""),
               variant = f1$variant, loglik = as.numeric(logLik(m)), nobs = nobs(m),
               n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
               term_interest = term, error = "", row.names = NULL, stringsAsFactors = FALSE)
  }, error = function(e) {
    data.frame(fit = key, term = NA, estimate = NA, se = NA, z = NA, p = NA, sd_prompt = NA, sd_model = NA,
               sd_model_slope = NA, cor_model_int_slope = NA, slope_name = if (is.null(slope)) "" else slope,
               singular = NA, messages = "", optimizer = NA, formula_used = NA, variant = NA,
               loglik = NA, nobs = nrow(dd),
               n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
               term_interest = term, error = conditionMessage(e), row.names = NULL, stringsAsFactors = FALSE)
  })
  cat(sprintf("%-24s %s\n", key, if (nzchar(res$error[1])) paste("ERROR", res$error[1]) else
              sprintf("%s %+.3f (se %.3f, p %.3g)  sd_prompt %.2f sd_model %.2f%s  [%s, v%d]%s%s",
                      term, res$estimate[res$term == term], res$se[res$term == term], res$p[res$term == term],
                      res$sd_prompt[1], res$sd_model[1],
                      if (is.na(res$sd_model_slope[1])) "" else sprintf(" sd_slope %.2f", res$sd_model_slope[1]),
                      res$optimizer[1], res$variant[1],
                      if (isTRUE(res$singular[1])) "  SINGULAR" else "",
                      if (nzchar(res$messages[1])) paste0("  [", res$messages[1], "]") else "")))
  flush(stdout())
  res
}

finish <- function(fits, outfile) {
  out <- do.call(rbind, fits)
  out$lme4_version <- as.character(packageVersion("lme4"))
  out$r_version <- R.version.string
  write.csv(out, outfile, row.names = FALSE)
  cat("wrote", outfile, "\n")
}

read_input <- function(infile) {
  d <- read.csv(infile, stringsAsFactors = FALSE)
  d$model <- factor(d$model)
  d$prompt_id <- factor(d$prompt_id)
  d
}
