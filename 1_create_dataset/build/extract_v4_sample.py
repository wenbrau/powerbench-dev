#!/usr/bin/env python3
"""Rebuild a bank JSONL from a generator-workflow transcript directory.

The workflow returns its rows, but the run also leaves a journal and per-agent transcripts on disk.
Reading those back is the reproducible path: the cell list each writer was handed is recoverable from
its own input message, so batch->cell assignment is recovered from the run rather than re-derived from
the batching arithmetic (which would silently break if the batching ever changed).

    python 1_create_dataset/build/extract_v4_sample.py <transcript-dir> \
        --out 1_create_dataset/build/dataset1_pilot_144.v4_sample.jsonl
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESIGN = json.loads((ROOT / "1_create_dataset/subsets/design144_combos.json").read_text(encoding="utf-8"))
MODES = DESIGN["modes"]
CELLS = [(d, c, m, s, st) for d, c, s, st in DESIGN["groups"] for m in MODES]

CELL_LINE = re.compile(
    r"^\s*(\d+)\.\s+domain=(\w+)\s*\|\s*context=(\w+)\s*\|\s*mode=(\w+)\s*\|\s*scale=(\w+)\s*\|\s*standing=(\w+)",
    re.M)


def agent_input(path):
    """First user message of an agent transcript."""
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("type") == "user":
            c = r["message"]["content"]
            return c if isinstance(c, str) else "".join(
                b.get("text", "") for b in c if isinstance(b, dict))
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript_dir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = Path(a.transcript_dir)

    results = {}
    for line in open(d / "journal.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r.get("type") == "result":
            results[r["agentId"]] = r["result"]

    writers, translators = {}, {}
    for aid, res in results.items():
        if not isinstance(res, dict):
            continue
        (writers if "prompts" in res else translators)[aid] = res

    # --- map each writer to its ordered cell-index list, read off its own assignment
    ci_by_index = {c: i for i, c in enumerate(CELLS)}
    writer_cells = {}
    for aid in writers:
        txt = agent_input(d / f"agent-{aid}.jsonl")
        block = txt.split("Cells:")[-1]
        cells = []
        for ref, dom, ctx, mode, scale, st in CELL_LINE.findall(block):
            key = (dom, ctx, mode, scale, st)
            if key not in ci_by_index:
                raise SystemExit(f"agent {aid}: cell {key} not in the 144 design")
            cells.append(ci_by_index[key])
        if not cells:
            raise SystemExit(f"agent {aid}: could not read its cell assignment")
        writer_cells[aid] = cells

    # --- a translator's batch is the one whose en items its refs line up with, matched by count
    #     and by the mode tags echoed in its own input
    trans_by_len = {}
    for aid, res in translators.items():
        trans_by_len.setdefault(len(res["translations"]), []).append((aid, res))

    rows = []
    unmatched_es = 0
    for aid, res in writers.items():
        cells = writer_cells[aid]
        by_ref = {}
        for p in res["prompts"]:
            by_ref.setdefault(p["ref"], []).append(p)
        en_items = []
        for ref in range(1, len(cells) + 1):
            reps = sorted(by_ref.get(ref, []), key=lambda p: p["replica"])[:3]
            for k, p in enumerate(reps):
                en_items.append((cells[ref - 1], k + 1, p["prompt"].strip()))

        # find this writer's translator: same item count, and its input contains our first prompt
        es_map = {}
        for cand_aid, cand in trans_by_len.get(len(en_items), []):
            txt = agent_input(d / f"agent-{cand_aid}.jsonl")
            if en_items and en_items[0][2][:60] in txt:
                es_map = {t["ref"]: t["prompt"].strip() for t in cand["translations"]}
                break

        for i, (ci, rep, en) in enumerate(en_items):
            dom, ctx, mode, scale, st = CELLS[ci]
            pair_id = f"p2s-{ci:03d}-r{rep}"
            base = dict(pair_id=pair_id, domain=dom, context=ctx, mode=mode,
                        scale=scale, standing=st, replica=rep)
            rows.append({"id": f"{pair_id}-en", "lang": "en", **base, "prompt": en})
            es = es_map.get(i + 1)
            if es:
                rows.append({"id": f"{pair_id}-es", "lang": "es", **base, "prompt": es})
            else:
                unmatched_es += 1

    rows.sort(key=lambda r: (int(r["pair_id"][4:7]), r["replica"], r["lang"]))
    out = Path(a.out)
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8", newline="\n")

    n_en = sum(1 for r in rows if r["lang"] == "en")
    cells_seen = len({r["pair_id"][:7] for r in rows})
    print(f"wrote {out}")
    print(f"  {len(rows)} rows ({n_en} en, {len(rows)-n_en} es) over {cells_seen} cells "
          f"from {len(writers)} writer(s) + {len(translators)} translator(s)")
    if unmatched_es:
        print(f"  !! {unmatched_es} en rows have no es translation")
    dupes = len([r["prompt"] for r in rows if r["lang"] == "en"]) - len({r["prompt"] for r in rows if r["lang"] == "en"})
    if dupes:
        print(f"  !! {dupes} duplicate en prompts")


if __name__ == "__main__":
    main()
