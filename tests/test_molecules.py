import pytest
import numpy.testing as npt

@pytest.mark.parametrize("test, expect_raises", [("CCO", None), ("C1CCCCC1", None), ("asdad", ValueError)])
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

@pytest.fixture()
def listmol():
    from property_prediction import ListMol
    return ListMol(["CCO","CCCCO","CCCCCCCO"])
class TestListMol:
    @pytest.mark.parametrize(
        "test, expect_raises",
        [
            (["CCO","CCCCO","CCCCCCCO"], ["CCO","CCCCO","CCCCCCCO"]),
            (["CCO","CCO","CCCCCCCO"], ["CCO","CCCCCCCO"]),
        ]
    )
    def test_list_mol_creation(self, test, expect_raises):
        from property_prediction import ListMol

        listobject = ListMol(test)
        listofmolobjects = listobject.lis

        output = []
        for object in listofmolobjects:
            output.append(object.smiles)

        npt.assert_array_equal(output, expect_raises)

    def test_list_mol_len(self, listmol):
        assert len(listmol) == 3

    def test_list_mol_getitem(self, listmol):
        assert listmol[0].smiles == "CCO"
        assert listmol[1].smiles == "CCCCO"
        assert listmol[2].smiles == "CCCCCCCO"

    def test_predict_all(self, listmol):
        listmol.predict_all()
        assert listmol[0].lipinski
        assert listmol[1].veber

    def test_return_df(self, listmol):
        from property_prediction import ListMol
        import pandas as pd

        listmol2 = ListMol(['', '', ''])

        result1 = listmol.return_df()
        result2 = listmol2.return_df()

        assert isinstance(result1, pd.DataFrame)
        assert isinstance(result2, pd.DataFrame)
