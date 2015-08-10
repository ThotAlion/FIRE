from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
#import 

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
        self.listSystemType = [""]
        # Adopt the model/view method to manage systems
        # creation of a Model
        self.systemTree = QStandardItemModel()
        self.systemTree.setColumnCount(1)
        self.systemTree.setHorizontalHeaderLabels(["Name"])
        
        
        # list of components:
        
        self.wAddBelowButton = QPushButton("Add below")
        self.wAddInButton = QPushButton("Add in")
        self.wRemoveButton = QPushButton("Remove")
        self.wMoveUpButton = QPushButton("Move up")
        self.wMoveDnButton = QPushButton("Move dn")
        self.wAddSystemList = QListWidget()
        self.wAddSystemList.addItems(self.listSystemType)
        self.wTree = QTreeView()
        self.wTree.setModel(self.systemTree)
        
        # organise the components in layouts
        buttonslayout = QHBoxLayout()
        buttonslayout.addWidget(self.wAddBelowButton)
        buttonslayout.addWidget(self.wAddInButton)
        buttonslayout.addWidget(self.wRemoveButton)
        buttonslayout.addWidget(self.wMoveUpButton)
        buttonslayout.addWidget(self.wMoveDnButton)
        self.wGroup = QGroupBox("Systems",self)
        self.mainlayout = QVBoxLayout()
        self.wGroup.setLayout(self.mainlayout)
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
        if SystemType == "PanTilt":
            newitem = PanTilt.PanTilt()
        elif SystemType == "PypotCreature":
            newitem = PypotCreature.PypotCreature()
        elif SystemType == "LeapMotion":
            newitem = LeapMotion.LeapMotion()
        elif SystemType == "Group":
            newitem = SystemGroup.SystemGroup()
        else:
            newitem = None
        return newitem
    
    def addSystemBelow(self):
        # create the new system
        SystemType = self.wAddSystemList.currentItem().text()
        newitem = self.createSystem(SystemType)
        if not newitem is None:
            i=self.wTree.currentIndex()
            parent = self.systemTree.itemFromIndex(i.parent())
            # if no item is selected, place at the end
            if i.row() == -1:
                self.systemTree.invisibleRootItem().appendRow(newitem)
            else:
                if parent is None:
                    parent = self.systemTree.invisibleRootItem()
                parent.insertRow(i.row()+1,newitem)
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
                    parent.appendRow(newitem)
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

