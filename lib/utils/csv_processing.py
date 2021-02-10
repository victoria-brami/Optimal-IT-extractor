'''
    This file will contain function needed to fill, read, save csv.
    It will find the last line of a csv file
'''
from lib.exceptions.exceptions_classes import *
from pathlib import Path
import os.path as osp
import pandas as pd

def create_csv(filename, destination=None, csv_keys=None):
    """

    :param filename: (str) name of the csv (needs to have .csv as suffix)
    :param destination: (str) path in which the
    :param csv_keys: (dict) contains the keys in CSV file
    :return: saved csv file in destination folder
    """

    # Ensure the folder exists
    if not Path(destination).exists():
        raise PathNotFoundError(destination)

    # destination filename
    csv_path = Path(osp.join(destination, filename))
    if csv_path.exists():
        raise AlreadyExistsError(csv_path)

    # Create, save csv and add keys
    keys = pd.DataFrame(csv_keys)
    keys.to_csv(csv_path, index=False)


def fill_csv():
    """ Function to fil a given csv """




if __name__ == '__main__':
    create_csv(Path('aaa.csv'), Path('../../../../Documents/code_tests'), csv_keys=dict(patient_id=[], ti=[]))