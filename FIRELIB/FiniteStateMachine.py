from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import zmq
import json
import Tools
import time
import csv

class FiniteStateMachine(Block.Block,QWidget):
    """ this class describes a block """
    
    def __init__(self,CSVFile):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        self.CSVFile = CSVFile
        self.state = {}
        self.trans = {}
        self.statenames = []
        r = csv.DictReader(open(self.CSVFile,'r'),delimiter = ';')
        ispace = r.fieldnames.index("SPACE")
        for row in r:
            self.statenames.append(row["Name"])
            self.state[row["Name"]]={}
            self.trans[row["Name"]]={}
            for state in r.fieldnames[1:ispace]:
                self.state[row["Name"]][state]=row[state]
            for trans in r.fieldnames[ispace+1:]:
                self.trans[row["Name"]][trans]=row[trans]
        for trans in r.fieldnames[ispace+1:]:
            self.inputs[trans] = Connexion(default = 0)
        for state in r.fieldnames[1:ispace]:
            self.outputs[state] = Connexion(default = 0)
        self.inputs["active"] = Connexion(default = 0)
        self.outputs["finished"] = Connexion(default = 0)
        
        self._currentState = ''
        
        # creation of components
        self.dict_buttons = {}
        for state in self.statenames:
            self.dict_buttons[state] = QPushButton(state)
            self.dict_buttons[state].setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.dict_buttons[state].setStyleSheet("color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);font-size: 24px;")
            self.connect(self.dict_buttons[state],SIGNAL("pressed()"),self.updateCurrentState)
        n = int(ceil(sqrt(len(self.state))))
        # composition
        k = 0
        mainlayout = QVBoxLayout(self)
        hbox = []
        for i in range(n):
            hbox.append(QHBoxLayout())
            mainlayout.addLayout(hbox[-1])
            for j in range(n):
                if k<len(self.state):
                    hbox[-1].addWidget(self.dict_buttons[self.statenames[k]])
                    k = k+1
        
        
        self.show()
    
    def updateCurrentState(self):
        for s in self.statenames:
            if self.dict_buttons[s].isDown():
                self.currentState = s
    
    @property
    def currentState(self):
        return self._currentState
        
    @currentState.setter
    def currentState(self,x):
        self._currentState = x
        for s in self.statenames:
            self.dict_buttons[s].setText(s)
            # self.dict_buttons[s].setStyleSheet("color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);font-size: 24px;")
        if self.dict_buttons.has_key(self._currentState):
            self.dict_buttons[self._currentState].setText("*"+self._currentState+"*")
            # self.dict_buttons[self._currentState].setStyleSheet("color: black;\
    # background-color: orange;font-size: 24px;")
    
    def start(self):
        a=1
        
    def init(self,f):
        self.currentState = self.statenames[0]
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        # compute transition function of inputs
        for t in self.trans[self.currentState]:
            if self.inputs[t].getValue(f) == 1:
                self.currentState = self.trans[self.currentState][t]
        
        # generate outputs
        for b in self.state[self.currentState]:
            vals = self.state[self.currentState][b]
            try:
                val = float(vals)
            except:
                val = vals
            self.outputs[b].setValue(val,f)
        return f
        

        