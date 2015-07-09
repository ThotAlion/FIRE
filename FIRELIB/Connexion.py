from numpy import *

class Connexion:
    """ This class defines a connexion of a system. It is defined by :
    - type : IN or OUT
    - name : string containing the name of the connexion (can include space)
    - description : description of the connexion for help
    - unit : unit of the connexion to control unity errors
    - connectedTo : name of the variable connected
    - value : matrix value of the connexion
    - valueInit : value of the connexion at initialisation
    """
    self.IN = "IN"
    self.OUT = "OUT"
    
    def __init__(self,type=self._IN,name = "default",description = "empty",unit = "WU",connectedTo="",valueInit = 0.0, valueMin = -Inf, valueMax = Inf):
        self._type = type
        self._name = name
        self._description = description
        self._unit = unit
        self._connectedTo = connectedTo
        self._valueInit = array(valueInit)
        self._value = self._valueInit
        if min(valueMin<valueMax)==False:
            self._valueMin = valueMin
            self._valueMax = valueMax
        else:
            raise "In connexion"+self._name+"valueMin = "+valueMin+" is greater than valueMax = "+valueMax
        if 

    
    
        
    
