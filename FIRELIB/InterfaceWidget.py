from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import PanTilt,LeapMotion,PypotCreature,InterfaceGroup

# widget to control FIRE Interface list
class InterfaceWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # list of Interface
        self.interfaceList = InterfaceGroup.InterfaceGroup(None,name="Interfaces")
        self._listInterfaceType = ["PanTilt","PypotCreature","LeapMotion","Group"]
        
        # list of components:
        self.wAddBelowButton = QPushButton("Add below")
        self.wRemoveButton = QPushButton("Remove")
        self.wMoveUpButton = QPushButton("Move up")
        self.wMoveDnButton = QPushButton("Move dn")
        self.wAddInterfaceList = QListWidget()
        self.wAddInterfaceList.addItems(self._listInterfaceType)
        self.wTree = QTreeWidget()
        self.wTree.setColumnCount(1)
        self.wTree.setHeaderLabels(["Name"])
        self.wTree.addTopLevelItem(self.root)
        self.root.setExpanded(True)
        
        # organise the components in layouts
        buttonslayout = QHBoxLayout()
        buttonslayout.addWidget(self.wAddBelowButton)
        buttonslayout.addWidget(self.wRemoveButton)
        buttonslayout.addWidget(self.wMoveUpButton)
        buttonslayout.addWidget(self.wMoveDnButton)
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addLayout(buttonslayout)
        self.mainlayout.addWidget(self.wAddInterfaceList)
        self.mainlayout.addWidget(self.wTree)
        
        # connect the signals
        self.connect(self.wAddBelowButton,SIGNAL("pressed()"),self.addInterfaceBelow)
        self.connect(self.wRemoveButton,SIGNAL("pressed()"),self.removeInterface)
        self.connect(self.wMoveUpButton,SIGNAL("pressed()"),self.moveUpInterface)
        self.connect(self.wMoveDnButton,SIGNAL("pressed()"),self.moveDnInterface)
        
        self.show()
    
    @property
    def interfaceList(self):
        return self._interfaceList
    @interfaceList.setter
    def interfaceList(self,value):
        self._interfaceList = value
        self.root = QTreeWidgetItem([self._interfaceList._name])
        self.addNode(self.root,self._interfaceList.children)
    
    def addNode(self,root,list):
        for c in list:
            if hasattr(c,'children'):
                a=QTreeWidgetItem(root,[c._name,c])
                addNode(a,c.children)
            else:
                QTreeWidgetItem(root,[c._name,c])
    
    def addInterfaceBelow(self):
        # create the new interface
        InterfaceType = self.wAddInterfaceList.currentItem().text()
        if InterfaceType == "PanTilt":
            newitem = PanTilt.PanTilt()
        elif InterfaceType == "PypotCreature":
            newitem = PypotCreature.PypotCreature()
        elif InterfaceType == "LeapMotion":
            newitem = LeapMotion.LeapMotion()
        elif InterfaceType == "Group":
            newitem = InterfaceGroup.InterfaceGroup()
        else:
            newitem = None
        print newitem    
        if not newitem is None:
            item=self.wTree.currentItem()
            # if no item is selected, place at the end
            if item is None:
                self.interfaceList.addInterface(newitem)
                self.interfaceList=self.interfaceList
            else:
                parent = item.parent()
                
                if parent is None:
                    QTreeWidgetItem(item,[InterfaceType.text()])
                else:
                    t = QTreeWidgetItem(parent,item)
                    t.setText(0,InterfaceType.text())
                    
    def removeInterface(self):
        item=self.wTree.currentItem()
        if not item is None:
            parent = item.parent()
            if not parent is None:
                i = parent.indexOfChild(item)
                parent.takeChild(i)
                
    def moveUpInterface(self):
        item=self.wTree.currentItem()
        if not item is None:
            parent = item.parent()
            if not parent is None:
                i = parent.indexOfChild(item)
                if i>0:
                    item = parent.takeChild(i)
                    parent.insertChild(i-1,item)
                    self.wTree.setCurrentItem(item)
    
    def moveDnInterface(self):
        item=self.wTree.currentItem()
        if not item is None:
            parent = item.parent()
            if not parent is None:
                i = parent.indexOfChild(item)
                if i<parent.childCount()-1:
                    item = parent.takeChild(i)
                    parent.insertChild(i+1,item)
                    self.wTree.setCurrentItem(item)


        
if __name__ == '__main__':
    styleFile = QFile("styleSheet.txt")
    styleFile.open(styleFile.ReadOnly)
    style = str(styleFile.readAll())
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    w = InterfaceWidget()
    sys.exit(app.exec_())

