from PyQt4.QtGui import *
from PyQt4.QtCore import *
from System import System
from Connexion import Connexion
from numpy import *

class Hub(System):
    """This system is a set of connexions. What is set in input is copied to the corresponding output. It is very convenient to rename some channels or make simple computations"""
    
    def __init__(self,name = "Hub"):
        """constructor"""
        System.__init__(self,name=name,icon=QIcon("FIRELIB/icons/hub.png"))
        self._index = 1
        self.controlWidget = hubWidget(self)
        self.executionState = self.NOTREADY
        
    def start(self):
        self.executionState = self.READY
        
    def close(self):
        self.executionState = self.FINISHED
        
    def deliverOutputs(self,channels):
        for i in range(self._outputs.rowCount()):
            # warning, a QString is returned and the replace method is overloaded (and not the same...)
            outputname = str(self._outputs.invisibleRootItem().child(i,0).text())
            inputname = outputname.replace("output","input")
            a = self._inputs.getConnexion(inputname,channels)
            channels = self._outputs.setConnexion(outputname,a,channels)
        return channels
        
    def addConnexion(self):
        self._inputs.invisibleRootItem().appendRow(Connexion("input "+str(self._index),direction=Connexion.IN,
            description = "will be copied in output "+str(self._index),
            unit = "WU",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
            
        self._outputs.invisibleRootItem().appendRow(Connexion("output "+str(self._index),direction=Connexion.OUT,
            description = "from input "+str(self._index),
            unit = "WU",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
        self._index = self._index + 1
            
    def removeConnexion(self,i):
        self._inputs.invisibleRootItem().takeRow(i)
        self._outputs.invisibleRootItem().takeRow(i)
        
    def writeConf(self):
        conf = System.writeConf(self)
        conf["_index"] = self._index
        return conf
        
    def readConf(self,conf):
        System.readConf(self,conf)
        self._index = conf["_index"]
    
    
class hubWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        self.inputs = parent._inputs
        self.outputs = parent._outputs
        self.parent = parent
        # list of components
        self.wLabelTitle = QLabel("System : Hub")
        self.setToolTip("This system directly copies an input to the matching output.")
        self.wAddConnexion = QPushButton("Add connexion")
        self.wRemoveConnexion = QPushButton("Remove connexion:")
        self.wComboConnexion = QComboBox()
        self.wComboConnexion.setModel(self.inputs)
        
        # widget setup
        self.setFixedSize(300,100)
        self.mainlayout = QVBoxLayout(self)
        self.remLayout = QHBoxLayout()
        self.remLayout.addWidget(self.wRemoveConnexion)
        self.remLayout.addWidget(self.wComboConnexion)
        self.mainlayout.addWidget(self.wLabelTitle)
        self.mainlayout.addWidget(self.wAddConnexion)
        self.mainlayout.addLayout(self.remLayout)
        
        # connect the signals
        self.connect(self.wAddConnexion,SIGNAL("pressed()"),parent.addConnexion)
        self.connect(self.wRemoveConnexion,SIGNAL("pressed()"),self.remove)
        
    def remove(self):
        i = self.wComboConnexion.currentIndex()
        self.parent.removeConnexion(i)
        