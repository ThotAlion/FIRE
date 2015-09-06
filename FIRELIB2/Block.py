from numpy import *

class Block(object):
    """ this class describes a block """
    
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self._active = False
    
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self, val):
        if self._active == False and val == True:
            self.init()
        self._active = val
            
    
    def start(self):
        print "This function is launched when the system is started"
        
    def init(self):
        print "This function is launched just before running"
    
    def getInputs(self,f):
        print "get inputs to deliver them in the reality."
        
    def setOutputs(self,f):
        print "set outputs in the data flow."
        