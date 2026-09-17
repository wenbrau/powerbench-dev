"""Frozen Common Crawl document shares and descriptive language-level associations."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .final_panel import ROOT, file_digest

PROXY_DIR = ROOT / "4_analysis/inputs/common_crawl"
LANG_CODES = {"en":"eng", "es":"spa", "pt":"por", "fr":"fra", "de":"deu", "zh":"zho", "hi":"hin", "sw":"swa"}


def extract_shares(data, crawl, mapping=LANG_CODES):
    d=data[data.crawl.eq(crawl)].copy()
    if d.empty:
        raise ValueError(f"missing crawl {crawl}")
    if d.primary_language.duplicated().any():
        raise ValueError("duplicate primary language in selected crawl")
    if not np.isfinite(d.pages).all() or (d.pages < 0).any():
        raise ValueError("invalid page counts")
    total=int(d.pages.sum())
    d=d.set_index("primary_language")
    out=[]
    for lang,iso in mapping.items():
        if iso not in d.index:
            raise ValueError(f"missing primary language {iso}")
        n=int(d.loc[iso,"pages"])
        if n <= 0 or total <= 0:
            raise ValueError("selected language counts must be positive")
        out.append(dict(lang=lang,primary_language=iso,crawl=crawl,pages=n,total_pages=total,
                        share_pct=100*n/total,log10_share_pct=np.log10(100*n/total)))
    return pd.DataFrame(out)


def load_proxy():
    source=PROXY_DIR/"languages.csv"
    metadata=json.loads((PROXY_DIR/"source.json").read_text())
    if file_digest(source) != metadata["sha256"]:
        raise ValueError("Common Crawl source checksum mismatch")
    return extract_shares(pd.read_csv(source),metadata["selected_crawl"]),metadata


def association(x, y_draws):
    """OLS slope per log10 share unit, with uncertainty over shared prompt draws.

    y_draws: (observed + bootstrap draws, languages), in percentage points.
    x: fixed log10 document shares. No regression iid-language standard errors or p values.
    """
    x=np.asarray(x,float);y=np.asarray(y_draws,float)
    if x.ndim != 1 or y.ndim != 2 or y.shape[1] != len(x) or len(x) < 3:
        raise ValueError("expected draws by at least three languages")
    if not np.isfinite(x).all() or not np.isfinite(y).all() or np.ptp(x) == 0:
        raise ValueError("finite outcomes and varying proxy required")
    centered=x-x.mean()
    slopes=y @ (centered / (centered @ centered))
    lo,hi=np.quantile(slopes[1:],[.025,.975])
    rho=float(spearmanr(x,y[0]).statistic) if np.ptp(y[0]) else np.nan
    return dict(n_languages=len(x),slope_pp_per_decade=float(slopes[0]),slope_lo=float(lo),
                slope_hi=float(hi),spearman_rho=rho,n_draws=len(slopes)-1,
                intercept=float(y[0].mean()-slopes[0]*x.mean()))
