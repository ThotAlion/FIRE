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
    
    def __init__(self,CSVFile,IP = '127.0.0.1',port = '8080'):
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
            self.inputs[trans] = Connexion(default = "0")
        for state in r.fieldnames[1:ispace]:
            self.outputs[state] = Connexion(default = "0")
        self.inputs["active"] = Connexion(default = "0")
        self.outputs["finished"] = Connexion(default = "0")
        
        self.currentState = self.statenames[0]
        
        # creation of components
        self.dict_buttons = {}
        print self.state
        for state in self.statenames:
            self.dict_buttons[state] = QPushButton(state)
            self.dict_buttons[state].setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        n = int(ceil(sqrt(len(self.state))))
        print n
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
        # signals
        
        
        self.show()
        
    
    def start(self):
        self.active = True
        
    def init(self):
        a=1
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        self.dict_buttons[self.currentState].setStyleSheet("background-color: yellow;");
        return f
        

        