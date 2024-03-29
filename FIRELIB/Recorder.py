from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import Tools
import pickle

class Objectives(QAbstractTableModel):
    
    def __init__(self,objectiveList = []):
        QAbstractItemModel.__init__(self)
        self.headerdata = ["Name","Nature","Consign"]
        self.objectiveList = objectiveList
        
    def data(self,i,role):
        if i.row()>=len(self.objectiveList):
            return QVariant()
        else:
            obj = self.objectiveList[i.row()]
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if i.column() == 0:
                    return obj["name"]
                elif i.column() == 1:
                    return obj["nature"]
                elif i.column() == 2:
                    return str(obj["consign"])
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
            
    def setData(self,i,value,role):
        if i.isValid():
            if role == Qt.EditRole:
                if i.column() == 1:
                    self.objectiveList[i.row()]["nature"] = str(value.toString())
                if i.column() == 2:
                    self.objectiveList[i.row()]["consign"] = value.toDouble()[0]
                return True
        else:
            return False
    
    def flags(self,i):
        if i.isValid():
            if i.column() in [0]:
                f = Qt.ItemIsEnabled | Qt.ItemIsSelectable
            if i.column() in [1,2]:
                f = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return f
    def rowCount(self,parent=QModelIndex()):
        return len(self.objectiveList)
        
    def columnCount(self,parent=QModelIndex()):
        return 3
        
    def toDict(self):
        return self.objectiveList
    
    def fromDict(self,a):
        self.objectiveList = a
            
class Poses(QAbstractTableModel):
    
    def __init__(self,poseList = []):
        QAbstractItemModel.__init__(self)
        self.headerdata = ["Name","duration"]
        self.poseList = poseList
        
    def data(self,i,role):
        if not i.isValid():
            return QVariant()
        else:
            obj = self.poseList[i.row()]
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if i.column() == 0:
                    return obj["name"]
                elif i.column() == 1:
                    return str(obj["duration"])
            if role == Qt.BackgroundRole:
                if obj["name"][0]=="k":
                    return QBrush(Qt.blue)
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
    
    def setData(self,i,value,role):
        if i.isValid():
            if role == Qt.EditRole:
                if i.column() == 0:
                    self.poseList[i.row()]["name"] = str(value.toString())
                if i.column() == 1:
                    self.poseList[i.row()]["duration"] = value.toDouble()[0]
                return True
        else:
            return False
    
    def flags(self,i):
        if i.isValid():
            if i.column() in []:
                f = Qt.ItemIsEnabled | Qt.ItemIsSelectable
            if i.column() in [0,1]:
                f = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return f
            
    def rowCount(self,parent=QModelIndex()):
        return len(self.poseList)
        
    def columnCount(self,parent=QModelIndex()):
        return 2
        
    def toDict(self):
        a = []
        for pose in self.poseList:
            b = {}
            b["name"] = pose["name"]
            b["duration"] = pose["duration"]
            b["objectives"] = pose["objectives"].toDict()
            a.append(b)
        return a
    
    def fromDict(self,a):
        self.poseList = []
        for pos in a:
            b = {}
            b["name"] = pos["name"]
            b["duration"] = pos["duration"]
            b["objectives"] = Objectives()
            b["objectives"].fromDict(pos["objectives"])
            self.poseList.append(b)

class Recorder(Block.Block,QWidget):
    """ this class describes a recorder """
    
    def __init__(self,channelList):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        # creation of inputs/outputs
        for ch in channelList:
            self.inputs[ch] = Connexion()
            self.outputs[ch] = {}
            self.outputs[ch]["position"] = Connexion(default = NaN)
            self.outputs[ch]["speed"] = Connexion(default = 0.0)
        
        self.robot = {}
        
        self.poseList = Poses()
        self.history = []
        self.objectiveList = Objectives()
        self.backPose = Objectives()
        self.holdPose = {}
        self.loadBackPose('_mou.seq')
        
        self.t0 = Tools.getTime()
        self.iCurrentPose = -1
        self.play = 0
        
        # creation of components
        self.objTable = QTableView()
        self.poseTable = QTableView()
        self.poseTable.setModel(self.poseList)
        self.tapeTable = QTableView()
        self.tapeDir = QFileSystemModel()
        self.tapeDir.setRootPath(QDir.currentPath()+"/TAPES/")
        self.tapeTable.setModel(self.tapeDir)
        self.tapeTable.setRootIndex(self.tapeDir.index(QDir.currentPath()+"/TAPES/"))
        self.cBackPose = QComboBox()
        self.cBackPose.setModel(self.tapeDir)
        self.cBackPose.setRootModelIndex(self.tapeDir.index(QDir.currentPath()+"/TAPES/"))
        imou = self.tapeDir.index(QDir.currentPath()+"/TAPES/_mou.seq")
        self.cBackPose.setCurrentIndex(imou.row())
        self.bInsertPose = QPushButton("Insert current pose below")
        self.bCopyPose = QPushButton("Copy pose")
        self.bPastePose = QPushButton("Paste pose")
        self.bDeletePose = QPushButton("Delete pose")
        self.bPlayPose = QPushButton("Play")
        self.bReverse = QPushButton("Reverse")
        self.sbTimeScaling = QDoubleSpinBox()
        self.sbTimeScaling.setPrefix("Time scaling :")
        self.sbTimeScaling.setValue(1.0)
        self.sbTimeScaling.setSingleStep(0.1)
        self.sbTimeScaling.setMinimum(0.1)
        self.cIsCycle = QCheckBox("is a Cycle ?")
        self.bAcquireSelected = QPushButton("Acquire selected")
        self.bAcquireAll = QPushButton("Acquire All")
        self.bSave = QPushButton("Save")
        self.bLoad = QPushButton("Load")
        self.scCtrlC = QShortcut(QKeySequence("Ctrl+C"),self)
        self.scCtrlV = QShortcut(QKeySequence("Ctrl+V"),self)
        self.scCtrlS = QShortcut(QKeySequence("Ctrl+S"),self)
        self.scCtrlZ = QShortcut(QKeySequence("Ctrl+Z"),self)
        
        # composition
        mainlayout = QHBoxLayout(self)
        tapelayout = QVBoxLayout()
        tapelayout.addWidget(self.bSave)
        tapelayout.addWidget(self.bLoad)
        tapelayout.addWidget(self.cBackPose)
        tapelayout.addWidget(self.tapeTable)
        mainlayout.addLayout(tapelayout)
        poselayout = QVBoxLayout()
        poselayout.addWidget(self.bInsertPose)
        poselayout.addWidget(self.bCopyPose)
        poselayout.addWidget(self.bPastePose)
        poselayout.addWidget(self.bDeletePose)
        poselayout.addWidget(self.bPlayPose)
        poselayout.addWidget(self.bReverse)
        poselayout.addWidget(self.sbTimeScaling)
        poselayout.addWidget(self.cIsCycle)
        poselayout.addWidget(self.poseTable)
        mainlayout.addLayout(poselayout)
        objlayout = QVBoxLayout()
        objlayout.addWidget(self.bAcquireSelected)
        objlayout.addWidget(self.bAcquireAll)
        objlayout.addWidget(self.objTable)
        mainlayout.addLayout(objlayout)
        self.show()
    
        # signals
        self.connect(self.bInsertPose,SIGNAL("pressed()"),self.insertPose)
        self.connect(self.bCopyPose,SIGNAL("pressed()"),self.copyPose)
        self.connect(self.scCtrlC,SIGNAL("activated()"),self.copyPose)
        self.connect(self.bPastePose,SIGNAL("pressed()"),self.pastePose)
        self.connect(self.scCtrlV,SIGNAL("activated()"),self.pastePose)
        self.connect(self.poseTable,SIGNAL("clicked(QModelIndex)"),self.updateObjective)
        self.connect(self.tapeTable,SIGNAL("clicked(QModelIndex)"),self.loadSeq)
        self.connect(self.cBackPose,SIGNAL("currentIndexChanged(QString)"),self.loadBackPose)
        self.connect(self.bDeletePose,SIGNAL("pressed()"),self.deletePose)
        self.connect(self.bReverse,SIGNAL("pressed()"),self.reverse)
        self.connect(self.bPlayPose,SIGNAL("pressed()"),self.togglePlay)
        self.connect(self.bAcquireSelected,SIGNAL("pressed()"),self.acquireSelected)
        self.connect(self.bAcquireAll,SIGNAL("pressed()"),self.acquireAll)
        self.connect(self.bSave,SIGNAL("pressed()"),self.save)
        self.connect(self.scCtrlS,SIGNAL("activated()"),self.save)
        self.connect(self.bLoad,SIGNAL("pressed()"),self.load)
        self.connect(self.scCtrlZ,SIGNAL("activated()"),self.undo)
        self.connect(self.poseList,SIGNAL("layoutAboutToBeChanged()"),self.store)
        self.connect(self.objectiveList,SIGNAL("layoutAboutToBeChanged()"),self.store)

    def insertPose(self):
        i=self.poseTable.currentIndex().row()
        pose = {}
        pose["name"] = "toto"
        pose["duration"] = 1
        pose["objectives"] = Objectives([])
        for ch in self.inputs:
            obj = {}
            obj['name'] = ch
            obj['nature'] = 'L'
            obj['consign'] = self.robot[ch]
            pose["objectives"].objectiveList.append(obj)
        
        self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.poseList.poseList.insert(i+1,pose)
        self.poseList.emit(SIGNAL("layoutChanged()"))
        self.updateObjective(i+1)
    
    def copyPose(self):
        i=self.poseTable.currentIndex().row()
        pose_model = self.poseList.poseList[i]
        objs = pose_model["objectives"].objectiveList
        self.holdPose = {}
        self.holdPose["name"] = pose_model["name"]
        self.holdPose["duration"] = pose_model["duration"]
        self.holdPose["objectives"] = Objectives([])
        for obj in objs:
            self.holdPose["objectives"].objectiveList.append(obj.copy())
            
    def pastePose(self):
        i=self.poseTable.currentIndex().row()
        if i>=0 and len(self.holdPose)>0:
            pose_model = self.holdPose
            objs = pose_model["objectives"].objectiveList
            pose = {}
            pose["name"] = pose_model["name"]
            pose["duration"] = pose_model["duration"]
            pose["objectives"] = Objectives([])
            for obj in objs:
                pose["objectives"].objectiveList.append(obj.copy())
            
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.poseList.poseList.insert(i+1,pose)
            self.poseList.emit(SIGNAL("layoutChanged()"))
            self.updateObjective(i+1)
            
    def undo(self):
        if len(self.history)>1:
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.history.pop(-1)
            self.poseList.fromDict(self.history[-1])
            self.poseList.emit(SIGNAL("layoutChanged()"))
            
    def store(self):
        self.history.append(self.poseList.toDict())
    
    def copyPoseOld(self):
        i=self.poseTable.currentIndex().row()
        pose_model = self.poseList.poseList[i]
        objs = pose_model["objectives"].objectiveList
        pose = {}
        pose["name"] = pose_model["name"]
        pose["duration"] = pose_model["duration"]
        pose["objectives"] = Objectives([])
        for obj in objs:
            pose["objectives"].objectiveList.append(obj.copy())
        
        self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.poseList.poseList.insert(i+1,pose)
        self.poseList.emit(SIGNAL("layoutChanged()"))
        self.updateObjective(i+1)
        
    def deletePose(self):
        i=self.poseTable.currentIndex().row()
        if i>=0 and i<=len(self.poseList.poseList)-1:
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.poseList.poseList.pop(i)
            self.poseList.emit(SIGNAL("layoutChanged()"))
            self.updateObjective(i)
        
    def updateObjective(self,i):
        if type(i) is QModelIndex:
            i = i.row()
        self.objTable.setModel(self.poseList.poseList[i]["objectives"])
        self.t0 = Tools.getTime()
        self.iCurrentPose = i
        self.initPos = self.robot.copy()
        self.poseTable.selectRow(i)
        
    def togglePlay(self):
        if self.play == 0:
            self.play = 1
            self.bPlayPose.setText("Stop")
        else:
            self.play = 0
            self.bPlayPose.setText("Play")
    
    def reverse(self):
        self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.poseList.poseList.reverse()
        self.poseList.emit(SIGNAL("layoutChanged()"))
        self.t0 = Tools.getTime()
        self.iCurrentPose = 0
        self.initPos = self.robot.copy()
        self.updateObjective(0)
    
    def acquireSelected(self):
        iobj = self.objTable.currentIndex().row()
        ipose = self.poseTable.currentIndex().row()
        name = self.poseList.poseList[ipose]["objectives"].objectiveList[iobj]["name"]
        self.poseList.poseList[ipose]["objectives"].emit(SIGNAL("layoutAboutToBeChanged()"))
        self.poseList.poseList[ipose]["objectives"].objectiveList[iobj]["consign"] = self.robot[name]
        self.poseList.poseList[ipose]["objectives"].emit(SIGNAL("layoutChanged()"))
        
    def acquireAll(self):
        ipose = self.poseTable.currentIndex().row()
        self.poseList.poseList[ipose]["objectives"].emit(SIGNAL("layoutAboutToBeChanged()"))
        for obj in self.poseList.poseList[ipose]["objectives"].objectiveList:
            name = obj["name"]
            obj["consign"] = self.robot[name]
        self.poseList.poseList[ipose]["objectives"].emit(SIGNAL("layoutChanged()"))
            
    
    def save(self):
        fileName = QFileDialog.getSaveFileName(self,"Save File",QDir.currentPath(),"move sequence (*.seq)");
        pickle.dump(self.poseList.toDict(),file(fileName,'wb'))
        
    def load(self):
        fileName = QFileDialog.getOpenFileName(self,"Open File",QDir.currentPath(),"move sequence (*.seq)");
        self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.poseList.fromDict(pickle.load(file(fileName,'rb')))
        self.poseList.emit(SIGNAL("layoutChanged()"))
        self.t0 = Tools.getTime()
        self.iCurrentPose = 0
        self.updateObjective(0)
        self.initPos = self.robot.copy()
        if self.play == 1:
            self.togglePlay()
        if self.cIsCycle.isChecked():
            self.cIsCycle.setCheckState(Qt.Unchecked)
        
    
    def loadSeq(self,i):
        fileName = self.tapeDir.filePath(i)
        self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.poseList.fromDict(pickle.load(file(fileName,'rb')))
        self.poseList.emit(SIGNAL("layoutChanged()"))
        self.t0 = Tools.getTime()
        self.iCurrentPose = 0
        self.updateObjective(0)
        self.initPos = self.robot.copy()
        if self.play == 1:
            self.togglePlay()
        if self.cIsCycle.isChecked():
            self.cIsCycle.setCheckState(Qt.Unchecked)
    
    def loadBackPose(self,filename):
        a = pickle.load(file(QDir.currentPath()+"/TAPES/"+filename,'rb'))
        self.backPose.fromDict(a[0]["objectives"])
        
    
    def start(self):
        a=1
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        print "get inputs to deliver them in the reality."
        
    def setOutputs(self,f):
        # recup the position of the robot
        for ch in self.inputs:
            self.robot[ch] = self.inputs[ch].getValue(f)
        
        if self.iCurrentPose>=0 and self.iCurrentPose<=len(self.poseList.poseList)-1:
            pose = self.poseList.poseList[self.iCurrentPose]
            xt = (Tools.getTime()-self.t0)/(pose["duration"]/self.sbTimeScaling.value())
            xt = min(xt,1)
            for obj in self.backPose.objectiveList:
                if obj["nature"] == 'M':
                    self.outputs[obj["name"]]["position"].setValue(NaN,f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)
                elif obj["nature"] == 'PM':
                    self.outputs[obj["name"]]["position"].setValue(self.robot[obj["name"]],f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)
                elif obj["nature"] == 'L':
                    delta = obj["consign"] - self.initPos[obj["name"]]
                    self.outputs[obj["name"]]["position"].setValue(obj["consign"],f)
                    self.outputs[obj["name"]]["speed"].setValue(delta/(pose["duration"]/self.sbTimeScaling.value()),f)
                elif obj["nature"] == 'S':
                    delta = obj["consign"] - self.initPos[obj["name"]]
                    a = -2*delta
                    b = 3*delta
                    x = self.initPos[obj["name"]] + a*xt*xt*xt+b*xt*xt
                    self.outputs[obj["name"]]["position"].setValue(x,f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)
                elif obj["nature"] == 'K':
                    x = self.initPos[obj["name"]]
                    self.outputs[obj["name"]]["position"].setValue(x,f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)
            
            for obj in pose["objectives"].objectiveList:
                if obj["nature"] == 'PM':
                    self.outputs[obj["name"]]["position"].setValue(self.robot[obj["name"]],f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)
                elif obj["nature"] == 'L':
                    delta = obj["consign"] - self.initPos[obj["name"]]
                    self.outputs[obj["name"]]["position"].setValue(obj["consign"],f)
                    self.outputs[obj["name"]]["speed"].setValue(delta/(pose["duration"]/self.sbTimeScaling.value()),f)
                elif obj["nature"] == 'S':
                    delta = obj["consign"] - self.initPos[obj["name"]]
                    a = -2*delta
                    b = 3*delta
                    x = self.initPos[obj["name"]] + a*xt*xt*xt+b*xt*xt
                    self.outputs[obj["name"]]["position"].setValue(x,f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)
                elif obj["nature"] == 'K':
                    x = self.initPos[obj["name"]]
                    self.outputs[obj["name"]]["position"].setValue(x,f)
                    self.outputs[obj["name"]]["speed"].setValue(0,f)        
                    
            if xt == 1 and self.play == 1:
                if self.iCurrentPose<=len(self.poseList.poseList)-2:
                    self.iCurrentPose = self.iCurrentPose+1
                    self.t0 = Tools.getTime()
                    self.initPos = self.robot.copy()
                elif self.cIsCycle.isChecked():
                    self.iCurrentPose = 0
                    self.t0 = Tools.getTime()
                    self.initPos = self.robot.copy()
                self.updateObjective(self.iCurrentPose)
        return f
        