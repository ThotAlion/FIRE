from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import FIRELIB

class FireGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.showMaximized()
        
        # widgets
        self.wInterface = FIRELIB.InterfaceWidget.InterfaceWidget()
        self.wSystem = FIRELIB.SystemWidget.SystemWidget()
        self.wConnexion = FIRELIB.ConnexionWidget.ConnexionWidget()
        self.wOneClickView1 = QFrame()
        self.wOneClickView2 = QFrame()
        # page setup
        self.mainLayout = QHBoxLayout(self)
        self.IntSysLayout = QVBoxLayout()
        self.OneClickViewLayout = QVBoxLayout()
        self.IntSysLayout.addWidget(self.wInterface)
        self.IntSysLayout.addWidget(self.wSystem)
        self.OneClickViewLayout.addWidget(self.wOneClickView1)
        self.OneClickViewLayout.addWidget(self.wOneClickView2)
        self.mainLayout.addLayout(self.IntSysLayout)
        self.mainLayout.addWidget(self.wConnexion)
        self.mainLayout.addLayout(self.OneClickViewLayout)

        
        # signals
        self.connect(self.wInterface.wTree,SIGNAL("clicked(QModelIndex)"),self.updateInterfaceConnexion)
        self.connect(self.wSystem.wTree,SIGNAL("clicked(QModelIndex)"),self.updateSystemConnexion)
        
    def updateInterfaceConnexion(self,i):
        item = self.wInterface.interfaceTree.itemFromIndex(i)
        self.wConnexion.wTabIn.setModel(item._inputs)
        self.wConnexion.wTabOut.setModel(item._outputs)
        
    def updateSystemConnexion(self,i):
        item = self.wSystem.interfaceTree.itemFromIndex(i)
        self.wConnexion.wTabIn.setModel(item._inputs)
        self.wConnexion.wTabOut.setModel(item._outputs)
        
styleFile = QFile("FIRELIB\styleSheet.txt")
styleFile.open(styleFile.ReadOnly)
style = str(styleFile.readAll())
app = QApplication(sys.argv)
app.setStyleSheet(style)
w = FireGui()
sys.exit(app.exec_())

