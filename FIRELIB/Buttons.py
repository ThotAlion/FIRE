from numpy import *
import Block
from Connexion import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Tools
import time

class Buttons(Block.Block,QWidget):
    """ this class describes a button block """
    
    def __init__(self,buttonNames,init,type='classic'):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        self.buttonNames = buttonNames
        self.buttonDict = {}
        self.type = type
        layout = QVBoxLayout(self)
        i = 0
        for b in self.buttonNames:
            self.outputs[b] = Connexion(default = 0)
            if self.type=='classic':
                self.buttonDict[b] = QPushButton(b)
                if b == "STOP":
                    self.buttonDict[b].setStyleSheet("color: yellow;background-color: red;font-size: 30px;")
                else:
                    self.buttonDict[b].setStyleSheet("color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);font-size: 24px;")
            elif self.type=='radio':
                self.buttonDict[b] = QRadioButton(b)
                if init[i]==1:
                    self.buttonDict[b].setChecked(True)
            elif self.type=='check':
                self.buttonDict[b] = QCheckBox(b)
                if init[i]==1:
                    self.buttonDict[b].setChecked(True)
            self.buttonDict[b].setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            
            layout.addWidget(self.buttonDict[b])
            i = i+1
        self.show()

    def start(self):
        a=1
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        for b in self.buttonDict:
            if self.type == 'classic':
                if self.buttonDict[b].isDown():
                    self.outputs[b].setValue(1,f)
                else:
                    self.outputs[b].setValue(0,f)
            elif self.type == 'radio':
                if self.buttonDict[b].isChecked():
                    self.outputs[b].setValue(1,f)
                else:
                    self.outputs[b].setValue(0,f)
            elif self.type == 'check':
                if self.buttonDict[b].isChecked():
                    self.outputs[b].setValue(1,f)
                else:
                    self.outputs[b].setValue(0,f)
        return f
           
    def close(self):
        a=1
        