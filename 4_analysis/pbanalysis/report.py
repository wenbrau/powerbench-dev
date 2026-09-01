"""Output convention. Every analysis writes ONE folder:

    4_analysis/results/<NN_short_name>/
        README.md      what question, what data, what is pooled and what is not, what the unit of
                       the bootstrap is, how to read each figure, preliminary conclusion, provenance
        meta.json      the same facts, machine-readable (used to rebuild results/README.md)
        stats.json     every number that appears in the README, with intervals
        <name>.csv     every table
        <name>.png     every figure

The README is written for a reader who did not run the code. `write_result` takes plain-language
strings and assembles the file; the analysis script only has to state what it did.

    from pbanalysis import report
    res = report.Result("01_baseline_d1_en", title="...", question="...")
    res.data("D1 English, 6 models, 576 prompts each; rows with valid=False excluded (n=...).")
    res.method("Per model. Bootstrap over prompts, stratified by mode, 3000 draws, seed 0. ...")
    res.table("by_model", df, "Rates in pp with 95% percentile intervals.")
    res.figure("stacked", fig, "How to read: ...")
    res.stat("pooled_excess_pp", 2.3, lo=-2.1, hi=6.4, p=0.31, note="6 models, 8 languages")
    res.conclusion("...")
    res.write()                        # -> results/01_baseline_d1_en/
    report.rebuild_index()             # -> results/README.md
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).resolve().parents[1]
RESULTS = ROOT / "4_analysis" / "results"


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


class Result:
    def __init__(self, name: str, title: str, question: str, results_dir: Path | str = RESULTS,
                 status: str = "preliminary"):
        self.name, self.title, self.question, self.status = name, title, question, status
        self.dir = Path(results_dir) / name
        self._data, self._method, self._notes, self._conclusion = [], [], [], ""
        self._tables, self._figures, self._stats = [], [], {}
        self._inputs = []

    # -- narrative pieces --------------------------------------------------------------
    def data(self, text: str):
        self._data.append(text)

    def method(self, text: str):
        self._method.append(text)

    def note(self, text: str):
        self._notes.append(text)

    def conclusion(self, text: str):
        self._conclusion = text

    def inputs(self, paths):
        for p in paths:
            p = Path(p)
            try:
                p = p.resolve().relative_to(ROOT)
            except ValueError:
                pass
            self._inputs.append(p.as_posix())

    # -- artefacts -----------------------------------------------------------------------
    def table(self, name: str, df: pd.DataFrame, caption: str, show: bool = True):
        self._tables.append((name, df, caption, show))

    def figure(self, name: str, fig, how_to_read: str):
        self._figures.append((name, fig, how_to_read))

    def stat(self, key: str, est: float, lo=None, hi=None, p=None, unit: str = "pp", note: str = ""):
        self._stats[key] = {"est": est, "lo": lo, "hi": hi, "p": p, "unit": unit, "note": note}

    # -- output --------------------------------------------------------------------------
    def write(self, max_table_rows: int = 40):
        self.dir.mkdir(parents=True, exist_ok=True)
        stamp = _dt.date.today().isoformat()
        commit = _git_commit()
        for name, fig, _ in self._figures:
            fig.savefig(self.dir / f"{name}.png", dpi=160, bbox_inches="tight")
        for name, df, _, _ in self._tables:
            df.to_csv(self.dir / f"{name}.csv", index=False, encoding="utf-8")
        with open(self.dir / "stats.json", "w", encoding="utf-8") as fh:
            json.dump(self._stats, fh, indent=1, ensure_ascii=False)
        meta = {"name": self.name, "title": self.title, "question": self.question,
                "status": self.status, "date": stamp, "commit": commit,
                "conclusion": self._conclusion, "inputs": self._inputs,
                "tables": [t[0] for t in self._tables], "figures": [f[0] for f in self._figures]}
        with open(self.dir / "meta.json", "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=1, ensure_ascii=False)

        L = [f"# {self.title}", "",
             f"*{self.status} · {stamp} · commit `{commit}` · `{self.name}`*", "",
             "## Question", "", self.question, ""]
        if self._data:
            L += ["## Data", ""] + [f"- {t}" for t in self._data] + [""]
        if self._inputs:
            L += ["Input files:", ""] + [f"- `{p}`" for p in self._inputs] + [""]
        if self._method:
            L += ["## Method", ""] + [f"- {t}" for t in self._method] + [""]
        if self._figures:
            L += ["## Figures", ""]
            for name, _, how in self._figures:
                L += [f"### {name}", "", f"![{name}]({name}.png)", "", how, ""]
        if self._tables:
            L += ["## Tables", ""]
            for name, df, cap, show in self._tables:
                L += [f"### {name}  (`{name}.csv`)", "", cap, ""]
                if show:
                    d = df.head(max_table_rows)
                    L += [_md_table(d), ""]
                    if len(df) > max_table_rows:
                        L += [f"*({len(df)} rows; first {max_table_rows} shown)*", ""]
        if self._stats:
            L += ["## Key numbers  (`stats.json`)", ""]
            for k, v in self._stats.items():
                s = f"- **{k}**: {_fmt(v['est'])}"
                if v.get("lo") is not None:
                    s += f" [{_fmt(v['lo'])}, {_fmt(v['hi'])}]"
                if v.get("p") is not None:
                    s += f", p = {v['p']:.3f}"
                s += f" {v.get('unit', '')}"
                if v.get("note"):
                    s += f" — {v['note']}"
                L.append(s)
            L.append("")
        if self._notes:
            L += ["## Notes and caveats", ""] + [f"- {t}" for t in self._notes] + [""]
        if self._conclusion:
            L += ["## Conclusion (preliminary)", "", self._conclusion, ""]
        (self.dir / "README.md").write_text("\n".join(L), encoding="utf-8")
        return self.dir


def _fmt(x) -> str:
    try:
        return f"{float(x):+.1f}" if abs(float(x)) < 1000 else f"{float(x):.3g}"
    except (TypeError, ValueError):
        return str(x)


def _md_table(df: pd.DataFrame) -> str:
    def cell(v, col):
        if isinstance(v, float):
            if col.endswith("_p") or col == "p":
                return f"{v:.3f}"
            return f"{v:.1f}"
        return str(v)
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(cell(r[c], c) for c in cols) + " |")
    return "\n".join(out)


def rebuild_index(results_dir: Path | str = RESULTS) -> Path:
    """results/README.md: one line per analysis folder (from its meta.json), newest last."""
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    L = ["# Analysis results", "",
         "One folder per analysis. Each README says what question it answers, which rows it uses, "
         "what is pooled, what the bootstrap unit is, and how to read the figures. "
         "Regenerate everything with the scripts in `4_analysis/`; regenerate this index with "
         "`python -c \"from pbanalysis import report; report.rebuild_index()\"`.", "",
         "| analysis | status | date | question | preliminary conclusion |", "|---|---|---|---|---|"]
    for d in sorted(p for p in results_dir.iterdir() if p.is_dir()):
        mp = d / "meta.json"
        if not mp.exists():
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        L.append(f"| [{m['name']}]({m['name']}/README.md) | {m.get('status','')} | {m.get('date','')} "
                 f"| {m['question']} | {m.get('conclusion','')} |")
    out = results_dir / "README.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out
