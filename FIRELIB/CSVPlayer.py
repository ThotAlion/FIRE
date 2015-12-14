from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import Tools
import time
import csv

class CSVPlayer(Block.Block,QWidget):
    """ this class describes a block """
    
    def __init__(self,members):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        self.tapeName = ""
        self.tape = []
        self.index = 0
        self.number = 0
        self.members = members
        # creation of outputs/inputs
        for member in self.members:
            for ch in self.members[member]:
                self.outputs[ch] = Connexion(default = NaN)
        self.outputs["Number"] = Connexion(default = "-1")
        self.outputs["Duration"] = Connexion(default = "1")
        self.outputs["Name"] = Connexion(default = "toto")
        self.inputs["Tape"] = Connexion(default = self.tapeName)
        self.inputs["Pause"] = Connexion(default = 0)

    def start(self):
        a=1
        
    def init(self,f):
        self.index = 0
        self.t0 = Tools.getTime()
        self.outputs["finished"].setValue(0,f)
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        t = Tools.getTime()
        # control of tape change
        tape_input = self.inputs["Tape"].getValue(f)
        if tape_input != self.tapeName:
            self.index = 0
            self.t0 = Tools.getTime()
            self.outputs["finished"].setValue(0,f)
            self.tapeName = tape_input
            self.tape = []
            r = csv.DictReader(open(self.tapeName,'r'),delimiter = ';')
            for row in r:
                self.tape.append(row)
        # control of outputs
        duration = float(self.tape[self.index]["Duration"])
        if (t-self.t0)>=duration and self.index<=len(self.tape)-2:
            self.index = self.index+1
            self.t0 = t
            self.number = self.number+1
            print self.index
        elif self.index==len(self.tape)-2:
            self.outputs["finished"].setValue(1,f)
        
        for name in self.tape[self.index]:
            self.outputs[name].setValue(self.tape[self.index][name],f)
        self.outputs["Number"].setValue(str(self.number),f)
        return f
           
    def close(self):
        a=1
        