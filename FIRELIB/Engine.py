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
        self.interfaceTimer = QTimer()
        
    
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
                    self._Systems.item(i).executionState = self._Systems.item(i).RUNNING
                except Exception,e:
                    self._Systems.item(i).executionState = self._Systems.item(i).ERROR
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
                t1 = Tools.getTime()

                for i in range(self._Systems.rowCount()):
                    if self._Systems.item(i).executionState == self._Systems.item(i).RUNNING:
                        self._Channels = self._Systems.item(i).deliverOutputs(self._Channels)
                t2 = Tools.getTime()        
                
                
                for i in range(self._Interfaces.rowCount()):
                    if self._Interfaces.item(i).executionState == self._Interfaces.item(i).RUNNING:
                        self._Interfaces.item(i).receiveInputs(self._Channels)
                t3 = Tools.getTime()
                # print "t1:"+str(t1-t0)
                # print "t2:"+str(t2-t1)
                # print "t3:"+str(t3-t2)
                
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
        
    def toggleAutoUpdate(self,val):
        if val == Qt.Checked:
            self.interfaceTimer.start(100)
        else:
            self.interfaceTimer.stop()
        
class EngineWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        # components
        self.wStartButton = QPushButton("Start")
        self.wPauseButton = QPushButton("Pause")
        self.wStopButton = QPushButton("Stop")
        self.wSamplingTime = QDoubleSpinBox()
        self.wAutoUpdate = QCheckBox("Real-time interface")
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
        samplingLayout.addWidget(self.wAutoUpdate)
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(samplingLayout)
        
        # connect the signals
        self.connect(self.wStartButton,SIGNAL("pressed()"),parent.start)
        self.connect(self.wPauseButton,SIGNAL("pressed()"),parent.togglePause)
        self.connect(self.wStopButton,SIGNAL("pressed()"),parent.close)
        self.connect(self.wSamplingTime,SIGNAL("valueChanged(double)"),parent.setSamplingTime)
        self.connect(self.wAutoUpdate,SIGNAL("stateChanged(int)"),parent.toggleAutoUpdate)
        
        
        
            