"""Pipeline class for the user to run"""
import argparse
import os
import pandas as pd
from property_prediction.io import read_smiles_json, read_smiles_csv
from property_prediction.molecules import ListMol

def pipeline(filename):
    """Run user pipeline end-to-end"""
    print(f"Begin processing {filename}")

    smiles_df = read_file(filename)
    print("Smiles readi in...")

    smiles_list = create_smiles_list(smiles_df)
    print("Smiles list created...")

    list_mol = create_mol_list(smiles_list)
    print("Mol objects created...")

    list_mol.predict_all()
    print("Properties predicted...")

    results_df = extract_predictor_results_to_df(list_mol)
    print("Predicted Properties written to dataframe...")
    # visualise
    # write to file

def read_file(filename):
    file_extension = os.path.splitext(filename)[1]
    if file_extension == '.csv':
        return read_smiles_csv(filename)
    elif file_extension == '.json':
        return read_smiles_json(filename)
    else:
        raise TypeError("File Type in currently not supported, please add request to add")

def create_smiles_list(smiles_df):
        return smiles_df["smiles"].to_list()

def create_mol_list(smiles_list):
     return ListMol(smiles_list)

def extract_predictor_results_to_df(list_mol):
    results = []
    for molecule in list_mol:
        row = {"smiles": molecule.smiles}
        row.update(molecule.predictions)
        results.append(row)
    return pd.DataFrame(results)

def main():
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
