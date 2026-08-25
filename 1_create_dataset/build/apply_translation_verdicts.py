#!/usr/bin/env python3
"""Apply the verdict files written by verify_*.workflow.js to a multilingual bank.

Additive: reads the bank, never writes to it, refuses to overwrite it. Writes

    <out>                       the bank with every "repaired" prompt replaced by its prompt_fixed
    <out>.verify.jsonl          one record per (pair_id, lang): status, issues, prompt_old, prompt_new
    <out>.provenance.json       hashes of inputs, per-language counts

    python 1_create_dataset/build/apply_translation_verdicts.py \
        --bank     current/banks/dataset1_full_576.v6r2.multilang.jsonl \
        --verdicts 1_create_dataset/build/_verify_dataset1_full_576 \
        --langs    de fr hi sw zh pt \
        --out      current/banks/dataset1_full_576.v6r2.multilang.verified.jsonl

Checks, per language: every pair_id has exactly one verdict, status is verified|repaired,
"repaired" carries a non-empty prompt_fixed that differs from the original and is not the English,
"verified" carries none. Exit code 1 if anything fails (nothing written unless --allow-partial).
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_jsonl(p: Path):
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", required=True)
    ap.add_argument("--verdicts", required=True, help="directory the verifiers wrote into")
    ap.add_argument("--langs", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--patch", default=None, nargs="+",
                    help="one or more JSONL files of post-verdict corrections {lang, pair_id, prompt_fixed, issues, "
                         "source[, prompt_old]}, applied ON TOP of the verdicts. Use for defects no "
                         "verifier caught; the verdict files stay untouched so they keep recording "
                         "what each verifier actually said.")
    ap.add_argument("--allow-partial", action="store_true",
                    help="apply what is valid, leave the rest as-is, and report instead of exiting 1")
    a = ap.parse_args()

    def resolve(s):
        p = Path(s)
        return p if p.is_absolute() else ROOT / p

    bank, vdir, out = resolve(a.bank), resolve(a.verdicts), resolve(a.out)
    if out.resolve() == bank.resolve():
        raise SystemExit("--out must not be the source bank; this script is additive")

    rows = load_jsonl(bank)
    en = {r["pair_id"]: r for r in rows if r.get("lang") == "en"}
    problems = []
    verdicts = {}  # (lang, pair_id) -> verdict dict
    for lang in a.langs:
        files = sorted(vdir.glob(f"{lang}_batch_*.json"))
        if not files:
            problems.append(f"{lang}: no verdict files in {vdir}")
            continue
        for f in files:
            try:
                arr = json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                problems.append(f"{f.name}: not valid JSON ({e})")
                continue
            if not isinstance(arr, list):
                problems.append(f"{f.name}: top level is not a list")
                continue
            for v in arr:
                pid = v.get("pair_id") if isinstance(v, dict) else None
                if pid not in en:
                    problems.append(f"{f.name}: unknown pair_id {pid!r}")
                    continue
                if (lang, pid) in verdicts:
                    problems.append(f"{f.name}: duplicate verdict for {pid}")
                    continue
                verdicts[(lang, pid)] = (v, f.name)

    lang_rows = {}
    for r in rows:
        if r.get("lang") in a.langs:
            lang_rows[(r["lang"], r["pair_id"])] = r

    records = []
    counts = {l: {"verified": 0, "repaired": 0, "missing": 0, "invalid": 0} for l in a.langs}
    new_prompt = {}
    for lang in a.langs:
        for pid, e in en.items():
            row = lang_rows.get((lang, pid))
            if row is None:
                problems.append(f"{lang}: bank has no row for {pid}")
                continue
            hit = verdicts.get((lang, pid))
            if hit is None:
                counts[lang]["missing"] += 1
                problems.append(f"{lang}: no verdict for {pid}")
                continue
            v, fname = hit
            status = v.get("status")
            fixed = v.get("prompt_fixed")
            issues = v.get("issues") or []
            old = row["prompt"]
            bad = None
            if status == "verified":
                if fixed not in (None, ""):
                    bad = "status verified but prompt_fixed present"
            elif status == "repaired":
                if not isinstance(fixed, str) or not fixed.strip():
                    bad = "status repaired but prompt_fixed empty"
                elif " ".join(fixed.split()) == " ".join(old.split()):
                    bad = "status repaired but prompt_fixed identical to original"
                elif " ".join(fixed.split()) == " ".join(e["prompt"].split()):
                    bad = "prompt_fixed is the English source"
            else:
                bad = f"unknown status {status!r}"
            if bad:
                counts[lang]["invalid"] += 1
                problems.append(f"{fname}: {pid}: {bad}")
                continue
            counts[lang][status] += 1
            new = " ".join(fixed.split()) if status == "repaired" else old
            new_prompt[(lang, pid)] = new
            records.append({
                "pair_id": pid, "lang": lang, "status": status, "issues": issues,
                "prompt_en": e["prompt"], "prompt_old": old, "prompt_new": new, "verdict_file": fname,
            })

    for lang in a.langs:
        c = counts[lang]
        print(f"{lang}: verified={c['verified']} repaired={c['repaired']} missing={c['missing']} invalid={c['invalid']}")

    if problems and not a.allow_partial:
        print(f"\n{len(problems)} problem(s); nothing written. First 40:")
        for p in problems[:40]:
            print("  -", p)
        raise SystemExit(1)

    # Patch layer: applied after the verdicts, on top of whatever text they produced.
    patches, patch_problems = {}, []
    for pf in [resolve(x) for x in (a.patch or [])]:
        for ln, line in enumerate(pf.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            v = json.loads(line)
            key = (v.get("lang"), v.get("pair_id"))
            if key not in lang_rows:
                patch_problems.append(f"{pf.name}:{ln}: no bank row for {key}")
                continue
            if key in patches:
                patch_problems.append(f"{pf.name}:{ln}: duplicate patch for {key}")
                continue
            base = new_prompt.get(key, lang_rows[key]["prompt"])
            fixed = v.get("prompt_fixed")
            if not isinstance(fixed, str) or not fixed.strip():
                patch_problems.append(f"{pf.name}:{ln}: empty prompt_fixed for {key}")
                continue
            if v.get("prompt_old") and " ".join(v["prompt_old"].split()) != " ".join(base.split()):
                patch_problems.append(f"{pf.name}:{ln}: {key} prompt_old does not match the post-verdict text")
                continue
            if " ".join(fixed.split()) == " ".join(base.split()):
                patch_problems.append(f"{pf.name}:{ln}: {key} patch changes nothing")
                continue
            if " ".join(fixed.split()) == " ".join(en[key[1]]["prompt"].split()):
                patch_problems.append(f"{pf.name}:{ln}: {key} patch is the English source")
                continue
            patches[key] = v
            new_prompt[key] = " ".join(fixed.split())
    if a.patch:
        per_lang = {}
        for (l, _) in patches:
            per_lang[l] = per_lang.get(l, 0) + 1
        print(f"patch: {len(patches)} row(s) {per_lang} from {', '.join(Path(x).name for x in a.patch)}")
        if patch_problems:
            print(f"  {len(patch_problems)} patch problem(s); nothing written. First 20:")
            for x in patch_problems[:20]:
                print("   -", x)
            raise SystemExit(1)
        by_key = {(r["lang"], r["pair_id"]): r for r in records}
        for key, v in patches.items():
            rec = by_key.get(key)
            if rec is not None:
                rec["prompt_new"] = new_prompt[key]
                rec["patched"] = True
                rec["patch_issues"] = v.get("issues") or []
                rec["patch_source"] = v.get("source") or "patch"

    out_rows = []
    for r in rows:
        key = (r.get("lang"), r.get("pair_id"))
        if key in new_prompt and new_prompt[key] != r["prompt"]:
            r = dict(r, prompt=new_prompt[key])
        out_rows.append(r)

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for r in out_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    rec_path = out.with_name(out.name + ".verify.jsonl")
    with rec_path.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    prov = {
        "source_bank": str(bank.relative_to(ROOT)) if bank.is_relative_to(ROOT) else str(bank),
        "source_sha256": sha256(bank),
        "verdict_dir": str(vdir),
        "verdict_files": {f.name: sha256(f) for f in sorted(vdir.glob("*_batch_*.json"))},
        "langs": a.langs,
        "counts": counts,
        "patch_files": {Path(x).name: sha256(resolve(x)) for x in (a.patch or [])},
        "patch_rows": sorted(f"{l}:{p}" for (l, p) in patches) if a.patch else [],
        "n_rows_out": len(out_rows),
        "partial": bool(problems),
        "problems": problems,
        "out_sha256": sha256(out),
    }
    out.with_name(out.name + ".provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {out} ({len(out_rows)} rows), {rec_path.name} ({len(records)} records), provenance")
    if problems:
        print(f"PARTIAL: {len(problems)} problem(s) left unapplied; see provenance.json")


if __name__ == "__main__":
    main()
