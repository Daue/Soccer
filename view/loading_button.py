from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import QSize, QTimer, Qt
from PyQt6.QtGui import QPalette
from enum import Enum


class LoadingButtonState(Enum):
    Idle = 0
    Loading = 1


class LoadingButton(QPushButton):
    IdleText = "Load"
    LoadingText = "Loading"

    def __init__(self):
        super().__init__()

        self.state = None
        self.loading_dot_count = 0
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.on_timeout)

        self.setMaximumSize(QSize(self.width(), 50))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        font = self.font()
        font.setPixelSize(18)
        font.setBold(True)
        self.setFont(font)

        self.setStyleSheet("QPushButton{color: white}")
        self.set_state(LoadingButtonState.Idle)

    def set_state(self, state: LoadingButtonState):
        self.state = state
        if self.state is LoadingButtonState.Idle:
            self.timer.stop()
            self.setEnabled(True)
            self.setText(self.IdleText)
        else:
            self.setEnabled(False)
            self.setText(self.LoadingText)
            self.timer.start()

    def on_timeout(self):
        dots = " . " * self.loading_dot_count
        self.setText(dots + self.LoadingText + dots)
        self.loading_dot_count += 1
        self.loading_dot_count %= 4


