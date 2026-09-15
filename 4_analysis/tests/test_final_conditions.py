"""Protect cross-dataset labels, condition pairing and literal nationality swaps."""
import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pbanalysis import final_panel as fp
from test_final_panel import row,write


def test_stage_and_condition_metadata_survive_final_judgments(tmp_path):
    base={**row(),"condition":"cn_us","user_nationality":"Chinese","affected_nationality":"American"}
    path=write(tmp_path/'run.jsonl',[base])
    d=fp.load_run_final(path,dataset='D2',extra_columns=('condition','user_nationality','affected_nationality'))
    assert d.loc[0,'dataset']=='D2'
    assert d.loc[0,'condition']=='cn_us'
    assert d.loc[0,'user_nationality']=='Chinese'


def test_regrade_cannot_change_nationality_condition(tmp_path):
    base={**row(),"condition":"cn_us"}
    path=write(tmp_path/'run.jsonl',[base]);grade=write(tmp_path/'grade.jsonl',[{**base,"condition":"us_cn"}])
    with pytest.raises(ValueError,match='condition'):
        fp.load_run_final(path,rejudge_path=grade)


def test_country_swaps_are_checked_by_prompt_not_row_order():
    from pbanalysis.final_conditions import validate_swaps
    d=pd.DataFrame([dict(prompt_id='p',condition='cn_us',user_country='China',affected_country='United States'),
                    dict(prompt_id='p',condition='us_cn',user_country='United States',affected_country='China')])
    validate_swaps(d,[('cn_us','us_cn')])
    validate_swaps(d.iloc[::-1],[('cn_us','us_cn')])
    d.loc[1,'affected_country']='France'
    with pytest.raises(ValueError,match='swap'):
        validate_swaps(d,[('cn_us','us_cn')])


def test_condition_adapter_preserves_complete_pair_bootstrap():
    from pbanalysis.final_conditions import condition_engine
    d=pd.DataFrame([dict(target=t,prompt_id=str(i),condition=c,mode='pg',refuse=v,valid=True,
                        truncated=False,scale='individual',standing='low')
        for t in ('A','B') for i in range(4) for c,v in [('human',i%2),('ai',1)]])
    e=condition_engine(d,B=100,seed=0)
    r=e.compare('ai','human','pg')
    assert r['n_pairs'].tolist()==[4,4]
    assert r['more'].tolist()==[2,2]
    assert r['delta'][0].tolist()==[.5,.5]
    assert (r['delta'][:,0]==r['delta'][:,1]).all()


def test_bank_metadata_equality_ignores_pandas_string_storage():
    from pbanalysis.final_conditions import validate_bank_rows
    bank=pd.DataFrame([dict(row_id='p',prompt_id='p',mode='pg',domain='Wealth')])
    data=bank.assign(target='A').copy()
    data['domain']=data['domain'].astype(object)
    validate_bank_rows(data,bank,{'A'})
    data.loc[0,'domain']='Health'
    with pytest.raises(ValueError,match='domain'):
        validate_bank_rows(data,bank,{'A'})
