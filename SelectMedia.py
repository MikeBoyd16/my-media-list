import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QListWidgetItem, QComboBox
from MyMediaList import *
from AddMovie import *
from AddTV import *
from AddMusic import *
from AddBook import *
from AddVideoGame import *


class SelectMedia(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window title and dimensions
        self.title = "Media Select"
        self.left = 100
        self.top = 100
        self.width = 770
        self.height = 580

        # Initialize widgets
        self.select_media_combo = QComboBox(self)
        self.back = QPushButton("Back", self)
        self.next = QPushButton("Next", self)

        # Initialize Add Media windows
        self.add_movie = AddMovie()
        self.add_tv = AddTV()
        self.add_music = AddMusic()
        self.add_book = AddBook()
        self.add_video_game = AddVideoGame()

        # Initialize window
        self.init_window()

    def init_window(self):
        # Set window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set back button dimensions and positioning
        self.back.move(250, 325)
        self.back.clicked.connect(self.go_to_my_list)

        # Set next button dimensions and positioning
        self.next.move(400, 325)
        self.next.clicked.connect(self.go_to_add_media)

        # Set media select dropdown dimensions and positioning
        self.select_media_combo.addItems(["Movie", "TV", "Music", "Book", "Video Game"])
        self.select_media_combo.setGeometry(50, 50, 200, 30)
        self.select_media_combo.move(280, 220)

        # CSS
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")

    def import_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Import File")
        file = open(file_name[0], "r")

        for line in file:
            line = line.replace("\n", "")
            self.movie_list.append(line)

        for i in range(len(self.movie_list)):
            movie = QListWidgetItem(self.movie_list[i])
            self.movie_list_area.addItem(movie)

    def go_to_my_list(self):
        self.hide()

    def go_to_add_media(self):
        media_selection = self.select_media_combo.currentText()

        if media_selection == "Movie":
            self.add_movie.show()
        elif media_selection == "TV":
            self.add_tv.show()
        elif media_selection == "Music":
            self.add_music.show()
        elif media_selection == "Book":
            self.add_book.show()
        elif media_selection == "Video Game":
            self.add_video_game.show()
