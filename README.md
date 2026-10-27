# DrugPropertyCalculator

DrugPropertyCalculator is a Python package for calculating simple molecular descriptors from SMILES strings and checking compounds against rule based absorption criteria. It uses RDKit to parse molecules and calculate descriptors.

## Features

- Parse and canonicalize SMILES strings.
- Calculate molecular weight (MW), rotatable bonds, hydrogen bond donors (HBD), hydrogen bond acceptors (HBA), calculated logP, and topological polar surface area (TPSA).
- Evaluate Lipinski's rule of five and Veber's rules, with a pass/fail result and explanations for any rule violations.
- Read a JSON compound collection keyed by source ID and export its SMILES values to CSV.

## Requirements

- Python 3.10–3.13
- RDKit, NumPy, pandas, and Matplotlib (installed as project dependencies)

## Installation

Clone the repository, then install the package and its development tools:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

To build the documentation locally, install the optional documentation dependency as well:

```bash
python -m pip install -e ".[dev,docs]"
```

## Quick start

```python
from property_prediction import Molecule, absorption

molecule = Molecule("CC(=O)Oc1ccccc1C(=O)O")  # aspirin
print(molecule.smiles)  # canonical SMILES
print(molecule.mw, molecule.logp, molecule.tpsa)

for result in absorption(molecule):
    print(result.name, "pass" if result.passes else "fail")
    for violation in result.violations:
        print(" -", violation)
```

`Molecule` raises `ValueError` if RDKit cannot parse the supplied SMILES. The `absorption` helper returns the Lipinski and Veber results; each result has a `name`, a boolean `passes`, and a tuple of `violations`.

You can also apply a rule directly:

```python
from property_prediction import Molecule, lipinski, veber

molecule = Molecule("CCO")
print(lipinski(molecule))
print(veber(molecule))
```

Lipinski's rule passes when at most one of MW > 500, logP > 5, HBD > 5, or HBA > 10 is exceeded. Veber's rule passes with 10 or fewer rotatable bonds and either TPSA ≤ 140 Å² or a total HBD + HBA count ≤ 12. These are rule-based screening checks, not experimental absorption measurements.

## Prepare and run the sample dataset

The repository includes `data/raw/MoBiVic_reduced.json`, a reduced compound collection stored as records keyed by source ID, each containing a `smiles` field. Convert it to `data/processed/smiles.csv` from the repository root:

```bash
python scripts/prepare_data.py
```

Then sample 10 compounds with a fixed random seed and print their absorption rule results:

```bash
python scripts/run_absorption.py
```

The script expects the processed CSV to exist, so run the preparation script first. The processed output directory is created as needed and generated data is not tracked in Git.

## Development

Install the development extras with `python -m pip install -e ".[dev]"`. The test suite is run with:

```bash
pytest
```

Build the Sphinx documentation from the repository root with:

```bash
python -m sphinx -b html docs docs/_build/html
```

## Project layout

```text
src/property_prediction/  Molecular descriptors, file I/O, predictors, visualisation
scripts/                  Data preparation and sample absorption workflow
data/raw/                 Reduced source compound set
tests/                    Unit tests
docs/                     Sphinx documentation
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
