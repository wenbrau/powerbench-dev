# D3 English A19 launch — 2026-09-10

The user authorized launch after the pre-run review. The detached runner started with
the arguments in `offline_plan.json`, plus `--yes`: 19 explicit targets, 504 prompts
per target, reasoning OFF, 64 workers, and the frozen `pins.json`. All 19 target pin
objects were checked again against the completed D1 metadata and match exactly.
Provider resolution was not run.

The default live preflight is enabled (12 calls per model). This launch note records
startup, not a claim that the preflight or collection has completed. The runner only
collects models that pass its preflight; excluded models require investigation with
the original pins retained.

Output: `current/runs/d3_en_A19_pinned_off.jsonl`.
Local process status and log: `/tmp/powerbench-d3-en-A19/process.json` and `run.log`.
The local monitor at <http://127.0.0.1:8765/> now reads D3 with 504 expected rows per
model. Its English labels and counts were checked in the browser; seven existing
monitor tests and JavaScript syntax validation passed.

The supervisor prevents idle sleep while the runner is alive. This remains a local
Mac process and does not provide operation while the machine is asleep or shut down.
Validate all 9,576 rows after collection; recover target or judge failures with the
same pins and preserve provenance before publishing results.
