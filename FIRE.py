from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class FireGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setStyleSheet("background-color: black; color: yellow;")
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.treesLayout = QVBoxLayout()
        self.setLayout.addLayout(self.treesLayout)
        self.interfaceTree = QTreeView()
        self.main_layout.addWidget(self.interfaceTree)
        self.showMaximized()

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
w = InterfaceWidget()
sys.exit(app.exec_())

