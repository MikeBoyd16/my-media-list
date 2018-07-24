import sys
import json
import datetime
from manage_categories import *
from manage_fields import *
from select_category import *
from add_item import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.catalog = {}
        self.category_names = []
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

        self.center_layout.addWidget(self.catalog_items)

        self.right_layout.addWidget(self.item_details)

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

        self.buttons = {"import_catalog": QPushButton(), "export_catalog": QPushButton(), "save_catalog": QPushButton(),
                        "categories": QPushButton(), "fields": QPushButton(), "search_catalog": QPushButton(),
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

        self.catalog_items = QListWidget(self)
        self.catalog_items.setIconSize(QSize(30, 30))
        self.catalog_items.itemClicked.connect(self.show_item_details)

        self.item_details = QTextEdit(self)
        self.item_details.setReadOnly(True)

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
        self.catalog_items.setStyleSheet("""
            .QListWidget {
                background-color: #d8eeea;
                color: #6d6d6d;
                font-weight:bold;
                font-size: 13px;
                border: none;
                outline: 0; /* Removes the dotted outline around selected catalog items */
            }
            .QListWidget::Item:hover{
                background-color: #C5D7D3;
            }
            .QListWidget::Item:selected {
                background-color: #C5D7D3;
            }
        """)
        self.item_details.setStyleSheet("""
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
        self.catalog_items.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.item_details.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def import_catalog(self):
        """Opens a json file and loads catalog data into the program"""
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        if file_name[0]:
            self.current_file = file_name[0]
            file = open(file_name[0], "r")
            self.catalog = json.load(file)
            self.update_catalog()

    def export_catalog(self):
        """Creates a new, or overwrites an existing, json file with the content of the current catalog"""
        file_name = QFileDialog.getSaveFileName(self, "Save File")
        if file_name[0]:
            file = open(file_name[0], "w")
            json.dump(self.catalog, file)

    def save_catalog(self):
        """Saves changes from the current session to the file the catalog was imported from"""
        if self.current_file:
            file = open(self.current_file, "w")
            json.dump(self.catalog, file)

    def search_catalog(self):
        pass

    def update_catalog(self):
        """Updates the catalog with the current set of items"""
        self.catalog_items.clear()
        for key, data in reversed(list(self.catalog.items())):
            catalog_item = QListWidgetItem(data["Title"])
            catalog_item.setData(Qt.UserRole, data)
            catalog_item.setSizeHint(QSize(35, 35))

            # Set the 'selected' and 'unselected' versions of each list item icon
            catalog_item_icon = QIcon()
            catalog_item_icon.addPixmap(QPixmap("images/list-item-icons/" + str(data["Media"]) + " Selected.png"), QIcon.Normal)
            catalog_item_icon.addPixmap(QPixmap("images/list-item-icons/" + str(data["Media"]) + ".png"), QIcon.Selected)
            catalog_item.setIcon(catalog_item_icon)

            self.catalog_items.addItem(catalog_item)

    def add_item(self):
        """Adds a new catalog item to the catalog"""
        select_category_window = SelectCategory()
        select_category_window.show()
        select_category_window.exec_()
        if "Title" in select_category_window.temp_input:  # Fields for key won't exist if the dialog is closed prematurely
            self.catalog[select_category_window.temp_input["Title"] + "-" +
                         select_category_window.temp_input["Media"] + "-" +
                         select_category_window.temp_input["Date Entered"]] = select_category_window.temp_input
            self.update_catalog()

    def categories(self):
        manage_categories = ManageCategories(self.category_names)
        manage_categories.show()
        manage_categories.exec_()
        self.category_names = manage_categories.category_names

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

    def show_item_details(self):
        """Displays the currently selected catalog item's details"""
        self.item_details.clear()
        item = self.catalog_items.currentItem()
        item_data = item.data(Qt.UserRole)
        item_key = item_data["Title"] + "-" + item_data["Media"] + "-" + item_data["Date Entered"]
        for label in self.catalog[item_key]:
            if label not in ["Status", "Media", "Date Entered"]:  # Do not display certain labels and data
                if self.catalog[item_key][label]:  # Only display a label if there is data associated with it
                    # If a label's associated data is in a list, display a comma separated string of that data
                    if isinstance(self.catalog[item_key][label], list):
                        self.item_details.append(label + ": " + ", ".join(self.catalog[item_key][label]) + "\n")
                    else:
                        self.item_details.append(label + ": " + str(self.catalog[item_key][label]) + "\n")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
