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


def veber(molecule: Molecule) -> RuleResult:
    """Veber's rules: Requires 10 or fewer rotatable bonds, plus either a TPSA of 140 A^2 or
    less or a total hydrogen bond count of 12 or fewer. Both criteria must
    hold, but the polar surface criterion can be satisfied either way.
    """
    violations = []

    if molecule.rot_bonds > 10:
        violations.append(f"rotatable bonds {molecule.rot_bonds} > 10")

    hbond_total = molecule.hbd + molecule.hba
    if molecule.tpsa > 140 and hbond_total > 12:
        violations.append(f"TPSA {molecule.tpsa:.1f} > 140 and H-bonds {hbond_total} > 12")

    return RuleResult("veber", not violations, tuple(violations))

ABSORPTION_RULES = (lipinski, veber)


def absorption(molecule: Molecule) -> list[RuleResult]:
    """Apply every absorption rule to one molecule."""
    return [rule(molecule) for rule in ABSORPTION_RULES]