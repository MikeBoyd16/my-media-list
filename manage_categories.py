import sys
import os
import json
import datetime
from manage_fields import *
from select_category import *
from add_item import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ManageCategories(QDialog):
    def __init__(self, category_names, category_icon_paths):
        super().__init__()
        self.row = -1
        self.category_names = category_names
        self.category_icon_paths = category_icon_paths
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()
        self.init_categories()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setGeometry(100, 100, 250, 500)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        self.layouts = {"main_layout": QVBoxLayout(), "header_layout": QHBoxLayout(), "controls_layout": QHBoxLayout(),
                        "fields_layout": QGridLayout(), "submit_layout": QVBoxLayout()}

        self.layouts["header_layout"].addWidget(self.header)
        self.header.setAlignment(Qt.AlignCenter)

        self.layouts["controls_layout"].addWidget(self.buttons["add_category"])
        self.layouts["controls_layout"].addWidget(self.buttons["remove_category"])
        self.layouts["controls_layout"].setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.layouts["fields_layout"].setSizeConstraint(QLayout.SetFixedSize)
        self.layouts["fields_layout"].setAlignment(Qt.AlignCenter)

        self.layouts["submit_layout"].addWidget(self.buttons["ok"])
        self.layouts["submit_layout"].setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.layouts["submit_layout"].addStretch(1)

        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            self.layouts[layout].setContentsMargins(10, 10, 10, 10)
            self.layouts[layout].setSpacing(15)

        self.setLayout(self.layouts["main_layout"])

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.header = QLabel("Manage Categories")
        self.buttons = {"add_category": QPushButton(), "remove_category": QPushButton(), "ok": QPushButton()}
        for button in self.buttons:
            button_text = button.replace("_", " ").title().rsplit(' ', 1)[0]
            self.buttons[button].setText("  " + button_text)
            self.buttons[button].setFixedSize(QSize(100, 40))
        for button in self.buttons:
            button_method = getattr(self, button)
            self.buttons[button].clicked.connect(button_method)

        self.category_fields = {}
        self.category_buttons = {}

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
                width: 40px;
            }
            .QPushButton:hover {
                background-color: #8CBDAF;
            }
            .QLineEdit {
                width: 120px; 
                margin-top: 14px;
                margin-bottom: 14px;
            }
        """)

    def init_categories(self):
        for idx in range(len(self.category_names)):
            self.row += 1

            self.category_fields[idx] = QLineEdit()
            self.category_fields[idx].setText(str(self.category_names[idx]))
            self.category_fields[idx].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.category_fields[idx].textChanged.connect(self.set_icon_status)
            self.layouts["fields_layout"].addWidget(self.category_fields[idx], idx, 0, 1, 1)

            self.category_buttons[idx] = QPushButton()
            if idx in self.category_icon_paths:
                self.category_buttons[idx].setIcon(QIcon(self.category_icon_paths[idx]))
            else:
                self.category_buttons[idx].setText("Icon")
            self.category_buttons[idx].setIconSize(QSize(30, 30))
            self.category_buttons[idx].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.category_buttons[idx].clicked.connect(self.set_icon)
            self.set_icon_status()
            self.layouts["fields_layout"].addWidget(self.category_buttons[idx], idx, 1, 1, 1)

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def add_category(self):
        """Adds a new field where a category can be entered"""
        self.row += 1

        self.category_fields[self.row] = QLineEdit()
        if self.row < len(self.category_names):
            self.category_fields[self.row].setText(str(self.category_names[self.row]))
        else:
            self.category_fields[self.row].setPlaceholderText("Enter a category name")
        self.category_fields[self.row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.category_fields[self.row].textChanged.connect(self.set_icon_status)
        self.layouts["fields_layout"].addWidget(self.category_fields[self.row], self.row, 0, 1, 1)

        self.category_buttons[self.row] = QPushButton()
        if self.row < len(self.category_icon_paths):
            self.category_buttons[self.row].setIcon(QIcon(self.category_icon_paths[self.row]))
            self.category_buttons[self.row].setIconSize(QSize(30, 30))
        else:
            self.category_buttons[self.row].setText("Icon")
        self.category_buttons[self.row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.category_buttons[self.row].clicked.connect(self.set_icon)
        self.set_icon_status()
        self.layouts["fields_layout"].addWidget(self.category_buttons[self.row], self.row, 1, 1, 1)

    def remove_category(self):
        """Removes an existing field where a category could be entered"""
        if self.row >= 0:
            self.category_fields[self.row].setParent(None)
            del(self.category_fields[self.row])
            self.category_buttons[self.row].setParent(None)
            del(self.category_buttons[self.row])
            os.remove(self.category_icon_paths[self.row])
            del(self.category_icon_paths[self.row])
            del(self.category_names[self.row])
            self.row -= 1

    def set_icon_status(self):
        """Enables/disables combo buttons based on the field combo selection"""
        for idx in range(self.row + 1):
            if self.category_fields[idx].text():
                self.category_buttons[idx].setEnabled(True)
                self.category_buttons[idx].setStyleSheet("""
                                    .QPushButton {background-color: #247ba0;}
                                    .QPushButton:hover {background-color: #8CBDAF;}
                                """)
            else:
                self.category_buttons[idx].setEnabled(False)
                self.category_buttons[idx].setStyleSheet(".QPushButton {background-color: #D7E7EE;}")

            self.update_icon_name(idx)

    def set_icon(self):
        """Sets the icon for a particular category"""
        current_button = self.sender()
        one_based_list = 1
        row_offset = 3
        current_row = (self.layouts["fields_layout"].indexOf(current_button) + one_based_list) // row_offset

        original_icon_path = QFileDialog.getOpenFileName(self, "Open Image", "c:\\", "Image Files (*.png *.jpg *.bmp)")
        if original_icon_path[0]:
            icon_object = QImage()
            icon_object.load(original_icon_path[0])
            icon = QPixmap.fromImage(icon_object)
            icon_object = icon.toImage()
        else:
            return

        new_icon_path = "images/category-icons/" + str(self.category_fields[current_row].text()) + ".jpg"
        icon_object.save(new_icon_path)
        self.category_icon_paths[current_row] = new_icon_path

        current_button.setText("")
        current_button.setIcon(QIcon(self.category_icon_paths[current_row]))
        current_button.setIconSize(QSize(35, 35))

    def update_icon_name(self, idx):
        if -1 < self.row < len(self.category_icon_paths):
            if idx in self.category_icon_paths:
                icon_path = "images/category-icons/" + str(self.category_fields[idx].text()) + ".jpg"
                if icon_path not in self.category_icon_paths[idx]:
                    os.rename(self.category_icon_paths[idx], icon_path)
                    self.category_icon_paths[idx] = icon_path
                    self.category_buttons[idx].setIcon(QIcon(self.category_icon_paths[idx]))

    def ok(self):
        """Returns focus to the main window"""
        self.category_names = {}
        for idx in range(len(self.category_fields)):
            if self.category_fields[idx].text():
                self.category_names[idx] = self.category_fields[idx].text()
        self.hide()
