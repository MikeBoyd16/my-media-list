import sys
import json
import datetime
import add_media
from manage_categories import *
from manage_fields import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SelectMedia(QDialog):
    def __init__(self):
        super().__init__()
        self.temp_input = {}
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""
        self.setWindowTitle("Media Select")
        self.setGeometry(100, 100, 200, 200)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for widgets in the window"""
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.select_media_combo, 0, 0)
        grid_layout.addWidget(self.ok, 1, 0)
        self.ok.move(50, 50)

        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)

        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(group_box)

        self.setLayout(v_box_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.select_media_combo = QComboBox(self)
        self.select_media_combo.addItems(["Music", "Audiobook", "Movie", "TV", "Anime", "Book", "Manga", "Video Game"])

        self.ok = QPushButton("OK", self)
        self.ok.clicked.connect(self.go_to_add_media)

    def init_styles(self):
        """Sets all stylesheet properties"""
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def get_media_selection(self):
        """Returns the currently selected media type"""
        return self.select_media_combo.currentText()

    def go_to_add_media(self):
        """Displays a new AddMedia form and places the resulting
        input in a temporary dictionary variable"""
        add_media_record = add_media.AddMedia(self.get_media_selection())
        add_media_record.exec_()
        self.temp_input = add_media_record.temp_input
        self.temp_input["Media"] = self.select_media_combo.currentText()
        now = datetime.datetime.now()
        self.temp_input["Date Entered"] = str(now.month) + "." + str(now.day) + "." + str(now.year) + ":" + \
                                          str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        self.hide()
