#!/usr/bin/env Rscript
# principal_curve.R — curva principal (Hastie & Stuetzle 1989, paquete princurve) sobre los dos ejes del índice geopolítico
# (axis_us, axis_cn), para construir una versión 1D no lineal del índice. Pedido de Nico (18/09): "calcular un subespacio 1D
# no lineal en el que proyectar los puntos para crear esta versión 1D del índice, que vaya de -1 a 1 entre los extremos del
# subespacio". Lo llama analysis_47_alignment_index_1d.py. No se escribe ningún estimador propio: princurve::principal_curve.
#
# Para cada grado de libertad del suavizador (df) pedido: ajuste, proyección de cada país sobre la curva (s), posición en
# longitud de arco (lambda), distancia a la curva y convergencia. La curva arranca en la primera componente principal.
#
# Uso:  Rscript principal_curve.R <datos.csv> <salida.csv> <df1,df2,...>
# datos.csv: columnas iso3, axis_us, axis_cn.

suppressPackageStartupMessages(library(princurve))
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) stop("uso: Rscript principal_curve.R <datos.csv> <salida.csv> <df1,df2,...>")
d <- read.csv(args[1], stringsAsFactors = FALSE)
X <- as.matrix(d[, c("axis_us", "axis_cn")])
dfs <- as.numeric(strsplit(args[3], ",")[[1]])
out <- list()
for (df in dfs) {
  set.seed(47)
  fit <- principal_curve(X, df = df, smoother = "smooth_spline", stretch = 2, maxit = 100, thresh = 1e-4)
  out[[as.character(df)]] <- data.frame(iso3 = d$iso3, df = df, lambda = fit$lambda, s_us = fit$s[, 1], s_cn = fit$s[, 2],
                                        dist_point = sqrt(rowSums((X - fit$s)^2)), order = order(fit$ord),
                                        converged = fit$converged, iterations = fit$num_iterations, total_dist = fit$dist,
                                        stringsAsFactors = FALSE)
  cat(sprintf("df %g: convergió %s en %d iteraciones; suma de distancias al cuadrado %.4f; longitud de arco %.3f\n",
              df, fit$converged, fit$num_iterations, fit$dist, max(fit$lambda) - min(fit$lambda)))
}
res <- do.call(rbind, out)
res$princurve_version <- as.character(packageVersion("princurve"))
write.csv(res, args[2], row.names = FALSE)
cat("wrote", args[2], "\n")
