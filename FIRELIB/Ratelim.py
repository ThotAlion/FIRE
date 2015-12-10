from numpy import *
import Block
from Connexion import *
import Tools
import time
import csv

class Ratelim(Block.Block):
    """ this class describes a block """
    
    def __init__(self,n,maxrate):
        Block.Block.__init__(self)
        self.n = n
        self.old = {}
        self.maxrate = maxrate
        for i in range(self.n):
            name = "ch"+str(i)
            self.inputs[name] = Connexion(default = NaN)
            self.outputs[name] = Connexion(default = 0)


    def start(self):
        a=1
        
    def init(self,f):
        self.t = Tools.getTime()
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        self.told = self.t
        self.t = Tools.getTime()
        for i in range(self.n):
            name = "ch"+str(i)
            a = self.inputs[name].getValue(f)
            if self.old.has_key(name):
                if type(a)==str or type(self.old[name])==str:
                    self.outputs[name].setValue(a,f)
                    self.old[name] = a
                else:
                    delta = a - self.old[name]
                    dt = self.t - self.told
                    deltamax = self.maxrate*dt
                    b = min(delta,deltamax)
                    b = max(b,-deltamax)
                    self.outputs[name].setValue(self.old[name]+b,f)
                    self.old[name] = self.old[name]+b
            else:
                self.outputs[name].setValue(a,f)
                self.old[name] = a
            
            

        return f
           
    def close(self):
        a=1
        