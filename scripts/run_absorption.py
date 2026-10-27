"""Apply the absorption rules to a sample of the cleaned compound set."""

from pathlib import Path

import pandas as pd

from property_prediction.molecules import Molecule
from property_prediction.predictors import absorption

ROOT = Path(__file__).resolve().parents[1]

frame = pd.read_csv(ROOT / "data/processed/smiles.csv").sample(10, random_state=0)

for row in frame.itertuples():
    results = absorption(Molecule(row.smiles))
    summary = "  ".join(f"{r.name}={'pass' if r.passes else 'FAIL'}" for r in results)
    print(f"{row.source_id:<12} {summary}")
    for r in results:
        for v in r.violations:
            print(f"{'':<12}   {v}")
