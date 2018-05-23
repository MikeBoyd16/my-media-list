import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, \
    QFileDialog, QTextEdit, QListWidget, QListWidgetItem, QLineEdit, QComboBox
from SelectMedia import *


class AddBook(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window title and dimensions
        self.title = "Add Book"
        self.left = 100
        self.top = 100
        self.width = 770
        self.height = 580

        # Initialize widgets
        self.select_media_combo = QComboBox(self)
        self.back = QPushButton("Back", self)
        self.next = QPushButton("Next", self)

        # Initialize window
        self.init_window()

    def init_window(self):
        # Set window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set back button dimensions and positioning
        self.back.move(250, 325)
        self.back.clicked.connect(self.go_to_select_media)

        # Set next button dimensions and positioning
        self.next.move(400, 325)

        # CSS
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")

    def go_to_select_media(self):
        self.hide()
