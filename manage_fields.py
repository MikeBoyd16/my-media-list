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
    def __init__(self, category, category_fields):
        super().__init__()
        self.row = -1
        self.category = category
        self.category_fields = category_fields
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()
        self.init_category_fields()

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
        self.header = QLabel(self.category + "Fields")
        self.buttons = {"add_field": QPushButton(), "remove_field": QPushButton(), "ok": QPushButton()}
        for button in self.buttons:
            button_text = button.replace("_", " ").title().rsplit(' ', 1)[0]
            self.buttons[button].setText("  " + button_text)
            self.buttons[button].setFixedSize(QSize(100, 40))
        for button in self.buttons:
            button_method = getattr(self, button)
            self.buttons[button].clicked.connect(button_method)

        self.field_names = {}
        self.field_types = {}
        self.combo_items_buttons = {}
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

    def init_category_fields(self):
        if self.category in self.category_fields:
            for current_row in range(len(self.category_fields[self.category])):
                self.row += 1

                self.field_names[current_row] = QLineEdit()
                self.field_names[current_row].setText(self.category_fields[self.category][current_row][0])
                self.field_names[current_row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                self.layouts["fields_layout"].addWidget(self.field_names[current_row], current_row, 0)

                self.field_types[current_row] = QComboBox()
                self.field_types[current_row].addItems(["Text", "Dropdown"])
                if self.category_fields[self.category][current_row][1] == "Dropdown":
                    self.field_types[current_row].setCurrentIndex(1)
                self.field_types[current_row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                self.field_types[current_row].currentIndexChanged.connect(self.combo_button_status)
                self.layouts["fields_layout"].addWidget(self.field_types[current_row], current_row, 1)

                self.combo_items_buttons[current_row] = QPushButton(" . . . ")
                self.combo_items_buttons[current_row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                self.combo_items_buttons[current_row].clicked.connect(self.get_combo_items)
                self.combo_button_status()
                self.layouts["fields_layout"].addWidget(self.combo_items_buttons[current_row], current_row, 2)

                self.combo_items[current_row] = self.category_fields[self.category][current_row][2]

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def add_field(self):
        """Adds a new field where a category can be entered"""
        self.row += 1

        self.field_names[self.row] = QLineEdit()
        self.field_names[self.row].setPlaceholderText("Enter a field name")
        self.field_names[self.row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.layouts["fields_layout"].addWidget(self.field_names[self.row], self.row, 0)

        self.field_types[self.row] = QComboBox()
        self.field_types[self.row].addItems(["Text", "Dropdown"])
        self.field_types[self.row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.field_types[self.row].currentIndexChanged.connect(self.combo_button_status)
        self.layouts["fields_layout"].addWidget(self.field_types[self.row], self.row, 1)

        self.combo_items_buttons[self.row] = QPushButton(" . . . ")
        self.combo_items_buttons[self.row].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.combo_items_buttons[self.row].clicked.connect(self.get_combo_items)
        self.combo_button_status()
        self.layouts["fields_layout"].addWidget(self.combo_items_buttons[self.row], self.row, 2)

    def remove_field(self):
        """Removes an existing field where a category could be entered"""
        if self.row >= 0:
            self.field_names[self.row].setParent(None)
            del(self.field_names[self.row])
            self.field_types[self.row].setParent(None)
            del(self.field_types[self.row])
            self.combo_items_buttons[self.row].setParent(None)
            del (self.combo_items_buttons[self.row])
            if self.row in self.combo_items:
                del(self.combo_items[self.row])
            self.row -= 1

    def ok(self):
        self.category_fields[self.category] = {}
        field_count = 0
        for current_row in range(self.row + 1):
            if self.field_names[current_row].text():
                self.category_fields[self.category][field_count] = []
                self.category_fields[self.category][field_count].insert(0, self.field_names[current_row].text())
                self.category_fields[self.category][field_count].insert(1, self.field_types[current_row].currentText())
                if current_row in self.combo_items:
                    self.category_fields[self.category][field_count].insert(2, self.combo_items[current_row])
                else:
                    self.category_fields[self.category][field_count].insert(2, "")
                field_count += 1
        self.hide()

    def combo_button_status(self):
        """Enables/disables combo buttons based on the field combo selection"""
        for idx in range(self.row + 1):
            if self.field_types[idx].currentText() == "Text":
                self.combo_items_buttons[idx].setEnabled(False)
                self.combo_items_buttons[idx].setStyleSheet(".QPushButton {background-color: #D7E7EE;}")
            else:
                self.combo_items_buttons[idx].setEnabled(True)
                self.combo_items_buttons[idx].setStyleSheet("""
                    .QPushButton {background-color: #247ba0;}
                    .QPushButton:hover {background-color: #8CBDAF;}
                """)

    def get_combo_items(self):
        """Calls an input dialog window to retrieve field items"""
        current_button = self.sender()
        current_row = ((self.layouts["fields_layout"].indexOf(current_button) + 1) // 3) - 1

        if self.category in self.category_fields and current_row in self.category_fields[self.category]:
            input_dialog = GetComboItems(self.field_names[current_row].text(),
                                         self.category_fields[self.category][current_row][2])
        else:
            input_dialog = GetComboItems(self.field_names[current_row].text())

        input_dialog.show()
        input_dialog.exec_()

        if input_dialog.input_field.text():
            self.combo_items[current_row] = input_dialog.input_field.text().split(",")


class GetComboItems(QDialog):
    def __init__(self, field_name, combo_items=""):
        super().__init__()
        self.field_name = field_name
        self.combo_items = combo_items
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()
        self.init_combo_items()

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

    def init_combo_items(self):
        if self.combo_items != "":
            self.input_field.setText("".join(self.combo_items).replace(" ", ", "))

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def submit(self):
        """Returns focus to the main window"""
        self.hide()
