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
        
    def init(self):
        for b in self.children:
            self.children[b].init()
            self.children[b].active==True
    
    def getInputs(self,f):
        for b in self.children:
            if self.children[b].active:
                self.children[b].getInputs(f)
        
    def setOutputs(self,f):
        for b in self.children:
            if self.children[b].active:
                f = self.children[b].setOutputs(f)
        return f
        