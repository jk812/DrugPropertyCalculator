"""Plots for property prediction results."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

from property_prediction.molecules import Molecule
from property_prediction.predictors import bioavailability_detail


def assess(frame: pd.DataFrame) -> pd.DataFrame:
    """Add a column per rule, plus logP and TPSA, for every compound."""
    rows = []
    for smiles in frame["smiles"]:
        molecule = Molecule(smiles)
        row = {r.name: r.passes for r in bioavailability_detail(molecule)}
        row["logp"] = molecule.logp
        row["tpsa"] = molecule.tpsa
        rows.append(row)
    return pd.DataFrame(rows)


def plot_property_space(data: pd.DataFrame, ax: Axes | None = None) -> Axes:
    """Density of the library in TPSA/logP space, with the rule limits marked."""
    if ax is None:
        _, ax = plt.subplots()

    hexes = ax.hexbin(data["tpsa"], data["logp"], gridsize=50, cmap="Blues", mincnt=1)
    plt.colorbar(hexes, ax=ax, label="compounds")

    ax.axvline(140, color="grey", linestyle="--")
    ax.axhline(5, color="grey", linestyle="--")
    ax.set_xlabel("TPSA")
    ax.set_ylabel("logP")
    return ax


def plot_rule_summary(data: pd.DataFrame, ax: Axes | None = None) -> Axes:
    """Bar chart of how many compounds pass each rule."""
    if ax is None:
        _, ax = plt.subplots()

    names = ["lipinski", "veber"]
    passed = [int(data[name].sum()) for name in names]

    ax.bar(names, passed, color="blue")
    ax.set_ylabel("compounds passing")
    ax.set_ylim(0, len(data))
    return ax
