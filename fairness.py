"""Binary prediction utility and group fairness metrics with explicit undefined rates."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

def _rate(n,d):return None if d==0 else float(n/d)

def confusion(y,p):
    y,p=np.asarray(y),np.asarray(p)
    if y.ndim!=1 or p.shape!=y.shape or len(y)==0:raise ValueError('Nonempty aligned vectors required')
    if not np.isin(y,[0,1]).all() or not np.isin(p,[0,1]).all():raise ValueError('Binary labels required')
    return {name:int(mask.sum()) for name,mask in {'tp':(y==1)&(p==1),'tn':(y==0)&(p==0),'fp':(y==0)&(p==1),'fn':(y==1)&(p==0)}.items()}

def evaluate(y,p,privileged):
    y,p,g=np.asarray(y),np.asarray(p),np.asarray(privileged)
    counts=confusion(y,p)
    if g.shape!=y.shape or not np.isin(g,[False,True,0,1]).all():raise ValueError('Aligned binary group vector required')
    g=g.astype(bool)
    if not g.any() or g.all():raise ValueError('Both cohorts must be present')
    rates=[]
    for mask in [~g,g]:
        c=confusion(y[mask],p[mask])
        rates.append({'selection':float(p[mask].mean()),'tpr':_rate(c['tp'],c['tp']+c['fn']),'fpr':_rate(c['fp'],c['fp']+c['tn'])})
    u,v=rates
    delta=lambda k:None if u[k] is None or v[k] is None else u[k]-v[k]
    eod,fprd=delta('tpr'),delta('fpr')
    return {**counts,'accuracy':float((y==p).mean()),'statistical_parity_difference':u['selection']-v['selection'],
       'disparate_impact':_rate(u['selection'],v['selection']),
       'equal_opportunity_difference':eod,'average_odds_difference':None if eod is None or fprd is None else (eod+fprd)/2}

def reweighing_weights(y,privileged):
    y,g=np.asarray(y),np.asarray(privileged).astype(bool)
    confusion(y,y)
    if y.shape!=g.shape:raise ValueError('Aligned group vector required')
    weights=np.zeros(len(y),dtype=float)
    for group in [False,True]:
        for label in [0,1]:
            mask=(g==group)&(y==label);joint=mask.mean()
            if joint:weights[mask]=(g==group).mean()*(y==label).mean()/joint
    return weights

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('csv',type=Path);args=parser.parse_args()
    frame=pd.read_csv(args.csv)
    print(json.dumps(evaluate(frame['label'],frame['prediction'],frame['privileged']),indent=2))
