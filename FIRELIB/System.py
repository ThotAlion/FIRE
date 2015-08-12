from Connexion import Connexion

class System(QStandardItem):
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
        QStandardItem.__init__(self,name)
        self._inputs = QStandardItemModel()
        self._outputs = QStandardItemModel()
    
    def deliverOutputs(self,channels):
        raise NotImplementedError
        