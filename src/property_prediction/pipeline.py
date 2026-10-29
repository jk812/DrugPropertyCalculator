"""Pipeline class for the user to run"""
import argparse
import os
from .io import read_smiles_csv, read_smiles_json
from .molecules import ListMol

def pipeline(filename):
    """Run user pipeline end-to-end"""
    print(f"Begin processing {filename}")
    smiles_df = read_file(filename)
    smiles_list = create_smiles_list(smiles_df)
    list_mol = create_mol_list(smiles_list)


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

def main():
    parser = argparse.ArgumentParser(
        description="Run the command line tool"
    )
    parser.add_argument(
        "data_input",
        #accept zero or one arg
        nargs="?",
        help="File path to your .csv or .json file"
    )

    args = parser.parse_args()

    data_input = args.data_input
    pipeline(data_input)

if __name__ == "__main__":
    main()
