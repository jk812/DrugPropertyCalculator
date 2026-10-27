import pytest
import numpy as np
import numpy.testing as npt


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

@pytest.mark.parametrize(
    "test, expect_raises",
    [
        (["CCO","CCCCO","CCCCCCCO"], ["CCO","CCCCO","CCCCCCCO"]),
        (["CCO","CCO","CCCCCCCO"], ["CCO","CCCCCCCO"]),
    ]
)
def test_list_mol_creation(test, expect_raises):
    from property_prediction import ListMol

    listobject = ListMol(test)
    listofmolobjects = listobject.lis

    output = []
    for object in listofmolobjects:
         output.append(object.smiles)

    npt.assert_array_equal(output, expect_raises)