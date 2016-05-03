from numpy import *
import Block

class Group(Block.Block):
    """ this class describes a group of blocks """
    
    def __init__(self):
        Block.Block.__init__(self)
        self.children = {}
        self.list = []
    
    def start(self):
        for b in self.children:
            self.children[b].start()
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        if len(self.list)==0:
            for b in self.children:
                self.children[b]._getInputs(f)
        else:
            for b in self.list:
                self.children[b]._getInputs(f)
        
    def setOutputs(self,f):
        if len(self.list)==0:
            for b in self.children:
                self.children[b]._setOutputs(f)
        else:
            for b in self.list:
                self.children[b]._setOutputs(f)
        return f
        
    def append(self,name,child):
        self.children[name] = child
        self.list.append(name)
        