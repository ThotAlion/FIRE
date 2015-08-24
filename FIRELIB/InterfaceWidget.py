from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import PanTilt,LeapMotion,PypotCreature,InterfaceGroup

class InterfaceTree(QStandardItemModel):
    
    def __init__(self):
            QStandardItemModel.__init__(self)
            self.setHorizontalHeaderLabels(["Name","Execution","Task"])
    
    def data(self,i,role):
        if not i.isValid():
            return QVariant()
        else:
            parent = self.itemFromIndex(i.parent())
            if parent is None:
                parent = self.invisibleRootItem()
            item = parent.child(i.row(),0)
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if i.column() == 0:
                    return QVariant(item.text())
                elif i.column() == 1:
                    return QVariant(item.executionState)
                elif i.column() == 2:
                    return QVariant(item.taskState)
                else:
                    return QVariant()
            if role == Qt.ToolTipRole:
                return QVariant(item.text())
            if role == Qt.DecorationRole and i.column() == 0:
                return item.icon()
                
    def flags(self,i):
        f = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return f
        
    def writeConf(self):
        conf = {}
        conf["list"] = []
        for i in range(self.rowCount()):
            int = self.item(i)
            conf["list"].append(int.writeConf())
        return conf
        
    def readConf(self,conf):
        for a in conf["list"]:
            int = createInterface(a["name"],withIO = False)
            int.readConf(a)
            self.appendRow(int)

# widget to control FIRE Interface list
class InterfaceWidget(QWidget):
    """
    This class is the component to manage all the FIRE robotic interfaces.
    As an interface inherits from a QStandardItem, the list of interfaces to manage is a QStandardModel (interfaceTree).
    The consequence is that a QTreeView can be plugged directly to this QStandardModel.
    All is included in a widget with button controls of the interface model.
    """
    def __init__(self):
        QWidget.__init__(self)
        # list of models to be available in GUI
        self.listInterfaceType = ["PanTilt","PypotCreature","LeapMotion","Group"]
        # Adopt the model/view method to manage interfaces
        # creation of a Model
        self.interfaceTree = InterfaceTree()
        
        # list of components:
        self.wAddBelowButton = QPushButton("Add below")
        self.wAddInButton = QPushButton("Add in")
        self.wRemoveButton = QPushButton("Remove")
        self.wMoveUpButton = QPushButton("Move up")
        self.wMoveDnButton = QPushButton("Move dn")
        self.wAddInterfaceList = QListWidget()
        self.wAddInterfaceList.addItems(self.listInterfaceType)
        self.wTree = QTreeView()
        self.wTree.setAnimated(True)
        self.wTree.setAlternatingRowColors(True)
        self.wTree.setModel(self.interfaceTree)
        
        # organise the components in layouts
        buttonslayout = QHBoxLayout()
        buttonslayout.addWidget(self.wAddBelowButton)
        buttonslayout.addWidget(self.wAddInButton)
        buttonslayout.addWidget(self.wRemoveButton)
        buttonslayout.addWidget(self.wMoveUpButton)
        buttonslayout.addWidget(self.wMoveDnButton)
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addLayout(buttonslayout)
        self.mainlayout.addWidget(self.wAddInterfaceList)
        self.mainlayout.addWidget(self.wTree)
        
        # connect the signals
        self.connect(self.wAddBelowButton,SIGNAL("pressed()"),self.addInterfaceBelow)
        self.connect(self.wAddInButton,SIGNAL("pressed()"),self.addInterfaceIn)
        self.connect(self.wRemoveButton,SIGNAL("pressed()"),self.removeInterface)
        self.connect(self.wMoveUpButton,SIGNAL("pressed()"),self.moveUpInterface)
        self.connect(self.wMoveDnButton,SIGNAL("pressed()"),self.moveDnInterface)
    

    
    def addInterfaceBelow(self):
        # create the new interface
        InterfaceType = self.wAddInterfaceList.currentItem()
        if InterfaceType is None:
            newitem = None
        else:
            newitem = createInterface(InterfaceType.text())
        if not newitem is None:
            i=self.wTree.currentIndex()
            parent = self.interfaceTree.itemFromIndex(i.parent())
            # if no item is selected, place at the end
            if i.row() == -1:
                self.interfaceTree.invisibleRootItem().appendRow([newitem,QStandardItem(),QStandardItem()])
            else:
                if parent is None:
                    parent = self.interfaceTree.invisibleRootItem()
                parent.insertRow(i.row()+1,[newitem,QStandardItem(),QStandardItem()])
            self.wTree.setCurrentIndex(newitem.index())
            
    def addInterfaceIn(self):
        # create the new interface
        InterfaceType = self.wAddInterfaceList.currentItem()
        if InterfaceType is None:
            newitem = None
        else:
            newitem = createInterface(InterfaceType.text())
        if not newitem is None:
            i=self.wTree.currentIndex()
            if not i.row()==-1:
                parent = self.interfaceTree.itemFromIndex(i)
                # if no item is selected, place at the end
                if parent._isGroup:
                    parent.appendRow([newitem,QStandardItem(),QStandardItem()])
                self.wTree.setCurrentIndex(newitem.index())
                    
    def removeInterface(self):
        i=self.wTree.currentIndex()
        if not i.row() == -1:
            parent = self.interfaceTree.itemFromIndex(i.parent())
            if parent is None:
                parent = self.interfaceTree.invisibleRootItem()
            parent.takeRow(i.row())
                
    def moveUpInterface(self):
        i=self.wTree.currentIndex()
        if not i.row() == -1 and i.row()>0:
            parent = self.interfaceTree.itemFromIndex(i.parent())
            if parent is None:
                parent = self.interfaceTree.invisibleRootItem()
            item = parent.takeRow(i.row())[0]
            parent.insertRow(i.row()-1,item)
            self.wTree.setCurrentIndex(item.index())

    def moveDnInterface(self):
        i=self.wTree.currentIndex()
        if (not i.row() == -1) and i.row()<self.interfaceTree.rowCount()-1:
            parent = self.interfaceTree.itemFromIndex(i.parent())
            if parent is None:
                parent = self.interfaceTree.invisibleRootItem()
            item = parent.takeRow(i.row())[0]
            parent.insertRow(i.row()+1,item)
            self.wTree.setCurrentIndex(item.index())

def createInterface(InterfaceType,withIO = True):
    if InterfaceType == "PanTilt":
        newitem = PanTilt.PanTilt(withIO = withIO)
    elif InterfaceType == "PypotCreature":
        newitem = PypotCreature.PypotCreature(withIO = withIO)
    elif InterfaceType == "LeapMotion":
        newitem = LeapMotion.LeapMotion(withIO = withIO)
    elif InterfaceType == "Group":
        newitem = InterfaceGroup.InterfaceGroup(withIO = withIO)
    else:
        newitem = None
    return newitem

# test bench        
if __name__ == '__main__':
    styleFile = QFile("styleSheet.txt")
    styleFile.open(styleFile.ReadOnly)
    style = str(styleFile.readAll())
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    w = InterfaceWidget()
    w.show()
    sys.exit(app.exec_())

