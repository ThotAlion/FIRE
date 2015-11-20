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
                t0 = Tools.getTime()
                self.Channels = self.Interfaces._setOutputs(self.Channels)
                self.Channels = self.Systems._setOutputs(self.Channels)
                self.Interfaces._getInputs(self.Channels)
                while Tools.getTime()-t0 <= self.samplingPeriod:
                    a=1
        except:
            (type,value,traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)