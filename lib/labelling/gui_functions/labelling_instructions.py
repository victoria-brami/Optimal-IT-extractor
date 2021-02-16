from PyQt5.QtWidgets import QMessageBox, QApplication


def display_label_selection_instructions():
    """
    Explains to the user how to label the images.
    :return: None
    """
    INSTRUCTIONS_OPTIMAL_TI_SELECTION = ' YOU WILL NOW BE ABLE TO LABEL THE IMAGES YOU SEE DEPENDING ON THEIR CONTRAST \n \n \n'
    INSTRUCTIONS_OPTIMAL_TI_SELECTION += ' SOME WARNINGS \n \n'
    INSTRUCTIONS_OPTIMAL_TI_SELECTION += '  For a given sequence, write on the side the images index candidates for optimal TI.\n '
    INSTRUCTIONS_OPTIMAL_TI_SELECTION += '  Ex: if the images 4, 5, and 6 are optimal, write down "4 5 6" \n \n'
    INSTRUCTIONS_OPTIMAL_TI_SELECTION += '  If the CSV file is open, please close it before !! \n \n'
    INSTRUCTIONS_OPTIMAL_TI_SELECTION += '  Press ESCAPE button when you finished labelling the sequence \n'
    INSTRUCTIONS_OPTIMAL_TI_SELECTION += '  If you want to STOP labelling, press ESCAPE button without filling the box \n'
    app = QApplication([])
    message = QMessageBox()
    message.setText(INSTRUCTIONS_OPTIMAL_TI_SELECTION)
    message.show()
    app.exec_()


def display_annoted_label_informations(csv_path=None):
    """
    Explains to the user the shape of the labels and where they have been stored in his computer.
    :return: None
    """
    # Message displayed in the window
    ANNOTED_LABEL_INFORMATION = ' YOU COMPLETED TI SCOUT SEQUENCE LABELLING \n \n'
    ANNOTED_LABEL_INFORMATION += ' To Keep in Mind \n'
    ANNOTED_LABEL_INFORMATION += '  1) The annotations were saved in the directory: {} \n'.format(csv_path)
    ANNOTED_LABEL_INFORMATION += '  2) For each line of the csv, you will find: the patient ID in the first column. \n'
    ANNOTED_LABEL_INFORMATION += '     Then a succession of 0 or 1: 1 if the image of the sequence is optimal, 0 otherwise.'

    app = QApplication([])
    message = QMessageBox()
    message.setText(ANNOTED_LABEL_INFORMATION)
    message.show()
    app.exec_()
