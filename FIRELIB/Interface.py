from Connexion import Connexion
from ConnexionWidget import ConnexionTree
from PyQt4.QtGui import *

class Interface(QStandardItem):
    """Generic class of an interface in FIRE. This class shall be inherited for each interface to integrate in FIRE application
    It is characterised by:
    - a constructor with the necessary constant parameters
    - a list of inputs
    - a list of outputs
    - a write_outputs method
    - a read_inputs method
    - a task executed in background to make sampling computations"""
    
    def __init__(self,name = "generic",icon = QIcon()):
        """constructor of the interface"""
        QStandardItem.__init__(self,icon,name)
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
        # widget to control the interface
        self.controlWidget = QLabel(name)
        
    def start(self):
        raise NotImplementedError
        
    def close(self):
        raise NotImplementedError
        
    def deliverOutputs(self,channels):
        raise NotImplementedError
        
    def receiveInputs(self,channels):
        raise NotImplementedError
        