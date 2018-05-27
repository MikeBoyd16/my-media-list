from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from SelectMedia import *


class AddMusic(QMainWindow):
    def __init__(self):
        super(AddMusic, self).__init__()
        self.labels = {"Type": QLabel(), "Favorite": QLabel(), "Name": QLabel(),
                       "Artist": QLabel(), "Album": QLabel(), "Duration": QLabel(),
                       "Genres": QLabel(), "Record Labels": QLabel(), "Producers": QLabel()}
        self.inputs = {"Type": QComboBox(), "Favorite": QComboBox(), "Name": QLineEdit(),
                       "Artist": QLineEdit(), "Album": QLineEdit(), "Duration": QLineEdit(),
                       "Genres": QLineEdit(), "Record Labels": QLineEdit(), "Producers": QLineEdit()}
        self.init_window_properties()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.init_widgets()
        self.init_window()

    def init_window_properties(self):
        self.title = "Add Music"
        self.left = 100
        self.top = 100
        self.width = 250
        self.height = 600

    def init_widgets(self):
        self.inputs["Type"].addItems(["Single", "Remix", "Studio Album", "Extended Play",
                                      "Reissue", "Live Album", "Remix Album"])
        self.inputs["Favorite"].addItems(["Yes", "No", "N/A"])

        for key in self.labels:
            self.labels[key].setText(key)

        self.submit = QPushButton("Submit", self)
        self.submit.setFixedHeight(40)

    def init_layout(self):
        grid_layout = QGridLayout(self.central_widget)

        row = 0
        for key in self.labels:
            grid_layout.addWidget(self.labels[key], row, 0)
            grid_layout.addWidget(self.inputs[key], row, 1)
            row += 1

        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)
        v_box_layout = QVBoxLayout(self.central_widget)
        v_box_layout.addWidget(group_box)
        v_box_layout.addWidget(self.submit)
        self.setLayout(v_box_layout)

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")
        self.init_layout()

    def submit_media(self):

        self.hide()
