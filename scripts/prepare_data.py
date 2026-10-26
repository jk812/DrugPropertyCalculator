#!/usr/bin/env python3
"""Turn the raw SMILES JSON into a CSV."""

from pathlib import Path

from property_prediction.io import read_smiles_json, write_csv

frame = read_smiles_json(Path("data/raw/MoBiVic_reduced.json"))
write_csv(frame, Path("data/processed/smiles.csv"))
print(f"{len(frame)} rows written to data/processed/smiles.csv")
