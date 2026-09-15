"""Complete-pair language comparisons with shared, mode-stratified prompt draws.

Arrays have shape (observed estimate + B draws, models). Each model has equal weight
when these arrays are averaged. A missing member excludes the whole pair for that model.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import binomtest


def divide(num, den):
    num, den = np.broadcast_arrays(num, den)
    return np.divide(num, den, out=np.full(num.shape, np.nan, dtype=float), where=den > 0)


class LanguagePairs:
    def __init__(self, df, B=5000, seed=20260915):
        if df.duplicated(["target", "lang", "prompt_id"]).any():
            raise ValueError("duplicate model/language/prompt")
        self.targets = sorted(df.target.unique())
        self.languages = sorted(df.lang.unique())
        self.B = B
        self.data, self.truncated, self.counts, self.meta = {}, {}, {}, {}
        rng = np.random.default_rng(seed)
        for mode, d in df.groupby("mode", sort=True):
            ids = sorted(d.prompt_id.unique())
            n = len(ids)
            idx = pd.MultiIndex.from_product([ids, self.targets], names=["prompt_id", "target"])
            values = d.assign(value=d.refuse.where(d.valid)).pivot(index=["prompt_id", "target"], columns="lang", values="value")
            tr = d.pivot(index=["prompt_id", "target"], columns="lang", values="truncated")
            self.data[mode] = values.reindex(index=idx, columns=self.languages).to_numpy(float).reshape(n, len(self.targets), -1)
            self.truncated[mode] = tr.reindex(index=idx, columns=self.languages).fillna(True).to_numpy(bool).reshape(n, len(self.targets), -1)
            self.meta[mode] = d.drop_duplicates("prompt_id").set_index("prompt_id").loc[ids]
            self.counts[mode] = np.vstack([np.ones(n), rng.multinomial(n, np.full(n, 1/n), size=B)])

    def compare(self, language, reference, mode, *, factor=None, level=None, exclude_truncated=False):
        a, b = self.languages.index(language), self.languages.index(reference)
        x, y = self.data[mode][:, :, a], self.data[mode][:, :, b]
        keep = np.isfinite(x) & np.isfinite(y)
        if factor is not None:
            keep &= self.meta[mode][factor].eq(level).to_numpy()[:, None]
        if exclude_truncated:
            keep &= ~(self.truncated[mode][:, :, a] | self.truncated[mode][:, :, b])
        more = (keep & (x > y)).sum(axis=0)
        less = (keep & (x < y)).sum(axis=0)
        both = (keep & (x == 1) & (y == 1)).sum(axis=0)
        counts = self.counts[mode]
        den = counts @ keep.astype(float)
        rate_a = divide(counts @ np.where(keep, x, 0), den)
        rate_b = divide(counts @ np.where(keep, y, 0), den)
        p = np.array([binomtest(int(u), int(u+v), .5).pvalue if u+v else 1. for u, v in zip(more, less)])
        return dict(delta=rate_a-rate_b, rate_language=rate_a, rate_reference=rate_b,
                    n_pairs=keep.sum(axis=0), more=more, less=less, both=both,
                    direction=divide(more-less, more+less), p_exact=p)

    def rates(self, language, mode):
        x = self.data[mode][:, :, self.languages.index(language)]
        return divide(self.counts[mode] @ np.nan_to_num(x), self.counts[mode] @ np.isfinite(x).astype(float))

    def ranges(self, mode):
        """Descriptive extrema on each model's common set across every language.

        The half-count log-odds range is explicitly a smoothed descriptor, not a test.
        Language ties are retained as comma-separated codes.
        """
        x = self.data[mode]
        keep = np.isfinite(x).all(axis=2)
        n = keep.sum(axis=0)
        k = np.where(keep[:, :, None], x, 0).sum(axis=0)
        rates = divide(k, n[:, None])
        out = []
        for i, target in enumerate(self.targets):
            if n[i] == 0:
                raise ValueError(f"no prompts complete in all languages for {target}, {mode}")
            low, high = rates[i].min(), rates[i].max()
            logits = np.log((k[i]+.5)/(n[i]-k[i]+.5))
            out.append(dict(target=target, mode=mode, n_complete=int(n[i]),
                            lowest_lang=",".join(l for l, v in zip(self.languages, rates[i]) if v == low),
                            highest_lang=",".join(l for l, v in zip(self.languages, rates[i]) if v == high),
                            min_rate=100*low, max_rate=100*high, range_pp=100*(high-low),
                            log_odds_range_half=float(logits.max()-logits.min())))
        return pd.DataFrame(out)
