from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QSlider, QWidget, QGridLayout, QHBoxLayout, QLineEdit, QDesktopWidget, QSizePolicy
from lib.labelling.gui_functions.main_widget import MainWidget
from lib.utils.image_visu import load_patient_mri_images
from lib.utils.misc import patient_id_extractor
from project_config import *
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QSize, Qt, QRect
import cv2
import numpy as np


RIGHT_REPR = ">"
LEFT_REPR = "<"

# Transform an array to qpixmap
def transform_array_to_qpixmap(image):
    """
    Convertion to QPixmap type
    :param image: (array) array image
    :return: (QImage) converted image
    """
    height, width = image.shape
    image = np.reshape(image, (height, width, 1))
    bytes_per_line = width * 3
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

    return QPixmap.fromImage(qimage)


########################################################################################################################
#                                               LEFT PANEL                                                             #
########################################################################################################################

class MRISequenceImages(QGridLayout):

    def __init__(self, mri_seq, patient_id, image_size,  stop=False):
        """

        :param mri_seq: (list) list of QPixmaps of a given mri sequence
        """
        super(MRISequenceImages, self).__init__()
        self.nb_images = len(mri_seq)
        self.mri_seq = [transform_array_to_qpixmap(mri_seq[i]) for i in range(self.nb_images)]
        self.patient_id = patient_id
        self.image_size = image_size

        # Background management
        self.real_image_size = self.mri_seq[0].size()
        self.displayed_image = None
        self.displayed_image_index = 1  # Starts with the first image
        self.initUI()

        # Stop option
        self.stop = stop

    def initUI(self):

        # build slidebar

        # build image
        self.displayed_image = self._build_image()
        # build image information
        self.displayed_image_information = self._build_image_information()

        self.addWidget(self.displayed_image, 1, 1)
        self.addWidget(self.displayed_image_information, 0, 0)

        # build buttons and connections
        self.setSpacing(1)
        previous_button = self._build_button(LEFT_REPR, self._click_for_image_change)
        previous_button.move(10, 800)
        next_button = self._build_button(RIGHT_REPR, self._click_for_image_change)
        next_button.move(60, 1000)

        self.addWidget(previous_button, 3, 0)
        self.addWidget(next_button, 3, 1)
        # Build informative bar (telling displayed image index)

    def _build_button(self, button_name, callback):

        # Button appearance
        button = QPushButton(button_name)
        button.setStyleSheet("border: 1px border-style: outset border-radius: 5px solid #222222;")
        button.setFixedSize(80, 40)

        # add button function
        button.key = button_name
        button.clicked.connect(callback)
        return button

    def _build_image(self):
        label = QLabel()
        # self.mri_seq[0] = self.mri_seq[0].scaled(self.image_size, Qt.IgnoreAspectRatio)
        label.setPixmap(self.mri_seq[0])
        label.setAlignment(Qt.AlignLeft)
        label.setFixedSize(self.image_size)
        self.displayed_image = label
        self.displayed_image.move(400, 400)
        return label

    def _build_image_information(self):
        label = QLabel(" Image {} / {}".format(self.displayed_image_index, self.nb_images))
        self.displayed_image_information = label
        self.displayed_image_information.setFont(QFont('Arial', 30))
        self.displayed_image_information.setAlignment(Qt.AlignLeft)
        return label

    def _click_for_image_change(self):

        """ Update the index of displayed image """
        if self.sender().key == LEFT_REPR and self.displayed_image_index > 1:
            self.displayed_image_index -= 1
        if self.sender().key == RIGHT_REPR and self.displayed_image_index < self.nb_images:
            self.displayed_image_index += 1
        self._refresh_image()
        self._refresh_image_information(self.displayed_image_index)
        print("image index", self.displayed_image_index)

    def _refresh_image(self):
        self.mri_seq[self.displayed_image_index - 1] = self.mri_seq[self.displayed_image_index - 1].scaled(self.image_size, Qt.IgnoreAspectRatio)
        self.displayed_image.setAlignment(Qt.AlignLeft)
        self.displayed_image.setFixedSize(self.image_size)
        self.displayed_image.setPixmap(self.mri_seq[self.displayed_image_index - 1])

    def _refresh_image_information(self, index):
        self.displayed_image_information = QLabel()
        self.displayed_image_information.setText(" Image {} / {}".format(index, self.nb_images))
        self.displayed_image_information.setFont(QFont('Arial', 30))
        self.displayed_image_information.setAlignment(Qt.AlignLeft)




########################################################################################################################
#                                               RIGHT PANEL                                                            #
########################################################################################################################

class TIScoutInformation(QGridLayout):
    
    def __init__(self, patient_id, ti_scout_information, register):
        """

        :param patient_id: (str) patient name
        :param ti_scout_information: (list) in which the information will be stored
        :param register: (bool) register the lines input in text box
        """
        super().__init__()
        self.patient_name = patient_id
        self.ti_scout_infos = ti_scout_information
        self._set_labels()


    def _set_labels(self):

        # Patient ID
        self.patient_name_label = QLabel()
        self.patient_name_label.setText("Patient {}".format(self.patient_name))
        self.patient_name_label.setFont(QFont('Arial', 20))
        self.patient_name_label.setAlignment(Qt.AlignRight)

        # Text explaining what to fill
        self.exp_text_1 = QLabel()
        self.exp_text_1.setText("Write down the indexes corresponding to optimal TIs")
        self.exp_text_1.setFont(QFont('Arial', 14))
        self.exp_text_1.setAlignment(Qt.AlignRight)

        # QLineEdit
        self.edit_ti_index = QLineEdit()
        self.edit_ti_index.setFixedSize(300, 30)
        self.edit_ti_index.setAlignment(Qt.AlignRight)

        # Empty Text
        self.exp_text_2 = QLabel()
        self.exp_text_2.setAlignment(Qt.AlignRight)
        self.exp_text_3 = QLabel()
        self.exp_text_3.setAlignment(Qt.AlignRight)

        self.ti_scout_infos.append(str(self.edit_ti_index.text()))
        print("Written text", str(self.edit_ti_index.text()))

        self.addWidget(self.patient_name_label, 2 * 0, 1)
        self.addWidget(self.exp_text_1, 2 * 4, 1)
        self.addWidget(self.edit_ti_index, 2 * 5, 1)
        self.addWidget(self.exp_text_2, 2 * 6, 1)
        self.addWidget(self.exp_text_3, 2 * 7, 1)



def test_function():
    # load image sequences
    patient_ids = patient_id_extractor(cfg.ROOT)
    patient_id = patient_ids[19]
    mri_seq, _, patient_id = load_patient_mri_images(cfg.ROOT, patient_id)
    print("Patient ID", patient_id)
    ti_info = []
    stop = False

    # create the main window in the application
    app = QApplication([])
    window = MainWidget()
    layout = QHBoxLayout()

    # Get window sizes
    screen_size = QDesktopWidget().screenGeometry()
    ration = 3 / 5
    inverse_ration = 1
    image_size = QSize(mri_seq[0].shape[1] * inverse_ration, mri_seq[0].shape[0] * inverse_ration)
    # image_size = QSize(int(screen_size.width() * ration )- 50, int(screen_size.height() * ration) - 50)

    left_panel = MRISequenceImages(mri_seq, patient_id, image_size)
    right_panel = TIScoutInformation(patient_id, ti_info, stop)

    layout.addLayout(left_panel)
    layout.addLayout(right_panel)

    # Add layout to the window and show the window
    window.setLayout(layout)
    window.showMaximized()
    app.exec_()
    return right_panel.ti_scout_infos


if __name__ == '__main__':
    infos = test_function()

    print('Optimal TIs', infos)

    print('GREAT, everything is fine !')
