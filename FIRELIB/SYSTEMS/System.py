import ../Connexion

class System:
    """Generic class of a system in FIRE. This class shall be inherited for each system to integrate in FIRE application
    It is characterised by:
    - a constructor with the necessary constant parameters
    - a list of inputs
    - a list of outputs
    - a read_inputs method
    - a write_outputs method
    - a task executed in background to make sampling computations"""
    
    def __init__(self,name = "generic"):
        """constructor of the system"""
        self.inputs = []
        self.outputs = []
        self.outputs.append(Connexion.Connexion(type=Connexion.OUT,
        name="time of read_inputs",
        description="Duration of the read_inputs function of "+self.name+" system.",))
        self.outputs.append(Connexion.Connexion(type=Connexion.OUT,
        name="time of write_outputs",
        description="Duration of the write_outputs function of "+self.name+" system.",))
        
    def 