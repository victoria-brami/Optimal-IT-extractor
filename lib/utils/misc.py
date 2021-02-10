import numpy as np
import os
import matplotlib.pyplot as plt

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
