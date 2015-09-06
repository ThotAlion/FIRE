from numpy import *

class Block(Object):
    """ this class describes a block """
    
    def __init__(self,default = 0.0, min = -Inf, max = Inf):
        self.connectedTo = ""
        self.default = 0.0
        self.min = -Inf
        self.max = Inf
    
    def getValue(self,f):
        eq = self.connectedTo
        if len(eq)>0:
            listk = f.keys()
            listk.sort()
            listk.reverse()
            for k in listk:
                eq = eq.replace(k,'f["'+k+'"]')
            try:
                a = eval(eq)
            except:
                a = self.default
        else:
            a = self.default
        return a
        
    def setValue(self,val,f):
        val = minimum(val,self.max)
        val = maximum(val,self.min)
        f[self.connectedTo] = val
        return f