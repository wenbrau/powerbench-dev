#!/usr/bin/env python3
"""results/REPORT.md -> one self-contained HTML page (reports/results_v2.html).

A RENDERER, not an analysis: it reads the markdown that `build_results_report.py` already
assembled from the per-analysis READMEs and computes no metric of its own. Every figure is
embedded as a base64 data URI, so the output file can be opened or mailed on its own with
nothing next to it (~3.4 MB).

What it adds over reading the markdown: the `Key numbers` bullets become a table with a
measured / not-distinguishable-from-zero flag read off the block's own p-values, Data and
Method sit side by side, tables over 14 rows collapse, and each block's conclusion and
caveats get their own panel.

    python 4_analysis/reports/build_results_html.py [out.html]

Style lives next to it in `results_html.css` + `results_html_shell.html`.
"""
import base64, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), "results")
SRC = os.path.join(ROOT, "REPORT.md")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results_v2.html")

# ---------- inline markdown ----------
def inline(t):
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t

NUM = re.compile(r"^[-+−]?[\d.,]+%?$|^[-+−]?\d+\.\d+$|^\[.*\]$|^[-+−]?[\d.]+ ?pp$")
def numeric(c):
    c = c.strip()
    return bool(c) and bool(NUM.match(c)) or bool(re.match(r"^[-+−][\d.]", c))

def table(lines, caption=None, src=None):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    head, body = rows[0], rows[2:]
    ncol = len(head)
    align = []
    for i in range(ncol):
        vals = [r[i] for r in body if i < len(r)]
        align.append("num" if vals and sum(numeric(v) for v in vals) >= max(1, len(vals) * 0.6) else "txt")
    h = ['<div class="tbl-wrap"><table>', "<thead><tr>"]
    for i, c in enumerate(head):
        h.append(f'<th class="{align[i]}">{inline(c)}</th>')
    h.append("</tr></thead><tbody>")
    for r in body:
        h.append("<tr>")
        for i, c in enumerate(r):
            h.append(f'<td class="{align[i] if i < ncol else "txt"}">{inline(c)}</td>')
        h.append("</tr>")
    h.append("</tbody></table></div>")
    t = "".join(h)
    if len(body) > 14:
        t = (f'<details class="long"><summary>{caption or "table"}'
             f'<span class="rowcount">{len(body)} rows</span></summary>{t}</details>')
    return t

def img(path, alt):
    p = os.path.join(ROOT, path)
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    kb = os.path.getsize(p) // 1024
    return (f'<img src="data:image/png;base64,{b64}" alt="{html.escape(alt)}" loading="lazy">', kb)

# ---------- parse ----------
raw = open(SRC, encoding="utf-8").read().split("\n")
preamble, blocks = [], []
cur = None
i = 0
while i < len(raw):
    l = raw[i]
    if l.startswith("## Block "):
        m = re.match(r"## (Block \d+) — (.+?)(?: \((.+)\))?$", l)
        cur = {"num": m.group(1), "title": m.group(2), "scope": m.group(3) or "",
               "meta": "", "sections": []}
        blocks.append(cur)
    elif cur is None:
        preamble.append(l)
    elif l.startswith("*preliminary"):
        cur["meta"] = l.strip("*")
    elif l.startswith("### "):
        cur["sections"].append({"name": re.sub(r"\s*\(.*\)\s*$", "", l[4:]).strip(),
                                "note": (re.search(r"\((.+)\)\s*$", l[4:]) or [None, ""])[1],
                                "lines": []})
    elif cur["sections"]:
        cur["sections"][-1]["lines"].append(l)
    i += 1

# ---------- render a section body ----------
def _blocks_of(L):
    """Split a section body into (heading_or_None, lines) groups on #### headings."""
    groups, head, buf = [], None, []
    for l in L:
        if l.strip().startswith("#### "):
            groups.append((head, buf)); head, buf = l.strip()[5:], []
        else:
            buf.append(l)
    groups.append((head, buf))
    return groups

def _prose(lines):
    out, ul = [], []
    def flush():
        nonlocal ul
        if ul:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in ul) + "</ul>")
            ul = []
    for l in lines:
        s = l.strip()
        if not s or s == "---" or s.startswith("<a id=") or s.startswith("!["):
            continue
        if s == "Input files:":
            flush(); out.append('<p class="sub">Input files</p>'); continue
        if s.startswith("- "):
            ul.append(s[2:]); continue
        flush(); out.append(f"<p>{inline(s)}</p>")
    flush()
    return "".join(out)

def render(sec, block, fig_start=0):
    fign = fig_start
    out = []
    for head, lines in _blocks_of(sec["lines"]):
        pipes = [l for l in lines if l.strip().startswith("|")]
        imgs = [l.strip() for l in lines if l.strip().startswith("![")]
        if head is None:
            body = _prose(lines)
            if pipes:
                body += table(pipes)
            if body:
                out.append(body)
            continue
        name, src = head, None
        m = re.match(r"(.+?)\s+\(`(.+?)`\)", head)
        if m:
            name, src = m.group(1).strip(), m.group(2)
        if imgs:
            mm = re.match(r"!\[(.*?)\]\((.+?)\)", imgs[0])
            tag, _kb = img(mm.group(2), mm.group(1))
            fign += 1
            cap = _prose(lines)
            out.append(
                f'<figure><figcaption class="fig-head">'
                f'<span class="fig-n">Fig {block["num"].split()[1]}.{fign}</span>'
                f'<code>{html.escape(name)}</code></figcaption>{tag}'
                f'<figcaption class="fig-cap">{cap}</figcaption></figure>')
            continue
        lab = f'<code>{html.escape(name)}</code>'
        if src:
            lab += f' <span class="src">{html.escape(src)}</span>'
        body = f'<div class="tbl"><div class="tbl-head">{lab}</div>'
        desc = _prose(lines)
        if desc:
            body += f'<div class="tbl-desc">{desc}</div>'
        if pipes:
            body += table(pipes, lab, src)
        else:
            body += '<p class="csvonly">Not inlined in the report — read it from the CSV.</p>'
        out.append(body + "</div>")
    return "".join(out), fign

# ---------- key numbers as a real table ----------
KEY = re.compile(r"\*\*(.+?)\*\*:\s*([-+−][\d.]+)\s*\[(.+?)\]\s*,\s*p\s*=\s*([\d.]+)\s*pp?(?:\s*—\s*(.+))?$")
def keynumbers(sec):
    rows, extra = [], []
    for l in sec["lines"]:
        s = l.strip()
        if not s.startswith("- "):
            continue
        m = KEY.match(s[2:])
        if m:
            name, val, ci, p, note = m.groups()
            rows.append((name, val, ci, float(p), note or ""))
        else:
            extra.append(s[2:])
    if not rows:
        return None
    h = ['<div class="tbl-wrap"><table class="keynum"><thead><tr>'
         '<th class="txt">quantity</th><th class="num">estimate (pp)</th>'
         '<th class="num">95% interval</th><th class="num">p</th>'
         '<th class="txt">read</th></tr></thead><tbody>']
    for name, val, ci, p, note in rows:
        sig = p < 0.05
        chip = ('<span class="chip yes">measured</span>' if sig
                else '<span class="chip no">not distinguishable from 0</span>')
        if note:
            chip += f'<span class="note">{inline(note)}</span>'
        h.append(f'<tr class="{"sig" if sig else ""}"><td class="txt"><code>{html.escape(name)}</code></td>'
                 f'<td class="num big">{html.escape(val)}</td><td class="num ci">[{html.escape(ci)}]</td>'
                 f'<td class="num">{p:.3f}</td><td class="txt">{chip}</td></tr>')
    h.append("</tbody></table></div>")
    body = "".join(h)
    if extra:
        body += "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in extra) + "</ul>"
    return body

# ---------- assemble ----------
SEC_ORDER = ["Question", "Data", "Method", "Figures", "Tables", "Key numbers",
             "Notes and caveats", "Conclusion"]
parts, nav = [], []
for b in blocks:
    bid = b["num"].lower().replace(" ", "-")
    nav.append((bid, b["num"], b["title"]))
    secs = {s["name"]: s for s in b["sections"]}
    meta = b["meta"]
    body = [f'<section class="block" id="{bid}">',
            '<header class="block-head">',
            '<p class="eyebrow"><span class="bnum">' + html.escape(b["num"]) + '</span>'
            + ('<span class="scope">' + html.escape(b["scope"]) + '</span>' if b["scope"] else '') + '</p>',
            f'<h2>{inline(b["title"])}</h2>',
            f'<p class="meta">{inline(meta)}</p>',
            "</header>"]
    # question as lead
    q = secs.get("Question")
    if q:
        txt = " ".join(x.strip() for x in q["lines"] if x.strip())
        body.append(f'<p class="lead">{inline(txt)}</p>')
    # data + method side by side
    dm = []
    for nm in ("Data", "Method"):
        if nm in secs:
            h, _ = render(secs[nm], b)
            dm.append(f'<div class="dm-col"><h3>{nm}</h3>{h}</div>')
    if dm:
        body.append(f'<div class="dm">{"".join(dm)}</div>')
    if "Figures" in secs:
        h, _ = render(secs["Figures"], b)
        body.append(f'<h3 class="rule">Figures</h3>{h}')
    if "Tables" in secs:
        h, _ = render(secs["Tables"], b)
        body.append(f'<h3 class="rule">Tables</h3><div class="tables">{h}</div>')
    if "Key numbers" in secs:
        kn = keynumbers(secs["Key numbers"])
        if kn is None:
            kn, _ = render(secs["Key numbers"], b)
        body.append(f'<h3 class="rule">Key numbers <span class="src">stats.json</span></h3>{kn}')
    if "Notes and caveats" in secs:
        h, _ = render(secs["Notes and caveats"], b)
        body.append(f'<aside class="caveats"><h3>Notes and caveats</h3>{h}</aside>')
    for nm in secs:
        if nm.startswith("Conclusion"):
            h, _ = render(secs[nm], b)
            body.append(f'<aside class="conclusion"><p class="k">Conclusion — preliminary</p>{h}</aside>')
            break
    body.append("</section>")
    parts.append("".join(body))

navhtml = "".join(
    f'<li><a href="#{i}"><span class="n">{n.split()[1]}</span><span class="t">{html.escape(t)}</span></a></li>'
    for i, n, t in nav)

preamble_txt = [x.strip() for x in preamble if x.strip() and not x.startswith("#")
                and not x.startswith("- [") and x.strip() != "## Contents"
                and not x.startswith("<a id=")]
gen_line = next((x for x in preamble_txt if x.startswith("Generated by")), "")
rules_line = next((x for x in preamble_txt if x.startswith("Reading rules")), "")

CSS = open(os.path.join(HERE, "results_html.css"), encoding="utf-8").read()
SHELL = open(os.path.join(HERE, "results_html_shell.html"), encoding="utf-8").read()
out = (SHELL.replace("{{CSS}}", CSS).replace("{{NAV}}", navhtml)
       .replace("{{BLOCKS}}", "".join(parts))
       .replace("{{GEN}}", inline(gen_line)).replace("{{RULES}}", inline(rules_line)))
open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
