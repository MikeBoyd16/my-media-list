import sys
import json
import datetime
from manage_categories import *
from manage_fields import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from select_category import *
from PyQt5.QtWidgets import *
from PIL import Image


class AddItem(QDialog):
    def __init__(self, category, category_fields):
        super().__init__()

        # Set this window to always be on top when visible
        self.setModal(True)

        # Initialize category variables
        self.category = category
        self.category_fields = category_fields

        # Initialize image variables
        self.original_image_path = ""
        self.new_image_path = ""
        self.image_width = 0
        self.image_height = 0

        # Initialize item variables
        self.item = {}

        # Initialize window variables
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initializes the window and its dimensions"""
        self.setGeometry(100, 100, 250, 600)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout for the widgets in the window"""
        self.layouts = {"main_layout": QVBoxLayout(), "header_layout": QHBoxLayout(),
                        "image_layout": QVBoxLayout(), "fields_layout": QVBoxLayout(),
                        "submit_layout": QVBoxLayout()}

        # Add the header to the header layout
        self.layouts["header_layout"].addWidget(self.header)
        self.layouts["header_layout"].setContentsMargins(10, 10, 10, 10)
        self.layouts["header_layout"].setSpacing(5)

        # Add the image container and browse image button to the image layout
        self.layouts["image_layout"].addWidget(self.image_container)
        self.layouts["image_layout"].addWidget(self.browse_image)
        self.layouts["image_layout"].setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layouts["image_layout"].setContentsMargins(0, 15, 0, 15)
        self.layouts["image_layout"].setSpacing(20)

        # Format the fields layout
        self.layouts["fields_layout"].setSizeConstraint(QLayout.SetFixedSize)
        self.layouts["fields_layout"].setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layouts["fields_layout"].setContentsMargins(0, 10, 0, 0)
        self.layouts["fields_layout"].setSpacing(10)

        # Add the submit button to the submit layout
        self.layouts["submit_layout"].addWidget(self.submit)
        self.layouts["submit_layout"].setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.layouts["submit_layout"].setContentsMargins(10, 10, 10, 10)
        self.layouts["submit_layout"].setSpacing(5)

        # Initialize category fields
        if len(self.category_fields[self.category]) > 0:
            self.init_fields_layouts()
        else:
            self.init_no_fields_layouts()
            self.browse_image.setEnabled(False)
            self.browse_image.setStyleSheet(".QPushButton {background-color: #F2F2F2;}")

        # Set the main layout as the window's layout
        self.setLayout(self.layouts["main_layout"])

    def init_fields_layouts(self):
        """Arranges the frame's layouts to include category fields"""
        for key in self.labels:
            self.layouts["fields_layout"].addWidget(self.labels[key])
            self.layouts["fields_layout"].addWidget(self.inputs[key])

        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])

    def init_no_fields_layouts(self):
        """Arranges the frame's layouts to not include category fields"""
        self.layouts["fields_layout"].addWidget(self.no_field_message)
        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            if layout == "fields_layout":
                self.layouts["main_layout"].addSpacerItem(QSpacerItem(100, 260))
            elif layout == "header_layout":
                self.layouts["main_layout"].addSpacerItem(QSpacerItem(100, 100))

    def init_widgets(self):
        """
        Populates the form with the correct widgets for the selected category
        """

        # Initialize the header
        self.header = QLabel("Add " + self.category)
        self.header.setStyleSheet(".QLabel{font-size: 24px;}")
        self.header.setFixedHeight(20)
        self.header.setAlignment(Qt.AlignCenter)

        # Initialize the no field message label
        self.no_field_message = QLabel("The " + self.category + " category doesn't have any fields.")
        self.no_field_message.setWordWrap(True)
        self.no_field_message.setStyleSheet(".QLabel{font-size: 14px;}")

        # Initialize the image container
        self.image_container = QLabel("Your image here \n(150px x 150px)")
        self.image_container.setFixedSize(150, 150)
        self.image_container.setAlignment(Qt.AlignCenter)

        # Initialize the browse image button
        self.browse_image = QPushButton("Browse")
        self.browse_image.clicked.connect(self.select_image)
        self.browse_image.setFixedSize(120, 30)

        # Initialize and populate the labels and inputs data structures
        self.labels, self.inputs = {}, {}
        for idx in range(len(self.category_fields[self.category])):
            key = str(idx)
            field_name = self.category_fields[self.category][key][0]
            field_type = self.category_fields[self.category][key][1]
            field_items = self.category_fields[self.category][key][2]

            self.labels[field_name] = QLabel()
            self.labels[field_name].setText(field_name)
            self.labels[field_name].setStyleSheet(".QLabel{font-size: 14px;}")
            self.labels[field_name].setAlignment(Qt.AlignCenter)
            if field_type == "Text":
                self.inputs[field_name] = QLineEdit()
            else:
                self.inputs[field_name] = QComboBox()
                self.inputs[field_name].addItems(field_items)
            self.inputs[field_name].setFixedSize(120, 20)

        # Initialize the submit button
        self.submit = QPushButton("Submit", self)
        self.submit.setFixedSize(100, 40)
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
            }
            .QPushButton:hover {
                background-color: #8CBDAF;
            }
        """)
        self.image_container.setStyleSheet("""
            .QLabel {
                width: 50 px;
                height: 50px;
                background-color: #FFFFFF;
                border: 1px solid #8CBDAF;
            }
        """)
        self.browse_image.setStyleSheet("""
            .QPushButton {
                background-color: #FFFFFF;
                color: #000000;
                margin-left: 25px;
            }
            .QPushButton:hover {
                background-color: #F6F6F6;
            }
        """)

    def select_image(self):
        """Sets the image for the item"""
        image_file = QFileDialog.getOpenFileName(self, "Open Image", "c:\\", "Image Files (*.png *.jpg *.bmp)")
        self.original_image_path = image_file[0]
        if self.original_image_path:
            image = QPixmap(self.original_image_path)
            self.image_width = QPixmap.width(image)
            self.image_height = QPixmap.height(image)

            # Calculate the image's aspect ratio
            width_ratio = 1.0
            height_ratio = 1.0
            if self.image_width > self.image_height:
                width_ratio = self.image_width / self.image_height
            else:
                height_ratio = self.image_height / self.image_width

            # Reduce image dimensions to be less than or equal to 150
            while self.image_width > 150 or self.image_height > 150:
                self.image_width -= width_ratio
                self.image_height -= height_ratio

            # Convert image dimensions back to integers
            self.image_width = int(self.image_width)
            self.image_height = int(self.image_height)

            # Set the scaled dimensions of the icon to fit the container
            image = image.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)

            # Add the image to the container
            self.image_container.setPixmap(image)

    def save_image(self):
        """Copies an image to the program directory and saves the path to the item record"""

        # Create an image object from the original image path
        image = Image.open(self.original_image_path)

        # Resize the image
        image_resized = image.resize((self.image_width, self.image_height), Image.ANTIALIAS)

        # Remove special characters from the item's 'Date Entered' field to make it compatible as a file name
        unformatted_date = self.item["Date Entered"].replace(":", "").replace(".", "").replace("-", "")

        # Add the new image path to the item record
        self.new_image_path = "images/item-images/" + unformatted_date + ".jpg"
        self.item["Image Path"] = self.new_image_path

        # Save the image as a new file at the new image path location
        image_resized.save(self.new_image_path, 'JPEG', quality=90)

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def submit_item(self):
        """Creates a new item and returns focus to the main window"""
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

        self.item["Category"] = self.category
        now = datetime.datetime.now()
        self.item["Date Entered"] = str(now.month) + "." + str(now.day) + "." + str(now.year) + "-" + \
                                        str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

        # Save the image to the program directory
        if self.original_image_path:
            self.save_image()

        # Close the window
        self.hide()
