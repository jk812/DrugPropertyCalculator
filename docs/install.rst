Installation Guide:
===================


The DrugPropertyCalculator package takes a set of smiles strings and
produces a suite of predictions. It requires Python 3.12 or newer.

get the code
------------

Clone the repo and enter the project directory

.. code-block:: console
    git clone https://github.com/jk812/DrugPropertyCalculator/blob/main/.github/workflows/pages.yml
    cd DrugPropertyCalculator

Create a virtual enviroment
---------------------------

On macOS:

.. code-block:: console

   python3 -m venv venv
   source venv/bin/activate

Install the package
-------------------

Install the package and the dependencies:

.. code-block:: console

    python -m pip install -e ".[dev,docs]"

The ``-e`` option installs the package in editable mode, so edits to the
source code are available without reinstalling it.
