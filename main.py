#Imports
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QPlainTextEdit, QComboBox, QFileDialog, QToolButton
import sys
import os
import re
import threading
import pytube as pt
import subprocess as sp


#global variables
downloadInProgress = False

def validateDirectory(path):
    path = str(path)
    if os.path.exists(path) and os.path.isdir(path):
        if path[-1] != "/":
            path += "/"
        return path
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads/')

def transformToMp3(title, path):
        if os.path.exists(f"{path}{title}.mp4"):
            command = ['ffmpeg', '-i', f'{path}{title}.mp4', f'{path}{title}.mp3']
            sp.run(command, creationflags=sp.CREATE_NO_WINDOW)
            os.remove(f"{path}{title}.mp4")

def validateName(title):
        prohibited_chars = [r'[^a-zA-Z0-9 ]']
        pattern = "|".join(prohibited_chars)
        updated_string = re.sub(pattern, '', title)
        return updated_string

def defineTypeOfLink(link, pt):
        try:
            yt = pt.YouTube(link)
            return yt
        except:
            try:
                yt = pt.Playlist(link)
                if len(yt)<1:
                    raise
                return yt
            except:
                return None

def downloadVideo(link, path, format, infoLabel):
    title = validateName(link.title)
    video_streams = link.streams
    if format == "MP4":
        stream = video_streams.filter(file_extension="mp4", progressive=True).get_highest_resolution()
        infoLabel.setText(f"Downloading \"{title}\" as MP4...")
        stream.download(path, filename=f"{title}.mp4")
        infoLabel.setText("")
    else:
        stream = video_streams.filter(only_audio=True, file_extension="mp4").order_by('abr').last()
        infoLabel.setText(f"Downloading \"{title}\" as MP3...")
        stream.download(path, filename=f"{title}.mp4")
        transformToMp3(title, path)
        infoLabel.setText("")

def downloadPlaylist(link, path, format, infoLabel):
    for video in link.videos:
        downloadVideo(video, path, format, infoLabel)


def downloadThread(link, path, format, infoLabel):
    global downloadInProgress
    if isinstance(link, pt.YouTube):
        downloadVideo(link, path, format, infoLabel)
        downloadInProgress = False
    elif isinstance(link, pt.Playlist):
        downloadPlaylist(link, path, format, infoLabel)
        downloadInProgress = False


def download(link, path, format, infoLabel):
    global downloadInProgress
    link = defineTypeOfLink(link, pt)
    path = validateDirectory(path.toPlainText())
    if link is not None and downloadInProgress == False:
        downloadInProgress = True
        thread = threading.Thread(target=downloadThread, args=(link,path,format, infoLabel,))
        thread.start()


def configSave(directoryText):
    with open("config.txt", 'w') as file:
        file.write(f"path = {validateDirectory(directoryText.toPlainText())}")

def configRead():
    config = {}
    try:
        with open("config.txt", "r") as file:
            configList = file.readlines()
            for line in configList:
                if line:
                    separated = line.strip().split(" = ")
                    if len(separated) == 2:
                        config[separated[0]] = separated[1]
    except:
        pass
    return config

def fileExplorerChoose(directoryText):
    directory = QFileDialog.getExistingDirectory(None, "Select Directory")
    directoryText.setPlainText(directory)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Window.ui", self)
        
        self.toolButton = self.findChild(QToolButton, "ToolButton")
        self.toolButton.clicked.connect(lambda : fileExplorerChoose(self.findChild(QPlainTextEdit, "DirectoryText")))
        
        self.downloadText = self.findChild(QPlainTextEdit, "DownloadText")
        try:
            self.findChild(QPlainTextEdit, "DirectoryText").setPlainText(configRead()['path'])
        except:
            pass
        
        self.format = self.findChild(QComboBox, "Format")
        
        self.infoLabel = self.findChild(QLabel, "InfoLabel")
        
        self.defaultDirectoryButton = self.findChild(QPushButton, "DefaultDirectoryButton")
        self.defaultDirectoryButton.clicked.connect(lambda : configSave(self.findChild(QPlainTextEdit, "DirectoryText")))
        
        self.downloadButton = self.findChild(QPushButton, "DownloadButton")
        self.downloadButton.clicked.connect(lambda : download(self.downloadText.toPlainText(), self.findChild(QPlainTextEdit, "DirectoryText"), self.format.currentText(), self.infoLabel))
        
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec()