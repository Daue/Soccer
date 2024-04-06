import os.path

from PyQt6.QtCore import QProcess, QObject, pyqtSignal
import csv
import shutil


class DataLoader(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.process = None
        self.data = []

    def load(self, cached_data=False):
        shutil.rmtree('./data', ignore_errors=True)
        self.data.clear()
        if cached_data:
            self.started.emit()
            self._load_data_from_file()
            self.finished.emit()
        else:
            self.process = QProcess()
            self.process.started.connect(self._load_from_web_started)
            self.process.finished.connect(self._load_from_web_finished)
            self.process.setProgram('python')
            self.process.setArguments(['./wrapper/wrap.py'])
            self.process.start()
        pass

    def _load_data_from_file(self):
        file_name = './data/result.csv'
        if not os.path.exists(file_name):
            return

        with open('./data/result.csv', encoding="utf8", newline='') as f:
            csv_reader = csv.DictReader(f)
            next(csv_reader)
            for row in csv_reader:
                self.data.append(row)

    def _load_from_web_started(self):
        self.started.emit()

    def _load_from_web_finished(self):
        self._load_data_from_file()
        self.process = None
        self.finished.emit()



