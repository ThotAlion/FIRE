from numpy import *
import Block
from Connexion import *
import Tools
import time
import csv

class Wires(Block.Block):
    """ this class describes a block """
    
    def __init__(self,n):
        Block.Block.__init__(self)
        self.n = n
        for i in range(self.n):
            name = "ch"+str(i)
            self.inputs[name] = Connexion(default = NaN)
            self.outputs[name] = Connexion(default = 0)

    def start(self):
        a=1
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        for i in range(self.n):
            name = "ch"+str(i)
            a = self.inputs[name].getValue(f)
            self.outputs[name].setValue(a,f)

        return f
           
    def close(self):
        a=1
        