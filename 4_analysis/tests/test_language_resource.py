"""Protect proxy denominators and the language-level association estimand."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_share_denominator_includes_other_and_unknown_languages():
    from pbanalysis.language_resource import extract_shares
    d=pd.DataFrame(dict(crawl=['C']*4,primary_language=['eng','spa','deu','<unknown>'],pages=[500,100,300,100]))
    r=extract_shares(d,'C',{'en':'eng','es':'spa'}).set_index('lang')
    assert r.loc['en','share_pct'] == 50
    assert r.loc['es','share_pct'] == 10
    assert r.loc['en','total_pages'] == 1000


def test_missing_duplicate_or_nonpositive_proxy_is_rejected():
    from pbanalysis.language_resource import extract_shares
    d=pd.DataFrame(dict(crawl=['C','C'],primary_language=['eng','spa'],pages=[50,10]))
    with pytest.raises(ValueError,match='missing'):
        extract_shares(d,'C',{'hi':'hin'})
    with pytest.raises(ValueError,match='duplicate'):
        extract_shares(pd.concat([d,d.iloc[:1]]),'C',{'en':'eng'})
    d.loc[1,'pages']=0
    with pytest.raises(ValueError,match='positive'):
        extract_shares(d,'C',{'es':'spa'})


def test_slope_uses_language_units_and_shared_reference_cancels():
    from pbanalysis.language_resource import association
    x=np.array([-2.,-1.,0.])
    # Each draw differs by a shared English-baseline offset. The slope remains -2.
    y=np.array([[6.,4.,2.],[16.,14.,12.],[-4.,-6.,-8.]])
    r=association(x,y)
    assert r['slope_pp_per_decade'] == pytest.approx(-2)
    assert r['slope_lo'] == pytest.approx(-2)
    assert r['slope_hi'] == pytest.approx(-2)
    assert r['spearman_rho'] == pytest.approx(-1)
    assert r['n_languages'] == 3


def test_constant_outcomes_have_zero_slope_and_undefined_rank_correlation():
    from pbanalysis.language_resource import association
    r=association(np.array([-2.,-1.,0.]),np.ones((3,3))*4)
    assert r['slope_pp_per_decade'] == 0
    assert np.isnan(r['spearman_rho'])
