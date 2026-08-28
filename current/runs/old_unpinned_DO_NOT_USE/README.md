# Old unpinned runs — DO NOT USE

These runs predate provider pinning: each request was routed to whatever OpenRouter provider
answered, so quantization and (for the `*_noreason_*` files) the reasoning-off guarantee are not
controlled. The reasoning-off audit found leaks on 16.7% of unpinned D3 rows (gemini 91%).

Superseded by the pinned OFF-arm runs in `current/runs/`:

| old (here) | superseded by |
|---|---|
| `d1_v6r2_7models_noreason_run.jsonl` | `d1_v6r2_7models_pinned_off_en.jsonl` (+ `d1_v6r2_6models_pinned_off_7langs.jsonl.gz` for the other 7 languages) |
| `d3_v6r2_7models_noreason_run.jsonl` | `d3_v6r2_6models_pinned_off.jsonl` |
| `d1_v6r2_7models_run.jsonl` (provider-default reasoning) | no pinned replacement yet |
| `d2_v6r2_7models_noreason_run.jsonl` | no pinned replacement yet (bank still being revised) |
| `sample10pct_7models_run.jsonl` (10% pilot) | superseded by the full-bank pinned runs |

Kept for provenance only. Any new analysis must read the pinned files.
