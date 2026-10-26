import pytest

@pytest.mark.parametrize(
    "test, expect_raises",
    [
        ("CCO", None),
        ("C1CCCCC1", None),
        ("asdad", ValueError)
    ]
)
def test_molecule_creation(test, expect_raises):
    from property_prediction import Molecule
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            Molecule(test)
        return
    else:
        mol = Molecule(test)
    assert hasattr(mol, "smiles")
    assert hasattr(mol, "mw")
    assert hasattr(mol, "rot_bonds")
    assert hasattr(mol, "hbd")
    assert hasattr(mol, "hba")
