#!/usr/bin/env python3
"""Panel C (revisión 19/09) — medio heatmap + barras que REFLEJAN el test (bloque 39).

Dos versiones, una por cada nula del bloque 39; cada versión lleva LAS DOS cosas:
  - estrella por barra   = ¿la barra (CN–CN / US–US / mixto) se separa del azar? (per-bar ≠ 0)
  - corchete de origen   = ¿mismo origen acuerda más que mixto? (dentro − mixto)
  - banda gris por barra = intervalo 2,5–97,5 % de la nula (no bootstrap sobre prompts)

  * panelC_test1_{mode}.png  — nula A: permutar los idiomas dentro de cada modelo (5.000).
  * panelC_test2_{mode}.png  — nula B: permutar las etiquetas CN/US entre los 24 modelos (10.000).

Ambas nulas y los estadísticos son exactamente los del bloque 39; acá solo se computan las dos
cantidades (por barra y contraste) bajo cada nula para poder dibujarlas juntas. Los modelos son la
unidad; los 276 pares no se tratan como independientes.

Correr desde la raíz del repo:  python 4_analysis/review_fig_languages/panelC/panelC_with_tests.py [--only <grupo> ...]
Sin llamadas a ninguna API. Grupos: he, de, pg, control y (pedido de Wendy 19/09) power_shifting = he + de + pg juntos
(R(idioma) sobre los 576 prompts por modelo; mismas nulas). Con --only se escribe panelC_test_stats_<grupo>.csv en vez
de panelC_test_stats.csv, para no pisar el de los cuatro modos.
  --redraw   (Wendy, 21/09) no permuta nada: lee panelC_test_stats.csv (los cuatro modos) y redibuja los tiles finales con la
             matriz recalculada (determinista). Desde el 21/09 el tile no lleva el recuadro de barras del acuerdo medio: el
             resultado del test va como nota al pie, con la q de BH sobre los tres tipos de par (igual que el panel F del cuerpo).
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for p in (str(ROOT / "4_analysis"), str(ROOT / "common")):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "powerbench-mpl"))
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import rankdata  # noqa: E402

from pbanalysis.final_panel import load_d1_multilingual, MODES  # noqa: E402

NA, NB, SEED = 5000, 10000, 39
LANGS = ["en", "de", "fr", "es", "pt", "zh", "hi", "sw"]
EXCL_SW = {"nemotron-3.5-lightning", "nova-2-lite"}
PS = "power_shifting"
GROUPS = list(MODES) + [PS]
LABELS = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control",
          PS: "Power shifting (he + de + pg)"}
ORIGIN = {"US": "#326CA0", "CN": "#B44941"}
KINDS = ["CN–CN", "US–US", "mixto"]
CAPS = ROOT / "4_analysis" / "results" / "30_fig1_glmm" / "capability_index.csv"


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "savefig.facecolor": "white"})


def rank_corr(R):
    K = rankdata(R, axis=1)
    K = K - K.mean(1, keepdims=True)
    nrm = np.sqrt((K ** 2).sum(1, keepdims=True))
    with np.errstate(invalid="ignore", divide="ignore"):
        K = K / nrm
    return K @ K.T


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "ns"


def main():
    style()
    df = load_d1_multilingual()
    d = df[df.valid].copy()
    origin = d.drop_duplicates("model").set_index("model").origin
    cap = pd.read_csv(CAPS).set_index("model")["index"]
    models = sorted(origin.index, key=lambda m: (origin[m] != "CN", -cap[m]))
    n = len(models)
    is_cn = np.array([origin[m] == "CN" for m in models])
    excl = np.array([m in EXCL_SW for m in models])
    ncn = int(is_cn.sum())
    upper = np.triu(np.ones((n, n), bool), k=0)

    iu = np.triu_indices(n, 1)
    uses7 = excl[:, None] | excl[None, :]

    def corr_matrix(T):
        C8 = rank_corr(T); C7 = rank_corr(T[:, :7])
        C = np.where(uses7, C7, C8)
        np.fill_diagonal(C, np.nan)
        return C

    def kind_vec(cn):
        a, b = cn[iu[0]], cn[iu[1]]
        return np.where(a & b, "CN–CN", np.where(~a & ~b, "US–US", "mixto"))

    def bars_and_contrast(C, pk):
        vals = C[iu]
        means = {k: float(np.nanmean(vals[pk == k])) for k in KINDS}
        dentro = float(np.nanmean(vals[(pk == "CN–CN") | (pk == "US–US")]))
        mixto = means["mixto"]
        return means, dentro - mixto

    pair_kind = kind_vec(is_cn)
    rng = np.random.default_rng(SEED)

    def perm_within(T):
        Tp = T.copy()
        for r in range(n):
            cols = np.arange(7) if excl[r] else np.arange(8)
            Tp[r, cols] = Tp[r, cols][rng.permutation(cols.size)]
        return Tp

    argv = sys.argv[1:]
    only = argv[argv.index("--only") + 1:] if "--only" in argv else []
    groups = only or GROUPS
    if "--redraw" in argv:
        st = pd.read_csv(HERE / "panelC_test_stats.csv")
        ps_csv = HERE / f"panelC_test_stats_{PS}.csv"          # el de power shifting se corrió con --only y vive en su propio csv
        if ps_csv.is_file():
            st = pd.concat([st, pd.read_csv(ps_csv)], ignore_index=True)
        for mode in [g for g in GROUPS if g in set(st["mode"])]:
            dm = d[d["mode"].isin(["he", "de", "pg"])] if mode == PS else d[d["mode"] == mode]
            cube = np.stack([dm[dm.model == m].pivot(index="prompt_id", columns="lang", values="refuse")
                             .reindex(columns=LANGS).to_numpy(float) for m in models])
            C = corr_matrix(np.nanmean(cube, axis=1))
            s1 = st[(st["mode"] == mode) & (st.test == "test1_langperm")].set_index("quantity")
            s2 = st[(st["mode"] == mode) & (st.test == "test2_blockperm")].set_index("quantity")
            SA = {k: dict(obs=float(s1.loc[k, "observed"]), lo=float(s1.loc[k, "null_lo"]), hi=float(s1.loc[k, "null_hi"]), p=float(s1.loc[k, "p"])) for k in KINDS}
            SA["contrast"] = dict(obs=float(s1.loc["dentro − mixto", "observed"]), p=float(s1.loc["dentro − mixto", "p"]))
            draw_final(mode, C, upper, models, origin, is_cn, ncn, n, SA, float(s2.loc["dentro − mixto", "p"]), HERE / f"panelC_final_{mode}.png")
            print(f"{mode:8s} redibujado desde panelC_test_stats.csv", flush=True)
        return
    rows_stats = []
    for mode in groups:
        dm = d[d["mode"].isin(["he", "de", "pg"])] if mode == PS else d[d["mode"] == mode]
        cube = np.stack([dm[dm.model == m].pivot(index="prompt_id", columns="lang", values="refuse")
                         .reindex(columns=LANGS).to_numpy(float) for m in models])
        T = np.nanmean(cube, axis=1)
        C = corr_matrix(T)
        obs_means, obs_contrast = bars_and_contrast(C, pair_kind)

        # ---- nula A: permutar idiomas dentro de cada modelo ----
        bar_null_A = {k: [] for k in KINDS}; contrast_A = []
        for _ in range(NA):
            Cp = corr_matrix(perm_within(T))
            m_, c_ = bars_and_contrast(Cp, pair_kind)
            for k in KINDS:
                bar_null_A[k].append(m_[k])
            contrast_A.append(c_)
        # ---- nula B: permutar etiquetas CN/US entre modelos (C fijo) ----
        bar_null_B = {k: [] for k in KINDS}; contrast_B = []
        for _ in range(NB):
            pk = kind_vec(rng.permutation(is_cn))
            m_, c_ = bars_and_contrast(C, pk)
            for k in KINDS:
                bar_null_B[k].append(m_[k])
            contrast_B.append(c_)

        def summarize(null_bars, null_contrast, tag):
            out = {}
            for k in KINDS:
                nd = np.array(null_bars[k]); mu = nd.mean()
                p2 = float((np.abs(nd - mu) >= abs(obs_means[k] - mu)).mean())  # dos colas
                out[k] = dict(obs=obs_means[k], lo=float(np.percentile(nd, 2.5)),
                              hi=float(np.percentile(nd, 97.5)), p=p2)
            nc = np.array(null_contrast)
            pc = float((nc >= obs_contrast).mean())  # una cola derecha: dentro > mixto
            out["contrast"] = dict(obs=obs_contrast, p=pc,
                                   lo=float(np.percentile(nc, 2.5)), hi=float(np.percentile(nc, 97.5)))
            for k in KINDS:
                rows_stats.append(dict(mode=mode, test=tag, quantity=k, observed=out[k]["obs"],
                                       null_lo=out[k]["lo"], null_hi=out[k]["hi"], p=out[k]["p"]))
            rows_stats.append(dict(mode=mode, test=tag, quantity="dentro − mixto", observed=obs_contrast,
                                   null_lo=out["contrast"]["lo"], null_hi=out["contrast"]["hi"], p=pc))
            return out

        SA = summarize(bar_null_A, contrast_A, "test1_langperm")   # barras + estrellas + banda gris
        SB = summarize(bar_null_B, contrast_B, "test2_blockperm")  # solo el corchete de origen

        draw_final(mode, C, upper, models, origin, is_cn, ncn, n, SA, SB["contrast"]["p"],
                   HERE / f"panelC_final_{mode}.png")
        print(f"{mode:8s}  " + "  ".join(f"{k}:{SA[k]['obs']:+.2f}(p{SA[k]['p']:.3f})" for k in KINDS)
              + f"  |  corchete mismo origen>mixto:{SB['contrast']['obs']:+.2f}(p{SB['contrast']['p']:.3f})",
              flush=True)

    out_csv = HERE / ("panelC_test_stats_" + "_".join(only) + ".csv" if only else "panelC_test_stats.csv")
    pd.DataFrame(rows_stats).to_csv(out_csv, index=False)
    print("wrote", out_csv)


def draw_final(mode, C, upper, models, origin, is_cn, ncn, n, S, contrast_p, out):
    """Medio heatmap + nota al pie con el resultado del test (Wendy, 21/09: sin el recuadro de barras del acuerdo medio).
    Nota: acuerdo medio por tipo de par con la q de BH sobre los tres tipos (Test 1, idiomas permutados dentro del modelo) y el
    contraste mismo origen > mixto con su p (Test 2, etiquetas CN/US permutadas), como en el panel F del cuerpo."""
    from statsmodels.stats.multitest import multipletests
    q = dict(zip(KINDS, multipletests([S[k]["p"] for k in KINDS], method="fdr_bh")[1]))
    Cshow = np.where(upper, np.nan, C)
    fig, ax = plt.subplots(figsize=(9.6, 8.8), layout="constrained")
    cmap = plt.get_cmap("RdBu_r").copy(); cmap.set_bad("white")
    im = ax.imshow(Cshow, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(n), models, rotation=90, fontsize=7.5)
    ax.set_yticks(range(n), models, fontsize=7.5)
    for ticks in (ax.get_xticklabels(), ax.get_yticklabels()):
        for t, m in zip(ticks, models):
            t.set_color(ORIGIN[origin[m]])
    ax.plot([-.5, ncn - .5], [ncn - .5, ncn - .5], color="black", lw=1.2)
    ax.plot([ncn - .5, ncn - .5], [ncn - .5, n - .5], color="black", lw=1.2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(f"Correlación entre los rankings de idiomas de cada par de modelos · {LABELS[mode]}", fontsize=11)
    cb = fig.colorbar(im, ax=ax, shrink=.55, label="Spearman", pad=.02, location="left")
    cb.ax.yaxis.set_label_position("left"); cb.ax.yaxis.set_ticks_position("left")
    npairs = {"CN–CN": 66, "US–US": 66, "mixto": 144}
    st = lambda v: ("***" if v < .001 else "**" if v < .01 else "*" if v < .05 else "ns")
    dc = lambda x: x.replace(".", ",")                       # coma decimal solo en los números, no en los puntos de la frase
    fq = lambda v: "q < 0,001" if v < .001 else "q < 0,01" if v < .01 else dc(f"q = {v:.2f}")
    fp_ = lambda v: "p < 0,001" if v < .001 else dc(f"p = {v:.3f}")
    fo = lambda v: dc(f"{v:+.2f}")
    parts = [f"{k} {fo(S[k]['obs'])} ({npairs[k]} pares, {fq(q[k])}, {st(q[k])})" for k in KINDS]
    line1 = ("Acuerdo medio (Spearman) por tipo de par: " + "; ".join(parts) + ". q: BH sobre los tres tipos; azar = idiomas permutados "
             "dentro de cada modelo (5.000).")
    bold = f"Mismo origen > mixto: {fo(S['contrast']['obs'])}, {fp_(contrast_p)} {st(contrast_p)}"      # en negrita (Wendy, 21/09)
    line3 = "Etiquetas CN/US permutadas entre modelos (10.000)."
    fig.suptitle(f"F2 · C · {LABELS[mode]}: ¿cuánto acuerdan los modelos en cómo rankean los idiomas?",
                 fontsize=12.5, y=1.02)
    fig.text(0.5, -0.02, line1, ha="center", va="top", fontsize=8.2, color="#333")
    fig.text(0.5, -0.042, bold, ha="center", va="top", fontsize=8.2, color="#333", fontweight="bold")
    fig.text(0.5, -0.064, line3, ha="center", va="top", fontsize=8.2, color="#333")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
