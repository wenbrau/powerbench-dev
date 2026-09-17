#!/usr/bin/env Rscript
# glmm_factor.R — Figura 1, paneles 2 y 3: ¿el refusal cambia con la escala del target (o con el
# standing del usuario), y ese cambio es específico de power shifting?  (bloque 31; lo llama
# analysis_31_fig1_factor_glmm.py, que exporta los datos con x = nivel ordenado 0, 1, 2 y lee la salida)
#
# Regresión logística mixta con lme4::glmer (Laplace, nAGQ = 1). x es el factor ordenado codificado
# como número (individual/group/society = 0/1/2; low/med/high = 0/1/2), así que el coeficiente de x es
# la tendencia lineal en log-odds por nivel (pedido de Nico: "factores ordenados, para poder hacer
# regresión"). ps = 1 para he/de/pg, 0 para control; xps = x * ps.
#
#   A  por modo (he, de, pg, control):   refuse ~ x + (1 + x || model) + (1 | prompt_id)                término x
#   B  power shifting (he + de + pg):    refuse ~ x + mode + (1 + x || model) + (1 | prompt_id)         término x
#   E  interacción, power shifting vs control (los cuatro modos):
#        refuse ~ x * ps + mode_he + mode_de + (1 + x + ps + xps || model) + (1 | prompt_id)           término x:ps
#   F  interacción por modo (modo m + control):
#        refuse ~ x * ps + (1 + x + ps + xps || model) + (1 | prompt_id)                               término x:ps
#   Las pendientes aleatorias por modelo (x; y x, ps, xps en E/F) evitan pseudorreplicar contrastes que
#   son dentro del modelo. Protocolo del 16/09 (glmm_common.R): variante sin correlaciones primero y la
#   correlacionada solo si aquella no converge; bobyqa y nlminbwrap; Wald, sin LRT.
#
# Uso:  Rscript glmm_factor.R <datos.csv> <salida.csv>
# datos.csv: columnas refuse (0/1), mode, prompt_id, model, x (0, 1, 2).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("uso: Rscript glmm_factor.R <datos.csv> <salida.csv>")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)[1]))
source(file.path(here, "glmm_common.R"))

d <- read_input(args[1])
d$ps <- as.integer(d$mode != "control")
d$xps <- d$x * d$ps
d$mode_he <- as.integer(d$mode == "he")
d$mode_de <- as.integer(d$mode == "de")

fits <- list()
for (md in c("he", "de", "pg", "control")) {
  dd <- droplevels(d[d$mode == md, ])
  fits[[paste0("A_", md)]] <- one(paste0("A_", md), dd,
    list(refuse ~ x + (1 + x || model) + (1 | prompt_id), refuse ~ x + (1 + x | model) + (1 | prompt_id)),
    "x", slope = "x")
}
dd <- droplevels(d[d$mode %in% c("he", "de", "pg"), ])
dd$mode <- relevel(factor(dd$mode), ref = "pg")
fits[["B_power_shifting"]] <- one("B_power_shifting", dd,
  list(refuse ~ x + mode + (1 + x || model) + (1 | prompt_id), refuse ~ x + mode + (1 + x | model) + (1 | prompt_id)),
  "x", slope = "x")

fits[["E_ps_vs_control"]] <- one("E_ps_vs_control", d,
  list(refuse ~ x * ps + mode_he + mode_de + (1 + x + ps + xps || model) + (1 | prompt_id),
       refuse ~ x * ps + mode_he + mode_de + (1 + x + ps + xps | model) + (1 | prompt_id)),
  "x:ps", slope = "xps")
for (md in c("he", "de", "pg")) {
  dd <- droplevels(d[d$mode %in% c(md, "control"), ])
  fits[[paste0("F_", md, "_vs_control")]] <- one(paste0("F_", md, "_vs_control"), dd,
    list(refuse ~ x * ps + (1 + x + ps + xps || model) + (1 | prompt_id),
         refuse ~ x * ps + (1 + x + ps + xps | model) + (1 | prompt_id)),
    "x:ps", slope = "xps")
}
finish(fits, args[2])
