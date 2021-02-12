import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt, QSize
from lib.labelling.gui_functions.main_widget import MainWidget
import cv2
from project_config import Config



def window_optimal_ti_scout_selection(patient_id, images_seq, optimal_indexes):
    """
        This function will gather all the information needed for the application

    :param patient_id:
    :param images_seq:
    :return:
    """

    # set the application
    app = QApplication([])
    window = MainWidget(index_close=2)
    layout = QVBoxLayout()

    # window size
    screen_size = QDesktopWidget().screenGeometry()
    images_size = QSize(screen_size.width() - 25, screen_size.height() - 950)

    # Set the image selection and the editable text
    pix_maps = [transform_array_to_qpixmap(image) for image in images_seq]

    # The class image selection must correspond to a window on which we can display the list of desired images
    image_selection = ImageSelection(pix_map, image_size, points_image, colors, skip=True, can_stop=True)

    # Calibration points
    blank_frame_lane = BLANK + "Lane n° {} \n \n Frame n° {}".format(lane, frame) + BLANK
    blank = QLabel(blank_frame_lane)
    information_points = QLabel(INSTRUCTIONS)

    # Add widgets to layout
    layout.addWidget(blank)
    layout.addWidget(image_selection)
    layout.addWidget(information_points)

    # Add layout to window and show the window
    window.setLayout(layout)
    window.showMaximized()
    app.exec_()

    return patient_id, points_image, image_selection.stop


if __name__ == "__main__":
    # Get the array
    ROOT_IMAGE = Path('../../../data/5_model_output/tries/raw_images/vid0_frame126.jpg')
    IMAGE = cv2.imread(str(ROOT_IMAGE))

    # Select the points
    print(window_ti_scout_labelling(IMAGE, 1, 2))