#!/usr/bin/env python3
"""Find parenthetical ENGLISH glosses a translator added, and emit them as a patch.

Read-only on the bank. Writes a patch JSONL that apply_translation_verdicts.py --patch consumes.

    python 1_create_dataset/build/find_english_glosses.py \
        --bank current/banks/dataset1_full_576.v6r2.multilang.verified.jsonl \
        --out  1_create_dataset/build/d1_v6r2_gloss_patch.jsonl

A parenthetical counts as an added English gloss only when ALL of these hold:
  - it is preceded by whitespace   (rules out German inclusive forms: "Professor(in)", "langjährige(r)")
  - it holds at least one Latin token of 4+ characters      (rules out "(in)", "(r)")
  - EVERY Latin token of 3+ characters appears in the English source, case-insensitively
    (rules out target-language parentheticals: pt "(com estabilidade)")
  - the identical parenthetical is not in the English source itself

The repair is the minimal one: drop the parenthetical and the single space before it, nothing else.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAREN = re.compile(r"(?<=\s)\(([^()]{2,60})\)")
TOKEN = re.compile(r"[A-Za-z][A-Za-z'\-]+")


def glosses(prompt: str, english: str):
    out = []
    low = english.lower()
    for m in PAREN.finditer(prompt):
        toks = TOKEN.findall(m.group(1))
        if not toks or not any(len(t) >= 4 for t in toks):
            continue
        if m.group(0) in english:
            continue
        if all(t.lower() in low for t in toks if len(t) >= 3):
            out.append(m.group(0))
    return out


def strip(prompt: str, found) -> str:
    out = prompt
    for g in found:
        out = out.replace(" " + g, "")
    return " ".join(out.split())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    bank = Path(a.bank) if Path(a.bank).is_absolute() else ROOT / a.bank
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out

    rows = [json.loads(l) for l in bank.read_text(encoding="utf-8").splitlines() if l.strip()]
    en = {r["pair_id"]: r["prompt"] for r in rows if r["lang"] == "en"}

    recs = []
    for r in rows:
        if r["lang"] == "en":
            continue
        found = glosses(r["prompt"], en[r["pair_id"]])
        if not found:
            continue
        new = strip(r["prompt"], found)
        assert new != r["prompt"], f"{r['pair_id']}: nothing removed"
        for g in found:
            assert g not in new, f"{r['pair_id']}: {g} survived"
        recs.append({
            "lang": r["lang"], "pair_id": r["pair_id"],
            "issues": [f"1: parenthetical English gloss {g} the English source does not have" for g in found],
            "prompt_old": r["prompt"], "prompt_fixed": new,
            "source": "find_english_glosses.py",
        })

    with out.open("w", encoding="utf-8", newline=chr(10)) as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    per = {}
    for r in recs:
        per[r["lang"]] = per.get(r["lang"], 0) + 1
    print(f"wrote {out} — {len(recs)} rows {per}")


if __name__ == "__main__":
    main()
