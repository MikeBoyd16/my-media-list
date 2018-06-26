import sys
import json
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint) # Removes the outer frame from main window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.my_media_list = {}

        self.title = "MyMediaList"
        self.left, self.top, self.width, self.height = 100, 100, 500, 600

        self.media_list_area = QListWidget(self)
        self.media_details_area = QTextEdit(self)

        self.init_window()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""

        # Initialize the menu and its actions
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        edit_menu = main_menu.addMenu("Edit")
        open_file = QAction(QIcon("images/import_list.png"), "Import List", self)
        open_file.triggered.connect(self.open_file)
        file_menu.addAction(open_file)
        save_file = QAction(QIcon("images/export_list.png"), "Export List", self)
        save_file.triggered.connect(self.save_file)
        file_menu.addAction(save_file)
        add_media = QAction(QIcon("images/add_media.png"),"Add Media", self)
        add_media.triggered.connect(self.add_media_record)
        edit_menu.addAction(add_media)
        remove_media = QAction(QIcon("images/remove_media.png"), "Remove Media", self)
        edit_menu.addAction(remove_media)
        edit_media = QAction(QIcon("images/edit_media.png"), "Edit Media", self)
        edit_menu.addAction(edit_media)

        # Set the window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Connect the selection of a list item with its associated data
        self.media_list_area.itemClicked.connect(self.show_media_record)
        self.media_details_area.isReadOnly()

        # Initialize window layout and styles and center it on the screen
        self.init_layout()
        self.init_styles()
        self.center_window()

    def init_layout(self):
        """Initializes the layout for the widgets in the window"""
        box_layout = QHBoxLayout(self.central_widget)
        box_layout.addWidget(self.media_list_area)
        box_layout.addWidget(self.media_details_area)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(0)
        self.setLayout(box_layout)

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        self.media_list_area.setStyleSheet("""
                        .QListWidget {
                            background-color: #1f2041;
                            color: #e9d2c0;
                            font-weight:bold;
                            font-size: 13px;
                            }
                        .QListWidget:item:selected:active {
                            background-color: #e9d2c0;
                            color: #1f2041;
                            }
                        """)
        self.media_details_area.setStyleSheet("""
                        .QTextEdit {
                            background-color: #e9d2c0;
                            color: #1f2041;
                            font-weight:bold;
                            font-size: 13px;
                            }
                        """)

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def update_list(self):
        """Updates the list area widget with the current set of list items"""

        # Clear the current set of list items from the list area
        self.media_list_area.clear()

        # Create list items for each record in the media list
        for key, data in self.my_media_list.items():
            list_item = QListWidgetItem(data["Title"])
            list_item.setData(Qt.UserRole, data)
            list_item.setSizeHint(QSize(35, 35))

            # Set the 'selected' and 'unselected' versions of each list item icon
            list_item_icon = QIcon()
            list_item_icon.addPixmap(QPixmap("images/" + str(data["Media"]) + ".png"), QIcon.Normal)
            list_item_icon.addPixmap(QPixmap("images/" + str(data["Media"]) + " Selected.png"), QIcon.Selected)
            list_item.setIcon(list_item_icon)

            # Add the list item to the list area
            self.media_list_area.addItem(list_item)

        # Set the icon size of all list item icons in the list area
        self.media_list_area.setIconSize(QSize(30, 30))

    def open_file(self):
        """Opens a json file and loads file data into the list area"""
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        if file_name[0]:
            file = open(file_name[0], "r")
            self.my_media_list = json.load(file)
            self.update_list()

    def save_file(self):
        """Creates a new, or overwrites an existing, json file with the content in the list area"""
        file_name = QFileDialog.getSaveFileName(self, "Save File")
        if file_name[0]:
            file = open(file_name[0], "w")
            json.dump(self.my_media_list, file)

    def add_media_record(self):
        """Adds a new media record to the media list"""
        select_media = SelectMedia()
        select_media.show()
        select_media.exec_()
        if "Title" in select_media.temp_input:  # Title as a key won't exist if the dialog is closed prematurely
            self.my_media_list[select_media.temp_input["Title"] + "-" + select_media.temp_input["Media"] + "-" +
                               select_media.temp_input["Date Entered"]] = select_media.temp_input
            self.update_list()

    def show_media_record(self):
        """Displays the currently selected list item's media record"""
        self.media_details_area.clear()
        item = self.media_list_area.currentItem()
        item_data = item.data(Qt.UserRole)
        item_key = item_data["Title"] + "-" + item_data["Media"] + "-" + item_data["Date Entered"]
        for label in self.my_media_list[item_key]:
            self.media_details_area.append(label + ": " + str(self.my_media_list[item_key][label]) + "\n")


class SelectMedia(QDialog):
    def __init__(self):
        super().__init__()
        self.temp_input = {}

        self.title = "Media Select"
        self.left, self.top, self.width, self.height = 100, 100, 200, 200

        self.select_media_combo = QComboBox(self)
        self.ok = QPushButton("OK", self)

        self.init_window()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""

        # Set the window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Move the OK button to the correct position
        self.ok.move(50, 50)

        # Display an AddMedia dialog form when OK is clicked
        self.ok.clicked.connect(self.go_to_add_media)

        # Load the SelectMedia combo box with all supported media types
        self.select_media_combo.addItems(["Music", "Audiobook", "Movie", "TV", "Anime", "Book", "Manga", "Video Game"])

        # Initialize window layout and styles and center it on the screen
        self.init_layout()
        self.init_styles()
        self.center_window()

    def init_layout(self):
        """Initializes the layout for the widgets in the window"""
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.select_media_combo, 0, 0)
        grid_layout.addWidget(self.ok, 1, 0)
        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)
        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(group_box)
        self.setLayout(v_box_layout)

    def init_styles(self):
        """Sets all stylesheet properties"""
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def get_media_selection(self):
        """Returns the currently selected media type"""
        return self.select_media_combo.currentText()

    def go_to_add_media(self):
        """Displays a new AddMedia dialog form and places the resulting input in a temporary dictionary variable"""
        add_media_record = AddMedia(self.get_media_selection())
        add_media_record.exec_()
        self.temp_input = add_media_record.temp_input
        self.temp_input["Media"] = self.select_media_combo.currentText()
        now = datetime.datetime.now()
        self.temp_input["Date Entered"] = str(now.month) + "." + str(now.day) + "." + str(now.year)
        self.hide()


class AddMedia(QDialog):
    music_widgets = \
        {
            "Type": "combo",
            "Rating": "combo",
            "Title": "line",
            "Main Artist": "line",
            "Featured Artist": "line",
            "Album": "line",
            "Year": "line",
            "Duration": "line",
            "Genres": "line",
            "Record Label": "line",
            "Songwriters": "line",
            "Producers": "line",
        }
    audiobook_widgets = \
        {
            "Title": "line",
            "Series": "line",
            "Authors": "line",
            "Narrators": "line",
            "Year": "line",
            "Genres": "line",
            "Listening Length": "line",
            "Score": "combo",
            "Tags": "line"
        }
    movie_widgets = \
        {
            "Title": "line",
            "Year": "line",
            "Duration": "line",
            "MPAA": "combo",
            "Genres": "line",
            "Actors": "line",
            "Directors": "line",
            "Writers": "line",
            "Producers": "line",
            "Quality Score": "combo",
            "Compatibility Score": "combo",
            "Tags": "line",
            "Comments": "line"
        }
    tv_widgets = \
        {
            "Title": "line",
            "Year": "line",
            "Season": "line",
            "Episode": "line",
            "Duration": "line",
            "Content Rating": "combo",
            "Genres": "line",
            "Actors": "line",
            "Creators": "line",
            "Writers": "line",
            "Producers": "line",
            "Quality Score": "combo",
            "Compatibility Score": "combo",
            "Tags": "line",
            "Comments": "line"
        }
    anime_widgets = \
        {
            "Title": "line",
            "Year": "line",
            "Type": "combo",
            "Episode": "line",
            "Duration": "line",
            "Content Rating": "combo",
            "Source": "combo",
            "Genres": "line",
            "Studio": "line",
            "Producers": "line",
            "Quality Score": "combo",
            "Compatibility Score": "combo",
            "Tags": "line",
            "Comments": "line"
        }
    book_widgets = \
        {
            "Title": "line",
            "Series": "line",
            "Authors": "line",
            "Year": "line",
            "Genres": "line",
            "Pages": "line",
            "Score": "combo",
            "Tags": "line",
            "Comments": "line"
        }
    manga_widgets = \
        {
            "Title": "line",
            "Volume": "line",
            "Genres": "line",
            "Writers": "line",
            "Illustrators": "line",
            "Publishers": "line",
            "Demographic": "combo",
            "Score": "combo",
            "Tags": "line"
        }
    video_game_widgets = \
        {
            "Title": "line",
            "Platform": "combo",
            "Year": "line",
            "Genres": "line",
            "Developers": "line",
            "Publishers": "line",
            "Hours Played": "line",
            "Campaign Finished?": "combo",
            "Achievement Progress": "line",
            "Quality Score": "combo",
            "Compatibility Score": "combo",
            "Tags": "line",
            "Comments": "line"
        }

    def __init__(self, media_type):
        super().__init__()
        self.media_type = media_type
        self.temp_input = {}
        self.labels = {}
        self.inputs = {}

        self.title = "Add Music"
        self.left, self.top, self.width, self.height = 100, 100, 250, 600

        self.init_widgets()
        self.submit = QPushButton("Submit", self)

        self.init_window()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""

        # Set the window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set the height for the Submit button
        self.submit.setFixedHeight(40)

        # Connect a new media record submission with the Submit button
        self.submit.clicked.connect(self.submit_media)

        # Initialize window layout and styles and center it on the screen
        self.init_layout()
        self.init_styles()
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
        Populates the form with the correct widgets for the selected media type
        """
        # Set the form's widget template to the template for the selected media type
        widgets = {}
        if self.media_type == "Music":
            widgets = AddMedia.music_widgets
        elif self.media_type == "Audiobook":
            widgets = AddMedia.audiobook_widgets
        elif self.media_type == "Movie":
            widgets = AddMedia.movie_widgets
        elif self.media_type == "TV":
            widgets = AddMedia.tv_widgets
        elif self.media_type == "Anime":
            widgets = AddMedia.anime_widgets
        elif self.media_type == "Book":
            widgets = AddMedia.book_widgets
        elif self.media_type == "Manga":
            widgets = AddMedia.manga_widgets
        elif self.media_type == "Video Game":
            widgets = AddMedia.video_game_widgets

        # Populate the form with widgets based on the selected template
        for key, value in widgets.items():
            self.labels[key] = QLabel()
            self.labels[key].setText(key)
            if value == "line":
                self.inputs[key] = QLineEdit()
            elif value == "combo":
                self.inputs[key] = QComboBox()

        # Fill the combo boxes with the correct items based on the selected media type
        if self.media_type == "Music":
            self.inputs["Type"].addItems(["Single", "Remix", "Studio Album", "Extended Play",
                                          "Reissue", "Live Album", "Remix Album"])
            self.inputs["Rating"].addItems(["Bad", "Fine", "Good", "Great"])
        elif self.media_type == "Audiobook":
            self.inputs["Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        elif self.media_type == "Movie":
            self.inputs["MPAA"].addItems(["G", "PG", "PG-13", "R", "NC-17"])
            self.inputs["Quality Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            self.inputs["Compatibility Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        elif self.media_type == "TV":
            self.inputs["Content Rating"].addItems(["TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA"])
            self.inputs["Quality Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            self.inputs["Compatibility Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        elif self.media_type == "Anime":
            self.inputs["Type"].addItems(["TV", "Movie", "OVA", "Special"])
            self.inputs["Content Rating"].addItems(["G", "PG", "PG-13", "R", "NC-17"])
            self.inputs["Source"].addItems(["Original", "Manga", "4-koma Manga", "Visual Novel", "Light Novel",
                                            "Novel", "Video Game", "Card Game"])
            self.inputs["Quality Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            self.inputs["Compatibility Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        elif self.media_type == "Book":
            self.inputs["Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        elif self.media_type == "Manga":
            self.inputs["Demographic"].addItems(["Kodomo", "Shonen", "Shoujo", "Josei", "Seinen", "Seijin",
                                                 "Mina", "4-koma"])
            self.inputs["Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        elif self.media_type == "Video Game":
            self.inputs["Platform"].addItems(["PC", "3DS", "DS", "GBA"])
            self.inputs["Campaign Finished?"].addItems(["Yes", "No"])
            self.inputs["Quality Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            self.inputs["Compatibility Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

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

    def submit_media(self):
        """Places the inputs from the input widgets into a temporary dictionary variable"""
        for key in self.inputs:
            if isinstance(self.inputs[key], QComboBox):
                self.temp_input[key] = self.inputs[key].currentText()
            else:
                if "," in self.inputs[key].text():  # If there are multiple inputs for one category, split them
                    input_list = self.inputs[key].text()
                    input_list = input_list.split(",")
                    self.temp_input[key] = input_list
                else:
                    self.temp_input[key] = self.inputs[key].text()
        self.hide()


def main():
    app = QApplication(sys.argv)
    my_list_window = MyListWindow()
    my_list_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
