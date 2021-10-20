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
import pydub.playback
import simpleaudio
from prefetch_generator import BackgroundGenerator

import input.utils
import input.pdfplumber as pdfplumber
import input.pypdf2 as pypdf2
import input.textract as textract
import input.ebooklib as ebooklib

import output.gtts as gtts

from lisui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.current_text = []
        self.current_line = 0

        self.play_flag = False


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

    # input
    def openFile(self):
        f = QFileDialog.getOpenFileName(self, "Sélection un fichier")[0]
        self.add_file(f)

    # play / pause
    def play(self):
        self.pushButton_play.setEnabled(False)
        self.pushButton_pause.setEnabled(True)

        self.play_flag = True
        self.tts(self.current_text)

        self.pushButton_play.setEnabled(True)
        self.pushButton_pause.setEnabled(False)

    def pause(self):
        self.play_flag = False
        self.pushButton_play.setEnabled(True)
        self.pushButton_pause.setEnabled(False)

    # quit
    def closeEvent(self, event):
        self.play_flag = False
        app.quit()

    # outputs
    def tts_generator(self, text):
        for line in text:
            audio = gtts.convert(line)
            yield audio
        return

    def tts(self, text):
        gen = self.tts_generator(text[self.current_line:])
        for audio in BackgroundGenerator(gen, max_prefetch=2):
            playback = simpleaudio.play_buffer(
                audio.raw_data,
                num_channels=audio.channels,
                bytes_per_sample=audio.sample_width,
                sample_rate=audio.frame_rate
            )
            from PyQt5.QtTest import QTest
            for _ in range(int(audio.duration_seconds*10)+1):
                QTest.qWait(100)
                if not self.play_flag:
                    playback.stop()
                    return

# inputs
    def update_list(self):
        self.listWidget.clear()
        self.listWidget.addItems(self.current_text)
        self.listWidget.setCurrentRow(self.current_line)

    def add_txt(self, filename):
        self.current_text = input.utils.read_txt(filename)
        self.current_line = 0
        self.update_list()

    def add_pdf(self, filename):
        self.current_text = pdfplumber.convert(filename)
        self.current_line = 0
        self.update_list()

    def add_epub(self, filename):
        self.current_text = ebooklib.convert(filename)
        self.current_line = 0
        self.update_list()

    def add_file(self, f):
        if mimetypes.guess_type(f)[0] == 'text/plain':
            self.add_txt(f)
            return True
        elif mimetypes.guess_type(f)[0] == 'application/pdf':
            self.add_pdf(f)
            return True
        elif mimetypes.guess_type(f)[0] == 'application/epub+zip':
            self.add_epub(f)
            return True

    # Drag and Drop files : https://gist.github.com/peace098beat/db8ef7161508e6500ebe
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if self.add_file(f):
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
