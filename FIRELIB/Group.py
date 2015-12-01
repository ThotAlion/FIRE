from numpy import *
import Block

class Group(Block.Block):
    """ this class describes a group of blocks """
    
    def __init__(self):
        Block.Block.__init__(self)
        self.children = {}
    
    def start(self):
        for b in self.children:
            self.children[b].start()
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        for b in self.children:
            self.children[b]._getInputs(f)
        
    def setOutputs(self,f):
        for b in self.children:
            f = self.children[b]._setOutputs(f)
        return f
        