import sys
import json
import datetime
from manage_categories import *
from manage_fields import *
from select_media import *
from add_media import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.my_media_list = {}
        self.current_file = ""
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setGeometry(100, 100, 625, 650)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Removes the outer frame from the window
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        self.main_layout = QHBoxLayout(self.central_widget)
        self.logo_layout = QGridLayout(self.central_widget)
        self.left_layout = QVBoxLayout(self.central_widget)
        self.center_layout = QVBoxLayout(self.central_widget)
        self.right_layout = QVBoxLayout(self.central_widget)

        self.logo_layout.addWidget(self.header_logo, 0, 0)
        self.logo_layout.addWidget(self.header_title, 1, 0)
        self.left_layout.addLayout(self.logo_layout)

        for button in self.buttons:
            self.left_layout.addWidget(self.buttons[button])

        self.center_layout.addWidget(self.media_list_area)

        self.right_layout.addWidget(self.media_details_area)

        # Remove margins and spacing from each layout
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.center_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.header_logo = QLabel(self)
        self.header_logo.setPixmap(QPixmap("images/omnilog_logo.png"))
        self.header_logo.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.header_title = QLabel(self)
        self.header_title.setText("OmniLog")
        self.header_title.setAlignment(Qt.AlignCenter)
        self.header_title.setFixedSize(130, 50)

        self.buttons = {"import_list": QPushButton(), "export_list": QPushButton(), "save_list": QPushButton(),
                        "categories": QPushButton(), "fields": QPushButton(), "search_list": QPushButton(),
                        "add_item": QPushButton(), "remove_item": QPushButton(), "edit_item": QPushButton(),
                        "quit_program": QPushButton()}
        for button in self.buttons:
            button_text = button.replace("_", " ").title().rsplit(' ', 1)[0]
            self.buttons[button].setText("  " + button_text)
            self.buttons[button].setIcon(QIcon("images/button-icons/" + button + ".png"))
            self.buttons[button].setIconSize(QSize(30, 30))
            self.buttons[button].setFixedSize(QSize(130, 52))
        for button in self.buttons:
            button_method = getattr(self, button)
            self.buttons[button].clicked.connect(button_method)

        self.media_list_area = QListWidget(self)
        self.media_list_area.setIconSize(QSize(30, 30))
        self.media_list_area.itemClicked.connect(self.show_media_record)

        self.media_details_area = QTextEdit(self)
        self.media_details_area.setReadOnly(True)

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        self.central_widget.setStyleSheet("""
            .QPushButton {
                background-color: #247ba0;
                border: 1px solid #8CBDAF;
                font-weight: bold;
                font-size: 12px;
                color: #f3ffbd;
                text-align: left;
                padding-left: 10px;
            }
            .QPushButton:hover {
                background-color: #8CBDAF;
            }
        """)
        self.header_logo.setStyleSheet("""
            .QLabel {
                background-color: #f3ffbd;
            }
        """)
        self.header_title.setStyleSheet("""
            .QLabel {
                background-color: #f3ffbd;
                color: #247ba0;
                font-weight:bold;
                font-size: 26px;
            }
        """)
        self.media_list_area.setStyleSheet("""
            .QListWidget {
                background-color: #d8eeea;
                color: #6d6d6d;
                font-weight:bold;
                font-size: 13px;
                border: none;
                outline: 0; /* Removes the dotted outline around selected list items */
            }
            .QListWidget::Item:hover{
                background-color: #C5D7D3;
            }
            .QListWidget::Item:selected {
                background-color: #C5D7D3;
            }
        """)
        self.media_details_area.setStyleSheet("""
            .QTextEdit {
                background-color: #247ba0;
                color: #f3ffbd;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
        """)
        scrollbar_stylesheet = ("""
            .QScrollBar:vertical {
                border: 1px solid #6d6d6d;
                background: white;
                width: 5px;
                margin: 0px 0px 0px 0px;
            }
            .QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 #6d6d6d, stop: 0.5 #6d6d6d, stop:1 #6d6d6d);
                min-height: 0px;
            }
            .QScrollBar::add-line:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 #6d6d6d, stop: 0.5 #6d6d6d,  stop:1 #6d6d6d);
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            .QScrollBar::sub-line:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0  #6d6d6d, stop: 0.5 #6d6d6d,  stop:1 #6d6d6d);
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        self.media_list_area.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.media_details_area.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def import_list(self):
        """Opens a json file and loads file data into the list area"""
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        if file_name[0]:
            self.current_file = file_name[0]
            file = open(file_name[0], "r")
            self.my_media_list = json.load(file)
            self.update_list()

    def export_list(self):
        """Creates a new, or overwrites an existing, json file with the content in the list area"""
        file_name = QFileDialog.getSaveFileName(self, "Save File")
        if file_name[0]:
            file = open(file_name[0], "w")
            json.dump(self.my_media_list, file)

    def save_list(self):
        """Saves changes from the current session to the file the list was imported from"""
        if self.current_file:
            file = open(self.current_file, "w")
            json.dump(self.my_media_list, file)

    def search_list(self):
        pass

    def update_list(self):
        """Updates the list area with the current set of list items"""
        self.media_list_area.clear()  # Clear the current set of list items from the list area
        for key, data in reversed(list(self.my_media_list.items())):
            list_item = QListWidgetItem(data["Title"])
            list_item.setData(Qt.UserRole, data)
            list_item.setSizeHint(QSize(35, 35))

            # Set the 'selected' and 'unselected' versions of each list item icon
            list_item_icon = QIcon()
            list_item_icon.addPixmap(QPixmap("images/list-item-icons/" + str(data["Media"]) + " Selected.png"), QIcon.Normal)
            list_item_icon.addPixmap(QPixmap("images/list-item-icons/" + str(data["Media"]) + ".png"), QIcon.Selected)
            list_item.setIcon(list_item_icon)

            self.media_list_area.addItem(list_item)

    def add_item(self):
        """Adds a new media record to the media list"""
        select_media = SelectMedia()
        select_media.show()
        select_media.exec_()
        if "Title" in select_media.temp_input:  # Title as a key won't exist if the dialog is closed prematurely
            self.my_media_list[select_media.temp_input["Title"] + "-" + select_media.temp_input["Media"] + "-" +
                               select_media.temp_input["Date Entered"]] = select_media.temp_input
            self.update_list()

    def categories(self):
        manage_categories = ManageCategories()
        manage_categories.show()
        manage_categories.exec_()

    def fields(self):
        manage_fields = ManageFields()
        manage_fields.show()
        manage_fields.exec_()

    def remove_item(self):
        pass

    def edit_item(self):
        pass

    def quit_program(self):
        sys.exit()

    def show_media_record(self):
        """Displays the currently selected list item's media record"""
        self.media_details_area.clear()
        item = self.media_list_area.currentItem()
        item_data = item.data(Qt.UserRole)
        item_key = item_data["Title"] + "-" + item_data["Media"] + "-" + item_data["Date Entered"]
        for label in self.my_media_list[item_key]:
            if label not in ["Status", "Media", "Date Entered"]:  # Do not display certain labels and data
                if self.my_media_list[item_key][label]:  # Only display a label if there is data associated with it
                    # If a label's associated data is in a list, display a comma separated string of that data
                    if isinstance(self.my_media_list[item_key][label], list):
                        self.media_details_area.append(label + ": " + ", ".join(self.my_media_list[item_key][label]) + "\n")
                    else:
                        self.media_details_area.append(label + ": " + str(self.my_media_list[item_key][label]) + "\n")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
