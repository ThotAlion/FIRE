from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import Tools
import pickle
import csv

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
    
    def toDictCSV(self):
        a = []
        for pose in self.poseList:
            b = {}
            b["Name"] = pose["name"]
            b["Duration"] = pose["duration"]
            for obj in pose["objectives"].objectiveList:
                if obj["nature"] == "M":
                    b[obj["name"]] =   "M"
                elif obj["nature"] == "PM":
                    b[obj["name"]] =   "P"
                elif obj["nature"] == "L":
                    b[obj["name"]] =   "L"+str(round(obj["consign"]*100)/100)
                elif obj["nature"] == "S":
                    b[obj["name"]] =   "S"+str(round(obj["consign"]*100)/100)
                elif obj["nature"] == "K":
                    b[obj["name"]] =   "K"
                elif obj["nature"] == "I":
                    b[obj["name"]] = str(round(obj["consign"]*100)/100)
            a.append(b)
        return a
    
    def fromDictCSV(self,a):
        print a
        self.poseList = []
        for pos in a:
            b = {}
            b["objectives"] = Objectives([])
            print b["objectives"].objectiveList
            for f in pos:
                if f == "Name":
                    b["name"] = pos[f]
                elif f == "Duration":
                    b["duration"] = pos[f]
                else:
                    c = {}
                    c["name"] = f
                    if pos[f][0] == "M":
                        c["nature"] = "M"
                        c["consign"] = "0.0"
                    elif pos[f][0] == "P":
                        c["nature"] = "PM"
                        c["consign"] = "0.0"
                    elif pos[f][0] == "K":
                        c["nature"] = "K"
                        c["consign"] = "0.0"
                    elif pos[f][0] == "L":
                        c["nature"] = "L"
                        c["consign"] = float(pos[f][1:])
                    elif pos[f][0] == "S":
                        c["nature"] = "S"
                        c["consign"] = float(pos[f][1:])
                    else:
                        c["nature"] = "I"
                        c["consign"] = float(pos[f])
                    b["objectives"].objectiveList.append(c)
            self.poseList.append(b)
            
    def fromDict(self,a):
        self.poseList = []
        for pos in a:
            b = {}
            b["name"] = pos["name"]
            b["duration"] = pos["duration"]
            b["objectives"] = Objectives()
            b["objectives"].fromDict(pos["objectives"])
            self.poseList.append(b)

class CSVRecorder(Block.Block,QWidget):
    """ this class describes a recorder """
    
    def __init__(self,members):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        # creation of inputs/outputs
        self.members = members
        for member in self.members:
            for ch in self.members[member]:
                self.inputs[ch] = Connexion()
                self.outputs[ch] = Connexion(default = NaN)
        self.outputs["Number"] = Connexion(default = "-1")
        self.outputs["Duration"] = Connexion(default = "1")
        self.outputs["Name"] = Connexion(default = "toto")
        self.number = 0
        
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
        self.connect(self.bSave,SIGNAL("pressed()"),self.saveCSV)
        self.connect(self.scCtrlS,SIGNAL("activated()"),self.saveCSV)
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
        for member in self.members:
            for ch in self.members[member]:
                obj = {}
                obj['name'] = ch
                obj['nature'] = 'L'
                obj['consign'] = float(self.robot[ch])
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
        self.number = self.number+1
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
    
    def saveCSV(self):
        a = self.poseList.toDictCSV()
        CSVFile = QFileDialog.getSaveFileName(self,"Save File",QDir.currentPath(),"move sequence (*.csv)");
        f = open(CSVFile,'w')
        head = ["Name","Duration"]
        for member in self.members:
            for ch in self.members[member]:
                head.append(ch)
        r = csv.DictWriter(f,delimiter = ';',lineterminator = '\n',fieldnames=head)
        r.writeheader()
        for row in a:
            r.writerow(row)
        f.close()
        
    def load(self):
        fileName = QFileDialog.getOpenFileName(self,"Open File",QDir.currentPath(),"move sequence (*.seq *.csv)");
        if fileName[-3:] == 'seq':
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            # transformation for shoulder_x
            a = pickle.load(file(fileName,'rb'))
            for p in a:
                for m in p["objectives"]:
                    if m["name"] == "r_shoulder_x":
                        m["consign"] = m["consign"]+90.0
                    if m["name"] == "l_shoulder_x":
                        m["consign"] = m["consign"]-90.0
                    if m["nature"] == "L":
                        m["nature"] = "S"
            self.poseList.fromDict(a)
            self.poseList.emit(SIGNAL("layoutChanged()"))
        elif fileName[-3:] == 'csv':
            a = []
            r = csv.DictReader(open(fileName,'r'),delimiter = ';')
            for row in r:
                a.append(row)
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.poseList.fromDictCSV(a)
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
        if fileName[-3:] == 'seq':
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            # transformation for shoulder_x
            a = pickle.load(file(fileName,'rb'))
            for p in a:
                for m in p["objectives"]:
                    if m["name"] == "r_shoulder_x":
                        m["consign"] = m["consign"]+90.0
                    if m["name"] == "l_shoulder_x":
                        m["consign"] = m["consign"]-90.0
                    if m["nature"] == "L":
                        m["nature"] = "S"
            self.poseList.fromDict(a)
            self.poseList.emit(SIGNAL("layoutChanged()"))
        elif fileName[-3:] == 'csv':
            a = []
            r = csv.DictReader(open(fileName,'r'),delimiter = ';')
            for row in r:
                a.append(row)
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.poseList.fromDictCSV(a)
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
        
    def init(self):
        print "This function is launched just before running"
    
    def getInputs(self,f):
        print "get inputs to deliver them in the reality."
        
    def setOutputs(self,f):
        # recup the position of the robot
        for member in self.members:
            for ch in self.members[member]:
                self.robot[ch] = self.inputs[ch].getValue(f)
        if self.iCurrentPose>=0 and self.iCurrentPose<=len(self.poseList.poseList)-1:
            t = Tools.getTime()
            tape = self.poseList.toDictCSV()
            
            duration = float(tape[self.iCurrentPose]["Duration"])/self.sbTimeScaling.value()
            #print [t,self.t0,duration,self.index]
            if (t-self.t0)>=duration and self.play == 1:
                if self.iCurrentPose<=len(tape)-2:
                    self.iCurrentPose = self.iCurrentPose+1
                    self.t0 = t
                    self.number = self.number+1
                elif self.cIsCycle.isChecked():
                    self.iCurrentPose = 0
                    self.t0 = t
                    self.number = self.number+1
                self.poseTable.selectRow(self.iCurrentPose)
            for name in tape[self.iCurrentPose]:
                if name == "Duration":
                    self.outputs["Duration"].setValue(str(round(duration*100)/100),f)
                else:
                    self.outputs[name].setValue(tape[self.iCurrentPose][name],f)
            self.outputs["Number"].setValue(str(self.number),f)
        return f
        