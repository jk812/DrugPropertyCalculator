"""Test the pipeline funtionality"""
from property_prediction.pipeline import read_file
# from property_prediction.io import read_smiles_json, read_smiles_csv
from unittest.mock import patch
import pytest

class TestReadFile():

    @patch('property_prediction.pipeline.read_smiles_csv')
    def test_read_file_name_csv(self, mock_read_csv):
        mock_read_csv.return_value = ['C', 'CNO']

        result = read_file('test.csv')

        mock_read_csv.assert_called_once_with('test.csv')
        assert result == ['C', 'CNO']

    @patch('property_prediction.pipeline.read_smiles_json')
    def test_read_file_name_json(self, mock_read_json):
        mock_read_json.return_value = ['CS', 'CONC']

        result = read_file('test.json')

        mock_read_json.assert_called_once_with('test.json')
        assert result == ['CS', 'CONC']

    def test_read_file_name_invalid_filename(self):
        with pytest.raises(TypeError):
            read_file('test.zip')
