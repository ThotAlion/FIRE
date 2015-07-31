from Connexion import Connexion

class Interface:
    """Generic class of an interface in FIRE. This class shall be inherited for each interface to integrate in FIRE application
    It is characterised by:
    - a constructor with the necessary constant parameters
    - a list of inputs
    - a list of outputs
    - a write_outputs method
    - a read_inputs method
    - a task executed in background to make sampling computations"""
    
    def __init__(self,name = "generic"):
        """constructor of the interface"""
        self._name = name
        self._inputs = []
        self._outputs = []
        
    def write_outputs():
        raise NotImplementedError
        
    def read_inputs():
        raise NotImplementedError
        