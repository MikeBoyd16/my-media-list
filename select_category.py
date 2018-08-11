import sys
import json
import datetime
from add_item import *
from manage_categories import *
from manage_fields import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SelectCategory(QDialog):
    def __init__(self, categories):
        super().__init__()
        self.categories = categories
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""
        self.setWindowTitle("Category Select")
        self.setGeometry(100, 100, 200, 200)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for widgets in the window"""
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.category_select, 0, 0)
        grid_layout.addWidget(self.ok, 1, 0)
        self.ok.move(50, 50)

        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)

        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(group_box)

        self.setLayout(v_box_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.category_select = QComboBox(self)
        if len(self.categories) > 0:
            for category in self.categories.values():
                self.category_select.addItem(category)
        else:
            self.category_select.addItem("No categories created")
        self.ok = QPushButton("OK", self)
        self.ok.clicked.connect(self.submit)

    def init_styles(self):
        """Sets all stylesheet properties"""
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def get_category(self):
        """Returns the currently selected media type"""
        return self.category_select.currentText()

    def submit(self):
        self.hide()
