# DrugPropertyCalculator

DrugPropertyCalculator is a Python package for exploring molecular properties from SMILES strings. It uses RDKit to calculate descriptors, applies Lipinski and Veber absorption screening rules, estimates aqueous solubility, and provides tools to prepare and visualise a compound collection.

These predictions are screening estimates, not experimental measurements or clinical assessments.

## What it does

- Converts a SMILES string to a canonical form and calculates molecular weight (`mw`), rotatable bonds (`rot_bonds`), hydrogen bond donors (`hbd`), hydrogen bond acceptors (`hba`), calculated logP (`logp`), and topological polar surface area (`tpsa`).
- Applies Lipinski's rule of five and Veber's rule, returning a pass/fail result and the thresholds exceeded.
- Estimates solubility as logS with an ESOL-style calculation and assigns a descriptive solubility category.
- Builds a `ListMol` collection of molecules, removing duplicates after SMILES canonicalisation.
- Reads a source-ID-keyed JSON collection, writes a SMILES CSV, and plots descriptor space and rule pass counts.

## Install

Use Python 3.11 or 3.12 (the versions used by the project's test workflow). From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. The package dependencies include RDKit, NumPy, pandas, and Matplotlib. Install the optional documentation tools with `python -m pip install -e ".[dev,docs]"`.

## Run with Docker

The package is also published as a container image.

```bash
docker container run --rm ibtau/drugpropertycalculator pytest
docker container run --rm ibtau/drugpropertycalculator python scripts/prepare_data.py
```

The image is on Docker Hub at
[ibtau/drugpropertycalculator](https://hub.docker.com/r/ibtau/drugpropertycalculator)
and includes the package, its dependencies, the test suite, the example
scripts and `data/raw/`.

To build it from this repository instead:

```bash
docker image build -t drugpropertycalculator .
```

The published image is built for arm64. On an Intel or AMD machine, build
locally with `--platform linux/amd64`.

## Use the package

```python
from property_prediction import ListMol, Molecule, lipinski, veber
from property_prediction.predictors import absorption, solubility, solubility_category

aspirin = Molecule("CC(=O)Oc1ccccc1C(=O)O")
print(aspirin.smiles)                  # canonical SMILES
print(aspirin.mw, aspirin.logp, aspirin.tpsa)

for result in absorption(aspirin):   # runs lipinski() and veber()
    print(result.name, result.passes, result.violations)

log_s = solubility(aspirin)
print(log_s, solubility_category(log_s))

unique_molecules = ListMol(["CCO", "OCC", "CCN"])
print(len(unique_molecules))          # 2; ethanol appears twice
print(unique_molecules[0].smiles)
```

`Molecule` raises `ValueError` for a SMILES string that RDKit cannot parse. `ListMol` also raises if any input string is invalid. The `lipinski()` and `veber()` functions can be called individually; each returns a `RuleResult` with `name`, `passes`, and `violations` fields.

Lipinski passes when no more than one of these limits is exceeded: molecular weight 500, logP 5, hydrogen bond donors 5, or hydrogen bond acceptors 10. Veber passes when there are at most 10 rotatable bonds **and** either TPSA is at most 140 Å² or the combined donor and acceptor count is at most 12.

## Work with the included data

The repository includes `data/raw/MoBiVic_reduced.json`, a collection keyed by source ID with a `smiles` value in each record. Run these commands from the repository root after installation:

```bash
python scripts/prepare_data.py
python scripts/run_absorption.py
python scripts/run_visualisation.py
```

`prepare_data.py` writes `data/processed/smiles.csv` with `source_id` and `smiles` columns. It must run before the other scripts. `run_absorption.py` prints Lipinski and Veber results for a reproducible sample of 10 compounds. `run_visualisation.py` assesses a reproducible sample of 5,000 compounds, saves the assessment to `data/processed/assessed.csv`, and opens plots of TPSA versus logP and the rule pass counts. If the assessment CSV already exists, the visualisation script reuses it; remove that generated file to recalculate after changing the input data. The `data/processed/` directory is ignored by Git.

The file helpers are available in `property_prediction.io`: `read_smiles_json()`, `read_smiles_csv()`, and `write_csv()`. The plotting helpers are in `property_prediction.visualisation`.

## Develop

```bash
pytest
ruff check .
python -m sphinx -b html docs docs/_build/html
```

The Sphinx command requires the `docs` extra. Source code lives in `src/property_prediction/`, example workflows in `scripts/`, tests in `tests/`, and documentation sources in `docs/`.

## License

MIT. See [LICENSE](LICENSE).
