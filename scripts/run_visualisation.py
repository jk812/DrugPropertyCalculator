"""Plot the absorption results for the cleaned compound set."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from property_prediction.visualisation import assess, plot_property_space, plot_rule_summary

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data/processed/assessed.csv"

if CACHE.exists():
    data = pd.read_csv(CACHE)
else:
    frame = pd.read_csv(ROOT / "data/processed/smiles.csv").sample(5000, random_state=0)
    data = assess(frame)
    data.to_csv(CACHE, index=False)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
plot_property_space(data, ax=axes[0])
plot_rule_summary(data, ax=axes[1])
plt.tight_layout()
plt.show()
