from numpy import *
import Block
from Connexion import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Tools
import time

class Display(Block.Block,QWidget):
    """ this class describes a button block """
    
    def __init__(self,labelNames):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        self.labelNames = labelNames
        self.labelDict = {}
        layout = QVBoxLayout(self)
        for b in self.labelNames:
            self.inputs[b] = Connexion(default = 0)
            self.labelDict[b] = QLabel(b+" : "+"0")
            self.labelDict[b].setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.labelDict[b].setStyleSheet("font-size: 24px;")
            layout.addWidget(self.labelDict[b])
        self.show()

    def start(self):
        a=1
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        for b in self.labelDict:
            self.labelDict[b].setText(b+" : "+str(self.inputs[b].getValue(f)))
        return f
           
    def close(self):
        a=1
        