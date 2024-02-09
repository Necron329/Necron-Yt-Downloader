os = None
QFileDialog = None
from downloading import validateDirectory
def setImports(os_lib, QfileDialog_lib):
    global os, QFileDialog
    os = os_lib
    QFileDialog = QfileDialog_lib

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