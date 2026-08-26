"""Open a run file whether it is stored plain or gzipped.

`current/runs/` holds both: small runs stay plain text, and anything that would cross GitHub's
100 MB per-file limit is committed as `<name>.jsonl.gz` instead (D1 in 7 languages is 120 MB plain,
41 MB gzipped). Consumers should not have to care which, so they ask for the plain path and this
resolves it.

    import _paths  # noqa: F401
    from runio import open_run, load_run

    for line in open_run(RUN):        # RUN = ".../d1_v6r2_6models_pinned_off_7langs.jsonl"
        row = json.loads(line)

    rows = load_run(RUN)              # or just get the parsed list

Writing is unchanged: the runner always writes plain (it needs a seekable, appendable file and its
resume reads it back). Compression is a storage step, not a pipeline step -- `gzip -k <file>`.
"""
from __future__ import annotations

import gzip
import io
import json
from pathlib import Path


def resolve_run(path) -> Path:
    """Return the file that actually exists: the plain path, or its .gz sibling."""
    p = Path(path)
    if p.exists():
        return p
    gz = p.with_name(p.name + ".gz") if p.suffix != ".gz" else p
    if gz.exists():
        return gz
    plain = p.with_suffix("") if p.suffix == ".gz" else p
    if plain.exists():
        return plain
    raise FileNotFoundError(f"neither {p} nor {p.with_name(p.name + '.gz')} exists")


def open_run(path, encoding: str = "utf-8") -> io.TextIOBase:
    """Text-mode handle over a run file, transparently gunzipping a .gz."""
    f = resolve_run(path)
    if f.suffix == ".gz":
        return gzip.open(f, "rt", encoding=encoding)
    return open(f, encoding=encoding)


def load_run(path) -> list:
    """Every row of a run file, parsed. Blank lines skipped."""
    with open_run(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]
