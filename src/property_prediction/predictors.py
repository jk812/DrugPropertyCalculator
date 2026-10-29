"""Property predictor methods."""

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .molecules import Molecule

predictors_list = []

def update_molecule(func):
    """Update a molecule in-place with the result of a predictor function, adding the result as an attribute."""

    def wrapper(molecule: Molecule):
        val = func(molecule)
        setattr(molecule, func.__name__.lower(), val)
        return val
    predictors_list.append(wrapper)
    return wrapper

@dataclass(frozen=True)
class RuleResult:
    """The outcome of a rule-based predictor."""

    name: str
    passes: bool
    violations: tuple[str, ...] = ()

@update_molecule
def lipinski(molecule: Molecule) -> bool:
    """Lipinski's rule of five. Returns True if the molecule passes, False otherwise.

    Requires 1 or fewer violations of the following:
    - MW <= 500
    - logP <= 5
    - HBD <= 5
    - HBA <= 10
    """
    mw_condition = molecule.mw <= 500
    logp_condition = molecule.logp <= 5
    hbd_condition = molecule.hbd <= 5
    hba_condition = molecule.hba <= 10
    conditions = [mw_condition, logp_condition, hbd_condition, hba_condition]
    violations = sum(not condition for condition in conditions)
    return violations <= 1


def lipinski_detail(molecule: Molecule) -> RuleResult:
    """Lipinski's rule of five, with detailed violation information."""
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

@update_molecule
def veber(molecule: Molecule) -> bool:
    """Veber's rules. Returns True if the molecule passes, False otherwise.

    Requires 10 or fewer rotatable bonds, plus a TPSA of 140 A^2 or
    less, both of which must be true for a molecule to pass.
    """
    rot_bonds_condition = molecule.rot_bonds <= 10
    polar_surface_condition = molecule.tpsa <= 140
    return rot_bonds_condition and polar_surface_condition

def veber_detail(molecule: Molecule) -> RuleResult:
    """
    Veber's rules, with detailed violation information.

    Requires 10 or fewer rotatable bonds, plus either a TPSA of 140 A^2 or
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

@update_molecule
def bioavailability(molecule: Molecule) -> bool:
    """Apply both Lipinski's rule of five and Veber's rules."""
    lipinski_result = lipinski(molecule)
    veber_result = veber(molecule)
    return lipinski_result and veber_result

BIOAVAILABILITY_RULES = (lipinski_detail, veber_detail)

def bioavailability_detail(molecule: Molecule) -> list[RuleResult]:
    """Apply every bioavailability rule to one molecule."""
    return [rule(molecule) for rule in BIOAVAILABILITY_RULES]


def solubility_category(solubility:float) -> str:
    """Categorize solubility based on the given solubility value.

    The ranges used are the same as those used by SwissADME (https://www.nature.com/articles/srep42717).
    insoluble <-10 <poorly <-6 <moderately <-4 <soluble <-2 <very <0 <highly

    Args:
        solubility (float): _description_

    Returns
    -------
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

@update_molecule
def aromatic_proportion(molecule: Molecule) -> float:
    """Calculate the aromatic proportion of a molecule.

    Args:
        molecule (Molecule): The molecule for which to calculate aromatic proportion.

    Returns
    -------
        float: The calculated aromatic proportion value.
    """
    num_aromatic_atoms = sum(1 for atom in molecule._mol.GetAtoms() if atom.GetIsAromatic())
    total_atoms = molecule._mol.GetNumAtoms()
    return num_aromatic_atoms / total_atoms

@update_molecule
def logS(molecule: Molecule) -> float:
    """Calculate the solubility of a molecule using Delaney's ESOL method.

    Args:
        molecule (Molecule): The molecule for which to calculate solubility.

    Returns
    -------
        float: The calculated solubility value.
    """
    aromatic_proportion(molecule)

    # ESOL formula: logS = 0.16 - 0.63 * logP - 0.0062 * MW + 0.066 * RB - 0.74 * AP
    logS = (
        0.16
        - 0.63 * molecule.logp
        - 0.0062 * molecule.mw
        + 0.066 * molecule.rot_bonds
        - 0.74 * molecule.aromatic_proportion
    )
    return logS
