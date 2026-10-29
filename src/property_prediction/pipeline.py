"""Pipeline class for the user to run"""
import argparse
import os
from .io import read_smiles_csv, read_smiles_json

def pipeline(filename):
    """Run user pipeline end-to-end"""
    print(f"Begin processing {filename}")
    df = read_file(filename)

def read_file(filename):
    file_extension = os.path.splitext(filename)[1]
    if file_extension == '.csv':
        return read_smiles_csv(filename)
    elif file_extension == '.json':
        return read_smiles_json(filename)
    else:
        raise TypeError("File Type in currently not supported, please add request to add")


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
