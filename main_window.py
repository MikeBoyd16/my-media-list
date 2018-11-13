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
        self.catalog = {"Profile": {"Category Names": {}, "Category Fields": {}, "Icon Paths": {}}, "Data": {}}
        self.current_file = ""
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()
        self.load_last_catalog()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setGeometry(100, 100, 625, 650)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        self.layouts = {"main_layout": QHBoxLayout(self.central_widget),
                        "logo_layout": QGridLayout(self.central_widget),
                        "left_layout": QVBoxLayout(self.central_widget),
                        "center_layout": QVBoxLayout(self.central_widget),
                        "right_layout": QVBoxLayout(self.central_widget)}

        self.layouts["logo_layout"].addWidget(self.logo, 0, 0)
        self.layouts["logo_layout"].addWidget(self.header, 1, 0)
        self.layouts["left_layout"].addLayout(self.layouts["logo_layout"])

        for button in self.buttons:
            self.layouts["left_layout"].addWidget(self.buttons[button])

        self.layouts["center_layout"].addWidget(self.catalog_items)

        self.layouts["right_layout"].addWidget(self.item_details)

        for layout in self.layouts:
            if layout != "main_layout":
                self.layouts["main_layout"].addLayout(self.layouts[layout])
            self.layouts[layout].setContentsMargins(0, 0, 0, 0)
            self.layouts[layout].setSpacing(0)

        self.setLayout(self.layouts["main_layout"])

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("images/omnilog_logo.png"))
        self.logo.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.header = QLabel(self)
        self.header.setText("OmniLog")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedSize(130, 50)

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

        # Disable the "Search Catalog" and "Edit Item" buttons for the current release
        self.buttons["search_catalog"].setEnabled(False)
        self.buttons["edit_item"].setEnabled(False)

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
        self.logo.setStyleSheet("""
            .QLabel {
                background-color: #f3ffbd;
            }
        """)
        self.header.setStyleSheet("""
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
                color: #FFFFFF;
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

        # Gray out the disabled buttons
        self.buttons["search_catalog"].setStyleSheet(""".QPushButton {background-color: #84888E;}""")
        self.buttons["edit_item"].setStyleSheet(""".QPushButton {background-color: #84888E;}""")

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
            self.current_file = file_name[0]

    def save_catalog(self):
        """Saves changes from the current session to the file the catalog was imported from"""
        if self.current_file:
            file = open(self.current_file, "w")
            json.dump(self.catalog, file)

            confirm_save = QMessageBox()
            confirm_save.setText("Your changes have been saved successfully.")
            confirm_save.exec_()
        else:
            self.export_catalog()

    def search_catalog(self):
        pass

    def update_catalog(self):
        """Updates the catalog with the current set of items"""
        self.catalog_items.clear()
        for key, data in reversed(list(self.catalog["Data"].items())):
            field_category = data["Category"]
            field_id = self.catalog["Profile"]["Category Fields"][field_category]["0"][0]
            catalog_item = QListWidgetItem(data[field_id])
            catalog_item.setData(Qt.UserRole, data)
            catalog_item.setSizeHint(QSize(35, 35))

            # Find the icon address for the item's category
            icon_address = ""
            for key, value in self.catalog["Profile"]["Category Names"].items():
                if value == field_category:
                    icon_address = self.catalog["Profile"]["Icon Paths"][key]

            # Add the icon to the item
            catalog_item_icon = QIcon()
            catalog_item_icon.addPixmap(QPixmap(icon_address), QIcon.Normal)
            catalog_item.setIcon(catalog_item_icon)

            # Add the item to the list of catalog items
            self.catalog_items.addItem(catalog_item)

            # Display the top item in the list of catalog items by default
            self.catalog_items.setCurrentRow(0)
            self.show_item_details()

    def add_item(self):
        """Adds a new catalog item to the catalog"""
        select_category = SelectCategory(self.catalog["Profile"]["Category Names"])
        select_category.show()
        select_category.exec_()

        if select_category.get_category() != "No categories created":
            add_item = AddItem(select_category.get_category(), self.catalog["Profile"]["Category Fields"])
            add_item.exec_()
            if "0" in self.catalog["Profile"]["Category Fields"][add_item.category]:
                self.catalog["Data"][add_item.item["Date Entered"]] = add_item.item
                self.update_catalog()

    def categories(self):
        """Creates and displays a ManageCategories frame with any existing profile data"""
        manage_categories = ManageCategories(self.catalog["Profile"]["Category Names"],
                                             self.catalog["Profile"]["Icon Paths"])
        manage_categories.show()
        manage_categories.exec_()
        self.catalog["Profile"]["Category Names"] = manage_categories.category_names
        self.catalog["Profile"]["Icon Paths"] = manage_categories.category_icon_paths

        # If a category doesn't yet exist in the Category Fields section, initialize it
        for row, category in self.catalog["Profile"]["Category Names"].items():
            if category not in self.catalog["Profile"]["Category Fields"]:
                self.catalog["Profile"]["Category Fields"][category] = {}

    def fields(self):
        """Creates and displays a ManageFields frame with any existing profile data"""
        select_category = SelectCategory(self.catalog["Profile"]["Category Names"])
        select_category.show()
        select_category.exec_()

        if select_category.get_category() != "No categories created":
            manage_fields = ManageFields(select_category.get_category(), self.catalog["Profile"]["Category Fields"])
            manage_fields.show()
            manage_fields.exec_()
            self.catalog["Profile"]["Category Fields"] = manage_fields.category_fields

    def remove_item(self):
        """Removes the selected item from the catalog"""
        confirm_remove = QMessageBox.question(self, "Remove Item",
                                              "Remove this item from the catalog?",
                                              QMessageBox.Yes, QMessageBox.No)
        if confirm_remove == QMessageBox.Yes:
            item = self.catalog_items.currentItem()
            item_data = item.data(Qt.UserRole)
            item_key = item_data["Date Entered"]
            del self.catalog["Data"][item_key]
            self.item_details.clear()
            self.update_catalog()

    def edit_item(self):
        pass

    def load_last_catalog(self):
        """Loads the address of the last used catalog into the program"""
        file = open("last_used_catalog.txt", "r")
        self.current_file = file.read()
        file.close()

        file = open(self.current_file, "r")
        self.catalog = json.load(file)
        file.close()

        self.update_catalog()


    def store_last_catalog(self):
        """Stores the address of the last used catalog into a text file"""
        file = open("last_used_catalog.txt", "w")
        file.write(self.current_file)
        file.close()

    def quit_program(self):
        """Prompts the user for confirmation that they want to quit the program"""
        confirm_exit = QMessageBox.question(self, "Confirm exit", "Are you sure you want to quit?",
                                            QMessageBox.Yes, QMessageBox.No)
        if confirm_exit == QMessageBox.Yes:
            self.store_last_catalog()
            sys.exit()

    def show_item_details(self):
        """Displays the currently selected catalog item's details"""
        self.item_details.clear()
        item = self.catalog_items.currentItem()
        item_data = item.data(Qt.UserRole)
        item_key = item_data["Date Entered"]
        for label in self.catalog["Data"][item_key]:
            if label not in ["Category", "Date Entered", "Image Path"]:  # Do not display certain labels and data
                if self.catalog["Data"][item_key][label]:  # Only display a label if there is data associated with it
                    # If a label's associated data is in a list, display a comma separated string of that data
                    if isinstance(self.catalog["Data"][item_key][label], list):
                        self.item_details.append(label + ": " + ", ".join(self.catalog["Data"][item_key][label]) + "\n")
                    else:
                        self.item_details.append(label + ": " + str(self.catalog["Data"][item_key][label]) + "\n")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
