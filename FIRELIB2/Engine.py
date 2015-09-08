from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import time
import Tools


class Engine(QThread):
    """ This class is the engine of FIRE application during its execution."""
    
    def __init__(self,interfaces,systems,channels):
        QThread.__init__(self)
        self.Interfaces = interfaces
        self.Systems = systems
        self.Channels = channels
        self.samplingPeriod = 0.02
        
    def start(self):
        self.Interfaces.start()
        self.Systems.start()
        time.sleep(1)
        QThread.start(self)
        
    def run(self):
        try:
            while True:
                f = self.Interfaces.setOutputs(self.Channels)
                f = self.Systems.setOutputs(self.Channels)
                self.Interfaces.getInputs(self.Channels)
                time.sleep(self.samplingPeriod)
        except:
            (type,value,traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)