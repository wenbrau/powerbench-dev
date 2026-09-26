"""Tables of the appendix subsection "Statistical checks" (app:checks) of the PowerBench ICLR 2027 submission.

  checks_interactions.tex  direct tests of the difference of an effect between two request types: block 93 (new interactions,
                           usage-weighted and language-range contrasts) + the scale x (type vs control) interactions of block 31
                           with their q from block 77 (nAGQ = 1 folders)
  checks_counterpart.tex   block 93, direction x (type vs control) by counterpart, BH over the 12 tests of each power
  checks_wald_t.tex        block 95, model-level tests with the Wald z reference and with a t reference (between-within df)

Nothing is fitted or resampled here; the tables transcribe the saved outputs. Same formatting as make_estimate_tables.py.

Run from the repository root:  python paper/iclr2027/submission/make_checks_tables.py
"""
from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "4_analysis" / "results"
OUT = Path(__file__).resolve().parent / "tables"
DAG = "$^{\\smash{\\dagger}}$"
LAB = {"he": "\\he", "de": "\\de", "pg": "\\pg", "control": "control", "ps": "power shifting (pooled)"}


def num(x, nd=2):
    d = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return f"{abs(d) if d == 0 else d:.{nd}f}".replace("-", "$-$")


def ci(lo, hi, nd=2):
    return f"[{num(lo, nd)}; {num(hi, nd)}]"


def pq(q, single=False):
    q = float(q)
    if q < .001:
        s = "$<$0.001"
    else:
        r = float(f"{q:.2g}")
        s = f"{r:.{max(2, -math.floor(math.log10(r)) + 1)}f}"
    return s + (DAG if single else "")


def row(*cells):
    return " & ".join(str(c) for c in cells) + " \\\\"


def block(title, ncol):
    return f"\\multicolumn{{{ncol}}}{{@{{}}l}}{{\\textit{{{title}}}}} \\\\"


def write(name, lines):
    p = OUT / name
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("written:", p.relative_to(ROOT))


def interactions():
    T = pd.read_csv(RES / "93_specificity_interactions" / "specificity_tests.csv").set_index("test")
    sx = pd.read_csv(RES / "31_fig1_glmm_scale_nagq1" / "glmm_scale_interaction_ps_vs_control.csv").set_index("fit")
    bh = pd.read_csv(RES / "77_bh_fig1_fig2c_nagq1" / "bh_families.csv")
    q31 = bh[bh.family.str.startswith("interacción scale × (modo vs control) por modo")].set_index("test").q_bh

    def t93(key, label, single=False, inv=False):
        r = T.loc[key]
        if inv:   # 26/09 (Nico): side and direction as target / user, the orientation of Figure 2 (v45)
            return row(label, f"{num(1 / r.ratio)} {ci(1 / r.ratio_hi, 1 / r.ratio_lo)}", pq(r.q_bh, single))
        return row(label, f"{num(r.ratio)} {ci(r.ratio_lo, r.ratio_hi)}", pq(r.q_bh, single))

    L = ["\\begin{tabular}{@{}lrr@{}}", "\\toprule", "Comparison & Ratio [95\\% CI] & $q$ \\\\", "\\midrule"]
    L.append(block("Scale of the target (Figure~\\ref{fig:baseline}D), GLMM", 3))
    L.append(t93("scale__pg_vs_he", "\\pg{} vs \\he"))
    L.append(t93("scale__de_vs_he", "\\de{} vs \\he"))
    for md in ("pg", "de", "he"):
        r = sx.loc[f"F_{md}_vs_control"]
        L.append(row(f"{LAB[md]}{{}} vs control", f"{num(r.xxps_odds_ratio)} {ci(r.xxps_or_lo, r.xxps_or_hi)}", pq(q31[f"{md} vs control"])))
    r = sx.loc["E_ps_vs_control"]
    L.append(row("Power shifting (pooled) vs control", f"{num(r.xxps_odds_ratio)} {ci(r.xxps_or_lo, r.xxps_or_hi)}", pq(r.xxps_p, True)))
    L.append(block("Scale against power standing (Figure~\\ref{fig:baseline}D, E), GLMM", 3))
    L.append(t93("scale_minus_standing__pg", "\\pg", True))
    L.append(t93("scale_minus_standing__ps", "Power shifting (pooled)", True))
    L.append(block("Side of the target, geopolitical set (Figure~\\ref{fig:nationality}C), GLMM", 3))
    for md in ("he", "de", "pg"):
        L.append(t93(f"side__{md}_vs_control", f"{LAB[md]}{{}} vs control", inv=True))
    L.append(t93("side__ps_vs_control", "Power shifting (pooled) vs control", True, inv=True))
    L.append(block("Side of the target, usage-weighted (Figure~\\ref{fig:nationality}D), bootstrap", 3))
    for md in ("he", "de", "pg"):
        L.append(t93(f"side_usage__{md}_vs_control", f"{LAB[md]}{{}} vs control", inv=True))
    L.append(t93("side_usage__ps_vs_control", "Power shifting (pooled) vs control", True, inv=True))
    for pole, name in (("usa", "the US"), ("china", "China")):
        L.append(block(f"{name[0].upper() + name[1:]} as target vs as user, four counterparts (Figure~\\ref{{fig:nationality}}E), GLMM", 3))
        for md in ("he", "de", "pg"):
            L.append(t93(f"direction__{pole}__all__{md}_vs_control", f"{LAB[md]}{{}} vs control", inv=True))
    L.append(block("The US as target vs as user in \\he, by counterpart, GLMM", 3))
    L.append(t93("counterpart__usa__he__rival_vs_ally_neutral", "Rival vs ally and neutral", inv=True))
    L.append(t93("counterpart__usa__he__rival_and_china_vs_ally_neutral", "Rival and China vs ally and neutral", inv=True))
    for w, name in (("eq", "equal weights"), ("use", "usage weights")):
        L.append(block(f"Language range over chance (Figure~\\ref{{fig:language}}D), {name}, bootstrap", 3))
        for md in ("he", "de", "pg"):
            L.append(t93(f"language_range__{md}_vs_control__{w}", f"{LAB[md]}{{}} vs control"))
    L += ["\\bottomrule", "\\end{tabular}"]
    write("checks_interactions.tex", L)


def counterpart():
    T = pd.read_csv(RES / "93_specificity_interactions" / "specificity_tests.csv").set_index("test")
    L = ["\\begin{tabular}{@{}lrrrrrr@{}}", "\\toprule",
         " & \\multicolumn{2}{c}{\\he} & \\multicolumn{2}{c}{\\de} & \\multicolumn{2}{c}{\\pg} \\\\",
         "\\cmidrule(l{2pt}r{2pt}){2-3}\\cmidrule(l{2pt}r{2pt}){4-5}\\cmidrule(l{2pt}r{2pt}){6-7}",
         "Counterpart & Ratio & $q$ & Ratio & $q$ & Ratio & $q$ \\\\", "\\midrule"]
    for pole, title, other in (("usa", "US as target vs as user, against the control", "China"),
                               ("china", "China as target vs as user, against the control", "US")):
        L.append(block(title, 7))
        for cp, lab in (("ally", "Ally"), ("neutral", "Neutral"), ("rival", "Rival"), ("power", other)):
            cells = []
            for md in ("he", "de", "pg"):
                r = T.loc[f"direction__{pole}__{cp}__{md}_vs_control"]
                cells += [num(1 / r.ratio), pq(r.q_bh)]   # target / user (26/09)
            L.append(row(lab, *cells))
    L += ["\\bottomrule", "\\end{tabular}"]
    write("checks_counterpart.tex", L)


def wald_t():
    T = pd.read_csv(RES / "95_between_model_small_sample" / "between_model_tests.csv")
    om = pd.read_csv(RES / "95_between_model_small_sample" / "reasoning_omnibus.csv").iloc[0]
    T = T[T.family != "DC × (type vs CT) (3)"].copy()    # not reported in the paper
    # direction × DC: the US rows first, then China, each in the order SE, DE, PG, control
    rank = {"SE": 0, "DE": 1, "PG": 2, "CT": 3}
    T["_o"] = range(len(T))
    d = T.test.str.startswith("direction")
    T.loc[d, "_o"] = T.loc[d, "_o"].min() + T.loc[d, "test"].map(lambda t: (0 if ", usa," in t else 4) + rank[t.split(", ")[-1]])
    T = T.sort_values("_o")
    single = T.n_family == 1
    use_p = T.family.str.startswith("side × DC") | single          # the paper gives p for these
    L = ["\\begin{tabular}{@{}llrrr@{}}", "\\toprule",
         "Panel & Test & Ratio & Wald $z$ & $t$ \\\\", "\\midrule"]
    names = {"DC (CN/US), SE": "DC, \\he", "DC (CN/US), DE": "DC, \\de", "DC (CN/US), PG": "DC, \\pg", "DC (CN/US), CT": "DC, control",
             "DC (CN/US), PS pooled": "DC, power shifting (pooled)", "DC (CN/US), four types": "DC, four request types",
             "DC × (PS vs CT)": "DC $\\times$ (power shifting vs control)", "AI × capability, PS − CT": "AI $\\times$ capability, power shifting $-$ control"}
    PANEL = {"Fig 1B": r"Fig.~\ref{fig:baseline}B", "Fig A2 (DC)": r"Fig.~\ref{fig:a2-DC}", "Fig 2E": r"Fig.~\ref{fig:nationality}E",
             "Fig 3 (DC)": r"App.~\ref{app:aiagent}", "Fig 3F": r"Fig.~\ref{fig:aiagent}F", "Fig A3 (capability)": r"Fig.~\ref{fig:a3-capability}",
             "Reasoning": r"Table~\ref{tab:ladder}"}
    last = None
    for _, r in T.iterrows():
        t = names.get(r.test, r.test.replace("×", "$\\times$").replace(", SE", ", \\he").replace(", DE", ", \\de").replace(", PG", ", \\pg")
                      .replace(", CT", ", control").replace(", PS", ", power shifting").replace("usa", "US").replace("china", "China"))
        sp = bool(use_p.loc[_])
        a, b = (r.p_wald_z, r.p_t) if sp else (r.q_z, r.q_t)
        panel = PANEL[r.panel] if r.panel != last else ""
        last = r.panel
        ratio = 1 / r.ratio if r.test.startswith(("side", "direction")) else r.ratio   # target / user (26/09)
        L.append(row(panel, t, num(ratio), pq(a, bool(single.loc[_])), pq(b, bool(single.loc[_]))))
    L.append(row("", "level $\\times$ DC, omnibus", "", f"$\\chi^2(2)={num(om.chi2)}$, {pq(om.p_chi2)}", f"$F(2, 6)={num(om.F)}$, {pq(om.p_F)}"))
    L += ["\\bottomrule", "\\end{tabular}"]
    write("checks_wald_t.tex", L)


if __name__ == "__main__":
    interactions()
    counterpart()
    wald_t()
