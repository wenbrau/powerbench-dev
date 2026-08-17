#!/usr/bin/env python3
"""Merge the 8-row patch transformations into the v6r2 D2/D3 banks.

Takes the two Workflow result files (the patch runs over dataset1_full_576.v6r2.jsonl),
folds their rows into the v6r banks — replacing rows that already existed, adding the ones
D2 had skipped — and writes the v6r2 banks in source order. The v6r banks are not touched.

    python 1_create_dataset/build/merge_patch8_v6r2.py --d2 <task.output> --d3 <task.output>
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "1_create_dataset/build"
PATCHED = ["p2s-005-r1", "p2s-021-r1", "p2s-023-r1", "p2s-281-r1",
           "p2s-420-r1", "p2s-421-r1", "p2s-422-r1", "p2s-392-r1"]


def result_of(path):
    """Workflow task output -> the script's return value."""
    return json.loads(Path(path).read_text())["result"]


def order_key(pair_id):
    return int(re.search(r"p2s-(\d+)", pair_id).group(1))


def merge(base_path, out_path, patch, label):
    base = [json.loads(l) for l in base_path.open()]
    by = {r["pair_id"]: r for r in base}
    replaced = [r["pair_id"] for r in patch if r["pair_id"] in by]
    added = [r["pair_id"] for r in patch if r["pair_id"] not in by]
    for r in patch:
        by[r["pair_id"]] = r
    rows = sorted(by.values(), key=lambda r: order_key(r["pair_id"]))
    out_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    print(f"{label}: {len(base)} -> {len(rows)} filas "
          f"({len(replaced)} reemplazadas, {len(added)} agregadas)")
    return rows, replaced, added


def main(d2_out, d3_out):
    src = {json.loads(l)["pair_id"]: json.loads(l)
           for l in (BUILD / "dataset1_full_576.v6r2.jsonl").open()
           if json.loads(l)["lang"] == "en"}

    prov = {"artifact": "D2/D3 patched for the 8 rewritten D1 scenarios",
            "source_bank": "current/banks/dataset1_full_576.v6r2.jsonl",
            "patched_pair_ids": PATCHED, "jobs": {}}
    problems = []

    for key, task, base_name, out_name in (
        ("d2", d2_out, "dataset2_full_576.v6r.jsonl", "dataset2_full_576.v6r2.jsonl"),
        ("d3", d3_out, "dataset3_full_504.v6r.jsonl", "dataset3_full_504.v6r2.jsonl"),
    ):
        res = result_of(task)
        rows, replaced, added = merge(BUILD / base_name, BUILD / out_name, res["rows"], key.upper())
        for s in res["skipped"]:
            problems.append(f"{key}: {s['pair_id']} sigue sin transformarse — {s['reason'][:90]}")
        for p in res["problems"]:
            problems.append(f"{key}: {p}")

        # the patched rows must carry the NEW D1 text
        for r in res["rows"]:
            body = r["prompt"].replace("{NAT} ", "").replace(" {NAT}", "")
            new_words = set(src[r["pair_id"]]["prompt"].split())
            overlap = sum(w in new_words for w in body.split()) / len(body.split())
            if overlap < 0.85:
                problems.append(f"{key}: {r['pair_id']} no deriva del texto v6r2 "
                                f"(solapamiento {overlap:.2f})")
            if key == "d2" and r["prompt"].count("{NAT}") != 1:
                problems.append(f"d2: {r['pair_id']} tiene {r['prompt'].count('{NAT}')} tokens")

        out = BUILD / out_name
        prov["jobs"][key] = {
            "workflow_result": str(Path(task).name), "out": str(out.relative_to(ROOT)),
            "rows": len(rows), "replaced": replaced, "added": added,
            "skipped": res["skipped"], "problems": res["problems"],
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        }

    (BUILD / "patch8_v6r2.provenance.json").write_text(
        json.dumps(prov, indent=2, ensure_ascii=False) + "\n")
    print(f"\nproblemas: {len(problems)}")
    for p in problems:
        print("  ", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--d2", required=True)
    ap.add_argument("--d3", required=True)
    a = ap.parse_args()
    raise SystemExit(main(a.d2, a.d3))
