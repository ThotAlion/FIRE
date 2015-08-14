from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import Hub 

class SystemTree(QStandardItemModel):
    
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

# widget to control FIRE System list
class SystemWidget(QWidget):
    """
    This class is the component to manage all the FIRE robotic system.
    As an System inherits from a QStandardItem, the list of systems to manage is a QStandardModel (systemTree).
    The consequence is that a QTreeView can be plugged directly to this QStandardModel.
    All is included in a widget with button controls of the system model.
    """
    def __init__(self):
        QWidget.__init__(self)
        # list of models to be available in GUI
        self.listSystemType = ["Hub"]
        # Adopt the model/view method to manage systems
        # creation of a Model
        self.systemTree = SystemTree() 
        
        # list of components:
        
        self.wAddBelowButton = QPushButton("Add below")
        self.wAddInButton = QPushButton("Add in")
        self.wRemoveButton = QPushButton("Remove")
        self.wMoveUpButton = QPushButton("Move up")
        self.wMoveDnButton = QPushButton("Move dn")
        self.wAddSystemList = QListWidget()
        self.wAddSystemList.addItems(self.listSystemType)
        self.wTree = QTreeView()
        self.wTree.setAnimated(True)
        self.wTree.setAlternatingRowColors(True)
        self.wTree.setModel(self.systemTree)
        
        # organise the components in layouts
        buttonslayout = QHBoxLayout()
        buttonslayout.addWidget(self.wAddBelowButton)
        buttonslayout.addWidget(self.wAddInButton)
        buttonslayout.addWidget(self.wRemoveButton)
        buttonslayout.addWidget(self.wMoveUpButton)
        buttonslayout.addWidget(self.wMoveDnButton)
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addLayout(buttonslayout)
        self.mainlayout.addWidget(self.wAddSystemList)
        self.mainlayout.addWidget(self.wTree)
        
        # connect the signals
        self.connect(self.wAddBelowButton,SIGNAL("pressed()"),self.addSystemBelow)
        self.connect(self.wAddInButton,SIGNAL("pressed()"),self.addSystemIn)
        self.connect(self.wRemoveButton,SIGNAL("pressed()"),self.removeSystem)
        self.connect(self.wMoveUpButton,SIGNAL("pressed()"),self.moveUpSystem)
        self.connect(self.wMoveDnButton,SIGNAL("pressed()"),self.moveDnSystem)
    
    def createSystem(self,SystemType):
        if SystemType == "Hub":
            newitem = Hub.Hub()
        else:
            newitem = None
        return newitem
    
    def addSystemBelow(self):
        # create the new system
        SystemType = self.wAddSystemList.currentItem()
        if SystemType is None:
            newitem = None
        else:
            newitem = self.createSystem(SystemType.text())
        if not newitem is None:
            i=self.wTree.currentIndex()
            parent = self.systemTree.itemFromIndex(i.parent())
            # if no item is selected, place at the end
            if i.row() == -1:
                self.systemTree.invisibleRootItem().appendRow([newitem,QStandardItem(),QStandardItem()])
            else:
                if parent is None:
                    parent = self.systemTree.invisibleRootItem()
                parent.insertRow(i.row()+1,[newitem,QStandardItem(),QStandardItem()])
            self.wTree.setCurrentIndex(newitem.index())
            
    def addSystemIn(self):
        # create the new System
        SystemType = self.wAddSystemList.currentItem().text()
        newitem = self.createSystem(SystemType)
        if not newitem is None:
            i=self.wTree.currentIndex()
            if not i.row()==-1:
                parent = self.systemTree.itemFromIndex(i)
                # if no item is selected, place at the end
                if parent._isGroup:
                    parent.appendRow([newitem,QStandardItem(),QStandardItem()])
                self.wTree.setCurrentIndex(newitem.index())
                    
    def removeSystem(self):
        i=self.wTree.currentIndex()
        if not i.row() == -1:
            parent = self.systemTree.itemFromIndex(i.parent())
            if parent is None:
                parent = self.systemTree.invisibleRootItem()
            parent.takeRow(i.row())
                
    def moveUpSystem(self):
        i=self.wTree.currentIndex()
        if not i.row() == -1 and i.row()>0:
            parent = self.systemTree.itemFromIndex(i.parent())
            if parent is None:
                parent = self.systemTree.invisibleRootItem()
            item = parent.takeRow(i.row())[0]
            parent.insertRow(i.row()-1,item)
            self.wTree.setCurrentIndex(item.index())

    def moveDnSystem(self):
        i=self.wTree.currentIndex()
        if (not i.row() == -1) and i.row()<self.systemTree.rowCount()-1:
            parent = self.systemTree.itemFromIndex(i.parent())
            if parent is None:
                parent = self.systemTree.invisibleRootItem()
            item = parent.takeRow(i.row())[0]
            parent.insertRow(i.row()+1,item)
            self.wTree.setCurrentIndex(item.index())



# test bench        
if __name__ == '__main__':
    styleFile = QFile("styleSheet.txt")
    styleFile.open(styleFile.ReadOnly)
    style = str(styleFile.readAll())
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    w = SystemWidget()
    w.show()
    sys.exit(app.exec_())

