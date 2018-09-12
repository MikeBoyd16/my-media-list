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
        self.setModal(True)
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
            if layout == "fields_layout":
                self.layouts["main_layout"].addWidget(self.top_line)
            elif layout == "submit_layout":
                self.layouts["main_layout"].addWidget(self.bottom_line)
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            self.layouts[layout].setContentsMargins(10, 10, 10, 10)
            self.layouts[layout].setSpacing(20)

        self.setLayout(self.layouts["main_layout"])

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.header = QLabel(self.category + " Fields")
        self.buttons = {"add_field": QPushButton(), "remove_field": QPushButton(), "ok": QPushButton()}
        for button in self.buttons:
            button_text = button.replace("_", " ").title().rsplit(' ', 1)[0]
            self.buttons[button].setText("  " + button_text)
            self.buttons[button].setFixedSize(QSize(100, 35))
        for button in self.buttons:
            button_method = getattr(self, button)
            self.buttons[button].clicked.connect(button_method)

        self.field_names = {}
        self.field_types = {}
        self.combo_items_buttons = {}
        self.combo_items = {}

        self.top_line = QFrame()
        self.top_line.setFrameShape(QFrame.HLine)
        self.top_line_shadow = QGraphicsDropShadowEffect()
        self.top_line_shadow.setBlurRadius(7.0)
        self.top_line_shadow.setOffset(2.3)
        self.top_line.setGraphicsEffect(self.top_line_shadow)

        self.bottom_line = QFrame()
        self.bottom_line.setFrameShape(QFrame.HLine)
        self.bottom_line_shadow = QGraphicsDropShadowEffect()
        self.bottom_line_shadow.setBlurRadius(7.0)
        self.bottom_line_shadow.setOffset(-2.3)
        self.bottom_line.setGraphicsEffect(self.bottom_line_shadow)

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
                width: 75px;
            }
        """)

    def init_category_fields(self):
        if self.category in self.category_fields:
            if len(self.category_fields[self.category]) > 0:
                for idx in range(len(self.category_fields[self.category])):
                    key = str(idx)
                    self.row += 1

                    self.field_names[key] = QLineEdit()
                    self.field_names[key].setText(self.category_fields[self.category][key][0])
                    self.field_names[key].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                    self.layouts["fields_layout"].addWidget(self.field_names[key], idx, 0)

                    self.field_types[key] = QComboBox()
                    self.field_types[key].addItems(["Text", "Dropdown"])
                    if self.category_fields[self.category][key][1] == "Dropdown":
                        self.field_types[key].setCurrentIndex(1)
                    self.field_types[key].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                    self.field_types[key].currentIndexChanged.connect(self.combo_button_status)
                    self.layouts["fields_layout"].addWidget(self.field_types[key], idx, 1)

                    self.combo_items_buttons[key] = QPushButton(". . .")
                    self.combo_items_buttons[key].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                    self.combo_items_buttons[key].clicked.connect(self.get_combo_items)
                    self.combo_button_status()
                    self.layouts["fields_layout"].addWidget(self.combo_items_buttons[key], idx, 2)

                    self.combo_items[key] = self.category_fields[self.category][key][2]

        # If there are fewer than six fields, populate the window with additional empty fields.
        while self.row < 5:
            self.add_field()

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def add_field(self):
        """Adds a new field where a category can be entered"""
        self.row += 1
        key = str(self.row)

        self.field_names[key] = QLineEdit()
        self.field_names[key].setPlaceholderText("Enter a field name")
        self.field_names[key].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.layouts["fields_layout"].addWidget(self.field_names[key], self.row, 0)

        self.field_types[key] = QComboBox()
        self.field_types[key].addItems(["Text", "Dropdown"])
        self.field_types[key].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.field_types[key].currentIndexChanged.connect(self.combo_button_status)
        self.layouts["fields_layout"].addWidget(self.field_types[key], self.row, 1)

        self.combo_items_buttons[key] = QPushButton(" . . . ")
        self.combo_items_buttons[key].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.combo_items_buttons[key].clicked.connect(self.get_combo_items)
        self.combo_button_status()
        self.layouts["fields_layout"].addWidget(self.combo_items_buttons[key], self.row, 2)

    def remove_field(self):
        """Removes an existing field where a category could be entered"""
        if self.row > 0:
            key = str(self.row)
            self.field_names[key].setParent(None)
            del(self.field_names[key])
            self.field_types[key].setParent(None)
            del(self.field_types[key])
            self.combo_items_buttons[key].setParent(None)
            del (self.combo_items_buttons[key])
            if key in self.combo_items:
                del(self.combo_items[key])
            self.row -= 1

    def ok(self):
        self.category_fields[self.category] = {}
        field_count = 0
        for current_row in range(self.row + 1):
            key = str(current_row)
            if self.field_names[key].text():
                self.category_fields[self.category][str(field_count)] = []
                self.category_fields[self.category][str(field_count)].insert(0, self.field_names[key].text())
                self.category_fields[self.category][str(field_count)].insert(1, self.field_types[key].currentText())
                if key in self.combo_items:
                    self.category_fields[self.category][str(field_count)].insert(2, self.combo_items[key])
                else:
                    self.category_fields[self.category][str(field_count)].insert(2, "")
                field_count += 1
        self.hide()

    def combo_button_status(self):
        """Enables/disables combo buttons based on the field combo selection"""
        for idx in range(self.row + 1):
            key = str(idx)
            if self.field_types[key].currentText() == "Text":
                self.combo_items_buttons[key].setEnabled(False)
                self.combo_items_buttons[key].setStyleSheet(".QPushButton {background-color: #D7E7EE;}")
            else:
                self.combo_items_buttons[key].setEnabled(True)
                self.combo_items_buttons[key].setStyleSheet("""
                    .QPushButton {background-color: #247ba0;}
                    .QPushButton:hover {background-color: #8CBDAF;}
                """)

    def get_combo_items(self):
        """Calls an input dialog window to retrieve field items"""
        current_button = self.sender()
        current_row = ((self.layouts["fields_layout"].indexOf(current_button) + 1) // 3) - 1
        key = str(current_row)

        if self.category in self.category_fields and key in self.category_fields[self.category]:
            input_dialog = GetComboItems(self.field_names[key].text(), self.category_fields[self.category][key][2])
        else:
            input_dialog = GetComboItems(self.field_names[key].text())

        input_dialog.show()
        input_dialog.exec_()

        if input_dialog.input_field.text():
            self.combo_items[key] = input_dialog.input_field.text().split(",")


class GetComboItems(QDialog):
    def __init__(self, field_name, combo_items=""):
        super().__init__()
        self.setModal(True)
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
