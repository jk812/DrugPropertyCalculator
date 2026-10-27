"""Tests for the absorption predictors."""

from property_prediction.molecules import Molecule
from property_prediction.predictors import lipinski, veber, solubility_category, solubility, aromatic_proportion
import pytest

def test_drug_like_molecule_passes():
    molecule = Molecule("CC(=O)Oc1ccccc1C(=O)O")  # aspirin
    assert lipinski(molecule).passes
    assert veber(molecule).passes


def test_lipinski_fails_big_greasy_molecule():
    assert not lipinski(Molecule("C" * 40)).passes


def test_veber_fails_too_many_rotatable_bonds():
    assert not veber(Molecule("C" * 25)).passes

@pytest.mark.parametrize("test, arom_prop", [("c1ccccc1", 1.0), ("CCC", 0.0), ("Cc1ccccc1", 0.857)])
def test_aromatic_proportion(test: str, arom_prop: float):
    molecule = Molecule(test)
    assert aromatic_proportion(molecule) == pytest.approx(arom_prop, abs=1e-3)

@pytest.mark.parametrize("solubility_val, solubility_cat",
                        [(-11, "insoluble"),
                         (-7.6, "poorly soluble"),
                         (15, "highly soluble")])
def test_solubility_category(solubility_val: float, solubility_cat: str):
    assert solubility_category(solubility_val) == solubility_cat

@pytest.mark.parametrize("test, solubility_val", [("CC([O-])=O", "highly soluble"), ("C"*40, "insoluble")])
def test_solubility_predictor(test, solubility_val):
    molecule = Molecule(test)
    sol = solubility(molecule)
    assert solubility_category(sol) == solubility_val
