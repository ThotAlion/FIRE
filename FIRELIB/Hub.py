from PyQt4.QtGui import *
from PyQt4.QtCore import *
from System import System
from Connexion import Connexion
from numpy import *

class Hub(System):
    """This system is a set of connexions. What is set in input is copied to the corresponding output. It is very convenient to rename some channels or make simple computations"""
    
    def __init__(self,name = "Hub"):
        """constructor"""
        System.__init__(self,name)
        self._index = 1
        self.controlWidget = hubWidget(self)
        
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
    
class hubWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        self.inputs = parent._inputs
        self.outputs = parent._outputs
        
        # list of components
        self.wAddConnexion = QPushButton("Add connexion")
        self.wRemoveConnexion = QPushButton("Remove connexion")
        self.wComboConnexion = QComboBox()
        self.wComboConnexion.setModel(self.inputs)
        
        # widget setup
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addWidget(self.wAddConnexion)
        self.mainlayout.addWidget(self.wRemoveConnexion)
        self.mainlayout.addWidget(self.wComboConnexion)
        
        # connect the signals
        self.connect(self.wAddConnexion,SIGNAL("pressed()"),parent.addConnexion)
        