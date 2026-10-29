Quickstart
==========

This quickstart shows how to calculate molecular properties from a SMILES
string and how to run the included data-preparation and screening workflows.
Complete the :doc:`install` instructions first, then run commands from the
repository root with the project environment activated.

Calculate properties for a molecule
-----------------------------------

Create a Python file (for example, ``example.py``) with the following code:

.. code-block:: python

   from property_prediction import Molecule, lipinski, veber
   from property_prediction.predictors import (
       absorption,
       solubility,
       solubility_category,
   )

   aspirin = Molecule("CC(=O)Oc1ccccc1C(=O)O")

   print("Canonical SMILES:", aspirin.smiles)
   print("Molecular weight:", aspirin.mw)
   print("LogP:", aspirin.logp)
   print("TPSA:", aspirin.tpsa)

   for result in absorption(aspirin):
       print(f"{result.name}: passes={result.passes}; violations={result.violations}")

   log_s = solubility(aspirin)
   print("Estimated logS:", log_s)
   print("Solubility category:", solubility_category(log_s))

Run it with:

.. code-block:: console

   python example.py

``Molecule`` canonicalises the SMILES and calculates molecular descriptors.
``absorption()`` returns Lipinski and Veber screening results; the individual
``lipinski()`` and ``veber()`` functions are also available. ``solubility()``
returns an estimated logS value, which can be mapped to a category with
``solubility_category()``. These are computational screening estimates, not
experimental measurements.

Work with a molecule collection
-------------------------------

``ListMol`` creates a collection of molecules and removes duplicates after
SMILES canonicalisation. For example, ``CCO`` and ``OCC`` both represent
ethanol, so only one is retained:

.. code-block:: python

   from property_prediction import ListMol

   molecules = ListMol(["CCO", "OCC", "CCN"])
   print(len(molecules))
   print(molecules[0].smiles)

An invalid SMILES string raises ``ValueError`` when creating a ``Molecule`` or
``ListMol``.

Run the included data workflows
-------------------------------

The repository includes ``data/raw/MoBiVic_reduced.json``, a collection keyed
by source ID. Prepare the CSV before running the screening or visualisation
scripts:

.. code-block:: console

   python scripts/prepare_data.py
   python scripts/run_absorption.py
   python scripts/run_visualisation.py

The preparation step writes ``data/processed/smiles.csv`` with ``source_id``
and ``smiles`` columns. The absorption script prints Lipinski and Veber
results for a reproducible sample of 10 compounds. The visualisation script
assesses a reproducible sample of 5,000 compounds, saves results to
``data/processed/assessed.csv``, and opens plots of TPSA versus logP and rule
pass counts. If that assessment CSV already exists, it is reused; remove it
to recalculate after changing the input data. Generated files in
``data/processed/`` are ignored by Git.

For details of the available Python functions, see the :doc:`reference`.
