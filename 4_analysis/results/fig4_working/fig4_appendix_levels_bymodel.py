"""F4 APPENDIX: per-model refusal LEVELS D1 (human) vs D3 (AI agent) in power grabbing.
Dumbbell: open dot = D1, filled dot = D3, segment = the AI-agent gap. REAL data (block 22).
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

R = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/22_d3_ai_final"
OUT = "/Users/wbrau/GitHub/powerbench-dev/4_analysis/results/fig4_working/fig4_appendix_levels_bymodel.png"
C = {"US": "#3B6EA5", "CN": "#B24747"}

pm = pd.read_csv(f"{R}/per_model_rates.csv")
pm = pm[pm["mode"] == "pg"]
w = pm.pivot_table(index=["model", "origin"], columns="condition", values="rate").reset_index()

fig, ax = plt.subplots(figsize=(8.2, 9))
y = 0
yticks, ylabels = [], []
for org in ["CN", "US"]:
    block = w[w.origin == org].sort_values("ai")
    for _, r in block.iterrows():
        ax.plot([r["human"], r["ai"]], [y, y], color=C[org], lw=1.8, alpha=0.55, zorder=1)
        ax.scatter(r["human"], y, s=52, facecolor="white", edgecolor=C[org], linewidth=1.6, zorder=3)
        ax.scatter(r["ai"], y, s=52, color=C[org], zorder=3)
        yticks.append(y); ylabels.append(r["model"]); y += 1
    y += 1

ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=9)
ax.set_ylim(-0.7, y - 0.5)
ax.set_xlabel("Refusal en power grabbing (%)", fontsize=11)
ax.grid(axis="x", ls=":", alpha=0.4)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.suptitle("Figura 4 · Apéndice — niveles de refusal por modelo: humano (D1) → agente IA (D3), power grabbing", fontsize=11.5, y=0.965)
ax.legend(handles=[Line2D([0], [0], marker="o", mfc="white", mec="#555", color="w", label="D1 = humano"),
                   Line2D([0], [0], marker="o", color="#555", ls="", label="D3 = agente IA"),
                   Line2D([0], [0], marker="o", color=C["US"], ls="", label="US"),
                   Line2D([0], [0], marker="o", color=C["CN"], ls="", label="CN")],
          loc="lower right", fontsize=9, frameon=False)
plt.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("saved", OUT)
