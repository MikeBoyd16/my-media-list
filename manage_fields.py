import sys
import json
import datetime
from manage_categories import *
from select_category import *
from add_item import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ManageFields(QDialog):
    def __init__(self):
        super().__init__()
        self.row_count = 0
        self.category = ""
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setGeometry(100, 100, 300, 500)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        self.layouts = {"main_layout": QVBoxLayout(), "header_layout": QHBoxLayout(), "controls_layout": QHBoxLayout(),
                        "fields_layout": QGridLayout(), "submit_layout": QVBoxLayout()}
        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            if layout == "header_layout":
                self.layouts[layout].addWidget(self.header)
                self.layouts[layout].setAlignment(Qt.AlignCenter)
            elif layout == "controls_layout":
                self.layouts[layout].addWidget(self.buttons["add_field"])
                self.layouts[layout].addWidget(self.buttons["remove_field"])
                self.layouts[layout].setAlignment(Qt.AlignCenter)
            elif layout == "fields_layout":
                self.layouts[layout].setSizeConstraint(QLayout.SetFixedSize)
                self.layouts[layout].setAlignment(Qt.AlignCenter)
            elif layout == "submit_layout":
                self.layouts[layout].addWidget(self.buttons["ok"])
                self.layouts[layout].setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
                self.layouts[layout].addStretch(1)
            self.layouts[layout].setContentsMargins(10, 10, 10, 10)
            self.layouts[layout].setSpacing(15)
        self.setLayout(self.layouts["main_layout"])

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.header = QLabel("Manage Fields")
        self.buttons = {"add_field": QPushButton(), "remove_field": QPushButton(), "ok": QPushButton()}
        for button in self.buttons:
            button_text = button.replace("_", " ").title().rsplit(' ', 1)[0]
            self.buttons[button].setText("  " + button_text)
            self.buttons[button].setFixedSize(QSize(100, 40))
        for button in self.buttons:
            button_method = getattr(self, button)
            self.buttons[button].clicked.connect(button_method)

        self.field_names = {}
        self.field_combos = {}
        self.combo_items = {}

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        self.setPalette(QPalette(QColor("#f3ffbd")))
        self.setStyleSheet("""
            .QLabel {
                font-weight: bold;
                font-size: 24px;
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
            }
            .QLineEdit {
                width: 100px;
            }
        """)

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def add_field(self):
        """Adds a new field where a category can be entered"""
        self.row_count += 1

        self.field_names[self.row_count] = QLineEdit()
        self.field_names[self.row_count].setPlaceholderText("Enter a field name")
        self.field_names[self.row_count].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.layouts["fields_layout"].addWidget(self.field_names[self.row_count], self.row_count - 1, 0)

        self.field_combos[self.row_count] = QComboBox()
        self.field_combos[self.row_count].addItems(["Text", "Dropdown"])
        self.field_combos[self.row_count].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.layouts["fields_layout"].addWidget(self.field_combos[self.row_count], self.row_count - 1, 1)

        self.combo_items[self.row_count] = QPushButton(" . . . ")
        self.combo_items[self.row_count].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.layouts["fields_layout"].addWidget(self.combo_items[self.row_count], self.row_count - 1, 2)

    def remove_field(self):
        """Removes an existing field where a category could be entered"""
        if self.row_count != 0:
            self.field_names[self.row_count].setParent(None)
            del(self.field_names[self.row_count])
            self.field_combos[self.row_count].setParent(None)
            del(self.field_combos[self.row_count])
            self.combo_items[self.row_count].setParent(None)
            del (self.combo_items[self.row_count])
            self.row_count -= 1

    def ok(self):
        """Returns focus to the main window"""
        self.hide()
