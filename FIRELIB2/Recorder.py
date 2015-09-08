from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *

class Objectives(QAbstractItemModel):
    
    def __init__(self,objectiveList = []):
        QAbstractItemModel.__init__(self)
        self.setHorizontalHeaderLabels(["Name","Nature","Consign"])
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
                    return obj["consign"]
                
    def setData(self,i,value,role):
        if i.isValid():
            if role == Qt.EditRole:
                if i.column() == 1:
                    self.objectiveList[i.row()]["nature"] = str(value.toString())
                if i.column() == 2:
                    self.objectiveList[i.row()]["consign"] = value.toDouble()
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
            
class Poses(QAbstractItemModel):
    
    def __init__(self,poseList = []):
        QAbstractItemModel.__init__(self)
        #self.setHorizontalHeaderLabels(["Name","duration"])
        self.setColumnCount(2)
        self.poseList = poseList
        
    def data(self,i,role):
        return "toto"
        # if not i.isValid():
            # return QVariant()
        # else:
            # obj = self.poseList[i.row()]
            # if role == Qt.DisplayRole or role == Qt.EditRole:
                # if i.column() == 0:
                    # return obj["name"]
                # elif i.column() == 1:
                    # return str(obj["duration"])
                
    # def setData(self,i,value,role):
        # if i.isValid():
            # if role == Qt.EditRole:
                # if i.column() == 1:
                    # self.poseList[i.row()]["duration"] = str(value.toString())
                # return True
        # else:
            # return False
    
    def flags(self,i):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        # if i.isValid():
            # if i.column() in [0]:
                # f = Qt.ItemIsEnabled | Qt.ItemIsSelectable
            # if i.column() in [1]:
                # f = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            # return f
            
    def rowCount(self,parent=QModelIndex()):
        return len(self.poseList)

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
        
        # creation of components
        self.objTable = QTableView()
        self.objTable.setModel(self.objectiveList)
        self.poseTable = QTableView()
        self.poseTable.setModel(self.poseList)
        self.tapeTable = QTableView()
        self.bInsertPose = QPushButton("Insert pose below")
        self.bDeletePose = QPushButton("Delete pose")
        self.bPlayPose = QPushButton("Play pose")
        self.bAcquireAll = QPushButton("Acquire all")
        self.bAcquireSelected = QPushButton("Acquire selected")
        
        # composition
        mainlayout = QHBoxLayout(self)
        poselayout = QVBoxLayout()
        poselayout.addWidget(self.bInsertPose)
        poselayout.addWidget(self.poseTable)
        mainlayout.addWidget(self.tapeTable)
        mainlayout.addLayout(poselayout)
        mainlayout.addWidget(self.objTable)
        self.show()
    
        # signals
        self.connect(self.bInsertPose,SIGNAL("pressed()"),self.insertPose)
    
    
    def insertPose(self):
        pose = {}
        pose["name"] = "toto"
        pose["duration"] = 1
        pose["objectives"] = Objectives()
        for ch in self.inputs:
            obj = {}
            obj['name'] = ch
            obj['nature'] = 'L'
            obj['consign'] = self.robot[ch]
            pose["objectives"].objectiveList.append(obj)
        self.poseList.poseList.append(pose)
        #self.poseList.reset()
        print self.poseList.poseList

    
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
        #print self.robot
        return f
        