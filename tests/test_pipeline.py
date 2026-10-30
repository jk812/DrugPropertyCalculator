"""Test the pipeline funtionality"""
from property_prediction.pipeline import read_file
from unittest.mock import patch
import pytest
import pandas as pd
from pathlib import Path
from property_prediction.pipeline import create_smiles_list
from property_prediction.pipeline import write_predicted_results_to_csv
from property_prediction.pipeline import pipeline
from property_prediction.pipeline import main

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

class TestWritePredictedResultsToCSV():
    def setup_class(self):
        self.test_df = pd.DataFrame({
            "smiles": ['C', 'N'],
            "lipinski": [True, False]
        })

    @patch('property_prediction.pipeline.write_csv')
    def test_write_predicted_results_to_csv_returns_correct_output_filename(self, mock_write_csv):
        input_filename = 'test_smiles.csv'
        expected_output_filename = Path('test_smiles_output.csv')
        assert write_predicted_results_to_csv(self.test_df, input_filename) == expected_output_filename
        mock_write_csv.assert_called_once_with(self.test_df, expected_output_filename)

class TestPipeline():

    @patch('property_prediction.pipeline.write_predicted_results_to_csv')
    @patch('property_prediction.pipeline.ListMol', autospec=True)
    @patch('property_prediction.pipeline.create_smiles_list')
    @patch('property_prediction.pipeline.read_file')
    def test_pipeline_calls_all_relevant_functions(self,
                                                    mock_read_file,
                                                    mock_create_smiles_list,
                                                    mock_ListMol,
                                                    mock_write_predicted_results_to_csv):
        from unittest.mock import call

        filename = 'testfilename.csv'
        results_df = pd.DataFrame({'smiles': ['CCO'], 'lipinski': [True]})
        mock_list_mol = mock_ListMol.return_value
        mock_list_mol.return_df.return_value = results_df

        pipeline(filename)
        mock_read_file.assert_called_once_with(filename)
        mock_create_smiles_list.assert_called_once_with(mock_read_file.return_value)
        mock_ListMol.assert_called_once_with(mock_create_smiles_list.return_value)
        assert mock_list_mol.mock_calls == [call.predict_all(), call.return_df()]
        mock_write_predicted_results_to_csv.assert_called_once_with(
            results_df,
            filename
            )

def TestMain():

    @patch('property_prediction.pipeline.write_predicted_results_to_csv')
    def test_main_calls_pipeline(self, mock_pipeline):
        main()
        mock_pipeline.assert_called_once()
