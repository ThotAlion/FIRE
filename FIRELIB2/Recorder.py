from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import Tools

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
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
    
    def setData(self,i,value,role):
        if i.isValid():
            if role == Qt.EditRole:
                if i.column() == 1:
                    self.poseList[i.row()]["duration"] = value.toDouble()[0]
                return True
        else:
            return False
    
    def flags(self,i):
        if i.isValid():
            if i.column() in [0]:
                f = Qt.ItemIsEnabled | Qt.ItemIsSelectable
            if i.column() in [1]:
                f = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return f
            
    def rowCount(self,parent=QModelIndex()):
        return len(self.poseList)
        
    def columnCount(self,parent=QModelIndex()):
        return 2

class Recorder(Block.Block,QWidget):
    """ this class describes a recorder """
    
    def __init__(self,channelList):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        # creation of inputs/outputs
        for ch in channelList:
            self.inputs[ch] = Connexion()
            self.outputs[ch] = Connexion(default = NaN)
        
        self.robot = {}
        
        self.poseList = Poses()
        self.objectiveList = Objectives()
        
        self.t0 = Tools.getTime()
        self.iCurrentPose = -1
        self.play = 0
        
        # creation of components
        self.objTable = QTableView()
        self.poseTable = QTableView()
        self.poseTable.setModel(self.poseList)
        self.tapeTable = QTableView()
        self.bInsertPose = QPushButton("Insert pose below")
        self.bDeletePose = QPushButton("Delete pose")
        self.bPlayPose = QPushButton("Play")
        self.bAcquireAll = QPushButton("Acquire all")
        self.bAcquireSelected = QPushButton("Acquire selected")
        
        # composition
        mainlayout = QHBoxLayout(self)
        poselayout = QVBoxLayout()
        poselayout.addWidget(self.bInsertPose)
        poselayout.addWidget(self.bDeletePose)
        poselayout.addWidget(self.bPlayPose)
        poselayout.addWidget(self.poseTable)
        mainlayout.addWidget(self.tapeTable)
        mainlayout.addLayout(poselayout)
        mainlayout.addWidget(self.objTable)
        self.show()
    
        # signals
        self.connect(self.bInsertPose,SIGNAL("pressed()"),self.insertPose)
        self.connect(self.poseTable,SIGNAL("clicked(QModelIndex)"),self.updateObjective)
        self.connect(self.bDeletePose,SIGNAL("pressed()"),self.deletePose)
        self.connect(self.bPlayPose,SIGNAL("pressed()"),self.togglePlay)

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
        
    def deletePose(self):
        i=self.poseTable.currentIndex().row()
        if i>=0 and i<=len(self.poseList.poseList)-1:
            self.poseList.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.poseList.poseList.pop(i)
            self.poseList.emit(SIGNAL("layoutChanged()"))    
        
    def updateObjective(self,i):
        self.objTable.setModel(self.poseList.poseList[i.row()]["objectives"])
        self.t0 = Tools.getTime()
        self.iCurrentPose = i.row()
        self.initPos = self.robot.copy()
        
    def togglePlay(self):
        if self.play == 0:
            self.play = 1
            self.bPlayPose.setText("Stop")
        else:
            self.play = 0
            self.bPlayPose.setText("Play")

    
    def start(self):
        self.active = True
        
    def init(self):
        print "This function is launched just before running"
    
    def getInputs(self,f):
        print "get inputs to deliver them in the reality."
        
    def setOutputs(self,f):
        # recup the position of the robot
        for ch in self.inputs:
            self.robot[ch] = self.inputs[ch].getValue(f)
        
        if self.iCurrentPose>=0 and self.iCurrentPose<=len(self.poseList.poseList)-1:
            pose = self.poseList.poseList[self.iCurrentPose]
            xt = (Tools.getTime()-self.t0)/pose["duration"]
            xt = min(xt,1)
            for obj in pose["objectives"].objectiveList:
                if obj["nature"] == 'M':
                    self.outputs[obj["name"]].setValue(NaN,f)
                elif obj["nature"] == 'PM':
                    self.outputs[obj["name"]].setValue(self.robot[obj["name"]],f)
                elif obj["nature"] == 'L':
                    delta = obj["consign"] - self.initPos[obj["name"]]
                    x = self.initPos[obj["name"]] + delta*xt
                    self.outputs[obj["name"]].setValue(x,f)
                elif obj["nature"] == 'S':
                    delta = obj["consign"] - self.initPos[obj["name"]]
                    a = -2*delta
                    b = 3*delta
                    x = self.initPos[obj["name"]] + a*xt*xt*xt+b*xt*xt
                    self.outputs[obj["name"]].setValue(x,f)
            if xt == 1 and self.play == 1:
                if self.iCurrentPose<=len(self.poseList.poseList)-2:
                    self.iCurrentPose = self.iCurrentPose+1
                    self.t0 = Tools.getTime()
                    self.initPos = self.robot.copy()
        return f
        