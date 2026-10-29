"""Makes mol objects and list objects."""

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Lipinski, Crippen
from property_prediction import predictors_list

class Molecule:
    """Contains molecule properties, e.g. molecular weight (mw)."""

    def __init__(self, smiles: str):
        self._mol = Chem.MolFromSmiles(smiles)
        if self._mol is None:
            raise ValueError("Input SMILES string is invalid.")

        self.smiles = Chem.MolToSmiles(self._mol)
        self.mw = Descriptors.MolWt(self._mol)
        self.rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(self._mol)
        self.hbd = Lipinski.NumHDonors(self._mol)
        self.hba = Lipinski.NumHAcceptors(self._mol)
        self.logp = Crippen.MolLogP(self._mol)
        self.tpsa = Descriptors.TPSA(self._mol)

class ListMol:
    """Contains list of Molecule objects."""

    def __init__(self, smileslist:list[str]):
        self.lis = [Molecule(smile) for smile in smileslist]
        self.check_for_duplicates()

    def check_for_duplicates(self):
        """Remove duplicate Molecule objects from within the ListMol object."""
        unique = set()
        duplicate_idx = []
        for idx, object in enumerate(self.lis):
            can_smi = object.smiles
            if can_smi in unique:
                duplicate_idx.append(idx)
            unique.add(can_smi)
        self.lis = [obj for idx, obj in enumerate(self.lis) if idx not in set(duplicate_idx)]

    def __len__(self):
        """Define length of ListMol object."""
        return len(self.lis)

    def __getitem__(self, idx):
        """Define indexing and slicing of ListMol object."""
        return self.lis[idx]

    def predict_all(self):
        """Apply all predictors to all Molecule objects in the ListMol object."""
        for prediction in predictors_list:
            prediction(self)
