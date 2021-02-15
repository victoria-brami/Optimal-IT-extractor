from lib.labelling.gui_functions.labelling_instructions import *
from lib.labelling.gui_functions.labelling_window import *
from lib.utils.csv_processing import *
from lib.labelling.gui_functions.mri_sequence_displayer import labelling_app
from lib.utils.image_visu import load_patient_mri_images
from lib.utils.misc import patient_id_extractor
from project_config import *
import numpy as np

def optimal_ti_selection(root_dir, patient_ids):
    """
    This function enables for each mri sequence to write down the
    images indexes corresponding to the best images rendering

    :param mri_sequence_paths: (list) list of patient names (string numbers)
    :param root_dir: root path
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
        print('optimal indexes', optimal_indexes)

        # If the user wants to stop the selection, he does not fill the Edit line
        if len(optimal_indexes) == 0:
            stop_labelling = False

        else:
            optimal_indexes = optimal_indexes.split(" ")
            if " " in optimal_indexes:
                optimal_indexes.remove(' ')
            if "" in optimal_indexes:
                optimal_indexes.remove('')

            # Gather the data in a vector (form of the vector: [patient_id, 0, ..., 1, 1, 0, ...0])
            sequence_label_vector = [0] * (cfg.NB_IMAGES_PER_MRI_SEQUENCE + 1)
            sequence_label_vector[0] = int(patient_id)

            print('PATIENT {} optimal indexes: {}'.format(patient_id, optimal_indexes))

            for idx in optimal_indexes:
                sequence_label_vector[int(idx)] = 1

        # Save the data while the user wants to continue labelling
        if not stop_labelling:
            list_optimal_tis.append(sequence_label_vector)

        # Go to next mri sequence
        sequence_index += 1

    return np.array(list_optimal_tis)


def label_and_save_optimal_tis(csv_path):
    """
    This is the main function.
    It will check all the patient mris sequence and enable the user to annotate them until he has had enough of it.
    :param patient_ids: (list of strings) patient names
    :param csv_path: (str) path to the csv in which the labels will be stored
    :return: None
    """
    # Find patient Ids
    patient_ids = patient_id_extractor(cfg.ROOT)
    last_patient_name = patient_ids[0]

    # Display the information linked to annotations
    display_annoted_label_informations(csv_path)

    # Check file, directory existence, otherwise return an error or build the directory


    # If the csv file does not exist, create it
    if not Path(csv_path).exists():
        create_csv('labels.csv', osp.join(cfg.PATH_TO_PROJECT, 'data'))

    # Otherwise retrieve the last line of csv to start with the right patient
    last_patient_index = patient_ids[0]

    last_patient_index, _ = get_csv_last_line(csv_path)
    last_patient_index = patient_ids.index(str(last_patient_index))

    print("Last patient index is", last_patient_index)

    # Process to the labelling
    print('LABELLING TI SCOUT MRIs SEQUENCES ...')
    list_optimal_ti_scouts = optimal_ti_selection(cfg.ROOT, patient_ids[last_patient_index + 1: last_patient_index+5])
    print("list_optimal_ti_scouts", list_optimal_ti_scouts)
    nb_annoted_sequences = len(list_optimal_ti_scouts)

    # Save the annotations in csv
    fill_csv(csv_path, list_optimal_ti_scouts)

    return list_optimal_ti_scouts



if __name__ == '__main__':
    patient_ids = patient_id_extractor(cfg.ROOT)
    label_and_save_optimal_tis(cfg.LABELS_CSV_PATH)
    print('GREAT, everything is Fine !')



