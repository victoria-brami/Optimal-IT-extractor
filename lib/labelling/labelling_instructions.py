from PyQt5.QtWidgets import QMessageBox, QApplication

INSTRUCTIONS_OPTIMAL_TI = ' YOU WILL NOW BE ABLE TO LABEL THE IMAGES YOU SEE DEPENDING ON THEIR CONTRAST \n \n'
INSTRUCTIONS_OPTIMAL_TI += ' SOME WARNINGS \n'
INSTRUCTIONS_OPTIMAL_TI += ' For a given sequence, write on the side the images index candidates for optimal TI.'

def display_label_selection_instructions():
    """
    Explains to the user how to label the images
    :return: None
    """
    app = QApplication([])
    message = QMessageBox()
    message.setText(INSTRUCTIONS_OPTIMAL_TI)
    message.show()
    app.exec_()