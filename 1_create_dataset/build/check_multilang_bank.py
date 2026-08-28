#!/usr/bin/env python3
"""Structural + linguistic sanity check on an assembled multilingual D1 bank.

Read-only. Exits 1 if any hard check fails; soft checks are reported as warnings.

    python 1_create_dataset/build/check_multilang_bank.py \
        --bank current/banks/dataset1_full_576.v6r2.multilang.verified.jsonl \
        --expect 576

Hard checks, per language:
  - exactly --expect rows, pair_ids unique and identical to the English set
  - prompt non-empty, and (for non-en) not byte-identical to the English source
  - metadata (domain, context, mode, scale, standing, replica, writer) matches the EN row
  - script: hi must carry Devanagari, zh must carry Han, the Latin-script langs must carry neither
Soft checks (warn only):
  - length ratio to the English source outside [0.45, 2.4] (hi/zh get a wider band)
  - a non-en prompt whose ASCII-word overlap with the English is >= 0.6 (untranslated leakage)
  - prompt does not end in '?' or '.' / '。' / '।'
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ("domain", "context", "mode", "scale", "standing", "replica", "writer")
LEN_BAND = {"hi": (0.5, 3.0), "zh": (0.15, 1.2)}
DEFAULT_BAND = (0.45, 2.4)


def has(text, lo, hi):
    return any(lo <= ord(c) <= hi for c in text)


def devanagari(t):
    return has(t, 0x0900, 0x097F)


def han(t):
    return has(t, 0x4E00, 0x9FFF) or has(t, 0x3400, 0x4DBF)


def ascii_words(t):
    return {w for w in re.findall(r"[A-Za-z']{4,}", t.lower())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", required=True)
    ap.add_argument("--expect", type=int, default=576)
    ap.add_argument("--max-report", type=int, default=12)
    a = ap.parse_args()

    p = Path(a.bank) if Path(a.bank).is_absolute() else ROOT / a.bank
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_lang = {}
    for r in rows:
        by_lang.setdefault(r["lang"], []).append(r)
    if "en" not in by_lang:
        raise SystemExit("no lang=='en' rows")
    en = {r["pair_id"]: r for r in by_lang["en"]}

    errors, warnings = [], []
    print(f"{p}\n{len(rows)} rows, {len(by_lang)} languages\n")
    print(f"{'lang':<5} {'rows':>5} {'uniq':>5} {'errors':>7} {'warn':>5}  notes")
    for lang in sorted(by_lang):
        rs = by_lang[lang]
        e, w = [], []
        ids = Counter(r["pair_id"] for r in rs)
        if len(rs) != a.expect:
            e.append(f"{len(rs)} rows, expected {a.expect}")
        dup = [k for k, v in ids.items() if v > 1]
        if dup:
            e.append(f"{len(dup)} duplicate pair_id(s): {dup[:3]}")
        missing = set(en) - set(ids)
        extra = set(ids) - set(en)
        if missing:
            e.append(f"{len(missing)} pair_id(s) with no EN source-side match: {sorted(missing)[:3]}")
        if extra:
            e.append(f"{len(extra)} pair_id(s) not in EN: {sorted(extra)[:3]}")

        lo, hi = LEN_BAND.get(lang, DEFAULT_BAND)
        for r in rs:
            src = en.get(r["pair_id"])
            t = (r.get("prompt") or "").strip()
            pid = r["pair_id"]
            if not t:
                e.append(f"{pid}: empty prompt")
                continue
            if src is None:
                continue
            for k in META:
                if r.get(k) != src.get(k):
                    e.append(f"{pid}: {k}={r.get(k)!r} but EN has {src.get(k)!r}")
            if lang != "en":
                if " ".join(t.split()) == " ".join(src["prompt"].split()):
                    e.append(f"{pid}: identical to the English source")
                    continue
                if lang == "hi" and not devanagari(t):
                    e.append(f"{pid}: no Devanagari")
                if lang == "zh" and not han(t):
                    e.append(f"{pid}: no Han characters")
                if lang not in ("hi", "zh") and (devanagari(t) or han(t)):
                    e.append(f"{pid}: unexpected Devanagari/Han in a Latin-script language")
                ratio = len(t) / max(1, len(src["prompt"]))
                if not (lo <= ratio <= hi):
                    w.append(f"{pid}: length ratio {ratio:.2f} outside [{lo}, {hi}]")
                ew = ascii_words(src["prompt"])
                if ew:
                    ov = len(ascii_words(t) & ew) / len(ew)
                    if ov >= 0.6:
                        w.append(f"{pid}: {ov:.0%} English word overlap — possible untranslated text")
            if not re.search(r"[?.!。！？।]$", t):
                w.append(f"{pid}: does not end in terminal punctuation ({t[-12:]!r})")
            if any(unicodedata.category(c) == "Cc" and c not in "\n\t" for c in t):
                e.append(f"{pid}: control characters in prompt")
        note = "ok" if not e else e[0][:70]
        print(f"{lang:<5} {len(rs):>5} {len(ids):>5} {len(e):>7} {len(w):>5}  {note}")
        errors += [f"[{lang}] {x}" for x in e]
        warnings += [f"[{lang}] {x}" for x in w]

    if warnings:
        print(f"\n{len(warnings)} warning(s); first {a.max_report}:")
        for x in warnings[:a.max_report]:
            print("  -", x)
    if errors:
        print(f"\n{len(errors)} ERROR(s); first {a.max_report}:")
        for x in errors[:a.max_report]:
            print("  -", x)
        sys.exit(1)
    print(f"\nOK: {len(by_lang)} languages x {a.expect} rows, no hard failures.")


if __name__ == "__main__":
    main()
