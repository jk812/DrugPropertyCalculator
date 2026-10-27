"""Tests for the absorption predictors."""

from property_prediction.molecules import Molecule
from property_prediction.predictors import lipinski, veber


def test_drug_like_molecule_passes():
    molecule = Molecule("CC(=O)Oc1ccccc1C(=O)O")  # aspirin
    assert lipinski(molecule).passes
    assert veber(molecule).passes


def test_lipinski_fails_big_greasy_molecule():
    assert not lipinski(Molecule("C" * 40)).passes


def test_veber_fails_too_many_rotatable_bonds():
    assert not veber(Molecule("C" * 25)).passes
