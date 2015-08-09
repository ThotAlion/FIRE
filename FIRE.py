from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class FireGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setStyleSheet("background-color: black; color: yellow;")
        self.showFullScreen()

# widget to control FIRE Interface list
class InterfaceWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setStyleSheet("background-color: black; color: yellow;")
        # list of components:
        self.addButton = QPushButton("Add")
        self.removeButton = QPushButton("Remove")
        self.moveUpButton = QPushButton("Move up")
        self.moveDnButton = QPushButton("Move dn")
        self.tree = QTreeView()
        
        # organise the components in layouts
        buttonslayout = QHBoxLayout()
        buttonslayout.addWidget(self.addButton)
        buttonslayout.addWidget(self.removeButton)
        buttonslayout.addWidget(self.moveUpButton)
        buttonslayout.addWidget(self.moveDnButton)
        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)
        mainlayout.addLayout(buttonslayout)
        mainlayout.addWidget(self.tree)
        
        self.show()
app = QApplication(sys.argv)
w = FireGui()
sys.exit(app.exec_())

