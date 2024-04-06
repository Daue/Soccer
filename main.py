from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QGuiApplication, QIcon

from model.data_loader import DataLoader
from view.list_widget import ListWidget
from view.web_widget import WebWidget
from view.loading_button import LoadingButton, LoadingButtonState

import qdarktheme
import sys
import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Soccer')
        self.setWindowIcon(QIcon('./view/ball.png'))

        self.loader = DataLoader()
        self.load_button = LoadingButton()
        self.list = ListWidget()
        self.web_view = WebWidget()

        # add layouts and widgets
        list_layout_widget = QWidget()
        list_layout_widget.setLayout(QVBoxLayout())
        list_layout_widget.layout().addWidget(self.load_button)
        list_layout_widget.layout().addWidget(self.list)
        splitter = QSplitter()
        splitter.addWidget(list_layout_widget)
        splitter.addWidget(self.web_view)
        self.setCentralWidget(splitter)

        # connections
        self.loader.started.connect(self.loading_data_started)
        self.loader.finished.connect(self.loading_data_finished)
        self.load_button.pressed.connect(self.loader.load)
        self.list.currentItemChanged.connect(self.list_item_changed)

        # init main window geometry
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        width = int(screen_geometry.width() * 0.6)
        height = int(screen_geometry.height() * 0.6)
        self.setGeometry((screen_geometry.width() - width)//2, (screen_geometry.height() - height)//2, width, height)

        # load cached data
        self.loader.load()

    def loading_data_started(self):
        self.list.clear()
        self.load_button.set_state(LoadingButtonState.Loading)
        self.list.setEnabled(False)
        pass

    def loading_data_finished(self):
        self.list.fill_data(self.loader.data)
        self.load_button.set_state(LoadingButtonState.Idle)
        self.list.setEnabled(True)

    def list_item_changed(self):
        item = self.list.currentItem()
        if item is not None:
            link = item.data(Qt.ItemDataRole.UserRole)
            self.web_view.setUrl(QUrl(link))


app = QApplication(sys.argv)
app.setPalette(qdarktheme.load_palette(theme="dark"))
app.setStyleSheet(qdarktheme.load_stylesheet(theme="dark"))

w = MainWindow()
w.show()
app.exec()
