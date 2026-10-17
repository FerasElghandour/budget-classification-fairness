"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

from fairness import evaluate, reweighing_weights
# Fictional, balanced cohorts; not historical fairness results.
labels = [0, 1, 0, 1, 0, 1, 0, 1]
group = [0, 0, 0, 0, 1, 1, 1, 1]
result = {'metrics': evaluate(labels, labels, group), 'weights': reweighing_weights(labels, group).tolist()}

import json
print(json.dumps(result, indent=2))

