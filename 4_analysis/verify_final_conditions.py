#!/usr/bin/env python3
"""Independently reconstruct exported paired tables with pandas, without bootstrap code."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def verify(name):
    out=ROOT/'4_analysis/results'/name
    df=pd.read_csv(out/'analysis_rows.csv.gz',low_memory=False)
    per=pd.read_csv(out/'paired_per_model.csv')
    pooled=pd.read_csv(out/'paired_pooled.csv')
    checks=0
    for r in per.itertuples():
        d=df[df.target.eq(r.target)&df['mode'].eq(r.mode)]
        v=d.assign(value=d.refuse.where(d.valid)).pivot(index='prompt_id',columns='condition',values='value')
        pairs=v[[r.positive_condition,r.negative_condition]].dropna();a,b=pairs.iloc[:,0],pairs.iloc[:,1]
        assert len(pairs)==r.n_pairs
        assert (a>b).sum()==r.n_more and (a<b).sum()==r.n_less and ((a==1)&(b==1)).sum()==r.n_both
        assert np.isclose(100*(a-b).mean(),r.estimate,atol=1e-10)
        assert np.isclose(100*a.mean(),r.positive_rate) and np.isclose(100*b.mean(),r.negative_rate)
        assert np.isclose(r.estimate,100*(r.n_more-r.n_less)/r.n_pairs)
        checks+=1
    for r in pooled.itertuples():
        p=per[per['mode'].eq(r.mode)&per.contrast.eq(r.contrast)]
        if r.bloc!='all':p=p[p.origin.eq(r.bloc)]
        assert len(p)==r.n_models
        assert np.isclose(p.estimate.mean(),r.estimate)
        assert np.isclose(p.positive_rate.mean(),r.positive_rate)
        assert np.isclose(p.negative_rate.mean(),r.negative_rate)
    sensitivity=pd.read_csv(out/'sensitivity_no_truncation_model.csv')
    definitions=pd.read_csv(out/'contrast_definitions.csv').set_index('contrast')
    for r in sensitivity.itertuples():
        d=df[df.target.eq(r.target)&df['mode'].eq(r.mode)]
        v=d.assign(value=d.refuse.where(d.valid & ~d.truncated)).pivot(index='prompt_id',columns='condition',values='value')
        definition=definitions.loc[r.contrast]
        p=v[[definition.positive_condition,definition.negative_condition]].dropna()
        assert len(p)==r.n_pairs
        assert np.isclose(100*(p.iloc[:,0]-p.iloc[:,1]).mean(),r.estimate,atol=1e-10)
    result=dict(passed=True,rows=len(df),valid=int(df.valid.sum()),per_model_contrasts=checks,
                pooled_contrasts=len(pooled),truncation_sensitivity_contrasts=len(sensitivity),
                method='Independent pandas pivot and discordant-count reconstruction from exported final analysis rows; loader separately validates raw-source/bank coverage and official-judgment precedence.')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(name,result,flush=True)


if __name__=='__main__':
    for name in ('21_d2_nationality_final','22_d3_ai_final'):verify(name)
