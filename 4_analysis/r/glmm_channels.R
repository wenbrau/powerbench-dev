#!/usr/bin/env Rscript
# glmm_channels.R — D2: separar el canal del USUARIO y el del AFECTADO en el efecto de la nacionalidad (bloque 101; lo llama
# analysis_101_nationality_channels.py). Pedido de Nico (26/09, tras los reviews): "corré el GLMM que decís".
#
# Cada contraste recíproco del paper (país X como usuario contra X como afectado) cambia a la vez el país del usuario y el del
# afectado. Las 18 condiciones combinan cinco grupos de país (US, alineados con US, neutrales, alineados con China, China) en
# ambos roles de forma conectada, así que un modelo aditivo con un efecto del grupo del usuario y otro del grupo del afectado
# está identificado.
#
# Grupos con contrastes suma-cero (contr.sum): cada coeficiente es la desviación de un grupo respecto de la media de los cinco;
# el 5º (China) se deriva como −(suma de los otros 4), con su varianza desde vcov. Ómnibus por canal: Wald conjunto b' V⁻¹ b
# sobre los 4 coeficientes, χ² con 4 gl. Contrastes: China − US y bloque chino − bloque US ((China + alineados con China)/2 −
# (US + alineados con US)/2), para cada canal.
#
#   A  por modo (he, de, pg, control):
#        refuse ~ ugrp + tgrp + (1 | model) + (1 | model:ugrp) + (1 | model:tgrp) + (1 | prompt_id)
#   E  interacción con power shifting vs control (los cuatro modos):
#        refuse ~ (ugrp + tgrp) * ps + mode_he + mode_de + (1 + ps || model) + (1 | model:ugrp) + (1 | model:tgrp)
#                 + (1 | model:ugrp:ps) + (1 | model:tgrp:ps) + (1 | prompt_id)
#   F  interacción por modo (modo m + control): lo mismo sin mode_he, mode_de.
#   Efectos aleatorios como en glmm_context.R: el intercepto por modelo × grupo es el perfil propio de cada modelo, y el de
#   modelo × grupo × ps su desviación propia en la interacción (lo que protege esos tests de pseudorreplicar). Variante 2 si la
#   primera no converge: sin los interceptos por modelo × grupo. Protocolo de glmm_common.R: nAGQ = 1, bobyqa y nlminbwrap,
#   Wald, ajuste singular aceptado.
#
# Uso:  Rscript glmm_channels.R <datos.csv> <salida.csv> <A|E|F>
# datos.csv: columnas refuse (0/1), mode, prompt_id, model, ugrp, tgrp (US, USal, neu, CNal, CN).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) stop("uso: Rscript glmm_channels.R <datos.csv> <salida.csv> <A|E|F>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

G <- c("US", "USal", "neu", "CNal", "CN")
K <- length(G)
d <- read_input(args[1])
d$ugrp <- factor(d$ugrp, levels = G); contrasts(d$ugrp) <- contr.sum(K)
d$tgrp <- factor(d$tgrp, levels = G); contrasts(d$tgrp) <- contr.sum(K)
d$ps <- as.integer(d$mode != "control")
d$mode_he <- as.integer(d$mode == "he")
d$mode_de <- as.integer(d$mode == "de")
d$model_u <- factor(paste(d$model, d$ugrp, sep = ":"))
d$model_t <- factor(paste(d$model, d$tgrp, sep = ":"))
d$model_u_ps <- factor(paste(d$model, d$ugrp, d$ps, sep = ":"))
d$model_t_ps <- factor(paste(d$model, d$tgrp, d$ps, sep = ":"))

L <- rbind(diag(K - 1), rep(-1, K - 1))            # 5 desviaciones desde los 4 coeficientes suma-cero
W <- rbind(CN_minus_US = c(-1, 0, 0, 0, 1),         # sobre las 5 desviaciones, en el orden de G
           bloc_CN_minus_US = c(-.5, -.5, 0, .5, .5))

summarise_channel <- function(b, V, idx, channel, key, meta) {
  bb <- b[idx]; Vb <- V[idx, idx]
  chi <- as.numeric(t(bb) %*% solve(Vb) %*% bb)
  dev <- as.numeric(L %*% bb); dse <- sqrt(diag(L %*% Vb %*% t(L)))
  out <- data.frame(fit = key, channel = channel, quantity = paste0("dev_", G), estimate = dev, se = dse,
                    z = dev / dse, p = 2 * pnorm(-abs(dev / dse)), chisq = NA, df = NA, stringsAsFactors = FALSE)
  for (w in rownames(W)) {
    lw <- as.numeric(W[w, ] %*% L); est <- sum(lw * bb); se <- sqrt(as.numeric(t(lw) %*% Vb %*% lw))
    out <- rbind(out, data.frame(fit = key, channel = channel, quantity = w, estimate = est, se = se, z = est / se,
                                 p = 2 * pnorm(-abs(est / se)), chisq = NA, df = NA, stringsAsFactors = FALSE))
  }
  out <- rbind(out, data.frame(fit = key, channel = channel, quantity = "omnibus", estimate = NA, se = NA, z = NA,
                               p = pchisq(chi, K - 1, lower.tail = FALSE), chisq = chi, df = K - 1, stringsAsFactors = FALSE))
  cbind(out, meta)
}

fit_key <- function(key, dd, fixed, re_list, interaction) {
  t0 <- Sys.time()
  res <- tryCatch({
    f1 <- fit_any(lapply(re_list, function(re) as.formula(paste(fixed, "+", re))), dd); m <- f1$m
    secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
    b <- fixef(m); V <- as.matrix(vcov(m)); nm <- names(b)
    iu <- if (interaction) grep("^ugrp[0-9]+:ps$", nm) else grep("^ugrp[0-9]+$", nm)
    it <- if (interaction) grep("^tgrp[0-9]+:ps$", nm) else grep("^tgrp[0-9]+$", nm)
    meta <- data.frame(singular = isSingular(m), messages = paste(msgs_of(m), collapse = " | "), optimizer = f1$optimizer,
                       variant = f1$variant, formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m),
                       n_prompts = nlevels(droplevels(dd$prompt_id)), n_models = nlevels(droplevels(dd$model)),
                       sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"), sd_model = vc_sd(m, "model", "(Intercept)"),
                       sd_model_u = vc_sd(m, "model_u", "(Intercept)"), sd_model_t = vc_sd(m, "model_t", "(Intercept)"),
                       seconds = secs, error = "", stringsAsFactors = FALSE)
    rbind(summarise_channel(b, V, iu, "user", key, meta), summarise_channel(b, V, it, "target", key, meta))
  }, error = function(e) {
    data.frame(fit = key, channel = NA, quantity = NA, estimate = NA, se = NA, z = NA, p = NA, chisq = NA, df = NA,
               singular = NA, messages = "", optimizer = NA, variant = NA, formula_used = NA, nobs = nrow(dd),
               n_prompts = NA, n_models = NA, sd_prompt = NA, sd_model = NA, sd_model_u = NA, sd_model_t = NA,
               seconds = as.numeric(difftime(Sys.time(), t0, units = "secs")), error = conditionMessage(e),
               stringsAsFactors = FALSE)
  })
  om <- res[res$quantity %in% "omnibus", ]
  cat(sprintf("%-22s %s  (%.0f s)\n", key,
              if (nzchar(res$error[1])) paste("ERROR", res$error[1]) else
                paste(sprintf("%s chi2 %.1f p %.3g", om$channel, om$chisq, om$p), collapse = "; "), res$seconds[1]))
  flush(stdout())
  res
}

what <- args[3]
fits <- list()
if (what == "A") {
  re <- c("(1 | model) + (1 | model_u) + (1 | model_t) + (1 | prompt_id)", "(1 | model) + (1 | prompt_id)")
  for (md in c("he", "de", "pg", "control")) {
    if (!any(d$mode == md)) next
    dd <- droplevels(d[d$mode == md, ])
    contrasts(dd$ugrp) <- contr.sum(K); contrasts(dd$tgrp) <- contr.sum(K)
    fits[[md]] <- fit_key(paste0("A_", md), dd, "refuse ~ ugrp + tgrp", re, FALSE)
  }
} else {
  re <- c("(1 + ps || model) + (1 | model_u) + (1 | model_t) + (1 | model_u_ps) + (1 | model_t_ps) + (1 | prompt_id)",
          "(1 + ps || model) + (1 | prompt_id)")
  if (what == "E") {
    fits[["E"]] <- fit_key("E_ps_vs_control", d, "refuse ~ (ugrp + tgrp) * ps + mode_he + mode_de", re, TRUE)
  } else {
    for (md in c("he", "de", "pg")) {
      if (!any(d$mode == md)) next
      dd <- droplevels(d[d$mode %in% c(md, "control"), ])
      contrasts(dd$ugrp) <- contr.sum(K); contrasts(dd$tgrp) <- contr.sum(K)
      fits[[md]] <- fit_key(paste0("F_", md, "_vs_control"), dd, "refuse ~ (ugrp + tgrp) * ps", re, TRUE)
    }
  }
}
out <- do.call(rbind, fits)
out$lme4_version <- as.character(packageVersion("lme4"))
out$r_version <- R.version.string
write.csv(out, args[2], row.names = FALSE)
cat("wrote", args[2], "\n")
