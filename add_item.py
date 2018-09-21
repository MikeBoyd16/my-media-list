import sys
import json
import datetime
from manage_categories import *
from manage_fields import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from select_category import *
from PyQt5.QtWidgets import *


class AddItem(QDialog):
    def __init__(self, category, category_fields):
        super().__init__()
        self.setModal(True)
        self.category = category
        self.category_fields = category_fields
        self.item = {}
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""
        self.setGeometry(100, 100, 250, 600)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for the widgets in the window"""
        self.layouts = {"main_layout": QVBoxLayout(), "header_layout": QHBoxLayout(),
                        "image_layout": QVBoxLayout(), "fields_layout": QGridLayout(),
                        "submit_layout": QVBoxLayout()}

        self.layouts["header_layout"].addWidget(self.header)
        self.header.setAlignment(Qt.AlignCenter)

        self.layouts["image_layout"].addWidget(self.image_container)
        self.layouts["image_layout"].addWidget(self.browse_image)

        self.layouts["fields_layout"].setSizeConstraint(QLayout.SetFixedSize)
        self.layouts["fields_layout"].setAlignment(Qt.AlignCenter)

        self.layouts["submit_layout"].addWidget(self.submit)
        self.layouts["submit_layout"].setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.layouts["submit_layout"].addStretch(1)

        if len(self.category_fields[self.category]) > 0:
            self.init_fields_layouts()
        else:
            self.init_no_fields_layouts()

        self.setLayout(self.layouts["main_layout"])

    def init_fields_layouts(self):
        """Arranges the frame's layouts to include category fields"""
        row = 0
        for key in self.labels:
            self.layouts["fields_layout"].addWidget(self.labels[key], row, 0)
            self.layouts["fields_layout"].addWidget(self.inputs[key], row, 1)
            row += 1

        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            self.layouts[layout].setContentsMargins(10, 10, 10, 10)
            self.layouts[layout].setSpacing(15)

    def init_no_fields_layouts(self):
        """Arranges the frame's layouts to not include category fields"""
        self.layouts["fields_layout"].addWidget(self.no_field_message, 0, 0, 2, 1)
        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            if layout == "fields_layout":
                self.layouts["main_layout"].addSpacerItem(QSpacerItem(100, 260))
            elif layout == "header_layout":
                self.layouts["main_layout"].addSpacerItem(QSpacerItem(100, 100))
            self.layouts[layout].setContentsMargins(10, 10, 10, 10)
            self.layouts[layout].setSpacing(15)

    def init_widgets(self):
        """
        Populates the form with the correct widgets for the selected category
        """
        self.header = QLabel("Add " + self.category)
        self.header.setStyleSheet(".QLabel{font-size: 24px;}")
        self.no_field_message = QLabel("The " + self.category + " category doesn't have any fields.")
        self.no_field_message.setWordWrap(True)
        self.no_field_message.setStyleSheet(".QLabel{font-size: 14px;}")

        self.image_container = QLabel()
        self.image = QPixmap()
        self.browse_image = QPushButton("Browse")
        self.browse_image.clicked.connect(self.select_image)

        self.labels, self.inputs = {}, {}
        for idx in range(len(self.category_fields[self.category])):
            key = str(idx)
            field_name = self.category_fields[self.category][key][0]
            field_type = self.category_fields[self.category][key][1]
            field_items = self.category_fields[self.category][key][2]

            self.labels[field_name] = QLabel()
            self.labels[field_name].setText(field_name)
            self.labels[field_name].setStyleSheet(".QLabel{font-size: 14px;}")
            if field_type == "Text":
                self.inputs[field_name] = QLineEdit()
            else:
                self.inputs[field_name] = QComboBox()
                self.inputs[field_name].addItems(field_items)

        self.submit = QPushButton("Submit", self)
        self.submit.setFixedHeight(40)
        self.submit.clicked.connect(self.submit_item)

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        self.setPalette(QPalette(QColor("#f3ffbd")))
        self.setStyleSheet("""
            .QLabel {
                font-weight: bold;
                color: #247ba0;
            }
            .QPushButton {
                background-color: #247ba0;
                border: 1px solid #8CBDAF;
                font-weight: bold;
                font-size: 12px;
                color: #f3ffbd;
                width: 100px;
            }
            .QPushButton:hover {
                background-color: #8CBDAF;
            }
            .QLineEdit {
                width: 50px;
                margin: 10px 20px 10px 20px;
            }
        """)

    def select_image(self):
        pass

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def submit_item(self):
        """Places the inputs from the input fields into a temp data structure"""
        for key in self.inputs:
            if isinstance(self.inputs[key], QComboBox):
                self.item[key] = self.inputs[key].currentText()
            else:
                # If there are multiple inputs for one field, split them
                if "," in self.inputs[key].text():
                    input_list = self.inputs[key].text()
                    input_list = input_list.split(",")

                    # If whitespace exists at the beginning of an input, remove it
                    for idx in range(len(input_list)):
                        if input_list[idx][0] == " ":
                            input_list[idx] = input_list[idx][1:]

                    self.item[key] = input_list
                else:
                    self.item[key] = self.inputs[key].text()
        self.hide()
