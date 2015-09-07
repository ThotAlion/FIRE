from numpy import *

class Connexion(object):
    """ this class describes a connexion (formalism is as simple as possible!) """
    
    def __init__(self,default = 0.0, min = -Inf, max = Inf):
        self.connectedTo = ""
        self.default = default
        self.min = min
        self.max = max
    
    def getValue(self,f):
        eq = self.connectedTo
        if len(eq)>0:
            listk = f.keys()
            listk.sort()
            listk.reverse()
            for k in listk:
                eq = eq.replace(k,'f["'+k+'"]')
            a = eval(eq)
        else:
            a = self.default
        return a
        
    def setValue(self,val,f):
        if len(self.connectedTo)>0:
            val = minimum(val,self.max)
            val = maximum(val,self.min)
            f[self.connectedTo] = val
        return f