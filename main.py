from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QPlainTextEdit, QComboBox, QFileDialog, QToolButton
import downloading
import pathOperations
import sys
import os
import re
import threading
import pytube as pt
from pydub import AudioSegment as pds

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Window.ui", self)
        
        self.toolButton = self.findChild(QToolButton, "ToolButton")
        self.toolButton.clicked.connect(lambda : pathOperations.fileExplorerChoose(self.findChild(QPlainTextEdit, "DirectoryText")))
        
        self.downloadText = self.findChild(QPlainTextEdit, "DownloadText")
        try:
            self.findChild(QPlainTextEdit, "DirectoryText").setPlainText(pathOperations.configRead()['path'])
        except:
            pass
        
        self.format = self.findChild(QComboBox, "Format")
        
        self.infoLabel = self.findChild(QLabel, "InfoLabel")
        
        self.defaultDirectoryButton = self.findChild(QPushButton, "DefaultDirectoryButton")
        self.defaultDirectoryButton.clicked.connect(lambda : pathOperations.configSave(self.findChild(QPlainTextEdit, "DirectoryText")))
        
        self.downloadButton = self.findChild(QPushButton, "DownloadButton")
        self.downloadButton.clicked.connect(lambda : downloading.download(self.downloadText.toPlainText(), self.findChild(QPlainTextEdit, "DirectoryText"), self.format.currentText(), self.infoLabel))
        
        self.show()
        
if __name__ == "__main__":
    downloading.setImports(os, re, threading, pt, pds)
    pathOperations.setImports(os, QFileDialog)
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec()