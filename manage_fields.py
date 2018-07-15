import sys
import json
import datetime
from manage_categories import *
from select_media import *
from add_media import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ManageFields(QDialog):
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.init_window()
        self.init_layout()
        self.init_styles()

    def init_window(self):
        """Initializes the window, its dimensions, and content"""
        self.setWindowTitle("Manage Fields")
        self.setGeometry(100, 100, 400, 400)
        self.center_window()

    def init_layout(self):
        """Initializes the layout and arranges the widgets in the proper order."""
        pass

    def init_widgets(self):
        """Initializes widgets and their properties"""
        pass

    def init_styles(self):
        """Sets the stylesheet properties for widgets"""
        pass

    def center_window(self):
        """Positions the window in the center of the screen"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
