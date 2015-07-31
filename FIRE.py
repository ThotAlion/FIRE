from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class FireGui(QMainWindow):
    def __init__(self):
        self = QMainWindow()
        self.setStyleSheet("background-color: black;")

app = QApplication(sys.argv)
w = FireGui()

