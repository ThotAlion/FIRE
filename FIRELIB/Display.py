from numpy import *
import Block
from Connexion import *
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
        for b in self.labelDict:
            self.inputs[b] = Connexion(default = 0)
            self.labelDict[b] = QLabel(b)
            self.labelDict[b].setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.labelDict[b].setStyleSheet("color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);font-size: 24px;")
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
            self.labelDict[b].setText(self.inputs[b].getValue(f))
        return f
           
    def close(self):
        a=1
        