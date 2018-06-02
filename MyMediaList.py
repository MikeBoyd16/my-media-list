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

        self.title = "MyMediaList"
        self.left, self.top, self.width, self.height = 100, 100, 500, 600

        self.media_list_area = QListWidget(self)
        self.media_details_area = QTextEdit(self)

        self.init_window()
        self.center()

    def init_window(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        edit_menu = main_menu.addMenu("Edit")

        open_file = QAction("Import List", self)
        open_file.triggered.connect(self.import_file)
        file_menu.addAction(open_file)

        save_file = QAction("Export List", self)
        save_file.triggered.connect(self.export_file)
        file_menu.addAction(save_file)

        add_media = QAction("Add Media", self)
        add_media.triggered.connect(self.add_media_record)
        edit_menu.addAction(add_media)

        edit_media = QAction("Edit Media", self)
        edit_menu.addAction(edit_media)

        remove_media = QAction("Remove Media", self)
        edit_menu.addAction(remove_media)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.media_list_area.itemClicked.connect(self.show_media_record)
        self.media_details_area.setDisabled(True)

        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")
        self.init_layout()

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def init_layout(self):
        box_layout = QHBoxLayout(self.central_widget)
        box_layout.addWidget(self.media_list_area)
        box_layout.addWidget(self.media_details_area)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(0)

        self.setLayout(box_layout)

    def update_list(self):
        self.media_list_area.clear()
        for key in self.my_media_list:
            self.media_list_area.addItem("[" + self.my_media_list[key]["Media"] + "] " +
                                         self.my_media_list[key]["Name"])

    def import_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Import File")
        file = open(file_name[0], "r")
        self.my_media_list = json.load(file)
        self.update_list()

    def export_file(self):
        file_name = QFileDialog.getSaveFileName(self, "Import File")
        file = open(file_name[0], "w")
        json.dump(self.my_media_list, file)

    def add_media_record(self):
        select_media = SelectMedia()
        select_media.show()
        select_media.exec_()
        self.my_media_list[str(select_media.temp_input["Month Entered"]) + "." +
                           str(select_media.temp_input["Day Entered"]) + "." +
                           str(select_media.temp_input["Year Entered"]) + "-" +
                           select_media.temp_input["Media"] + "-" +
                           select_media.temp_input["Name"]] = select_media.temp_input
        self.update_list()

    def show_media_record(self):
        pass


class SelectMedia(QDialog):
    def __init__(self):
        super().__init__()
        self.temp_input = {}
        self.title = "Media Select"
        self.left = 100
        self.top = 100
        self.width = 200
        self.height = 200

        self.select_media_combo = QComboBox(self)
        self.ok = QPushButton("OK", self)

        self.init_window()

    def init_layout(self):
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.select_media_combo, 0, 0)
        grid_layout.addWidget(self.ok, 1, 0)
        group_box = QGroupBox("")
        group_box.setLayout(grid_layout)
        v_box_layout = QVBoxLayout()
        v_box_layout.addWidget(group_box)
        self.setLayout(v_box_layout)

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.ok.move(50, 50)
        self.ok.clicked.connect(self.go_to_add_media)
        self.select_media_combo.addItems(["Movie", "TV", "Music", "Book", "Video Game"])
        self.init_layout()

    def get_media_selection(self):
        return self.select_media_combo.currentText()

    def go_to_add_media(self):
        add_media_record = AddMedia()
        add_media_record.exec_()
        self.temp_input = add_media_record.temp_input
        self.temp_input["Media"] = self.select_media_combo.currentText()
        now = datetime.datetime.now()
        self.temp_input["Month Entered"] = now.month
        self.temp_input["Day Entered"] = now.day
        self.temp_input["Year Entered"] = now.year
        self.hide()


class AddMedia(QDialog):
    def __init__(self):
        super().__init__()
        self.temp_input = {}
        self.labels = {"Type": QLabel(), "Favorite": QLabel(), "Name": QLabel(),
                       "Artist": QLabel(), "Album": QLabel(), "Duration": QLabel(),
                       "Genres": QLabel(), "Record Labels": QLabel(), "Producers": QLabel()}
        self.inputs = {"Type": QComboBox(), "Favorite": QComboBox(), "Name": QLineEdit(),
                       "Artist": QLineEdit(), "Album": QLineEdit(), "Duration": QLineEdit(),
                       "Genres": QLineEdit(), "Record Labels": QLineEdit(), "Producers": QLineEdit()}
        self.init_window_properties()
        self.init_widgets()
        self.init_window()

    def init_window_properties(self):
        self.title = "Add Music"
        self.left = 100
        self.top = 100
        self.width = 250
        self.height = 600

    def init_widgets(self):
        self.inputs["Type"].addItems(["Single", "Remix", "Studio Album", "Extended Play",
                                      "Reissue", "Live Album", "Remix Album"])
        self.inputs["Favorite"].addItems(["Yes", "No", "N/A"])

        for key in self.labels:
            self.labels[key].setText(key)

        self.submit = QPushButton("Submit", self)
        self.submit.setFixedHeight(40)

    def init_layout(self):
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

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("QMainWindow {background: #BCBCBC;}")
        self.submit.clicked.connect(self.submit_media)
        self.init_layout()

    def submit_media(self):
        for key in self.inputs:
            if isinstance(self.inputs[key], QComboBox):
                self.temp_input[key] = self.inputs[key].currentText()
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
