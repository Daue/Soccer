from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QStyledItemDelegate, QWidget, QGridLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QVariant, QSize
from PyQt6.QtGui import QImage, QPixmap

import os


class ListItemWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__()

        # main widget layout
        layout = QGridLayout()

        # date + icon
        date_layout = QHBoxLayout()
        date_layout.addWidget(
            self._create_label(kwargs['date'], 35))
        date_layout.addWidget(
            self._create_icon(kwargs['match_icon']))

        # team1
        team1_layout = QHBoxLayout()
        team1_layout.setSpacing(0)
        team1_layout.setContentsMargins(0, 0, 0, 0)
        team1_layout.addWidget(
            self._create_label(kwargs['team1_name'], None, 13))
        team1_layout.addWidget(
            self._create_icon(kwargs['team1_icon']))

        # score
        score_layout = QHBoxLayout()
        score_layout.setSpacing(0)
        score_layout.setContentsMargins(0, 0, 0, 0)
        score_layout.addWidget(
            self._create_label(f'{kwargs['team1_score']} : {kwargs['team2_score']}', 45, 15, True))

        # team2
        team2_layout = QHBoxLayout()
        team2_layout.setSpacing(0)
        team2_layout.setContentsMargins(0, 0, 0, 0)
        team2_layout.addWidget(
            self._create_icon(kwargs['team2_icon']))
        team2_layout.addWidget(
            self._create_label(kwargs['team2_name'], None, 13))

        layout.addLayout(date_layout, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(team1_layout, 0, 1, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(score_layout, 0, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(team2_layout, 0, 3, Qt.AlignmentFlag.AlignLeft)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 1)

        self.setLayout(layout)

    def _create_label(self, text, width=None, pixel_size=None, bold=False):
        label = QLabel(text)
        if width is not None:
            label.setFixedWidth(width)
        font = label.font()
        font.setBold(bold)
        if pixel_size is not None:
            font.setPixelSize(pixel_size)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        return label

    def _create_icon(self, file_path):
        label = QLabel()
        pixmap = QPixmap(os.path.join('data', file_path))
        label.setPixmap(
            pixmap.scaled(16, 16, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
        label.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        return label


class StyledItemDelegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()

    def sizeHint(self, option, index):
        return QSize(super().sizeHint(option, index).width(), 50)


class ListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAlternatingRowColors(True)
        self.setItemDelegate(StyledItemDelegate())

    def fill_data(self, data):
        for row_data in data:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, QVariant(row_data['link']))
            widget = ListItemWidget(**row_data)
            self.addItem(item)
            self.setItemWidget(item, widget)
