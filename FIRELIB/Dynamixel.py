from Connexion import Connexion
from Interface import Interface
from numpy import *
import pypot.dynamixel

class Dynamixel(Interface):
    """Interface for Dynamixel motor"""
    
    def __init__(self,name = "dynamixel",ID=1,Model="AX-12",stops=[-150,150]):
        """constructor of the interface"""
        self._name = name
        self._inputs.append(Connexion(type=IN,
        name = "goal position",
        description = "Commanded position of the servo.",
        unit = "deg",
        connectedTo="",
        valueInit = 0.0, 
        valueMin = stops[0], 
        valueMax = stops[1]))
        
        self._outputs = []
        
        
        
    def write_outputs():
        raise NotImplementedError
        
    def read_inputs():
        for output in outputs:
            if output.name == "goal position" and output.isConnected:
                if output.value == NaN
                    
        