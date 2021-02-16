import cv2
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QSlider, QGridLayout, QHBoxLayout, QLineEdit, \
    QDesktopWidget

from lib.labelling.gui_functions.main_widget import MainWidget
from lib.utils.image_visu import load_patient_mri_images
from lib.utils.misc import patient_id_extractor
from project_config import *

RIGHT_REPR = ">"
LEFT_REPR = "<"


def transform_array_to_qpixmap(image_path):
    """
    Format conversion
    :param image_path: (str) path to the image
    :return: (QPixmap) Transform an array to qpixmap
    """

    image = cv2.imread(image_path)
    height, width, _ = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qimage = QImage(image, width, height, QImage.Format_Grayscale8)

    return QPixmap.fromImage(qimage)


def display(image_path):
    """

    :param image_path: (str) path to the image
    :return: Display the image
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('img', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class EditIndex(QLineEdit):
    """
       QTextEdit class: used to fill the right indexes for ti scout labelling
       """

    def __init__(self, ti_infos, stop):
        """
        Builds QLineEdit Class
        :param size:
        :param ti_infos:
        """
        super().__init__()
        #  self.setTabChangesFocus(True)
        # self.setFixedSize(size)
        self.setReadOnly(False)
        self.setPlaceholderText('example: 4 5 6')
        self.ti_infos = ti_infos
        self.stop = stop

    def keyReleaseEvent(self, event):
        """
        If escape is pressed, the last selected point is erased.
        If space bar is pressed, the entire widget is closed.
        """
        if event.key() == Qt.Key_W:
            self.parentWidget().erase_point()

        if event.key() == Qt.Key_Escape:
            self.ti_infos = str(self.text())
            self.parentWidget().close()

        # if we would like to stop the selection, we push RIGHT ARROW
        if event.key() == Qt.Key_Right:
            self.stop = True
            print("Stop button was pressed. It has now the value: ", self.stop)

    def focusOutEvent(self, event):
        """
        Register the information given by the user when it is closed.
        """
        # If something has been written
        if self.text() != "":
            self.ti_infos = str(self.text())
            # self.clear()

    def closeEvent(self, event):
        if self.stop:
            self.parentWidget().close()


########################################################################################################################
#                                               LEFT PANEL                                                             #
########################################################################################################################

class MRISequenceImages(QGridLayout):

    def __init__(self, mri_seq, patient_id, image_size, stop=False):
        """

        :param mri_seq: (list) list of QPixmaps of a given mri sequence
        """
        super(MRISequenceImages, self).__init__()
        self.nb_images = len(mri_seq)

        self.images_paths = [osp.join(cfg.PATH_TO_PROJECT, 'data', 'TIScoutBlackBlood_split', patient_id,
                                      mri_seq[i][0].split(' ')[-1] + '.png') for i in range(self.nb_images)]
        self.brightness_value_now = 0

        self.mri_seq = [transform_array_to_qpixmap(self.images_paths[i]) for i in range(self.nb_images)]

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
        self.verticalSlider = self._build_vertical_contrast_slider()
        self.addWidget(self.verticalSlider, 1, 0)

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

        self.addWidget(previous_button, 3, 1)
        self.addWidget(next_button, 3, 2)
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

    def _build_vertical_contrast_slider(self):
        slider = QSlider()
        slider.setOrientation(Qt.Vertical)
        slider.valueChanged['int'].connect(self.brightness_value)  # in order to adapt the contrast
        return slider

    def _build_image(self):
        label = QLabel()
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
        self._refresh_image(self.brightness_value_now)
        self._refresh_image_information(self.displayed_image_index)

    def _refresh_image(self, contrast_value):
        self.mri_seq[self.displayed_image_index - 1] = cv2.imread(self.images_paths[self.displayed_image_index - 1])
        self.mri_seq[self.displayed_image_index - 1] = cv2.cvtColor(self.mri_seq[self.displayed_image_index - 1],
                                                                    cv2.COLOR_BGR2GRAY)
        lim = 255 - contrast_value
        self.mri_seq[self.displayed_image_index - 1][self.mri_seq[self.displayed_image_index - 1] > lim] = 255
        self.mri_seq[self.displayed_image_index - 1][
            self.mri_seq[self.displayed_image_index - 1] <= lim] += contrast_value // 2
        self.mri_seq[self.displayed_image_index - 1] = QImage(self.mri_seq[self.displayed_image_index - 1],
                                                              self.image_size.width(), self.image_size.height(),
                                                              QImage.Format_Grayscale8)
        self.mri_seq[self.displayed_image_index - 1] = QPixmap.fromImage(self.mri_seq[self.displayed_image_index - 1])

        self.mri_seq[self.displayed_image_index - 1] = self.mri_seq[self.displayed_image_index - 1].scaled(
            self.image_size, Qt.IgnoreAspectRatio)
        self.displayed_image.setAlignment(Qt.AlignLeft)
        self.displayed_image.setFixedSize(self.image_size)
        self.displayed_image.setPixmap(self.mri_seq[self.displayed_image_index - 1])

    def _refresh_image_information(self, index):
        # self.displayed_image_information = QLabel()
        self.displayed_image_information.setText(" Image {} / {}".format(index, self.nb_images))
        self.displayed_image_information.setFont(QFont('Arial', 30))
        self.displayed_image_information.setAlignment(Qt.AlignLeft)

    def brightness_value(self, contrast_value):
        self.brightness_value_now = contrast_value
        self._refresh_image(contrast_value)


########################################################################################################################
#                                               RIGHT PANEL                                                            #
########################################################################################################################

class TIScoutInformation(QGridLayout):

    def __init__(self, patient_id, ti_scout_information, can_stop=False):
        """
        Contains all the information in the right side of window application (text box, patient name, instructions)

        :param patient_id: (str) patient name
        :param ti_scout_information: (list) in which the information will be stored
        :param register: (bool) register the lines input in text box
        """
        super().__init__()
        self.patient_name = patient_id
        self.ti_scout_infos = ti_scout_information

        # Condition to stop labelling
        self.can_stop = can_stop
        self.stop = False

        # set the labels
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
        self.edit_ti_index = EditIndex(self.ti_scout_infos, self.stop)
        self.edit_ti_index.setFixedSize(320, 30)
        self.edit_ti_index.setAlignment(Qt.AlignRight)
        self.ti_scout_infos = self.edit_ti_index.ti_infos

        # Empty Text
        self.exp_text_2 = QLabel()
        self.exp_text_2.setAlignment(Qt.AlignRight)
        self.exp_text_3 = QLabel()
        self.exp_text_3.setAlignment(Qt.AlignRight)

        # self.ti_scout_infos.append(str(self.edit_ti_index.text()))
        # print("Written text", str(self.edit_ti_index.text()))

        self.addWidget(self.patient_name_label, 2 * 0, 1)
        self.addWidget(self.exp_text_1, 2 * 4, 1)
        self.addWidget(self.edit_ti_index, 2 * 5, 1)
        self.addWidget(self.exp_text_2, 2 * 6, 1)
        self.addWidget(self.exp_text_3, 2 * 7, 1)

        self.stop = self.edit_ti_index.stop
        print("stop values", self.edit_ti_index.stop, self.stop)

    def erase(self):
        self.stop = self.edit_ti_index.stop
        self.update()


def labelling_app(patient_id):
    # load image sequences
    mri_im, mri_seq, patient_id = load_patient_mri_images(cfg.ROOT, patient_id)
    ti_info = []
    stop = False

    # create the main window in the application
    app = QApplication([])
    window = MainWidget()
    layout = QHBoxLayout()

    # Get window sizes
    # screen_size = QDesktopWidget().screenGeometry()
    ration = 3 / 5
    inverse_ration = 1
    image_size = QSize(mri_im[0].shape[1] * inverse_ration, mri_im[0].shape[0] * inverse_ration)

    left_panel = MRISequenceImages(mri_seq, patient_id, image_size)
    right_panel = TIScoutInformation(patient_id, ti_info, stop)

    layout.addLayout(left_panel)
    layout.addLayout(right_panel)

    # Add layout to the window and show the window
    window.setLayout(layout)
    window.showMaximized()
    app.exec_()
    return patient_id, right_panel.edit_ti_index.ti_infos, right_panel.stop


if __name__ == '__main__':
    patient_ids = patient_id_extractor(cfg.ROOT)
    patient_id = patient_ids[19]

    infos = labelling_app(patient_id)
    print('GREAT, everything is fine !')
