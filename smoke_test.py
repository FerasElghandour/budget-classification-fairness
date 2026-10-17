import numpy as np
from fairness import evaluate,reweighing_weights
y=np.array([0,1,0,1,0,1,0,1]);g=np.array([0,0,0,0,1,1,1,1]);p=y.copy()
r=evaluate(y,p,g)
assert r['accuracy']==1 and r['equal_opportunity_difference']==0 and r['disparate_impact']==1
w=reweighing_weights(y,g);assert np.allclose(w,1)
r=evaluate(y,np.zeros(8),g);assert r['disparate_impact'] is None
try:evaluate(y,p,np.zeros(8))
except ValueError:pass
else:raise AssertionError('Absent cohort accepted')
print('Fairness gaps, undefined ratios, balanced reweighing, and cohort validation passed.')
