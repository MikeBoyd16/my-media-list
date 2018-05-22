import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, \
    QFileDialog, QTextEdit, QListWidget, QListWidgetItem, QLineEdit


class MyListWindow(QMainWindow):
    movie_list = []

    def __init__(self):
        super().__init__()

        # Initialize window title and dimensions
        self.title = "MyMovieList"
        self.left = 100
        self.top = 100
        self.width = 770
        self.height = 580

        # Initialize widgets
        self.movie_list_area = QListWidget(self)
        self.movie_details_area = QTextEdit(self)
        self.add_movie = QPushButton("", self)
        self.remove_movie = QPushButton("", self)
        self.edit_movie = QPushButton("", self)

        # Initialize window
        self.init_window()
        self.search_movies_window = SearchMoviesWindow()

    def init_window(self):
        # Add menu
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")

        # Add "import file" menu option
        open_file = QAction("&Import List", self)
        open_file.triggered.connect(self.import_file)
        file_menu.addAction(open_file)

        # Set window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set widget dimensions
        self.movie_list_area.setGeometry(70, 50, 250, 450)
        self.movie_details_area.setGeometry(350, 50, 350, 450)

        # Set button dimensions and positioning
        self.add_movie.setIcon(QtGui.QIcon("add_movie.png"))
        self.add_movie.setIconSize(QtCore.QSize(24, 24))
        self.add_movie.setFixedSize(50, 50)
        self.add_movie.move(10, 100)
        self.add_movie.setStyleSheet("QPushButton {background: #61E722;}")
        self.add_movie.clicked.connect(self.go_to_search)

        self.remove_movie.setIcon(QtGui.QIcon("remove_movie.png"))
        self.remove_movie.setIconSize(QtCore.QSize(24, 24))
        self.remove_movie.setFixedSize(50, 50)
        self.remove_movie.move(10, 180)
        self.remove_movie.setStyleSheet("QPushButton {background: #E72222;}")

        self.edit_movie.setIcon(QtGui.QIcon("edit_movie.png"))
        self.edit_movie.setIconSize(QtCore.QSize(24, 24))
        self.edit_movie.setFixedSize(50, 50)
        self.edit_movie.move(10, 260)
        self.edit_movie.setStyleSheet("QPushButton {background: #E7E122;}")

        # Disable text editing
        self.movie_details_area.setDisabled(True)

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

    def go_to_search(self):
        self.search_movies_window.show()


class SearchMoviesWindow(QMainWindow):
    movie_list = []

    def __init__(self):
        super().__init__()

        # Initialize window title and dimensions
        self.title = "Movie Search"
        self.left = 100
        self.top = 100
        self.width = 770
        self.height = 580

        # Initialize widgets
        self.search_movie_text = QLineEdit(self)
        self.search_movie_submit = QPushButton("Search", self)
        self.movie_details_area = QTextEdit(self)
        self.back = QPushButton("Back", self)
        self.next = QPushButton("Next", self)

        # Initialize window
        self.init_window()

    def init_window(self):
        # Set window title and dimensions
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Set widget dimensions
        self.movie_details_area.setGeometry(225, 80, 350, 410)

        # Set button dimensions and positioning
        self.back.move(275, 525)
        self.back.clicked.connect(self.go_to_my_list)

        self.next.move(425, 525)

        self.search_movie_text.resize(140, 30)
        self.search_movie_text.move(275, 40)

        self.search_movie_submit.move(435, 40)

        # Disable text editing
        self.movie_details_area.setDisabled(True)

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

    def on_submit(self):
        movie_input = self.search_movie_text


def main():
    app = QApplication(sys.argv)
    my_list_window = MyListWindow()
    my_list_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
