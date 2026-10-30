#!/usr/bin/env python

"""Pipeline script for the user to run."""
import argparse
import os
import pandas as pd
from pathlib import Path
from property_prediction.io import read_smiles_json, read_smiles_csv, write_csv
from property_prediction.molecules import ListMol

def pipeline(filename):
    """Run user pipeline end-to-end.

    This function reads in a file of SMILES,
    creates a list of molecules, predicts properties, and writes the results
    to a csv. Additionally, it also creates visualisations of some predicted
    properties.
    """
    print(f"Begin processing {filename}")

    smiles_df = read_file(filename)
    print("Smiles reading in...")

    smiles_list = create_smiles_list(smiles_df)
    print("Smiles list created...")

    list_mol = ListMol(smiles_list)
    print("Mol objects created...")

    list_mol.predict_all()
    print("Properties predicted...")

    results_df = list_mol.return_df()
    print("Predicted Properties written to dataframe...")

    output_file = write_predicted_results_to_csv(results_df, filename)
    print(f"Predicted Properties written to: {output_file}")
    # visualise
    # write to file

def read_file(filename:str) -> pd.DataFrame:
    """Read a file containing SMILES data.

    Args:
        filename (str): Filepath to the input file, either .csv or .json.

    Raises
    ------
        TypeError: File type not supported, only .csv and .json are supported.

    Returns
    -------
        pd.DataFrame: The DataFrame containing the SMILES data.
    """
    file_extension = os.path.splitext(filename)[1]
    if file_extension == '.csv':
        return read_smiles_csv(filename)
    elif file_extension == '.json':
        return read_smiles_json(filename)
    else:
        raise TypeError("File Type in currently not supported, please add request to add")

def create_smiles_list(smiles_df: pd.DataFrame) -> list[str]:
    """Create a list of SMILES strings from a DataFrame.

    Args:
        smiles_df (pd.DataFrame): The DataFrame containing the SMILES data.

    Returns
    -------
        list[str]: A list of SMILES strings.
    """
    return smiles_df["smiles"].to_list()


def write_predicted_results_to_csv(results_df: pd.DataFrame, filename: str) -> str:
    """Write the predicted results to a CSV file.

    Args:
        results_df (pd.DataFrame): DataFrame containing the predicted properties for each molecule.
        filename (str): File path to the output CSV file.

    Returns
    -------
        str: File path to the output CSV file.
    """
    input_filename = Path(filename)
    output_filename = input_filename.with_name(input_filename.stem + "_output.csv")
    write_csv(results_df, output_filename)
    return output_filename

def main():
    """Run the pipeline from the command line."""
    parser = argparse.ArgumentParser(
        description="Run the command line tool"
    )
    parser.add_argument(
        "data_input",
        help="File path to your .csv or .json file"
    )

    args = parser.parse_args()
    pipeline(args.data_input)

if __name__ == "__main__":
    main()
