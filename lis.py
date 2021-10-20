import sys
import os
import time
import mimetypes

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy as np
from tqdm import tqdm
from pydub.playback import play

import input.pdfplumber as pdfplumber
import input.pypdf2 as pypdf2

import output.gtts as gtts

from lisui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.current_text = []
        self.current_line = 0

# slots
    # line selection
    def textLineSelectionChanged(self):
        line = min(self.listWidget.currentRow(), len(self.current_text))
        self.setCurrentLine(line)

    def setCurrentLine(self, line):
        # QSignalBlocker to avoid a recursive call
        with QSignalBlocker(self.spinBox_position) as blocker:
            self.current_line = min(line, len(self.current_text))
            self.spinBox_position.setValue(self.current_line)
            self.listWidget.setCurrentRow(self.current_line)

    # play / pause
    def play(self):
        for l in self.current_text:
            self.tts_line(l)

# outputs
    def tts_line(self, line):
        audio = gtts.convert(line)
        print(type(audio), audio)

        play(audio)

# inputs
    def update_list(self):
        self.listWidget.clear()
        self.listWidget.addItems(self.current_text)
        self.listWidget.setCurrentRow(self.current_line)

    def add_txt(self, filename):
        raise NotImplementedError

    def add_pdf(self, filename):
        self.current_text = pdfplumber.convert(filename)
        self.current_line = 0
        self.update_list()

    # Drag and Drop files : https://gist.github.com/peace098beat/db8ef7161508e6500ebe
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f, mimetypes.guess_type(f))
            if mimetypes.guess_type(f)[0] == 'text/plain':
                self.add_txt(f)
                return
            elif mimetypes.guess_type(f)[0] == 'application/pdf':
                self.add_pdf(f)
                return


if __name__ == '__main__':
    try:
        from PyQt5.QtWinExtras import QtWin
        QtWin.setCurrentProcessExplicitAppUserModelID('cyril-meyer.lis.gui')
    except ImportError:
        pass

    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('media/icon.png'))
    window = MainWindow()
    window.show()
    app.exec()
