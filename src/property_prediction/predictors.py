"""Property predictor methods"""

from dataclasses import dataclass
from property_prediction import Molecule

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


def solubility_category(solubility:float) -> str:
    """Categorize solubility based on the given solubility value.
    The ranges used are the same as those used by SwissADME (https://www.nature.com/articles/srep42717).
    insoluble <-10 <poorly <-6 <moderately <-4 <soluble <-2 <very <0 <highly

    Args:
        solubility (float): _description_

    Returns:
        str: _description_
    """

    if solubility < -10:
        return "insoluble"
    elif solubility < -6:
        return "poorly soluble"
    elif solubility < -4:
        return "moderately soluble"
    elif solubility < -2:
        return "soluble"
    elif solubility < 0:
        return "very soluble"
    else:
        return "highly soluble"

def solubility(molecule: Molecule) -> float:
    """Calculate the solubility of a molecule using the ESOL method.

    Args:
        molecule (Molecule): The molecule for which to calculate solubility.

    Returns:
        float: The calculated solubility value.
    """
    # ESOL formula: logS = 0.16 - 0.63 * logP - 0.0062 * MW + 0.066 * RB - 0.74 * HBD
    logS = (
        0.16
        - 0.63 * molecule.logp
        - 0.0062 * molecule.mw
        + 0.066 * molecule.rot_bonds
        - 0.74 * molecule.hbd
    )
    return logS
