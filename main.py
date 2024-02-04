from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QPlainTextEdit, QComboBox
import downloading
import sys
import os
import re
import threading
import pytube as pt
from pydub import AudioSegment as pd

class MainWindow(QMainWindow):
    def validateDirectory(self, path):
        path = str(path)
        if os.path.exists(path) and os.path.isdir(path):
            if path[-1] != "\\":
                path += "\\"
            return path
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads\\')
        
    def __init__(self):
        super().__init__()
        uic.loadUi("Window.ui", self)
        self.downloadText = self.findChild(QPlainTextEdit, "DownloadText")
        self.directoryText = self.validateDirectory(self.findChild(QPlainTextEdit, "DirectoryText").toPlainText)
        self.format = self.findChild(QComboBox, "Format")
        self.downloadButton = self.findChild(QPushButton, "DownloadButton")
        self.downloadButton.clicked.connect(lambda : downloading.download(self.downloadText.toPlainText(), self.directoryText, self.format.currentText(), os, re, threading, pt, pd))
        self.show()
app = QApplication(sys.argv)
UIWindow = MainWindow()
app.exec()