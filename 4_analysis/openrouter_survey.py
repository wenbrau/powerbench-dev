#!/usr/bin/env python3
"""Survey OpenRouter for target-panel candidates, with real prices.

Two things worth knowing, both learned the hard way:

1. The discount flag is NOT in `/api/v1/models`. It lives on
   `/api/v1/models/{author}/{slug}/endpoints`, under `pricing.discount` (0.66 = 66% off), because
   a discount belongs to one PROVIDER's endpoint rather than to the model.
2. A discounted endpoint is often MORE expensive than the default route. `/api/v1/models` already
   reports the cheapest routed price, so a 50%-off endpoint at one provider can still sit above it.
   Effective price = min(default route, best discounted endpoint) — anything else overstates the
   saving. Of 39 discounted models, only a handful actually beat their own default route.

    python3 4_analysis/openrouter_survey.py            # print the table
    python3 4_analysis/openrouter_survey.py --refresh  # re-query all endpoints (~340 requests)
"""
import argparse
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "4_analysis/openrouter_discounts.json"
# one full 576-cell English run: prompt ~140 tokens, response ~650 (observed median resp_len)
N, TIN, TOUT = 576, 140, 650


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "powerbench-research"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def run_cost(p_per_m, c_per_m):
    return N * (TIN * p_per_m + TOUT * c_per_m) / 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    models = fetch("https://openrouter.ai/api/v1/models")["data"]
    byid = {m["id"]: m for m in models}

    if a.refresh or not CACHE.exists():
        ids = sorted({m["id"].split(":")[0] for m in models})
        print(f"querying {len(ids)} endpoint lists…")

        def one(mid):
            try:
                d = fetch(f"https://openrouter.ai/api/v1/models/{mid}/endpoints")
                eps = (d.get("data") or d).get("endpoints", [])
                return mid, [(float(e["pricing"]["discount"]), e.get("provider_name"),
                              float(e["pricing"]["prompt"]) * 1e6,
                              float(e["pricing"]["completion"]) * 1e6)
                             for e in eps if e.get("pricing", {}).get("discount")]
            except Exception:
                return mid, None
        out = {}
        with ThreadPoolExecutor(max_workers=24) as ex:
            for f in as_completed([ex.submit(one, i) for i in ids]):
                mid, v = f.result()
                out[mid] = v
        CACHE.write_text(json.dumps(out))
    disc = json.loads(CACHE.read_text())

    rows = []
    for mid, eps in disc.items():
        if not eps or mid not in byid:
            continue
        lp = float(byid[mid]["pricing"]["prompt"]) * 1e6
        lc = float(byid[mid]["pricing"]["completion"]) * 1e6
        d, prov, p, c = max(eps)
        default, discounted = run_cost(lp, lc), run_cost(p, c)
        rows.append({"id": mid, "discount": d, "provider": prov,
                     "default_run": default, "discounted_run": discounted,
                     "effective_run": min(default, discounted),
                     "discount_helps": discounted < default})

    rows.sort(key=lambda r: r["effective_run"])
    print(f"{'model':44s}{'disc':>6s}{'default':>10s}{'discounted':>12s}{'effective':>11s}  helps?")
    for r in rows:
        print(f"{r['id']:44s}{r['discount']*100:5.0f}%{'$'+format(r['default_run'],'.2f'):>10s}"
              f"{'$'+format(r['discounted_run'],'.2f'):>12s}{'$'+format(r['effective_run'],'.2f'):>11s}"
              f"  {'yes' if r['discount_helps'] else 'no — default route is cheaper'}")
    helps = [r for r in rows if r["discount_helps"]]
    print(f"\n{len(rows)} models carry a discounted endpoint; only {len(helps)} of them beat their "
          f"own default route: {', '.join(r['id'] for r in helps)}")
    print(f"\ncost basis: one {N}-cell English run, ~{TIN} prompt / ~{TOUT} completion tokens.")


if __name__ == "__main__":
    main()
