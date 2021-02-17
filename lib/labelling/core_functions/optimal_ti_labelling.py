from lib.labelling.gui_functions.labelling_instructions import *
from lib.utils.csv_processing import *
from lib.labelling.gui_functions.mri_sequence_displayer import labelling_app
from lib.utils.image_visu import load_patient_mri_images
from lib.utils.misc import patient_id_extractor
from project_config import *
import numpy as np
import argparse


def optimal_ti_selection(root_dir, patient_ids):
    """
    This function enables for each mri sequence to write down the
    images indexes corresponding to the best images rendering

    :param root_dir: (strings) root path to data folder
    :param patient_ids: (list of strings) list of patients names (folder numbers)
    :return: (array) labelled data for each patient (1 if the image in the sequence is optimal, 0 otherwise)
    """
    # Number of sequences to label
    nb_mri_sequences = len(patient_ids)

    # Display first the instructions for labelling
    display_label_selection_instructions()

    # Start labelling the optimal TIs
    list_optimal_tis = []
    sequence_index = 0
    stop_labelling = False

    while sequence_index < nb_mri_sequences and not stop_labelling:

        # Load the images composing the sequences and their headers
        patient_images, _, _ = load_patient_mri_images(root_dir, patient_ids[sequence_index])

        # Plot the images of the sequence and write down the optimal image indexes (where we display the window)
        (patient_id, optimal_indexes, stop) = labelling_app(patient_ids[sequence_index])

        # Gather the data in a vector (form of the vector: [patient_id, 0, ..., 1, 1, 0, ...0])
        sequence_label_vector = [0] * (cfg.NB_IMAGES_PER_MRI_SEQUENCE + 1)

        # If the user wants to stop the selection, he does not fill the Edit line
        if len(optimal_indexes) == 0:
            stop_labelling = True

        else:
            optimal_indexes = optimal_indexes.split(" ")
            if " " in optimal_indexes:
                optimal_indexes.remove(' ')
            if "" in optimal_indexes:
                optimal_indexes.remove('')

            sequence_label_vector[0] = int(patient_id)

            # In case the user wrote down an invalid parameter: the application closes
            possible_indexes = [str(j) for j in range(cfg.NB_IMAGES_PER_MRI_SEQUENCE)]

            for idx in optimal_indexes:
                # In case the user wrote down an invalid parameter: the application closes
                if idx not in possible_indexes:
                    stop_labelling = True
                # otherwise we edit the labels correctly
                else:
                    sequence_label_vector[int(idx)] = 1

            if stop_labelling:
                display_annotations_error()

        # Save the data while the user wants to continue labelling
        if not stop_labelling:
            list_optimal_tis.append(sequence_label_vector)

        # Go to next mri sequence
        sequence_index += 1

    return np.array(list_optimal_tis)


def label_and_save_optimal_tis(csv_path, nb_to_label=None):
    """
    This is the main function.
    It will check all the patient mris sequence and enable the user to annotate them until he has had enough of it.
    :param nb_to_label: (int) the number of MRI sequences you want to label
    :param csv_path: (str) path to the csv in which the labels will be stored
    :return: None
    """

    # Find patient Ids
    patient_ids = patient_id_extractor(cfg.ROOT)

    # If the csv file does not exist, create it
    if not Path(csv_path).exists():
        create_csv('labels.csv', osp.join(cfg.PATH_TO_PROJECT, 'data'))

    # Otherwise retrieve the last line of csv to start with the right patient
    last_patient_index, last_patient_name, _ = get_csv_last_line(csv_path)

    if nb_to_label is None or nb_to_label > (len(patient_ids) - last_patient_index):
        nb_to_label = len(patient_ids) - last_patient_index

    # Process to the labelling
    print('LABELLING TI SCOUT MRIs SEQUENCES ...')
    list_optimal_ti_scouts = optimal_ti_selection(cfg.ROOT,
                                                  patient_ids[last_patient_index + 1: last_patient_index + nb_to_label])

    # Save the annotations in csv
    fill_csv(csv_path, list_optimal_ti_scouts)

    # Display the information linked to annotations
    display_annoted_label_informations(csv_path)

    return list_optimal_ti_scouts

def main_ti_generator():
    """

    :return: main function for labelling
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--nb_sequences', '-n', type=int, default=None)
    args = parser.parse_args()
    label_and_save_optimal_tis(cfg.LABELS_CSV_PATH, nb_to_label=args.nb_sequences)


if __name__ == '__main__':
    main_ti_generator()
    print('GREAT, everything is Fine !')
