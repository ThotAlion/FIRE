from PyQt4.QtGui import *
from PyQt4.QtCore import *
from System import System
import Tools
import time
from Connexion import Connexion
from numpy import *
import cPickle as pickle
import os.path
import pyqtgraph

class Recorder(System):
    """This system is a set of connexions. But it can record the inputs function of time to restore them as outputs"""
    
    def __init__(self,name = "Recorder"):
        """constructor"""
        System.__init__(self,name=name,icon=QIcon("FIRELIB/icons/recorder.png"))
        self.fileName = ""
        self.tStartPlay = 0.0
        self.time = 0.0
        self.tStartRec = 0
        self.data = {}
        self.RECORDING = "RECORDING"
        self.isRecording = False
        self.controlWidget = recorderControlWidget(self)
        self.configWidget = recorderConfigWidget(self)
        self.executionState = self.NOTREADY

    def start(self):
        
        self.executionState = self.READY
        
    def init(self):
        path = str(QDir.currentPath()+"/TAPES/"+self.fileName)
        if os.path.isfile(path):
            self.data = pickle.load(file(str(QDir.currentPath()+"/TAPES/"+self.fileName),'rb'))
            self.tStartPlay = Tools.getTime()
        else:
            self.data = {}
        
    def close(self):
        self.executionState = self.FINISHED
        
    def deliverOutputs(self,channels):
        if self.isRecording:
            t = Tools.getTime()-self.tStartRec
            if not self.data.has_key("time"):
                self.data["time"] = []
            for i in range(self._inputs.rowCount()):
                input = self._inputs.item(i)
                input.updateInput(channels)
                inputname = str(input.text())
                if not self.data.has_key(inputname):
                    self.data[inputname] = []
                self.data[inputname].append(input.value[0])
                self.data["time"].append(t)
                
        elif len(self.data)>0:
            # identify the index to pickup the data
            t = Tools.getTime()-self.tStartPlay
            time = array(self.data["time"])
            if t<=max(time):
                # take the data and copy it on each output
                
                for i_output in range(self._outputs.rowCount()):
                    output = self._outputs.item(i_output)
                    outname = str(output.text())
                    vect = array(self.data[outname])
                    minlen = min(len(time),len(vect))
                    val = interp(t,time[0:minlen],vect[0:minlen])
                    output.value = val
                    output.updateOutput(channels)
            else:
                self.executionState = self.FINISHED
        return channels
                    
    def startRecord(self):
        self.tStartRec = Tools.getTime()
        self.data = {}
        self.isRecording = True
        
    def endRecord(self):
        if self.isRecording == True:
            time.sleep(0.5)
            # securise the data tree
            # globalLen = Inf
            # for f in self.data:
                # globalLen = min(globalLen,len(self.data[f]))
            # for f in self.data:
                # self.data[f] = self.data[f][0:globalLen]
            # save the file
            pickle.dump(self.data,file(str(QDir.currentPath()+"/TAPES/"+self.fileName),'wb'),protocol=-1)
            self.isRecording = False
            
        
    def startPlay(self):
        if self.isRecording == False:
            self.tStartPlay = Tools.getTime()
            self.data = pickle.load(file(str(QDir.currentPath()+"/TAPES/"+self.fileName),'rb'))
            self.executionState = self.RUNNING
    
    def setFileName(self,name):
        # try to open the file
        self.fileName = name
        path = str(QDir.currentPath()+"/TAPES/"+self.fileName)
        if os.path.isfile(path):
            self.data = pickle.load(file(path,'rb'))
            # add the missing connexions
            for field in self.data.keys():
                if not field == "time":
                    self.addConnexion(field)
            # and remove
            i_input = 0
            while i_input < self._inputs.rowCount():
                input = self._inputs.item(i_input)
                if not str(input.text()) in self.data.keys():
                    self.removeConnexion(i_input)
                else:
                    i_input = i_input+1
        else:
            self.data = {}
        
    def addConnexion(self,name):
        listCon = []
        for i in range(self._inputs.rowCount()):
            listCon.append(str(self._inputs.item(i).text()))
        if not name in listCon:
            self._inputs.invisibleRootItem().appendRow(Connexion(name,direction=Connexion.IN,
                description = "Signal storing "+name,
                unit = "WU",
                connectedTo="",
                valueInit = 0.0, 
                valueMin = -Inf, 
                valueMax = Inf))
                
            self._outputs.invisibleRootItem().appendRow(Connexion(name,direction=Connexion.OUT,
                description = "output of "+name+" from the tape",
                unit = "WU",
                connectedTo="",
                valueInit = 0.0, 
                valueMin = -Inf, 
                valueMax = Inf))
            
    def removeConnexion(self,i):
        self._inputs.invisibleRootItem().takeRow(i)
        self._outputs.invisibleRootItem().takeRow(i)
        
    def writeConf(self):
        conf = System.writeConf(self)
        conf["fileName"] = self.fileName
        return conf
        
    def readConf(self,conf):
        System.readConf(self,conf)
        self.setFileName(conf["fileName"])
        
        
    
    
class recorderConfigWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        self.inputs = parent._inputs
        self.outputs = parent._outputs
        self.parent = parent
        # list of components
        self.wLabelTitle = QLabel("System : Recorder")
        self.setToolTip("This system record and plays trajectories stored in a file.")
        self.wFileNameLabel = QLabel("File name :")
        self.wFileName = QComboBox()
        self.wFileName.setEditable(True)
        self.tapeDir = QFileSystemModel()
        self.tapeDir.setRootPath(QDir.currentPath()+"/TAPES/")
        self.tapeDir.setNameFilters(["*.tap"])
        self.wFileName.setModel(self.tapeDir)
        self.wFileName.setRootModelIndex(self.tapeDir.index(QDir.currentPath()+"/TAPES/"))
        self.wFileName.clearEditText()
        self.wAddConnexion = QPushButton("Add connexion")
        self.wEditAddConnexion = QLineEdit("")
        self.wRemoveConnexion = QPushButton("Remove connexion:")
        self.wComboRemoveConnexion = QComboBox()
        self.wComboRemoveConnexion.setModel(self.inputs)
        self.wplot = pyqtgraph.PlotWidget()
        
        # widget setup
        self.setFixedSize(500,500)
        self.mainlayout = QVBoxLayout(self)
        self.filelayout = QHBoxLayout()
        self.filelayout.addWidget(self.wFileNameLabel)
        self.filelayout.addWidget(self.wFileName)
        self.addlayout = QHBoxLayout()
        self.addlayout.addWidget(self.wAddConnexion)
        self.addlayout.addWidget(self.wEditAddConnexion)
        self.remLayout = QHBoxLayout()
        self.remLayout.addWidget(self.wRemoveConnexion)
        self.remLayout.addWidget(self.wComboRemoveConnexion)
        
        self.mainlayout.addWidget(self.wLabelTitle)
        self.mainlayout.addLayout(self.filelayout)
        self.mainlayout.addLayout(self.addlayout)
        self.mainlayout.addLayout(self.remLayout)
        self.mainlayout.addWidget(self.wplot)
        
        # connect the signals
        self.connect(self.wAddConnexion,SIGNAL("pressed()"),self.addCon)
        self.connect(self.wRemoveConnexion,SIGNAL("pressed()"),self.removeCon)
        self.connect(self.wFileName,SIGNAL("editTextChanged(QString)"),parent.setFileName)
        self.connect(self.wFileName,SIGNAL("editTextChanged(QString)"),self.updatePlot)
        
    def removeCon(self):
        i = self.wComboRemoveConnexion.currentIndex()
        self.parent.removeConnexion(i)
        
    def addCon(self):
        name = str(self.wEditAddConnexion.text())
        if len(name)>0:
            self.parent.addConnexion(name)
            
    def updatePlot(self):
        time.sleep(1)
        data = self.parent.data
        if len(data)>0:
            self.wplot.clear()
            for v in data:
                if not v is "time":
                    self.wplot.plot(data["time"],data[v],'w')
        
        
class recorderControlWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        self.inputs = parent._inputs
        self.outputs = parent._outputs
        self.parent = parent
        # components
        self.wLabelTitle = QLabel("System : Recorder")
        self.wRecord = QPushButton("Record")
        self.wStop = QPushButton("Stop")
        self.wPlay = QPushButton("Play")
        self.wPause = QPushButton("Pause")
        
        
        # widget setup
        self.setFixedSize(300,200)
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addWidget(self.wLabelTitle)
        self.mainlayout.addWidget(self.wRecord)
        self.mainlayout.addWidget(self.wStop)
        self.mainlayout.addWidget(self.wPlay)
        self.mainlayout.addWidget(self.wPause)
        
        #signals
        self.connect(self.wRecord,SIGNAL("pressed()"),parent.startRecord)
        self.connect(self.wStop,SIGNAL("pressed()"),parent.endRecord)
        self.connect(self.wPlay,SIGNAL("pressed()"),parent.startPlay)
        