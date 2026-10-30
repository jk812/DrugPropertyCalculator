"""Tests for the plotting helpers."""

import matplotlib
import pandas as pd

matplotlib.use("Agg")  # headless backend so it runs in CI

from property_prediction.visualisation import assess, plot_property_space, plot_rule_summary

DATA = pd.DataFrame(
    {
        "lipinski": [True, True, False],
        "veber": [True, False, False],
        "logp": [1.2, 6.4, 2.0],
        "tpsa": [60.0, 150.0, 90.0],
    }
)


def test_assess_returns_a_row_per_compound():
    frame = pd.DataFrame({"smiles": ["CCO", "CC(=O)Oc1ccccc1C(=O)O"]})
    result = assess(frame)
    assert len(result) == 2
    assert {"lipinski", "veber", "logp", "tpsa"} <= set(result.columns)


def test_property_space_labels_its_axes():
    ax = plot_property_space(DATA)
    assert ax.get_xlabel() == "TPSA"
    assert ax.get_ylabel() == "logP"


def test_rule_summary_bar_heights_match_pass_counts():
    ax = plot_rule_summary(DATA)
    heights = [bar.get_height() for bar in ax.patches]
    assert heights == [2, 1]
