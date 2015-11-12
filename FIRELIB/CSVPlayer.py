from numpy import *
import Block
from Connexion import *
import Tools
import time
import csv

class CSVPlayer(Block.Block):
    """ this class describes a block """
    
    def __init__(self,CSVFile):
        Block.Block.__init__(self)
        self.tape = []
        r = csv.DictReader(open(CSVFile,'r'),delimiter = ';')
        for row in r:
            self.tape.append(row)
        for name in r.fieldnames:
            self.outputs[name] = Connexion(default = NaN)
        self.outputs["Number"] = Connexion(default = "-1")
        self.index = 0
        self.number = -1
        

    def start(self):
        self.t0 = Tools.getTime()
        self.active = True
        
    def init(self):
        self.index = 0
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        t = Tools.getTime()
        duration = self.tape[self.index]["Duration"]
        if t-self.t0>=duration and self.index<=len(self.tape)-1:
            self.index = self.index+1
            self.t0 = Tools.getTime()
            self.number = self.number+1
        for name in r.fieldnames:
            self.outputs[name].setValue(self.tape[self.index][name],f)
        self.outputs[Number].setValue(str(self.number),f)
        return f
           
    def close(self):
        a=1
        