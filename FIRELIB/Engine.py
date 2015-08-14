from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import Tools

class Engine(QThread):
    """ This class is the engine of FIRE application during its execution."""
    
    def __init__(self,parent,interfaces,systems,channels):
        QThread.__init__(self,parent)
        self._Interfaces = interfaces
        self._Systems = systems
        self._Channels = channels
        self.samplingPeriod = 0.02
        self._isActive = True
        self._isPaused = False
        self.engineWidget = EngineWidget(self)
    
    def start(self):
        for i in range(self._Interfaces.rowCount()):
            if not self._Interfaces.item(i).executionState == self._Interfaces.item(i).RUNNING:
                try:
                    self._Interfaces.item(i).start()
                    self._Interfaces.item(i).executionState = self._Interfaces.item(i).RUNNING
                except Exception,e:
                    self._Interfaces.item(i).executionState = self._Interfaces.item(i).ERROR
                    print e
                
        for i in range(self._Systems.rowCount()):
            if not self._Systems.item(i).executionState == self._Systems.item(i).RUNNING:
                try:
                    self._Systems.item(i).start()
                    self._Systems.item(i).executionState = self._Interfaces.item(i).RUNNING
                except Exception,e:
                    self._Systems.item(i).executionState = self._Interfaces.item(i).ERROR
        self._isActive = True
        self._isPaused = False
        QThread.start(self)
    
    def run(self):
        try:
            while self._isActive:
                while self._isPaused:
                    self.wait(100)
                t0 = Tools.getTime()
                
                for i in range(self._Interfaces.rowCount()):
                    if self._Interfaces.item(i).executionState == self._Interfaces.item(i).RUNNING:
                        self._Channels = self._Interfaces.item(i).deliverOutputs(self._Channels)
               
                for i in range(self._Systems.rowCount()):
                    if self._Systems.item(i).executionState == self._Systems.item(i).RUNNING:
                        self._Channels = self._Systems.item(i).deliverOutputs(self._Channels)
                
                for i in range(self._Interfaces.rowCount()):
                    if self._Interfaces.item(i).executionState == self._Interfaces.item(i).RUNNING:
                        self._Interfaces.item(i).receiveInputs(self._Channels)
                
                while Tools.getTime()-t0<self.samplingPeriod:
                    a=1
        except:
            (type,value,traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)    
                
    def close(self):
        self._isPaused = False
        self._isActive = False
        for i in range(self._Interfaces.rowCount()):
            self._Interfaces.item(i).close()
                
        for i in range(self._Systems.rowCount()):
            self._Systems.item(i).close()
        
    def togglePause(self):
        if self._isPaused == True:
            self._isPaused = False
        else:
            self._isPaused = True
            
    def setSamplingTime(self,T):
        self.samplingPeriod = T/1000
        
class EngineWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        # components
        self.wStartButton = QPushButton("Start")
        self.wPauseButton = QPushButton("Pause")
        self.wStopButton = QPushButton("Stop")
        self.wSamplingTime = QDoubleSpinBox()
        self.wSamplingTime.setMinimum(0)
        self.wSamplingTime.setMaximum(10000)
        self.wSamplingTime.setValue(parent.samplingPeriod*1000)
        
        
        self.wSamplingTimeLabel = QLabel("Sampling Time (ms): ")
        
        # widget organisation
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.wStartButton)
        buttonLayout.addWidget(self.wPauseButton)
        buttonLayout.addWidget(self.wStopButton)
        samplingLayout = QHBoxLayout()
        samplingLayout.addWidget(self.wSamplingTime)
        samplingLayout.addWidget(self.wSamplingTimeLabel)
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(samplingLayout)
        
        # connect the signals
        self.connect(self.wStartButton,SIGNAL("pressed()"),parent.start)
        self.connect(self.wPauseButton,SIGNAL("pressed()"),parent.togglePause)
        self.connect(self.wStopButton,SIGNAL("pressed()"),parent.close)
        self.connect(self.wSamplingTime,SIGNAL("valueChanged(double)"),parent.setSamplingTime)
        
        
            