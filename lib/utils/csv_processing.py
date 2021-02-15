'''
    This file will contain function needed to fill, read, save csv.
    It will find the last line of a csv file
'''
from lib.exceptions.exceptions_classes import *
from pathlib import Path
import os.path as osp
import pandas as pd
from project_config import *

def create_csv(filename, destination=None, csv_keys=None, nb_columns=cfg.NB_IMAGES_PER_MRI_SEQUENCE):
    """
    :param filename: (str) name of the csv (needs to have .csv as suffix)
    :param destination: (str) path in which the
    :param csv_keys: (dict) contains the keys in CSV file
    :return: saved csv file in destination folder
    """

    # Ensure the folder exists
    if not Path(destination).exists():
        raise PathNotFoundError(destination)

    if csv_keys is None:
        csv_keys = dict(patient_id=[])
        for image_idx in range(nb_columns):
            csv_keys['ti_scout_{}'.format(image_idx)] = []

    # check destination filename correctness
    csv_path = Path(osp.join(destination, filename))
    if csv_path.exists():
        raise AlreadyExistsError(csv_path)

    # Create, save csv and add keys
    keys = pd.DataFrame(csv_keys)
    keys.to_csv(csv_path, index=False)


def fill_csv(csv_path, optimal_ti_indexes):
    """
    Function to fill a given csv.
    :param csv_path: (str) path to csv file
    :return: None
    """
    # Check csv existence
    if not osp.isfile(csv_path):
        raise PathNotFoundError(csv_path)

    # Check data to add is not empty
    if len(optimal_ti_indexes) == 0:
        raise NoDataToAddError(csv_path)

    with open(csv_path, 'a', newline='') as csv_file:

        contents = dict(patient_id=optimal_ti_indexes[:, 0], ti_scout=optimal_ti_indexes[:, 1:])
        index = pd.MultiIndex.from_tuples(tuple(optimal_ti_indexes))
        columns = ['patient_id']
        for image_idx in range(cfg.NB_IMAGES_PER_MRI_SEQUENCE):
            columns.append('ti_scout_{}'.format(image_idx))
        data = pd.DataFrame(data=optimal_ti_indexes[:, :], columns=columns)

        # add to csv file
        data.to_csv(csv_file, header=False)


def get_csv_last_line(csv_path):
    """ get the last line index and contents """

    # Check csv existence
    if not osp.isfile(csv_path):
        raise PathNotFoundError(csv_path)

    data = pd.read_csv(csv_path)
    if not data.empty:
        (patient_id, ti_scout) = data.index.values[-1][1], data.index.values[-1][2:]
    else:
        (patient_id, ti_scout) = (37, -1)

    return patient_id, ti_scout




if __name__ == '__main__':
    create_csv(Path('aaa.csv'), Path('../../../../Documents/code_tests'))