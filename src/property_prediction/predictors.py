from property_prediction import Molecule

class PropertyPredictor:
    """Base class for property predictors.
    """
    @staticmethod
    def calculate(mol:Molecule):
        """Calculates the property of a molecule.
        """
        if not isinstance(mol, Molecule):
            raise ValueError("Input must be a Molecule object.")
        raise NotImplementedError("This method should be implemented by subclasses.")
