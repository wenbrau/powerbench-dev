"""Hand-calculated checks for estimates, multiplicity and missing denominators."""
import importlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
a = importlib.import_module("analysis_19_d1_final")


def test_equal_model_mean_does_not_weight_by_available_rows():
    draws = {"A": np.array([0., .1]), "B": np.array([1., .9])}
    np.testing.assert_allclose(a.mean_models(draws, ["A", "B"]), [.5, .5])


def test_bh_preserves_nan_and_original_order():
    np.testing.assert_allclose(a.bh([.04, .001, np.nan, .03]), [.04, .003, np.nan, .04], equal_nan=True)


def test_bootstrap_p_never_reports_zero():
    s = a.interval(np.array([.2, .1, .2, .3]))
    assert s["estimate"] == 20.
    assert s["p_boot"] == .5
    assert s["lo"] > 0


def test_rates_use_valid_denominator_and_harm_conditions_on_nonrefusal():
    d = pd.DataFrame([dict(target="A", model="A", origin="US", lab="L", mode="pg", valid=v,
                           refuse=r, harmful=h) for v,r,h in
                      [(True,1.,0.), (True,0.,1.), (True,0.,0.), (False,np.nan,np.nan)]])
    t = a.point_rates(d).iloc[0]
    assert t.n_total == 4 and t.n_valid == 3 and t.n_refuse == 1
    assert np.isclose(t.rate, 100/3)
    assert t.n_nonrefused == 2 and t.harm_nonrefused == 50
    assert t.rate_lo < t.rate < t.rate_hi


def test_zero_refusal_rate_has_nonzero_upper_interval():
    d = pd.DataFrame([dict(target="A", model="A", origin="US", lab="L", mode="he", valid=True,
                           refuse=0., harmful=0.) for _ in range(20)])
    t = a.point_rates(d).iloc[0]
    assert t.rate == 0
    assert t.rate_hi > 0


def test_bootstrap_tail_mass_counts_roundoff_as_zero():
    from analysis_19_d1_final import interval
    import numpy as np
    # Three exact-zero draws represented with opposite floating-point residuals.
    r=interval(np.array([.1,0.,1e-17,-1e-17,.2,.3,.4,.5,.6,.7,.8]))
    assert np.isclose(r['p_boot'],8/11)
