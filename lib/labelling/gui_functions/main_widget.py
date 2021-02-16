from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class MainWidget(QWidget):

    def __init__(self, index_close=2):
        super().__init__()
        self.setFocusPolicy(True)
        self.setFixedSize(850, 400)
        # The index of the child that is the image selection widget
        self.index_close = index_close


    def keyReleaseEvent(self, event):
        """
        If space bar is pressed, it closes the application.
        """
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """
        Close the image selection widget in order to register the points.
        """
        children = self.children()
        children[self.index_close].close()

    def erase(self):
        self.children()[1].erase()

