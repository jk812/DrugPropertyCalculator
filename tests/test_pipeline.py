"""Test the pipeline funtionality"""
from property_prediction import pipeline
from property_prediction.pipeline import read_file
from unittest.mock import patch
import pytest
import pandas as pd
from property_prediction.pipeline import create_smiles_list
from property_prediction.pipeline import create_mol_list
from property_prediction.molecules import ListMol

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


class TestCreateSmilesList():
    def setup_class(self):
        self.smiles_df = pd.DataFrame({
            "source_id": [1, 2, 3, 4],
            "smiles": ['C', 'CO', 'CCO', 'CCOO'],
            "name": ['Methane', 'methanol', 'ethanol', 'etanoic acid']
        })
        self.non_smiles_df = pd.DataFrame({
            "source_id": [1, 2, 3, 4],
            "not_smiles": ['C', 'CO', 'CCO', 'CCOO'],
            "name": ['Methane', 'methanol', 'ethanol', 'etanoic acid']
        })

    def test_create_smiles_list_returns_list(self):
        assert isinstance(create_smiles_list(self.smiles_df), list)

    def test_create_smiles_list_returns_corret_list(self):
        assert create_smiles_list(self.smiles_df) == ['C', 'CO', 'CCO', 'CCOO']

    def test_create_smiles_list_throws_error(self):
        with pytest.raises(KeyError):
            create_smiles_list(self.non_smiles_df)

class TestCreateMolList():
    def check_mol_list_object_is_created(self):
        smiles_list = ['C', 'CO', 'CCO', 'CCOO']
        expected_mol_list = ListMol(smiles_list)
        created_mol_list = create_mol_list(smiles_list)
        assert isinstance(created_mol_list, ListMol)
        assert created_mol_list.len() == expected_mol_list.len()