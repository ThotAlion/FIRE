from Connexion import Connexion
from ConnexionWidget import ConnexionTree
from PyQt4.QtGui import QStandardItem,QStandardItemModel,QLabel

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
        self._inputs = ConnexionTree()
        self._outputs = ConnexionTree()
        # types of execution states
        self.READY = "READY"
        self.RUNNING = "RUNNING"
        self.NOTREADY = "NOT READY"
        # types of task state
        self.PROGRESS = "IN PROGRESS"
        self.FINISHED = "FINISHED"
        self.STOPPED = "STOPPED"
        # if the interface is a group of interfaces
        self._isGroup = False
        # states of the Interface
        self.executionState = self.READY
        self.taskState = self.STOPPED
        # widget to control the system
        self.controlWidget = QLabel(name)
    
    def start(self):
        raise NotImplementedError
        
    def close(self):
        raise NotImplementedError
    
    def deliverOutputs(self,channels):
        raise NotImplementedError
        
        