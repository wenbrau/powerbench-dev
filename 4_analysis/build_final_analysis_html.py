#!/usr/bin/env python3
"""Assemble the four computed reports into one portable, tabbed HTML file.

Run after regenerating an individual report:
    .venv/bin/python 4_analysis/build_final_analysis_html.py
"""
import base64
import hashlib
import html
import json
from pathlib import Path
import re

RESULTS=Path(__file__).resolve().parent/'results'
REPORTS=[('19_d1_final','Overview'),('20_d1_languages_final','Languages'),
         ('21_d2_nationality_final','Nationality'),('22_d3_ai_final','AI vs Human')]

STYLE='''
:root{color-scheme:light;--ink:#202b38;--muted:#627080;--accent:#245d80;--line:#dce3e9;--nav-height:110px}
*{box-sizing:border-box}body{margin:0;background:#f5f7f9;color:var(--ink);font:16px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.navbar{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.97);border-bottom:1px solid var(--line);box-shadow:0 2px 12px #24344308}
.nav-inner{max-width:1236px;margin:auto;padding:16px 28px;display:flex;align-items:center;gap:32px}
.brand{font-size:21px;font-weight:750;letter-spacing:-.6px;white-space:nowrap}.brand small{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:550}
.tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;flex:1}
.tab{font:inherit;text-align:left;background:transparent;border:1px solid transparent;border-radius:9px;padding:9px 15px;color:var(--muted);cursor:pointer;line-height:1.35}
.tab .number{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px}.tab .label{font-size:14px;font-weight:650;white-space:nowrap}
.tab:hover{background:#edf3f7;color:var(--ink)}.tab[aria-selected=true]{background:#e8f1f7;border-color:#c9ddea;color:var(--accent)}
.tab:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #588eaf;outline-offset:3px}
main{max-width:1236px;margin:28px auto 70px;padding:0 28px}.report-panel{background:#fff;border:1px solid var(--line);border-radius:12px;padding:34px 38px;min-width:0}
[hidden]{display:none!important}h1{font-size:clamp(25px,3vw,34px);letter-spacing:-.6px;line-height:1.2;margin:0 0 18px}h2{font-size:23px;line-height:1.25;letter-spacing:-.3px;margin-top:34px}h3{font-size:19px}
p,li{overflow-wrap:anywhere}li{margin:8px 0}a{color:var(--accent);text-underline-offset:3px}section{margin:44px 0}section h2{text-transform:none}
img{display:block;width:100%;height:auto;margin:20px 0}details{margin:20px 0;overflow:auto;border:1px solid var(--line);border-radius:8px;padding:12px 16px}summary{cursor:pointer;font-weight:650}
table{font-size:12px;border-collapse:collapse;white-space:nowrap}td,th{padding:7px;border-bottom:1px solid var(--line);text-align:right}th{background:#f5f7f9}td:first-child,th:first-child{text-align:left}
.audit{background:#fffcf3;border-color:#e4d9b9}.audit h2{margin-top:24px}.audit:target{outline:2px solid #b69a52;outline-offset:4px}
[id]{scroll-margin-top:calc(var(--nav-height) + 20px)}footer{text-align:center;color:var(--muted);font-size:12px;padding:0 20px 32px}
@media(max-width:760px){.nav-inner{display:block;padding:10px 16px}.brand{font-size:18px;margin-bottom:8px}.brand small{display:inline;margin-left:10px;font-size:9px}.tabs{gap:4px}.tab{padding:8px}.tab .label{font-size:12px}.tab .number{font-size:9px}main{margin-top:16px;padding:0 12px}.report-panel{padding:24px 18px}h2{font-size:21px}}
@media(max-width:430px){.tabs{grid-template-columns:repeat(2,minmax(0,1fr))}.tab .number{display:inline;margin-right:6px}.tab .label{font-size:12px}.brand small{letter-spacing:0}}
@media print{.navbar,footer{display:none}body{background:#fff}main{margin:0;padding:0;max-width:none}.report-panel{padding:0;border:0}details{overflow:visible}section,img{break-inside:avoid}}
'''
SCRIPT='''
const tabs = [...document.querySelectorAll('[role="tab"]')];
const panels = [...document.querySelectorAll('[role="tabpanel"]')];
const navbar = document.querySelector('.navbar');
function showSection(id, {focus = false, scroll = true} = {}) {
  panels.forEach(panel => panel.hidden = panel.id !== id);
  tabs.forEach(tab => {
    const active = tab.getAttribute('aria-controls') === id;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    if (active && focus) tab.focus({preventScroll:true});
  });
  const chosen = tabs.find(tab => tab.getAttribute('aria-controls') === id);
  document.title = `PowerBench · ${chosen.querySelector('.label').textContent}`;
  if (scroll) window.scrollTo({top:0, behavior:'instant'});
}
function followHash({focus = false} = {}) {
  const id = (location.hash.match(/^#(figure[1-4])(?:$|-)/) || [,'figure1'])[1];
  showSection(id, {focus});
  if (location.hash === '#figure4-audit') {
    const audit = document.getElementById('figure4-audit');
    audit.open = true;
    requestAnimationFrame(() => audit.scrollIntoView({block:'start'}));
  }
}
function selectTab(tab, focus = false) {
  const hash = '#' + tab.getAttribute('aria-controls');
  if (location.hash !== hash) history.pushState(null, '', hash);
  followHash({focus});
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault(); selectTab(tabs[next], true);
  });
});
window.addEventListener('hashchange', () => followHash());
new ResizeObserver(() => document.documentElement.style.setProperty('--nav-height', navbar.offsetHeight + 'px')).observe(navbar);
followHash();
'''


def report_body(path):
    source=path.read_text()
    # These reports are produced by the shared renderer; reject unexpected structure.
    if source.count('</style>')!=1 or '<script' in source.lower():
        raise ValueError(f'Unexpected report markup: {path}')
    return source.split('</style>',1)[1]


def main():
    buttons=[];panels=[];sources=[];expected_images=0
    for i,(directory,label) in enumerate(REPORTS,1):
        path=RESULTS/directory/'report.html';sources.append(path)
        body=report_body(path);expected_images+=body.count('data:image/png;base64,')
        if i==4:
            audit_path=path.parent/'audit.html';csv_path=path.parent/'html_reconciliation.csv';sources.extend([audit_path,csv_path])
            audit=report_body(audit_path)
            audit=audit.replace('href="report.html"','href="#figure4"')
            download='data:text/csv;base64,'+base64.b64encode(csv_path.read_bytes()).decode()
            audit=audit.replace('href="html_reconciliation.csv"',f'download="html_reconciliation.csv" href="{download}"')
            audit=re.sub(r'<(/?)h([12])>',lambda m:f'<{m[1]}h{int(m[2])+1}>',audit)
            body=body.replace('href="audit.html"','href="#figure4-audit"')
            body+='\n<details class="audit" id="figure4-audit"><summary>Figure 4 · historical HTML audit</summary>'+audit+'</details>'
        buttons.append(f'<button class="tab" type="button" role="tab" id="tab{i}" aria-controls="figure{i}" aria-selected="{str(i==1).lower()}" tabindex="{0 if i==1 else -1}"><span class="number">Figure {i}</span><span class="label">{html.escape(label)}</span></button>')
        panels.append(f'<article class="report-panel" role="tabpanel" id="figure{i}" aria-labelledby="tab{i}" tabindex="0"'+(' hidden' if i!=1 else '')+'>'+body+'</article>')
    page='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PowerBench · Final analysis</title><style>'+STYLE+'</style></head><body>'
    page+='<header class="navbar"><div class="nav-inner"><div class="brand">PowerBench<small>24-model analysis</small></div><nav class="tabs" role="tablist" aria-label="Analysis figures">'+''.join(buttons)+'</nav></div></header>'
    page+='<noscript><style>.report-panel[hidden]{display:block!important;margin-top:28px}</style><p>JavaScript is disabled. All four reports are shown below.</p></noscript><main>'+''.join(panels)+'</main><footer>PowerBench · Figures 1–4 · 12 US and 12 China models</footer><script>'+SCRIPT+'</script></body></html>'
    assert page.count('data:image/png;base64,')==expected_images==32
    # Everything needed to read the report, including audit and comparison CSV, is inline.
    for href in re.findall(r'href=["\x27]([^"\x27]+)',page):
        assert href.startswith(('#','data:')),href
    out=RESULTS/'final_analysis.html';out.write_text(page)
    sources.append(Path(__file__))
    (RESULTS/'final_analysis.meta.json').write_text(json.dumps(dict(figures=32,sections=4,
        sha256={str(p.relative_to(RESULTS.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}),indent=2)+'\n')
    print(f'{out}: {out.stat().st_size:,} bytes, 4 sections, {expected_images} embedded figures')


if __name__=='__main__':main()
