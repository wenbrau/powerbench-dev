#!/usr/bin/env Rscript
# glmm_ai_bias.R -- Figura 4 (D3 vs D1): GLMM confirmatorio del DiD del bloque 18, analogo a los
# ajustes E/F del panel 1 de Figura 1 (bloque 30, glmm_origin.R). Scratch de fig4_working/ (pedido
# de Wendy, 2026-09-18): no es un bloque numerado todavia.
#
# refuse ~ ai (1 = D3/agente IA, 0 = D1/persona) x ps (1 = he/de/pg, 0 = control) [x cn (1 = modelo
# chino)] + mode_he + mode_de (referencia pg; ausentes en los ajustes por modo, que ya son de 2
# niveles), con interceptos aleatorios cruzados por prompt y por modelo, y pendiente aleatoria del
# termino ai:ps por modelo -- es ese termino el que se prueba, asi que sin la pendiente por modelo
# el test pseudorreplicaria (mismo argumento que la pendiente de ps en glmm_origin.R E/F, aplicado
# aca al contraste ai:ps en vez de cn:ps).
#
#   E_ai_ps            pooled (he+de+pg vs control), termino ai:ps       -- la brecha D3-D1 es mayor
#                                                                            en power shifting que en
#                                                                            control? (confirma el
#                                                                            DiD pooled del bloque 18)
#   F_<modo>_vs_ctl     modo m + control, termino ai:ps                  -- lo mismo, un modo a la vez
#   E_ai_ps_cn          E_ai_ps + cn, termino ai:ps:cn                   -- esa brecha difiere CN vs US?
#   F_<modo>_vs_ctl_cn  F_<modo>_vs_ctl + cn, termino ai:ps:cn
#
# Protocolo (el de glmm_common.R, decision de Nico 16/09 para Figura 1): variante sin correlaciones
# (||) primero, correlacionada solo si no converge; bobyqa y nlminbwrap; Wald, nAGQ = 0; un ajuste
# singular cuenta como convergido. Cadena de respaldo propia de este script si ai:ps por modelo no
# converge: cae a solo (1+ai||model), despues a (1|model) -- ver el orden de las listas abajo.
#
# Uso:  Rscript glmm_ai_bias.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), ai (0/1), ps (0/1), cn (0/1), mode_he, mode_de (0/1),
# prompt_id, model.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_ai_bias.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "..", "..", "r", "glmm_common.R"))

d <- read_input(args[1])
d$ai <- as.integer(d$ai)
d$ps <- as.integer(d$ps)
d$cn <- as.integer(d$cn)
d$mode_he <- as.integer(d$mode_he)
d$mode_de <- as.integer(d$mode_de)
d$mode3 <- ifelse(d$ps == 0, "ctl", ifelse(d$mode_he == 1, "he", ifelse(d$mode_de == 1, "de", "pg")))

fits <- list()

pooled_formulas <- function(extra_rhs) {
  # extra_rhs: "" para el pooled sin origen, " * cn" para el pooled con origen
  list(
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + mode_he + mode_de + (1 + ai + ai:ps || model) + (1 | prompt_id)")),
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + mode_he + mode_de + (1 + ai:ps || model) + (1 | prompt_id)")),
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + mode_he + mode_de + (1 + ai || model) + (1 | prompt_id)")),
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + mode_he + mode_de + (1 | model) + (1 | prompt_id)"))
  )
}
permode_formulas <- function(extra_rhs) {
  list(
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + (1 + ai + ai:ps || model) + (1 | prompt_id)")),
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + (1 + ai:ps || model) + (1 | prompt_id)")),
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + (1 + ai || model) + (1 | prompt_id)")),
    as.formula(paste0("refuse ~ ai * ps", extra_rhs, " + (1 | model) + (1 | prompt_id)"))
  )
}

# ---- sin origen: termino ai:ps
fits[["E_ai_ps"]] <- one("E_ai_ps", d, pooled_formulas(""), "ai:ps", slope = "ai:ps")
for (m in c("he", "de", "pg")) {
  dd <- droplevels(d[d$mode3 %in% c(m, "ctl"), ])
  fits[[paste0("F_", m, "_vs_ctl")]] <- one(paste0("F_", m, "_vs_ctl"), dd, permode_formulas(""), "ai:ps", slope = "ai:ps")
}

# ---- con origen: termino ai:ps:cn (la brecha ai:ps, CN vs US)
fits[["E_ai_ps_cn"]] <- one("E_ai_ps_cn", d, pooled_formulas(" * cn"), "ai:ps:cn", slope = "ai:ps")
for (m in c("he", "de", "pg")) {
  dd <- droplevels(d[d$mode3 %in% c(m, "ctl"), ])
  fits[[paste0("F_", m, "_vs_ctl_cn")]] <- one(paste0("F_", m, "_vs_ctl_cn"), dd, permode_formulas(" * cn"), "ai:ps:cn", slope = "ai:ps")
}

finish(fits, args[2])
