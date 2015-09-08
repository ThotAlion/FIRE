from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Objectives(QStandardItemModel):
    
    def __init__(self):
        QStandardItemModel.__init__(self,objectiveList = [])
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
            
class Poses(QStandardItemModel)
    
    def __init__(self):
        QStandardItemModel.__init__(self,poseList = [])
        self.setHorizontalHeaderLabels(["Name","duration"])
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
                    return obj["duration"]
                
    def setData(self,i,value,role):
        if i.isValid():
            if role == Qt.EditRole:
                if i.column() == 1:
                    self.objectiveList[i.row()]["duration"] = str(value.toString())
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
            

class Recorder(Block.Block,QWidget):
    """ this class describes a recorder """
    
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self._active = False
        self.show()
    
    
    def start(self):
        print "This function is launched when the system is started"
        
    def init(self):
        print "This function is launched just before running"
    
    def getInputs(self,f):
        print "get inputs to deliver them in the reality."
        
    def setOutputs(self,f):
        print "set outputs in the data flow."
        