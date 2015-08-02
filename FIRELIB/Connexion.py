from numpy import *

class Connexion(object):
    """ This class defines a connexion of a system. It is defined by :
    - type : IN or OUT
    - name : string containing the name of the connexion (can include space)
    - description : description of the connexion for help
    - unit : unit of the connexion to control unity errors
    - connectedTo : name of the variable connected
    - value : matrix value of the connexion or string
    - valueInit : value of the connexion at initialisation
    - valueMax : maximal value
    - valueMin : minimal value
    """
    IN = "IN"
    OUT = "OUT"
    
    def __init__(self,description = "empty",unit = "WU",connectedTo="",valueInit = 0.0, valueMin = -Inf, valueMax = Inf):
        self.description = description
        self.unit = unit
        self.connectedTo = connectedTo
        self.valueMin = valueMin
        self.valueMax = valueMax
        self.valueInit = valueInit
        self.value = self.valueInit
        

    # data protections
    @property        
    def description(self):
        return self._description
    @description.setter
    def description(self,x):
        if type(x)==str:
            self._description = x
        else:
            print "Connexion description must be a string"    
    
    @property    
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self,x):
        if type(x)==str:
            self._unit = x
        else:
            print "Connexion unit must be a string"    
    
    @property    
    def connectedTo(self):
        return self._connectedTo
    @connectedTo.setter
    def connectedTo(self,x):
        if type(x)==str:
            self._unit = x
        else:
            print "Connexion tag must be a string"
    
    @property
    def valueInit(self):
        return self._valueInit
    @valueInit.setter
    def valueInit(self,x):
        if type(x)==ndarray:
            self._valueInit=x
        elif type(x)==list:
            self._valueInit=array(x)
        else:
            self._valueInit=array([x])
    
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self,x):
        if type(x)==str:
            self._value=x
        else:
            if type(x)==ndarray:
                self._value=x
            elif type(x)==list:
                self._value=array(x)
            else:
                self._value=array([x])
            self._value = minimum(self._value,self.valueMax)
            self._value = maximum(self._value,self.valueMin)

    @property
    def valueMax(self):
        return self._valueMax
    @valueMax.setter
    def valueMax(self,x):
        if type(x)==ndarray:
            self._valueMax=x
        elif type(x)==list:
            self._valueMax=array(x)
        else:
            self._valueMax=array([x])        
    
    @property
    def valueMin(self):
        return self._valueMin
    @valueMin.setter
    def valueMin(self,x):
        if type(x)==ndarray:
            self._valueMin=x
        elif type(x)==list:
            self._valueMin=array(x)
        else:
            self._valueMin=array([x])
            
    @property
    def isConnected(self):
        return len(connectedTo)>0
        
    
    
    
        
    
