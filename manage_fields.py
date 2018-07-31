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
    def __init__(self, selected_category):
        super().__init__()
        self.row_count = 0
        self.selected_row = 0
        self.selected_category = selected_category
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

        self.layouts["header_layout"].addWidget(self.header)
        self.layouts["header_layout"].setAlignment(Qt.AlignCenter)

        self.layouts["controls_layout"].addWidget(self.buttons["add_field"])
        self.layouts["controls_layout"].addWidget(self.buttons["remove_field"])
        self.layouts["controls_layout"].setAlignment(Qt.AlignCenter)

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
        self.combo_buttons = {}
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
        self.layouts["fields_layout"].addWidget(self.field_names[self.row_count], self.row_count, 0)

        self.field_combos[self.row_count] = QComboBox()
        self.field_combos[self.row_count].addItems(["Text", "Dropdown"])
        self.field_combos[self.row_count].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.field_combos[self.row_count].currentIndexChanged.connect(self.combo_button_status)
        self.layouts["fields_layout"].addWidget(self.field_combos[self.row_count], self.row_count, 1)

        self.combo_buttons[self.row_count] = QPushButton(" . . . ")
        self.combo_buttons[self.row_count].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.combo_buttons[self.row_count].clicked.connect(self.get_combo_items)
        self.combo_button_status()
        self.layouts["fields_layout"].addWidget(self.combo_buttons[self.row_count], self.row_count, 2)

    def remove_field(self):
        """Removes an existing field where a category could be entered"""
        if self.row_count != 0:
            self.field_names[self.row_count].setParent(None)
            del(self.field_names[self.row_count])
            self.field_combos[self.row_count].setParent(None)
            del(self.field_combos[self.row_count])
            self.combo_buttons[self.row_count].setParent(None)
            del (self.combo_buttons[self.row_count])
            if self.row_count in self.combo_items:
                self.combo_items[self.row_count].setParent(None)
                del(self.combo_items[self.row_count])
            self.row_count -= 1

    def ok(self):
        """Returns focus to the main window"""
        self.hide()

    def combo_button_status(self):
        """Enables/disables combo buttons based on the field combo selection"""
        for idx in range(1, self.row_count + 1):
            if self.field_combos[idx].currentText() == "Text":
                self.combo_buttons[idx].setEnabled(False)
                self.combo_buttons[idx].setStyleSheet(".QPushButton {background-color: #D7E7EE;}")
            else:
                self.combo_buttons[idx].setEnabled(True)
                self.combo_buttons[idx].setStyleSheet("""
                    .QPushButton {background-color: #247ba0;}
                    .QPushButton:hover {background-color: #8CBDAF;}
                """)

    def get_combo_items(self):
        """Calls an input dialog window to retrieve field items"""
        current_button = self.sender()
        one_based_list = 1
        row_offset = 3
        current_row = (self.layouts["fields_layout"].indexOf(current_button) + one_based_list) / row_offset

        input_dialog = GetComboItems(self.field_names[current_row].text())
        input_dialog.show()
        input_dialog.exec_()

        if input_dialog.input_field.text():
            self.combo_items[current_row] = input_dialog.input_field.text().split(",")


class GetComboItems(QDialog):
    def __init__(self, field_name):
        super().__init__()
        self.field_name = field_name
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setGeometry(100, 100, 150, 150)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.input_field)
        self.main_layout.addWidget(self.ok)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)
        self.setLayout(self.main_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""
        if self.field_name:
            self.header = QLabel(self.field_name)
        else:
            self.header = QLabel("No Name")
        self.header.setAlignment(Qt.AlignCenter)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter field items")
        self.ok = QPushButton("OK")
        self.ok.clicked.connect(self.submit)

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        self.setPalette(QPalette(QColor("#f3ffbd")))
        self.setStyleSheet("""
            .QLabel {
                font-weight: bold;
                font-size: 24px;
                color: #247ba0;
                margin: 0;
            }
            .QPushButton {
                background-color: #247ba0;
                border: 1px solid #8CBDAF;
                font-weight: bold;
                font-size: 12px;
                color: #f3ffbd;
                height: 30px;
            }
            .QPushButton:hover {
                background-color: #8CBDAF;
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

    def submit(self):
        """Returns focus to the main window"""
        self.hide()
