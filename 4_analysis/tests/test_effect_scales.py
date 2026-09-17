"""Analytical checks for scale choice and preservation of paired sampling."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis_24_effect_scales import logit_change, paired_counts
from pbanalysis.paired_languages import LanguagePairs


def test_equal_odds_multipliers_can_have_different_absolute_changes():
    # 10% -> 20% and 40% -> 60% both multiply odds by 2.25.
    actual = logit_change(np.array([20., 60.]), np.array([10., 40.]), np.array([100., 100.]), 0.)
    np.testing.assert_allclose(actual, np.log(2.25))


def test_symmetric_smoothing_preserves_sign_and_reversal_at_boundaries():
    for alpha in (.25, .5, 1.):
        before = np.array([0., 0., 100., 20., 60.])
        after = np.array([0., 100., 0., 30., 50.])
        dl = logit_change(after, before, 100., alpha)
        assert np.isfinite(dl).all()
        np.testing.assert_array_equal(np.sign(dl), np.sign(after-before))
        np.testing.assert_allclose(dl, -logit_change(before, after, 100., alpha))


def test_model_mean_logit_can_reverse_mean_percentage_point_direction():
    # +10 pp centrally, -5 pp near zero: signs per model stay fixed.
    before, after = np.array([40., 6.]), np.array([50., 1.])
    assert (after-before).mean() > 0
    assert logit_change(after, before, 100., .5).mean() < 0


def test_marginal_odds_ratio_is_not_matched_pair_odds_ratio():
    # both=10, more=20, less=5, neither=65; matched OR=4.
    marginal = logit_change(np.array([30.]), np.array([15.]), 100., 0.)[0]
    np.testing.assert_allclose(np.exp(marginal), (30/70)/(15/85))
    assert not np.isclose(marginal, np.log(20/5))


def test_complete_pair_masks_and_shared_resampling():
    records = []
    for target in ('A', 'B'):
        for lang in ('en', 'sw'):
            for i in range(20):
                records.append(dict(target=target, lang=lang, prompt_id=f'p{i:02}', mode='pg',
                    refuse=int(i < (10 if lang == 'en' else 15)), valid=not (i == 19 and lang == 'en'),
                    truncated=(i == 14 and lang == 'sw')))
    e = LanguagePairs(pd.DataFrame(records), B=100, seed=1)
    n, kp, kn, more, less, both = paired_counts(e, 'sw', 'en', 'pg')
    np.testing.assert_array_equal(n[0], [19, 19])
    np.testing.assert_array_equal(kp[0], [15, 15])
    np.testing.assert_array_equal(kn[0], [10, 10])
    np.testing.assert_array_equal(more, [5, 5])
    np.testing.assert_array_equal(less, [0, 0])
    np.testing.assert_array_equal(both, [10, 10])
    assert np.any(n[1:, 0] != n[0, 0])  # valid denominators vary by resample
    dl = logit_change(kp, kn, n, .5)
    np.testing.assert_allclose(dl[:, 0], dl[:, 1])
    nr, kpr, knr, *_ = paired_counts(e, 'sw', 'en', 'pg', exclude_truncated=True)
    np.testing.assert_array_equal(nr[0], [18, 18])
    np.testing.assert_array_equal(kpr[0], [14, 14])
    np.testing.assert_array_equal(knr[0], [10, 10])
