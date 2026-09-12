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


def _parts_dir(p: Path) -> Path:
    """`<stem>.parts/` next to the plain path: a run too large even gzipped (the 19-model
    7-language D1 is 505 MB plain, ~130 MB gzipped, over GitHub's 100 MB) is committed as
    several `*.jsonl.gz` pieces plus a MANIFEST.json. Rows are keyed by (target, id), so the
    order of the pieces is irrelevant."""
    stem = p.name[:-len(".jsonl.gz")] if p.name.endswith(".jsonl.gz") else p.stem
    return p.with_name(stem + ".parts")


def resolve_run(path) -> Path:
    """Return what actually exists: the plain path, its .gz sibling, or its `.parts/` directory."""
    p = Path(path)
    if p.exists():
        return p
    gz = p.with_name(p.name + ".gz") if p.suffix != ".gz" else p
    if gz.exists():
        return gz
    plain = p.with_suffix("") if p.suffix == ".gz" else p
    if plain.exists():
        return plain
    parts = _parts_dir(p)
    if parts.is_dir() and any(parts.glob("*.jsonl.gz")):
        return parts
    raise FileNotFoundError(f"none of {p}, {p.with_name(p.name + '.gz')} or {parts}/ exists")


class _PartsReader:
    """Iterates the lines of every `*.jsonl.gz` in a parts directory, as one text stream."""

    def __init__(self, d: Path, encoding: str):
        self.files = sorted(d.glob("*.jsonl.gz"))
        self.encoding = encoding

    def __iter__(self):
        for f in self.files:
            with gzip.open(f, "rt", encoding=self.encoding) as fh:
                yield from fh

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self) -> str:
        return "".join(self)


def open_run(path, encoding: str = "utf-8"):
    """Text-mode, line-iterable handle over a run file: plain, gzipped, or split into parts."""
    f = resolve_run(path)
    if f.is_dir():
        return _PartsReader(f, encoding)
    if f.suffix == ".gz":
        return gzip.open(f, "rt", encoding=encoding)
    return open(f, encoding=encoding)


def load_run(path) -> list:
    """Every row of a run file, parsed. Blank lines skipped."""
    with open_run(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]
