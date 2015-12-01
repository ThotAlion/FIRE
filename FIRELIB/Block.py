from numpy import *
import Connexion

class Block(object):
    """ this class describes a block """
    
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self.inputs["activate"] = Connexion.Connexion(0)
        self.outputs["finished"] = Connexion.Connexion(0)
        self._active = False

    def start(self):
        print "This function is launched when the system is started"
        
    def init(self,f):
        print "This function is launched just before running"
    
    
    def _getInputs(self,f):
        if self._active == True:
            self.getInputs(f)
    
    def getInputs(self,f):
        print "get inputs to deliver them in the reality."
        
    def _setOutputs(self,f):
        if self._active == False and self.inputs["activate"].getValue(f) == 1:
            f = self.init(f)
            self._active = True
        elif self.inputs["activate"].getValue(f) == 0:
            self._active = False
            
        if self._active == True:
            f = self.setOutputs(f)
        return f
        
    def setOutputs(self,f):
        print "set outputs in the data flow."
        return f
        