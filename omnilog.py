import sys
import json
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.my_media_list = {}
        self.current_file = ""

        self.init_widgets()
        self.init_window()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setGeometry(100, 100, 625, 600)
        self.setWindowFlags(Qt.FramelessWindowHint) # Removes the outer frame from the window

        for button in self.buttons:
            button_method = getattr(self, button)
            self.buttons[button].clicked.connect(button_method)
        self.media_list_area.itemClicked.connect(self.show_media_record)

        self.init_layout()
        self.init_styles()
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        self.main_layout = QHBoxLayout(self.central_widget)
        self.left_layout = QVBoxLayout(self.central_widget)
        self.center_layout = QVBoxLayout(self.central_widget)
        self.right_layout = QVBoxLayout(self.central_widget)

        self.left_layout.addWidget(self.header)
        for button in self.buttons:
            self.left_layout.addWidget(self.buttons[button])

        self.center_layout.addWidget(self.media_list_area)

        self.right_layout.addWidget(self.media_details_area)

        # Remove margins and spacing from each layout
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
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
        self.header = QLabel(self)
        self.header.setText("OmniLog")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedSize(130, 125)

        self.buttons = {"import_list": QPushButton(), "export_list": QPushButton(), "save_list": QPushButton(),
                        "profile_management": QPushButton(), "search_list": QPushButton(), "add_item": QPushButton(),
                        "remove_item": QPushButton(), "edit_item": QPushButton(), "quit_program": QPushButton()}

        for button in self.buttons:
            button_text = button.replace("_", " ").title().rsplit(' ', 1)[0]
            self.buttons[button].setText("    " + button_text)
            self.buttons[button].setIcon(QIcon("images/button-icons/" + button + ".png"))
            self.buttons[button].setIconSize(QSize(30, 30))
            self.buttons[button].setFixedSize(QSize(130, 60))

        self.media_list_area = QListWidget(self)
        self.media_list_area.setIconSize(QSize(30, 30))

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
        self.header.setStyleSheet("""
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

    def profile_management(self):
        pass

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


class SelectMedia(QDialog):
    def __init__(self):
        super().__init__()

        self.temp_input = {}

        self.init_widgets()
        self.init_window()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""
        self.setWindowTitle("Media Select")
        self.setGeometry(100, 100, 200, 200)

        # Move the OK button to the correct position
        self.ok.move(50, 50)

        # Display an AddMedia form when OK is clicked
        self.ok.clicked.connect(self.go_to_add_media)

        self.init_layout()
        self.init_styles()
        self.center_window()

    def init_layout(self):
        """Initializes the layout for widgets in the window"""
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.select_media_combo, 0, 0)
        grid_layout.addWidget(self.ok, 1, 0)
        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)
        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(group_box)
        self.setLayout(v_box_layout)

    def init_widgets(self):
        """Initializes widgets and their properties"""
        self.select_media_combo = QComboBox(self)
        self.select_media_combo.addItems(["Music", "Audiobook", "Movie", "TV", "Anime", "Book", "Manga", "Video Game"])
        self.ok = QPushButton("OK", self)

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
        """Displays a new AddMedia form and places the resulting
        input in a temporary dictionary variable"""
        add_media_record = AddMedia(self.get_media_selection())
        add_media_record.exec_()
        self.temp_input = add_media_record.temp_input
        self.temp_input["Media"] = self.select_media_combo.currentText()
        now = datetime.datetime.now()
        self.temp_input["Date Entered"] = str(now.month) + "." + str(now.day) + "." + str(now.year) + ":" + \
                                          str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        self.hide()


class AddMedia(QDialog):
    music_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Type": "combo",
            "Source Type": "combo",
            "Source Name": "line",
            "Duration": "line",
            "Main Artist": "line",
            "Featured Artists": "line",
            "Record Label": "line",
            "Songwriters": "line",
            "Producers": "line",
            "Release Date": "line",
            "Genres": "line"
        }
    audiobook_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Series": "line",
            "Listening Length": "line",
            "Authors": "line",
            "Narrators": "line",
            "Release Date": "line",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }
    movie_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Duration": "line",
            "Actors": "line",
            "Directors": "line",
            "Writers": "line",
            "Producers": "line",
            "Release Date": "line",
            "MPAA": "combo",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }
    tv_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Season": "line",
            "Episode": "line",
            "Duration": "line",
            "Actors": "line",
            "Creators": "line",
            "Writers": "line",
            "Producers": "line",
            "Release Date": "line",
            "Content Rating": "combo",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }
    anime_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Type": "combo",
            "Source": "combo",
            "Episode": "line",
            "Duration": "line",
            "Studio": "line",
            "Producers": "line",
            "Release Date": "line",
            "Content Rating": "combo",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }
    book_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Series": "line",
            "Pages": "line",
            "Authors": "line",
            "Release Date": "line",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }
    manga_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Volume": "line",
            "Writers": "line",
            "Illustrators": "line",
            "Publishers": "line",
            "Demographic": "combo",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }
    video_game_widgets = \
        {
            "Title": "line",
            "Score": "combo",
            "Platform": "combo",
            "Hours Played": "line",
            "Campaign Finished?": "combo",
            "Achievement Progress": "combo",
            "Developers": "line",
            "Publishers": "line",
            "Release Date": "line",
            "Genres": "line",
            "Tags": "line",
            "Comments": "line"
        }

    def __init__(self, media_type):
        super().__init__()
        self.media_type = media_type
        self.temp_input = {}
        self.labels = {}
        self.inputs = {}

        self.init_widgets()
        self.init_window()

    def init_window(self):
        """Initialize the window, its dimensions, and content"""
        self.setWindowTitle("Add Music")
        self.setGeometry(100, 100, 250, 600)

        # Connect a new media record submission with the Submit button
        self.submit.clicked.connect(self.submit_media)

        # Check source type every time the selection changes
        if self.media_type == "Music":
            self.inputs["Type"].currentIndexChanged.connect(self.source_name_status)
            self.inputs["Source Type"].currentIndexChanged.connect(self.source_name_status)

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
            self.inputs["Type"].addItems(["Song", "Remix", "Album"])
            self.inputs["Source Type"].addItems(["Single", "LP", "EP", "Studio Album",
                                                 "Live Album", "Remix Album", "Reissue"])
            self.inputs["Source Name"].setDisabled(True)
        elif self.media_type == "Movie":
            self.inputs["MPAA"].addItems(["G", "PG", "PG-13", "R", "NC-17"])
        elif self.media_type == "TV":
            self.inputs["Content Rating"].addItems(["TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA"])
        elif self.media_type == "Anime":
            self.inputs["Type"].addItems(["TV", "Movie", "OVA", "Special"])
            self.inputs["Content Rating"].addItems(["G", "PG", "PG-13", "R", "NC-17"])
            self.inputs["Source"].addItems(["Original", "Manga", "4-koma", "Visual Novel", "Light Novel",
                                            "Novel", "Video Game", "Card Game"])
        elif self.media_type == "Manga":
            self.inputs["Demographic"].addItems(["Kodomo", "Shonen", "Shoujo", "Josei", "Seinen", "Seijin",
                                                 "Mina", "4-koma"])
        elif self.media_type == "Video Game":
            self.inputs["Platform"].addItems(["PC - Steam", "PC - Origin", "PC - Uplay", "PC - No DRM",
                                              "Nintendo - Switch", "Nintendo - Wii U", "Nintendo - Wii",
                                              "Nintendo - Gamecube", "Nintendo - N64", "Nintendo - SNES",
                                              "Nintendo - NES", "Nintendo - 3DS", "Nintendo - DS", "Nintendo - GBA",
                                              "Nintendo - GBC", "Nintendo - GB", "Microsoft - Xbox One X",
                                              "Microsoft - Xbox One", "Microsoft - Xbox 360", "Microsoft - Xbox",
                                              "Sony - Playstation 4", "Sony - Playstation 3", "Sony - Playstation 2",
                                              "Sony - Playstation", "Sony - Vita", "Sony - PSP"])
            self.inputs["Campaign Finished?"].addItems(["Yes", "No", "N/A"])
            self.inputs["Achievement Progress"].addItems(["<10%", "10-19%", "20-29%", "30-39%", "40-49%", "50-59%",
                                                          "60-69%", "70-79%", "80-89%", "90-99%", "100%", "N/A"])
        self.inputs["Score"].addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

        self.submit = QPushButton("Submit", self)
        self.submit.setFixedHeight(40)

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

    def source_name_status(self):
        """Enables or disables the 'Source Name' line edit based on
        the input for the 'Source Type' input for music"""
        if self.inputs["Type"].currentText() != "Album" and self.inputs["Source Type"].currentText() != "Single":
            self.inputs["Source Name"].setDisabled(False)
        else:
            self.inputs["Source Name"].setDisabled(True)

    def submit_media(self):
        """Places the inputs from the input widgets into a temporary
        dictionary variable"""
        for key in self.inputs:
            if isinstance(self.inputs[key], QComboBox):
                if key == "Score":
                    self.temp_input[key] = int(self.inputs[key].currentText())
                else:
                    self.temp_input[key] = self.inputs[key].currentText()
            else:
                # If there are multiple inputs for one category, split them
                if "," in self.inputs[key].text() and key != "Comments":
                    input_list = self.inputs[key].text()
                    input_list = input_list.split(",")

                    # If whitespace exists at the beginning of an input, remove it
                    for idx in range(len(input_list)):
                        if input_list[idx][0] == " ":
                            input_list[idx] = input_list[idx][1:]

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
