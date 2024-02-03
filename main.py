from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QPlainTextEdit, QComboBox
import downloading
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Window.ui", self)
        self.show()
app = QApplication(sys.argv)
UIWindow = MainWindow()
app.exec()