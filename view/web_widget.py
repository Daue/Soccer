from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class WebWidget(QWebEngineView):

    def __init__(self):
        super().__init__()
        self.setUrl(QUrl.fromLocalFile("/view/default_page.html"))