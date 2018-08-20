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
        self.setGeometry(100, 100, 200, 200)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for widgets in the window"""
        widget_layout = QVBoxLayout()
        widget_layout.addWidget(self.header)
        widget_layout.addWidget(self.category_select)
        widget_layout.addWidget(self.ok)

        self.setLayout(widget_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.header = QLabel("Select Category")
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
        self.setPalette(QPalette(QColor("#f3ffbd")))
        self.setStyleSheet("""
            .QLabel {
                font-weight: bold;
                font-size: 24px;
                color: #247ba0;
                margin-top: -20px;
                height: 5px;
            }
            .QPushButton {
                background-color: #247ba0;
                border: 1px solid #8CBDAF;
                font-weight: bold;
                font-size: 12px;
                color: #f3ffbd;
                max-width: 100px;
                min-height: 35px;
                margin: 20px 0px 10px 45px;
            }
            .QPushButton:hover {
                background-color: #8CBDAF;
            }
            .QComboBox {
                background-color: #247ba0;
                border: 1px solid #8CBDAF;
                font-weight: bold;
                font-size: 12px;
                color: #f3ffbd;
                max-width: 160px;
                min-height: 20px;
                margin-left: 20px;
            }
            .QComboBox QAbstractItemView { 
                max-width: 160px;
            }
        """)

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
