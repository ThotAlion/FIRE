from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import FIRELIB

class FireGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.showMaximized()
        #self.showFullScreen()
        
        # widgets
        self.wInterface = FIRELIB.InterfaceWidget.InterfaceWidget()
        self.wSystem = FIRELIB.SystemWidget.SystemWidget()
        self.wConnexion = FIRELIB.ConnexionWidget.ConnexionWidget()
        self.channels = {}
        self.engine = FIRELIB.Engine.Engine(self,self.wInterface.interfaceTree,
                            self.wSystem.systemTree,self.channels)
        
        

        # page setup
        self.mainLayout = QHBoxLayout(self)
        self.IntSysLayout = QVBoxLayout()
        self.OneClickViewLayout = QVBoxLayout()
        self.configLayout = QStackedLayout()
        self.controlLayout = QStackedLayout()
        self.OneClickViewLayout.addLayout(self.configLayout)
        self.OneClickViewLayout.addLayout(self.controlLayout)
        self.IntSysLayout.addWidget(self.wInterface)
        self.IntSysLayout.addWidget(self.wSystem)
        self.IntSysLayout.addWidget(self.engine.engineWidget)
        self.mainLayout.addLayout(self.IntSysLayout)
        self.mainLayout.addWidget(self.wConnexion)
        self.mainLayout.addLayout(self.OneClickViewLayout)

        
        # signals
        self.connect(self.wInterface.wTree,SIGNAL("clicked(QModelIndex)"),self.updateInterfaceConnexion)
        self.connect(self.wSystem.wTree,SIGNAL("clicked(QModelIndex)"),self.updateSystemConnexion)
        self.connect(self.engine.interfaceTimer,SIGNAL("timeout()"),self.wInterface,SLOT("update()"))
        self.connect(self.engine.interfaceTimer,SIGNAL("timeout()"),self.wSystem,SLOT("update()"))
        self.connect(self.engine.interfaceTimer,SIGNAL("timeout()"),self.wConnexion,SLOT("update()"))
        
        
    def updateInterfaceConnexion(self,i):
        if i.column() == 0:
            item = self.wInterface.interfaceTree.itemFromIndex(i)
            self.wConnexion.wTabIn.setModel(item._inputs)
            self.wConnexion.wTabOut.setModel(item._outputs)
            self.configLayout.addWidget(item.configWidget)
            self.configLayout.setCurrentWidget(item.configWidget)
            self.controlLayout.addWidget(item.controlWidget)
            self.controlLayout.setCurrentWidget(item.controlWidget)
        
    def updateSystemConnexion(self,i):
        if i.column() == 0:
            item = self.wSystem.systemTree.itemFromIndex(i)
            self.wConnexion.wTabIn.setModel(item._inputs)
            self.wConnexion.wTabOut.setModel(item._outputs)
            self.configLayout.addWidget(item.configWidget)
            self.configLayout.setCurrentWidget(item.configWidget)
            self.controlLayout.addWidget(item.controlWidget)
            self.controlLayout.setCurrentWidget(item.controlWidget)
        
styleFile = QFile("FIRELIB\styleSheet.txt")
styleFile.open(styleFile.ReadOnly)
style = str(styleFile.readAll())
app = QApplication(sys.argv)
app.setStyleSheet(style)
w = FireGui()
sys.exit(app.exec_())

