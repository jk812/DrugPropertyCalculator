"""Placeholder Tests for reading and writing compound files."""

import json

import pandas as pd
import pytest

from property_prediction.io import read_smiles_json, write_csv


@pytest.fixture
def smiles_json(tmp_path):
    path = tmp_path / "compounds.json"
    path.write_text(json.dumps({
        "CMP-001": {"smiles": "CCO", "name": "ethanol"},
        "CMP-002": {"smiles": "", "name": "blank"},
    }))
    return path


def test_reads_json_into_two_columns(smiles_json):
    frame = read_smiles_json(smiles_json)
    assert list(frame.columns) == ["source_id", "smiles"]
    assert list(frame["source_id"]) == ["CMP-001"]   # blank row dropped


def test_missing_column_raises(tmp_path):
    path = tmp_path / "wrong.json"
    path.write_text(json.dumps({"a": {"structure": "CCO"}}))
    with pytest.raises(ValueError, match="has no 'smiles' column"):
        read_smiles_json(path)


def test_csv_round_trips(tmp_path):
    frame = pd.DataFrame({"source_id": ["a"], "smiles": ["CCO"]})
    target = tmp_path / "deep" / "out.csv"
    write_csv(frame, target)
    pd.testing.assert_frame_equal(pd.read_csv(target), frame)