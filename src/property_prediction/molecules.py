from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Lipinski, Crippen

class Molecule:
    """Contains molecule properties, e.g. molecular weight (mw).
    """
    def __init__(self, smiles:str):
        self._mol = Chem.MolFromSmiles(smiles)
        if self._mol is None:
            raise ValueError("Input SMILES string is invalid.")

        self.smiles = Chem.MolToSmiles(self._mol)
        self.mw = Descriptors.MolWt(self._mol)
        self.rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(self._mol)
        self.hbd = Lipinski.NumHDonors(self._mol)
        self.hba = Lipinski.NumHAcceptors(self._mol)
        self.logp = Crippen.MolLogP(self._mol)