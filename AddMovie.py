import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, \
    QFileDialog, QTextEdit, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QLabel
from SelectMedia import *


class AddMovie(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window title and dimensions
        self.title = "Add Movie"
        self.left = 100
        self.top = 100
        self.width = 770
        self.height = 580

        # Initialize widgets
        self.label_name = QLabel(self)
        self.text_name = QLineEdit(self)
        self.label_date = QLabel(self)
        self.text_date = QLineEdit(self)
        self.label_mpaa = QLabel(self)
        self.text_mpaa = QLineEdit(self)
        self.label_duration = QLabel(self)
        self.text_duration = QLineEdit(self)
        self.label_genres = QLabel(self)
        self.text_genres = QLineEdit(self)
        self.label_directors = QLabel(self)
        self.text_directors = QLineEdit(self)
        self.label_writers = QLabel(self)
        self.text_writers = QLineEdit(self)
        self.label_producers = QLabel(self)
        self.text_producers = QLineEdit(self)
        self.label_stars = QLabel(self)
        self.text_stars = QLineEdit(self)
        self.label_quality_rating = QLabel(self)
        self.text_quality_rating = QLineEdit(self)
        self.label_personal_rating = QLabel(self)
        self.text_personal_rating = QLineEdit(self)
        self.back = QPushButton("Back", self)
        self.next = QPushButton("Next", self)

        # Initialize window
        self.init_window()

    def init_window(self):
        # Set window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set label text
        self.label_name.setText("Name:")
        self.label_name.setGeometry(50, 50, 50, 50)
        self.text_name.setGeometry(100, 100, 100, 100)
        self.label_date.setText("Date:")
        self.label_mpaa.setText("MPAA:")
        self.label_duration.setText("Duration:")
        self.label_genres.setText("Genres:")
        self.label_directors.setText("Directors:")
        self.label_writers.setText("Writers:")
        self.label_producers.setText("Producers:")
        self.label_stars.setText("Stars:")
        self.label_quality_rating.setText("Quality Rating:")
        self.label_personal_rating.setText("Personal Rating:")

        # Set back button dimensions and positioning
        self.back.move(250, 325)
        self.back.clicked.connect(self.go_to_select_media)

        # Set next button dimensions and positioning
        self.next.move(400, 325)

        # CSS
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")

    def go_to_select_media(self):
        self.hide()
