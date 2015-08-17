from PyQt4.QtGui import *
from PyQt4.QtCore import *
from System import System
from Connexion import Connexion
from numpy import *
import pickle

class Recorder(System):
    """This system is a set of connexions. But it can record the inputs function of time to restore them as outputs"""
    
    def __init__(self,name = "Recorder"):
        """constructor"""
        System.__init__(self,name=name,icon=QIcon("FIRELIB/icons/recorder.png"))
        self.fileName = ""
        self.tInit = 0.0
        self.controlWidget = recorderControlWidget(self)
        self.configWidget = recorderConfigWidget(self)

    def start(self):
        self.executionState = self.RUNNING
        self.taskState = self.PROGRESS
        
    def close(self):
        self.executionState = self.READY
        self.taskState = self.STOPPED
        
    def deliverOutputs(self,channels):
        for i in range(self._outputs.rowCount()):
            # warning, a QString is returned and the replace method is overloaded (and not the same...)
            outputname = str(self._outputs.invisibleRootItem().child(i,0).text())
            inputname = outputname.replace("output","input")
            a = self._inputs.getConnexion(inputname,channels)
            channels = self._outputs.setConnexion(outputname,a,channels)
        return channels
        
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
        #self.tapeDir.setNameFilters(["*.tap"])
        self.wFileName.setModel(self.tapeDir)
        self.wFileName.setRootModelIndex(self.tapeDir.index(QDir.currentPath()+"/TAPES/"))
        self.wFileName.clearEditText()
        self.wAddConnexion = QPushButton("Add connexion")
        self.wEditAddConnexion = QLineEdit("")
        self.wRemoveConnexion = QPushButton("Remove connexion:")
        self.wComboRemoveConnexion = QComboBox()
        self.wComboRemoveConnexion.setModel(self.inputs)
        
        # widget setup
        self.setFixedSize(300,200)
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
        
        # connect the signals
        self.connect(self.wAddConnexion,SIGNAL("pressed()"),self.addCon)
        self.connect(self.wRemoveConnexion,SIGNAL("pressed()"),self.removeCon)
        
    def removeCon(self):
        i = self.wComboRemoveConnexion.currentIndex()
        self.parent.removeConnexion(i)
        
    def addCon(self):
        name = str(self.wEditAddConnexion.text())
        if len(name)>0:
            self.parent.addConnexion(name)
        
        
class recorderControlWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        return
        