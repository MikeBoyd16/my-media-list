import sys
import json
import datetime
from manage_categories import *
from manage_fields import *
from select_category import *
from PyQt5.QtWidgets import *


class AddItem(QDialog):
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

    def __init__(self, category):
        super().__init__()
        self.category = category
        self.temp_input = {}
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
        if self.category == "Music":
            widgets = AddItem.music_widgets
        elif self.category == "Audiobook":
            widgets = AddItem.audiobook_widgets
        elif self.category == "Movie":
            widgets = AddItem.movie_widgets
        elif self.category == "TV":
            widgets = AddItem.tv_widgets
        elif self.category == "Anime":
            widgets = AddItem.anime_widgets
        elif self.category == "Book":
            widgets = AddItem.book_widgets
        elif self.category == "Manga":
            widgets = AddItem.manga_widgets
        elif self.category == "Video Game":
            widgets = AddItem.video_game_widgets

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
        if self.category == "Music":
            self.inputs["Type"].currentIndexChanged.connect(self.source_name_status)
            self.inputs["Source Type"].currentIndexChanged.connect(self.source_name_status)

        # Fill the combo boxes with the correct items based on the selected category
        if self.category == "Music":
            self.inputs["Type"].addItems(["Song", "Remix", "Album"])
            self.inputs["Source Type"].addItems(["Single", "LP", "EP", "Studio Album",
                                                 "Live Album", "Remix Album", "Reissue"])
            self.inputs["Source Name"].setDisabled(True)
        elif self.category == "Movie":
            self.inputs["MPAA"].addItems(["G", "PG", "PG-13", "R", "NC-17"])
        elif self.category == "TV":
            self.inputs["Content Rating"].addItems(["TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA"])
        elif self.category == "Anime":
            self.inputs["Type"].addItems(["TV", "Movie", "OVA", "Special"])
            self.inputs["Content Rating"].addItems(["G", "PG", "PG-13", "R", "NC-17"])
            self.inputs["Source"].addItems(["Original", "Manga", "4-koma", "Visual Novel", "Light Novel",
                                            "Novel", "Video Game", "Card Game"])
        elif self.category == "Manga":
            self.inputs["Demographic"].addItems(["Kodomo", "Shonen", "Shoujo", "Josei", "Seinen", "Seijin",
                                                 "Mina", "4-koma"])
        elif self.category == "Video Game":
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

    def source_name_status(self):
        """Enables or disables the 'Source Name' line edit based on
        the input for the 'Source Type' input for music"""
        if self.inputs["Type"].currentText() != "Album" and self.inputs["Source Type"].currentText() != "Single":
            self.inputs["Source Name"].setDisabled(False)
        else:
            self.inputs["Source Name"].setDisabled(True)

    def submit_item(self):
        """Places the inputs from the input fields into a temp data structure"""
        for key in self.inputs:
            if isinstance(self.inputs[key], QComboBox):
                if key == "Score":
                    self.temp_input[key] = int(self.inputs[key].currentText())
                else:
                    self.temp_input[key] = self.inputs[key].currentText()
            else:
                # If there are multiple inputs for one field, split them
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
