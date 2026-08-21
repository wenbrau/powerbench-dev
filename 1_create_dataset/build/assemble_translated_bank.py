#!/usr/bin/env python3
"""Assemble the batch files written by translate_*.workflow.js into a new multilingual bank.

Additive by construction: reads the source bank, never writes to it, and refuses to overwrite it.
Coordinates on every translated row are copied from the English row — a translator's output is only
ever used for the prompt text.

    python 1_create_dataset/build/assemble_translated_bank.py \
        --bank  current/banks/dataset1_full_576.v6r2.jsonl \
        --trans 1_create_dataset/build/_trans_dataset1_full_576 \
        --langs de fr hi sw zh pt \
        --out   current/banks/dataset1_full_576.v6r2.multilang.jsonl

Checks, per language: every English pair_id translated exactly once, nothing extra, nothing empty,
and no row left identical to its English source (the untranslated-passthrough failure). There is
deliberately NO length check — that was an English-authoring rule and does not transfer.

Writes <out> plus <out>.provenance.json. Exit code 1 if anything failed.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

COORDS = ("domain", "context", "mode", "scale", "standing", "replica", "writer")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_jsonl(p: Path):
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", required=True)
    ap.add_argument("--trans", required=True, help="directory the translators wrote into")
    ap.add_argument("--langs", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-partial", action="store_true",
                    help="write what is complete and report the rest instead of exiting 1")
    a = ap.parse_args()

    def resolve(s):
        p = Path(s)
        return p if p.is_absolute() else ROOT / p

    bank, trans_dir, out = resolve(a.bank), resolve(a.trans), resolve(a.out)
    if out.resolve() == bank.resolve():
        raise SystemExit("--out must not be the source bank; this script is additive")

    rows = load_jsonl(bank)
    en = {r["pair_id"]: r for r in rows if r.get("lang") == "en"}
    if not en:
        raise SystemExit(f"{bank}: no lang=='en' rows")
    existing = {r.get("lang") for r in rows}

    problems, new_rows, per_lang = [], [], {}

    for lang in a.langs:
        if lang in existing:
            problems.append(f"{lang}: source bank already has rows for this language")
            continue

        got = {}
        files = sorted(trans_dir.glob(f"{lang}_batch_*.json"))
        if not files:
            problems.append(f"{lang}: no {lang}_batch_*.json in {trans_dir}")
            continue

        for f in files:
            try:
                payload = json.loads(f.read_text(encoding="utf-8"))
            except Exception as exc:
                problems.append(f"{lang}: {f.name} is not valid JSON ({exc})")
                continue
            if isinstance(payload, dict):  # tolerate a {"items": [...]} wrapper
                payload = payload.get("items", payload.get("translations", []))
            if not isinstance(payload, list):
                problems.append(f"{lang}: {f.name} is not a JSON array")
                continue
            for entry in payload:
                pid, text = entry.get("pair_id"), (entry.get("prompt") or "")
                if pid not in en:
                    problems.append(f"{lang}: {f.name} has unknown pair_id {pid!r}")
                    continue
                if pid in got:
                    problems.append(f"{lang}: {pid} translated twice ({f.name})")
                    continue
                text = " ".join(text.split())
                if not text:
                    problems.append(f"{lang}: {pid} empty translation ({f.name})")
                    continue
                if text == " ".join(en[pid]["prompt"].split()):
                    problems.append(f"{lang}: {pid} identical to the English (untranslated)")
                    continue
                got[pid] = text

        missing = sorted(set(en) - set(got))
        if missing:
            problems.append(f"{lang}: missing {len(missing)} of {len(en)} — e.g. {missing[:5]}")

        per_lang[lang] = {"files": len(files), "translated": len(got), "missing": len(missing)}
        if missing and not a.allow_partial:
            continue

        for pid, text in got.items():
            src = en[pid]
            row = {"id": f"{pid}-{lang}", "pair_id": pid, "lang": lang}
            row.update({k: src[k] for k in COORDS if k in src})
            row["prompt"] = text
            new_rows.append(row)

    for lang, st in per_lang.items():
        print(f"  {lang}: {st['translated']}/{len(en)} translated, {st['files']} batch files, {st['missing']} missing")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems[:40]:
            print("  -", p)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more")
    if problems and not a.allow_partial:
        raise SystemExit("\nnothing written. Re-run the failed batches, then re-run this script.")

    # canonical language order: en, then the languages the bank already had (in bank order),
    # then the newly added ones in the order they were requested.
    lang_order = {"en": 0}
    for r in rows:
        lang_order.setdefault(r.get("lang"), len(lang_order))
    for lang in a.langs:
        lang_order.setdefault(lang, len(lang_order))

    pid_order = {pid: i for i, pid in enumerate(r["pair_id"] for r in rows if r.get("lang") == "en")}
    allrows = rows + new_rows
    allrows.sort(key=lambda r: (pid_order.get(r["pair_id"], 1 << 30), lang_order.get(r.get("lang"), 99)))

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        for r in allrows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    prov = {
        "artifact": "multilingual bank assembled from translator batch files",
        "source_bank": {"file": str(bank.relative_to(ROOT)), "sha256": sha256(bank), "en_rows": len(en)},
        "trans_dir": str(trans_dir.relative_to(ROOT)) if trans_dir.is_relative_to(ROOT) else str(trans_dir),
        "languages_added": a.langs,
        "per_language": per_lang,
        "rows_in": len(rows),
        "rows_added": len(new_rows),
        "rows_out": len(allrows),
        "partial": bool(problems),
        "problems": problems,
        "out": {"file": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out)},
    }
    prov_path = out.with_suffix(out.suffix + ".provenance.json")
    prov_path.write_text(json.dumps(prov, indent=1, ensure_ascii=False), encoding="utf-8")
    prov["out"]["sha256"] = sha256(out)
    prov_path.write_text(json.dumps(prov, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"\nwrote {out}  ({len(rows)} + {len(new_rows)} = {len(allrows)} rows)")
    print(f"wrote {prov_path}")
    if problems:
        print("NOTE: written with --allow-partial; the bank is INCOMPLETE (see provenance).")


if __name__ == "__main__":
    main()
