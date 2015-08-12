from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import Tools

class Engine(QThread):
    """ This class is the engine of FIRE application during its execution."""
    
    def __init__(self,parent,interfaces,systems,channels):
        Qthread.__init__(self,parent)
        self._Interfaces = interfaces
        self._Systems = systems
        self._Channels = channels
        self.samplingPeriod = 0.02
        self._isActive = True
        self._isPaused = False
        self.engineWidget = EngineWidget(self)
    
    def start(self):
        for i in range(self._Interfaces.rowCount()):
            self._Interfaces.item(i).start()
                
        for i in range(self._Systems.rowCount()):
            self._Systems.item(i).start()
            
        Qthread.start(self)
    
    def run(self):
        
        while self._isActive:
            while self._isPaused:
                self.wait(100)
            t0 = Tools.getTime()
            for i in range(self._Interfaces.rowCount()):
                self._Channels = self._Interfaces.item(i).deliverOutputs(self._Channels)
                
            for i in range(self._Systems.rowCount()):
                self._Channels = self._Systems.item(i).deliverOutputs(self._Channels)
                
            for i in range(self._Interfaces.rowCount()):
                self._Interfaces.item(i).receiveInputs(self._Channels)
                
            while Tools.getTime()-t0<self.samplingPeriod:
                a=1
                
    def close(self):
        self._isPaused = False
        self._isActive = False
        for i in range(self._Interfaces.rowCount()):
            self._Interfaces.item(i).close()
                
        for i in range(self._Systems.rowCount()):
            self._Systems.item(i).close()
            
        Qthread.close(self)
        
class EngineWidget(QWidget):
    
    def __init__(self):
        
        # components
        wStartButton
        wPauseButton
            