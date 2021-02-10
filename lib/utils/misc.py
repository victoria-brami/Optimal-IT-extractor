import numpy as np
import os
import matplotlib.pyplot as plt
from lib.exceptions.exceptions_classes import *

# Extract patients IDs looking at folders
def patient_id_extractor(path):

    patient_ids = os.listdir(path)
    if '.DS_Store' in patient_ids:
        patient_ids.remove('.DS_Store')
    patient_ids.sort(key=int)
    return patient_ids

# Splits a list of strings and resort them by their indexes
def sort_my_strings_list(str_list):
    sorted_list = []
    for name in str_list:
        new_name = name.split('_')
        sorted_list.append(int(new_name[-1]))
    sorted_list = np.argsort(sorted_list)
    return sorted_list

# show a figure
def show_my_figure():
    plt.show()

# Close a figure
def close_my_figure():
    plt.close()

# Create directory (from one or two subfolders)
def create_new_directory(root_dir, subfolders):
    """

    :param root_dir: (str) main path
    :param subfolders: (list of str) list of subfolders names
    :return: creates nex directory if needed
    """

    if not os.path.isdir(root_dir):
        raise PathNotFoundError(root_dir)

    else:
        if len(subfolders) >= 1 and not os.path.isdir(os.path.join(root_dir, subfolders[0])):
            os.mkdir(os.path.join(root_dir, subfolders[0]))
        if len(subfolders) >= 2 and not os.path.isdir(os.path.join(root_dir, subfolders[0], subfolders[1])):
            os.mkdir(os.path.join(root_dir, subfolders[0], subfolders[1]))




