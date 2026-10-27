"""Property predictor methods"""

from dataclasses import dataclass
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

@dataclass(frozen=True)
class RuleResult:
    """The outcome of a rule-based predictor."""

    name: str
    passes: bool
    violations: tuple[str, ...] = ()


def lipinski(molecule: Molecule) -> RuleResult:
    """Lipinski's rule of five"""
    violations = [
        f"{label} {value:.1f} > {limit}"
        for label, value, limit in (
            ("MW", molecule.mw, 500),
            ("logP", molecule.logp, 5),
            ("HBD", molecule.hbd, 5),
            ("HBA", molecule.hba, 10),
        )
        if value > limit
    ]
    return RuleResult("lipinski", len(violations) <= 1, tuple(violations))