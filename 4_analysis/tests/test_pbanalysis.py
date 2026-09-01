"""Synthetic-data tests for pbanalysis. Run:  python -m pytest 4_analysis/tests -q
(or plain `python 4_analysis/tests/test_pbanalysis.py`).

The generator builds a table with the real structure -- prompts x languages x models, one prompt
per (mode, cell) -- with KNOWN refusal probabilities, so every check has a known answer."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pbanalysis import Boot, ci, metrics  # noqa: E402


def synth(n_prompts=192, langs=("en", "zh"), models=("A", "B"), p=None, seed=1,
          lang_shift=None, prompt_sd=1.0):
    """p: mode -> base refusal probability. Each prompt gets a latent difficulty shared across
    languages and models (that is what makes translations non-independent)."""
    rng = np.random.default_rng(seed)
    p = p or {"he": 0.05, "de": 0.20, "pg": 0.25}
    lang_shift = lang_shift or {}
    recs = []
    for mode in ("he", "de", "pg"):
        for i in range(n_prompts):
            pid = f"{mode}-{i:03d}"
            latent = rng.normal(0, prompt_sd)
            for lg in langs:
                for mdl in models:
                    logit = np.log(p[mode] / (1 - p[mode])) + latent + lang_shift.get(lg, 0.0)
                    pr = 1 / (1 + np.exp(-logit))
                    recs.append({"dataset": "D1", "target": mdl, "model": mdl, "origin": "US",
                                 "prompt_id": pid, "row_id": f"{pid}-{lg}", "lang": lg,
                                 "condition": "baseline", "mode": mode, "standing": "med",
                                 "domain": "X", "context": "Y", "scale": "individual",
                                 "refuse": float(rng.random() < pr), "harmful": 0.0,
                                 "valid": True, "provider": "p"})
    return pd.DataFrame(recs)


def test_metrics_algebra():
    assert abs(metrics.components(0.1, 0.2) - 0.28) < 1e-12
    assert abs(metrics.excess(0.1, 0.2, 0.40) - 0.12) < 1e-12
    assert abs(metrics.excess(0.1, 0.2, 0.28)) < 1e-12
    assert abs(metrics.mean3(0.1, 0.2, 0.3) - 0.2) < 1e-12


def test_point_estimate_is_plain_mean():
    df = synth()
    bs = Boot(df, B=50)
    m = bs.mask(model="A", lang="en")
    for mode in ("he", "de", "pg"):
        plain = df[(df.model == "A") & (df.lang == "en") & (df["mode"] == mode)]["refuse"].mean()
        assert abs(bs.rate(m, mode)[0] - plain) < 1e-12


def test_invalid_rows_are_dropped():
    df = synth()
    df.loc[df.index[:10], "valid"] = False
    df.loc[df.index[:10], "refuse"] = np.nan
    bs = Boot(df, B=10)
    assert bs.n == len(df) - 10


def test_excess_zero_under_independent_triggers():
    # pg refusal generated as noisy-OR of two independent triggers -> excess should be ~0
    rng = np.random.default_rng(3)
    n = 4000
    recs = []
    for mode in ("he", "de", "pg"):
        for i in range(n):
            if mode == "he":
                r = rng.random() < 0.10
            elif mode == "de":
                r = rng.random() < 0.30
            else:
                r = (rng.random() < 0.10) or (rng.random() < 0.30)
            recs.append({"dataset": "D1", "target": "A", "model": "A", "origin": "US",
                         "prompt_id": f"{mode}-{i}", "row_id": f"{mode}-{i}", "lang": "en",
                         "condition": "baseline", "mode": mode, "standing": "med", "domain": "X",
                         "context": "Y", "scale": "individual", "refuse": float(r), "harmful": 0.0,
                         "valid": True, "provider": "p"})
    bs = Boot(pd.DataFrame(recs), B=500)
    c = ci(bs.summary(bs.mask(model="A"))["excess"])
    assert c["lo"] <= 0 <= c["hi"], c
    assert abs(c["est"]) < 0.03


def test_ci_coverage_roughly_nominal():
    # true excess under the generator: pg has its own base rate, so true excess = p_pg - noisyOR
    p = {"he": 0.05, "de": 0.20, "pg": 0.30}
    # the latent shifts rates on the probability scale; get the truth by simulation at huge n
    big = synth(n_prompts=40000, langs=("en",), models=("A",), p=p, seed=99)
    r = metrics.rates(big)
    truth = metrics.excess(r["he"], r["de"], r["pg"])
    hits = 0
    for seed in range(20):
        df = synth(n_prompts=192, langs=("en",), models=("A",), p=p, seed=seed)
        bs = Boot(df, B=400, seed=seed)
        c = ci(bs.summary(bs.mask(model="A"))["excess"])
        hits += c["lo"] <= truth <= c["hi"]
    assert hits >= 16, hits  # 20 trials at 95%: 16+ is well within binomial noise


def test_paired_language_contrast_is_tighter_than_unpaired():
    # Same prompts in en and zh, zh shifted up. Paired (same draws, same prompts) interval on the
    # difference must be narrower than the interval you would get treating them as independent.
    df = synth(n_prompts=192, langs=("en", "zh"), models=("A",), lang_shift={"zh": 0.6}, prompt_sd=1.5)
    bs = Boot(df, B=600, seed=0)
    en, zh = bs.mask(lang="en"), bs.mask(lang="zh")
    paired = bs.summary(zh)["pg"] - bs.summary(en)["pg"]
    w_paired = np.diff(np.quantile(paired[1:], [0.025, 0.975]))[0]
    # independent: shuffle the draw order of one arm
    rng = np.random.default_rng(1)
    a, b = bs.summary(zh)["pg"][1:], bs.summary(en)["pg"][1:]
    indep = a - rng.permutation(b)
    w_indep = np.diff(np.quantile(indep, [0.025, 0.975]))[0]
    assert w_paired < w_indep, (w_paired, w_indep)
    assert ci(paired)["est"] > 0 and ci(paired)["p"] < 0.05


def test_translations_do_not_inflate_n():
    # 8 languages of the same prompts must NOT give a much tighter interval than 1 language when
    # the latent prompt difficulty dominates: the unit is the prompt, not the row.
    p = {"he": 0.05, "de": 0.20, "pg": 0.25}
    one = synth(n_prompts=192, langs=("en",), models=("A",), p=p, prompt_sd=2.5, seed=5)
    eight = synth(n_prompts=192, langs=tuple("abcdefgh"), models=("A",), p=p, prompt_sd=2.5, seed=5)
    w1 = np.diff(np.quantile(Boot(one, B=600).summary(np.ones(len(one), bool))["pg"][1:], [0.025, 0.975]))[0]
    w8 = np.diff(np.quantile(Boot(eight, B=600).summary(np.ones(len(eight), bool))["pg"][1:], [0.025, 0.975]))[0]
    assert w8 > 0.5 * w1, (w1, w8)   # a naive row bootstrap would give w8 ~ w1 / sqrt(8) = 0.35 w1


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok ", name)
