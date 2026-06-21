"""Progreso de la corrida cross-model en curso. Cuenta jobs nuevos hechos."""
import json, os, time
from collections import Counter

TARGETS_NEW = ["google/gemini-2.5-flash-lite", "deepseek/deepseek-v4-pro", "qwen/qwen3.7-plus"]
PER = 1152  # 576 es + 576 en por target
TOTAL = len(TARGETS_NEW) * PER

d = json.load(open("experiment_full_results.json"))
done = Counter(r["target"] for r in d if r["target"] in TARGETS_NEW)
total_done = sum(done.values())

print(f"NUEVOS: {total_done}/{TOTAL}  ({total_done/TOTAL:.0%})")
for t in TARGETS_NEW:
    n = done.get(t, 0)
    bar = "#" * round(n / PER * 24)
    print(f"  {t.split('/')[-1]:22s} {n:4d}/{PER}  {bar:<24} {n/PER:.0%}")

# ritmo: usa mtime del archivo vs nada -> estimación cruda por ahora
age = time.time() - os.path.getmtime("experiment_full_results.json")
print(f"\n  último checkpoint hace {age:.0f}s")
