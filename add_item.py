import sys
import json
import datetime
from manage_categories import *
from manage_fields import *
from select_category import *
from PyQt5.QtWidgets import *


class AddItem(QDialog):
    def __init__(self, category):
        super().__init__()
        self.category = category
        self.item = {}
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""
        self.setWindowTitle("Add Music")
        self.setGeometry(100, 100, 250, 600)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for the widgets in the window"""
        grid_layout = QGridLayout()

        row = 0
        for key in self.labels:
            grid_layout.addWidget(self.labels[key], row, 0)
            grid_layout.addWidget(self.inputs[key], row, 1)
            row += 1

        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)
        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(group_box)
        v_box_layout.addWidget(self.submit)
        self.setLayout(v_box_layout)

    def init_widgets(self):
        """
        Populates the form with the correct widgets for the selected category
        """
        widgets = {}

        # Populate the form with widgets based on the selected template
        self.labels = {}
        self.inputs = {}
        for key, value in widgets.items():
            self.labels[key] = QLabel()
            self.labels[key].setText(key)
            if value == "line":
                self.inputs[key] = QLineEdit()
            elif value == "combo":
                self.inputs[key] = QComboBox()

        self.submit = QPushButton("Submit", self)
        self.submit.setFixedHeight(40)
        self.submit.clicked.connect(self.submit_item)

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        self.setStyleSheet("""
                        QMainWindow {
                            background: #BCBCBC;
                            }
                        """)

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
