"""Placeholder Tests for reading and writing compound files."""

import json
import csv

import pandas as pd
import pytest

from property_prediction.io import read_smiles_json, write_csv, read_smiles_csv

test_data_json = {
        "CMP-001": {"smiles": "CCO", "name": "ethanol"},
        "CMP-002": {"smiles": "", "name": "blank"},
    }

test_data_csv = [["smiles", "Name"],["CCO", "ethanol"], ["", ""], ["CN", "cyanide"]]

@pytest.fixture
def smiles_json(tmp_path):
    path = tmp_path / "compounds.json"
    path.write_text(json.dumps(test_data_json))
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

@pytest.fixture
def smiles_csv(tmp_path):
    path = tmp_path / "compounds.csv"
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(test_data_csv)
    return path

def test_read_smiles_csv_returns_df(smiles_csv):
    frame = read_smiles_csv(smiles_csv)
    assert isinstance(frame, pd.DataFrame)

def test_read_smiles_csv_contains_correct_values(smiles_csv):
    expected_frame = pd.DataFrame(
        {"source_id": [0, 1, 2],
        "smiles": ["CCO", pd.NA, "CN"],
        }
    )
    frame = read_smiles_csv(smiles_csv)
    pd.testing.assert_frame_equal(frame, expected_frame)

