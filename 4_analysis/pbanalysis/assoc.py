"""Small association helpers used by the analyses (item-level agreement, rank correlation).
Descriptive companions to the bootstrap; none of these drive a headline claim."""
from __future__ import annotations

import numpy as np
from scipy import stats as sps


def cohen_kappa(a, b) -> float:
    """Cohen's kappa between two binary vectors (NaNs dropped pairwise)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if a.size == 0:
        return float("nan")
    po = np.mean(a == b)
    pe = np.mean(a) * np.mean(b) + (1 - np.mean(a)) * (1 - np.mean(b))
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def spearman(x, y) -> dict:
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return {"rho": float("nan"), "p": float("nan"), "n": int(ok.sum())}
    r = sps.spearmanr(x[ok], y[ok])
    return {"rho": float(r.statistic), "p": float(r.pvalue), "n": int(ok.sum())}


def sign_consistency(values) -> dict:
    """How many of a set of estimates share the majority sign (for 'consistent across models /
    languages' statements)."""
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    pos, neg = int((v > 0).sum()), int((v < 0).sum())
    return {"n": int(v.size), "positive": pos, "negative": neg,
            "majority_sign": "+" if pos >= neg else "-", "share": max(pos, neg) / v.size if v.size else float("nan")}
