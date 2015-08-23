from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import FIRELIB
import pickle

class FireGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.showMaximized()
        #self.showFullScreen()
        
        # widgets
        self.wInterface = FIRELIB.InterfaceWidget.InterfaceWidget()
        self.wSystem = FIRELIB.SystemWidget.SystemWidget()
        self.wConnexion = FIRELIB.ConnexionWidget.ConnexionWidget()
        self.wSave = QPushButton("Save")
        self.wLoad = QPushButton("Load")
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
        self.IntSysLayout.addWidget(self.wSave)
        self.IntSysLayout.addWidget(self.wLoad)
        self.mainLayout.addLayout(self.IntSysLayout)
        self.mainLayout.addWidget(self.wConnexion)
        self.mainLayout.addLayout(self.OneClickViewLayout)

        
        # signals
        self.connect(self.wInterface.wTree,SIGNAL("clicked(QModelIndex)"),self.updateInterfaceConnexion)
        self.connect(self.wSystem.wTree,SIGNAL("clicked(QModelIndex)"),self.updateSystemConnexion)
        self.connect(self.engine.interfaceTimer,SIGNAL("timeout()"),self.wInterface,SLOT("update()"))
        self.connect(self.engine.interfaceTimer,SIGNAL("timeout()"),self.wSystem,SLOT("update()"))
        self.connect(self.engine.interfaceTimer,SIGNAL("timeout()"),self.wConnexion,SLOT("update()"))
        self.connect(self.wSave,SIGNAL("pressed()"),self.saveConfig)
        self.connect(self.wLoad,SIGNAL("pressed()"),self.loadConfig)
        
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
            
    def saveConfig(self):
        fileName = QFileDialog.getSaveFileName(self,"Save File",QDir.currentPath()+"/CONF/","FIRE Configurations (*.conf)");
        data = {}
        data["interfaces"] = self.wInterface.interfaceTree.writeConf()
        data["systems"] = self.wSystem.systemTree.writeConf()
        print fileName
        pickle.dump(data,file(str(fileName),'wb'),protocol=-1)
        
    def loadConfig(self):
        fileName = QFileDialog.getOpenFileName(self,"Open File",QDir.currentPath()+"/CONF/","FIRE Configurations (*.conf)");
        a = pickle.load(file(str(fileName),'rb'))
        self.wInterface.interfaceTree.readConf(a["interfaces"])
        self.wSystem.systemTree.readConf(a["systems"])
        
        
styleFile = QFile("FIRELIB\styleSheet.txt")
styleFile.open(styleFile.ReadOnly)
style = str(styleFile.readAll())
app = QApplication(sys.argv)
app.setStyleSheet(style)
w = FireGui()
sys.exit(app.exec_())

