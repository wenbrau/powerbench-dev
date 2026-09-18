"""F4 APPENDIX: DiD = (AI-agent shift in a power-shifting mode) - (AI-agent shift in the control),
per model, pooled by bloc. Isolates the power-specific part of the AI-agent penalty.

Clustering: the power modes and the control are DIFFERENT prompt sets, so the two shifts cannot be
paired by prompt. The only shared unit is the MODEL -> aggregate the per-model DiD across the 12
models of each bloc (model-level SE, Student-t with 11 df). REAL data (block 22 per_model_rates).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.lines import Line2D
import matplotlib.transforms as mtransforms

R = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/22_d3_ai_final"
OUT = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/fig4_working/fig4_appendix_did.png"
C = {"US": "#3B6EA5", "CN": "#B24747"}
FILL = {"US": "#9FBBD8", "CN": "#DFA9A9"}
MODES = ["he", "de", "pg"]
MNAME = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing"}

pm = pd.read_csv(f"{R}/per_model_rates.csv")
sh = pm.pivot_table(index=["model", "origin"], columns=["mode", "condition"], values="rate")
# per-model shift per mode and control
shift = {}
for m in MODES + ["control"]:
    shift[m] = sh[(m, "ai")] - sh[(m, "human")]
did = pd.DataFrame({m: shift[m] - shift["control"] for m in MODES})
did["origin"] = [i[1] for i in did.index]

fig, ax = plt.subplots(figsize=(10, 6.2))
group_w = 2.2
bar_w = 0.82
offs = {"US": -0.48, "CN": 0.48}
centers = np.arange(len(MODES)) * group_w
rng = np.random.default_rng(0)
tcrit = stats.t.ppf(0.975, 11)
print(f"{'mode':8s}{'bloc':5s}{'DiD':>7s}{'se':>6s}   95% CI")
for gi, m in enumerate(MODES):
    for org in ["US", "CN"]:
        pos = centers[gi] + offs[org]
        vals = did.loc[did.origin == org, m].to_numpy(float)
        mean = vals.mean()
        se = vals.std(ddof=1) / np.sqrt(len(vals))
        lo, hi = mean - tcrit * se, mean + tcrit * se
        ax.bar(pos, mean, width=bar_w, facecolor=FILL[org], edgecolor=C[org], linewidth=1.6, alpha=0.85, zorder=2)
        ax.errorbar(pos, mean, yerr=[[mean - lo], [hi - mean]], fmt="none", ecolor=C[org], elinewidth=1.9, capsize=4, zorder=5)
        jx = pos + (rng.random(len(vals)) - 0.5) * bar_w * 0.6
        ax.scatter(jx, vals, s=30, color=C[org], alpha=0.8, zorder=4, edgecolors="white", linewidths=0.5)
        print(f"{m:8s}{org:5s}{mean:7.2f}{se:6.2f}   [{lo:5.2f},{hi:5.2f}]")

ax.axhline(0, color="#333", lw=1.1, zorder=1)
ax.set_xticks([])
ax.set_ylabel("DiD  (shift del modo − shift del control)  (pp)", fontsize=11.5)
ax.set_xlim(centers[0] - group_w * 0.42, centers[-1] + group_w * 0.42)
ax.grid(axis="y", ls=":", alpha=0.4)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
fig.subplots_adjust(top=0.78, bottom=0.13, left=0.11, right=0.97)
fig.text(0.5, 0.945, "Figura 4 · Apéndice — parte específica del sesgo: modo de power-shifting vs su control (DiD)", ha="center", fontsize=12.5)
trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
for gi, m in enumerate(MODES):
    ax.text(centers[gi], 1.03, MNAME[m], transform=trans, ha="center", va="bottom", fontsize=12.5, fontweight="bold")
ax.legend(handles=[Line2D([0], [0], marker="s", color=C["US"], ls="", ms=9, label="US (12 modelos)"),
                   Line2D([0], [0], marker="s", color=C["CN"], ls="", ms=9, label="CN (12 modelos)"),
                   Line2D([0], [0], marker="o", color="#888", ls="", label="DiD por modelo"),
                   Line2D([0], [0], color="#444", label="IC95% entre modelos (t, 11 gl)")],
          loc="lower center", bbox_to_anchor=(0.5, 1.10), ncol=4, fontsize=9, frameon=False, columnspacing=1.6)
fig.text(0.02, 0.035, "DiD por modelo, promediado por bloque · IC95% clusterizado por modelo (los modos y el control son prompts distintos, no pareables)",
         ha="left", fontsize=8.5, color="#555")
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("saved", OUT)
