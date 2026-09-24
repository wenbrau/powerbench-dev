#!/usr/bin/env Rscript
# glmm_ai_main.R — Figura de IA (D3 agente IA vs D1 humano): efecto PRINCIPAL del usuario IA por modo con el GLMM de modelos
# aleatorios del protocolo (glmm_common.R), para COMPARAR con los paneles A (bootstrap sobre prompts, bloque 54) y B (t entre
# 23 modelos, bloque 56) de la figura cerrada por Nico. Pedido de Wendy (2026-09-20): "hacer versión GLMM para comparar", sin
# reemplazar la figura. Lo llaman analysis_85_fig3a_glmm.py (bloque 85, tabla oficial) y review_fig_aiagent_glmm/compare_ai_glmm.py.
#
# Por modo:  refuse ~ ai + (1 + ai || model) + (1 | prompt_id),  ai = +0,5 usuario IA (D3), −0,5 humano (D1 inglés).
#   - log-OR y OR de refusal IA vs humano, Wald (panel B análogo, en la escala del OR).
#   - pp MARGINALES: p(IA), p(humano) y Δ pp integrando logistic(eta + u) sobre u ~ N(0, var(prompt) + var(model) +
#     0,25·var(pendiente ai)); IC de Δ por simulación de los efectos fijos ~ MVN(fixef, vcov) (panel A análogo).
# Protocolo de glmm_common.R: nAGQ = 1, || primero y correlacionada si no converge, bobyqa y nlminbwrap, Wald, singular aceptado.
#
# Uso:  Rscript glmm_ai_main.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, ai (+0.5 / -0.5), prompt_id, model.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_ai_main.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))
set.seed(22)

d <- read_input(args[1])
gu <- seq(-6, 6, length.out = 801); gw <- dnorm(gu) * (gu[2] - gu[1]); gw <- gw / sum(gw)
pmarg <- function(b0, b1, s, sigma) sum(plogis(b0 + s * b1 + gu * sigma) * gw)

out <- data.frame()
for (md in c("he", "de", "pg", "control")) {
  dd <- droplevels(d[d$mode == md, ])
  f <- function(corr) as.formula(paste("refuse ~ ai", if (corr) "+ (1 + ai | model)" else "+ (1 + ai || model)", "+ (1 | prompt_id)"))
  f1 <- fit_any(list(f(FALSE), f(TRUE)), dd); m <- f1$m
  b <- fixef(m); V <- as.matrix(vcov(m)); se <- sqrt(diag(V))
  s2 <- vc_sd(m, "prompt_id", "(Intercept)")^2 + vc_sd(m, "model", "(Intercept)")^2 + 0.25 * vc_sd(m, "model", "ai")^2
  s2[is.na(s2)] <- 0; sigma <- sqrt(s2)
  p_ai <- pmarg(b["(Intercept)"], b["ai"], 0.5, sigma); p_hu <- pmarg(b["(Intercept)"], b["ai"], -0.5, sigma)
  L <- t(chol(V)); S <- 4000; dstar <- numeric(S)
  for (i in seq_len(S)) {
    bs <- b + as.numeric(L %*% rnorm(length(b))); names(bs) <- names(b)
    dstar[i] <- pmarg(bs["(Intercept)"], bs["ai"], 0.5, sigma) - pmarg(bs["(Intercept)"], bs["ai"], -0.5, sigma)
  }
  ci <- quantile(dstar, c(.025, .975))
  out <- rbind(out, data.frame(
    mode = md, estimate = unname(b["ai"]), se = unname(se["ai"]), z = unname(b["ai"] / se["ai"]),
    p = unname(2 * pnorm(-abs(b["ai"] / se["ai"]))),
    OR = exp(unname(b["ai"])), OR_lo = exp(unname(b["ai"] - 1.96 * se["ai"])), OR_hi = exp(unname(b["ai"] + 1.96 * se["ai"])),
    p_ai_pp = 100 * p_ai, p_human_pp = 100 * p_hu, delta_pp = 100 * (p_ai - p_hu), delta_lo = 100 * ci[[1]], delta_hi = 100 * ci[[2]],
    sd_model_slope = vc_sd(m, "model", "ai"), sd_model = vc_sd(m, "model", "(Intercept)"), sd_prompt = vc_sd(m, "prompt_id", "(Intercept)"),
    sigma_tot = sigma, singular = isSingular(m), optimizer = f1$optimizer, variant = f1$variant,
    formula_used = paste(deparse(formula(m)), collapse = ""), nobs = nobs(m), n_models = length(unique(dd$model)),
    n_prompts = length(unique(dd$prompt_id)), lme4_version = as.character(packageVersion("lme4")), r_version = R.version.string,
    stringsAsFactors = FALSE))
  cat(sprintf("%-8s OR %.3f [%.3f, %.3f] p %.2g | pp IA %.2f humano %.2f delta %+.2f [%+.2f, %+.2f] | sd_slope %.2f%s [%s, v%d]\n",
              md, exp(b["ai"]), exp(b["ai"] - 1.96 * se["ai"]), exp(b["ai"] + 1.96 * se["ai"]), out$p[nrow(out)],
              100 * p_ai, 100 * p_hu, 100 * (p_ai - p_hu), 100 * ci[[1]], 100 * ci[[2]], vc_sd(m, "model", "ai"),
              if (isSingular(m)) " SINGULAR" else "", f1$optimizer, f1$variant))
  flush(stdout())
}
write.csv(out, args[2], row.names = FALSE)
