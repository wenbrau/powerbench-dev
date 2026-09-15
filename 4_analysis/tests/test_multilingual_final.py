"""Regression checks for language coverage and paired inference."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pbanalysis import final_panel as fp
from test_final_panel import row, write


def test_read_all_languages_preserves_pairing_key(tmp_path):
    en = row()
    es = {**en, "id": "p-es", "lang": "es", "refuse": 1}
    path = write(tmp_path / "run.jsonl", [en, es])
    d = fp.load_run_final(path, lang=None)
    assert len(d) == 2
    assert d.prompt_id.nunique() == 1
    assert set(d.lang) == {"en", "es"}


def test_multilingual_coverage_and_metadata_protection():
    d = pd.DataFrame([dict(target="A", lang=l, prompt_id="p", mode="pg", domain="Rank",
                          context="Work", scale="individual", standing="low", trigger=None)
                      for l in ("en", "es")])
    check = lambda data: fp.validate_multilingual(data, expected_targets={"A"},
                            expected_ids={"pg": {"p"}}, languages=("en", "es"))
    check(d)
    with pytest.raises(ValueError, match="language"):
        check(d.iloc[:1])
    with pytest.raises(ValueError, match="duplicate"):
        check(pd.concat([d, d.iloc[:1]]))
    d.loc[1, "standing"] = "high"
    with pytest.raises(ValueError, match="standing"):
        check(d)


def synthetic():
    # Only p0/p1 are complete: +1 and 0; unpaired p2 must not inflate the estimate.
    recs = []
    for model in ("A", "B"):
        for lang, vals in [("en", [0, 1, np.nan]), ("es", [1, 1, 0])]:
            for i, value in enumerate(vals):
                recs.append(dict(target=model, lang=lang, prompt_id=f"p{i}", mode="pg",
                                 refuse=value, valid=np.isfinite(value), truncated=(i == 0 and lang == "es"),
                                 scale="individual", standing="low"))
    return pd.DataFrame(recs)


def engine(d=None):
    from pbanalysis.paired_languages import LanguagePairs
    return LanguagePairs(synthetic() if d is None else d, B=200, seed=7)


def test_complete_pairs_and_exact_discordances():
    result = engine().compare("es", "en", "pg")
    assert result["n_pairs"].tolist() == [2, 2]
    assert result["more"].tolist() == [1, 1]
    assert result["less"].tolist() == [0, 0]
    np.testing.assert_allclose(result["delta"][0], [.5, .5])
    np.testing.assert_allclose(result["direction"], [1., 1.])
    np.testing.assert_allclose(result["p_exact"], [1., 1.])


def test_reversal_and_shared_prompt_draws():
    e = engine()
    forward = e.compare("es", "en", "pg")["delta"]
    backward = e.compare("en", "es", "pg")["delta"]
    np.testing.assert_allclose(forward, -backward, equal_nan=True)
    np.testing.assert_allclose(forward[:, 0], forward[:, 1], equal_nan=True)


def test_truncation_exclusion_removes_both_pair_members():
    r = engine().compare("es", "en", "pg", exclude_truncated=True)
    assert r["n_pairs"].tolist() == [1, 1]
    np.testing.assert_allclose(r["delta"][0], [0., 0.])
    assert np.isnan(r["direction"]).all()
    np.testing.assert_allclose(r["p_exact"], [1., 1.])


def test_duplicate_language_prompt_cannot_be_averaged():
    d = synthetic()
    with pytest.raises(ValueError, match="duplicate"):
        engine(pd.concat([d, d.iloc[:1]]))


def test_raw_levels_and_range_use_different_explicit_denominators():
    e = engine()
    np.testing.assert_allclose(e.rates("es", "pg")[0], [2/3, 2/3])
    ranges = e.ranges("pg")
    assert ranges.n_complete.tolist() == [2, 2]
    np.testing.assert_allclose(ranges.range_pp, [50., 50.])
    assert ranges.lowest_lang.tolist() == ["en", "en"]
    assert ranges.highest_lang.tolist() == ["es", "es"]
    assert np.isfinite(ranges.log_odds_range_half).all()
