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

        # Set this window to always be on top when visible
        self.setModal(True)

        # Initialize category variables
        self.categories = categories

        # Initialize window variables
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initializes the window and its dimensions"""
        self.setGeometry(100, 100, 100, 225)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for widgets in the window"""
        widget_layout = QVBoxLayout()

        # Add the header to the main layout
        widget_layout.addWidget(self.header)
        widget_layout.setAlignment(self.header, Qt.AlignHCenter)

        # Add the category select dropdown to the main layout
        widget_layout.addWidget(self.category_select)
        widget_layout.setAlignment(self.category_select, Qt.AlignHCenter)

        # Add the OK button to the main layout
        widget_layout.addWidget(self.ok)
        widget_layout.setAlignment(self.ok, Qt.AlignHCenter)

        # Set the main layout as the window's layout
        self.setLayout(widget_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""

        # Initialize the header
        self.header = QLabel("Select Category")
        self.header.setMaximumHeight(25)

        # Initialize and populate the category select dropdown
        self.category_select = QComboBox(self)
        self.category_select.setFixedWidth(150)
        self.category_select.setMinimumHeight(22)
        if len(self.categories) > 0:
            for category in self.categories.values():
                self.category_select.addItem(category)
        else:
            self.category_select.addItem("No categories created")

        # Initialize the OK button
        self.ok = QPushButton("OK", self)
        self.ok.setMinimumWidth(100)
        self.ok.setMinimumHeight(30)
        self.ok.clicked.connect(self.submit)

    def init_styles(self):
        """Sets all stylesheet properties"""
        self.setPalette(QPalette(QColor("#f3ffbd")))
        self.setStyleSheet("""
            .QLabel {
                font-weight: bold;
                font-size: 20px;
                color: #247ba0;
            }
            .QPushButton {
                background-color: #247ba0;
                border: 1px solid #8CBDAF;
                font-weight: bold;
                font-size: 12px;
                color: #f3ffbd;
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
                margin: 0;
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
        """Returns focus to the main window"""
        self.hide()
