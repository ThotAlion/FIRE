from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from numpy import *


class ConnexionTree(QStandardItemModel):
    
    def __init__(self):
        QStandardItemModel.__init__(self)
        self.setHorizontalHeaderLabels(["Name","Connected To","Value","Init","Min","Max"])
        
    def data(self,i,role):
        if not i.isValid():
            return QVariant()
        else:
            item = self.item(i.row(),0)
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if i.column() == 0:
                    return QVariant(item.text())
                elif i.column() == 1:
                    return QVariant(item.connectedTo)
                elif i.column() == 2:
                    if type(item.value) == ndarray:
                        return QVariant(str(item.value))
                    elif type(item.value) == str:
                        return QVariant(item.value)
                elif i.column() == 3:
                    if type(item.valueInit) == ndarray:
                        return QVariant(str(item.valueInit))
                    elif type(item.valueInit) == str:
                        return QVariant(item.valueInit)
                elif i.column() == 4:
                    return QVariant(str(item.valueMin))
                elif i.column() == 5:
                    return QVariant(str(item.valueMax))
                else:
                    return QVariant()
            if role == Qt.ToolTipRole:
                return QVariant(item.description+" ("+item.unit+").")
                
    def setData(self,i,value,role):
        if i.isValid():
            item = self.item(i.row(),0)
            if role == Qt.EditRole:
                if i.column() == 1:
                    item.connectedTo = str(value.toString())
                    return True
        else:
            return False
    
    def setConnexion(self,name,value,channels):
        connexions = self.findItems(name)
        if len(connexions)==1:
            connexion = connexions[0]
            connexion.value = value
            if connexion.isConnected:
                channels = connexion.updateOutput(channels)
        elif len(connexions)==0:
            print "connexion "+name+" not set."
        return channels
        
    def getConnexion(self,name,channels):
        connexions = self.findItems(name)
        if len(connexions)==1:
            connexion = connexions[0]
            if connexion.direction == connexion.IN:
                if connexion.isConnected:
                    connexion.updateInput(channels)
                    return connexion.value
                else:
                    return connexion.valueInit
            elif connexion.direction == connexion.OUT:
                return connexion.value
        elif len(connexions)==0:
            print "connexion "+name+" not get."
            
    def flags(self,i):
        if i.isValid():
            if i.column() in [0,2,3,4,5]:
                f = Qt.ItemIsEnabled | Qt.ItemIsSelectable
            if i.column() in [1]:
                f = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return f
            

# widget to control FIRE connexions
class ConnexionWidget(QWidget):
    """
    This class is the component to manage all the FIRE connexions.
    The connexion are inherited from QStandardItem therefore, a model is connected to the widget.
    This models are included inside each system or interfaces.
    """
    def __init__(self):
        QWidget.__init__(self)
        # list of components:
        self.wTabIn = QTreeView()
        self.wTabOut = QTreeView()
        self.wTabIn.setEditTriggers(self.wTabIn.AllEditTriggers)
        self.wTabIn.setAlternatingRowColors(True)
        self.wTabIn.setAnimated(True)
        self.wTabOut.setEditTriggers(self.wTabIn.AllEditTriggers)
        self.wTabOut.setAlternatingRowColors(True)
        self.wTabOut.setAnimated(True)
        
        # organise the components in layouts
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addWidget(self.wTabIn)
        self.mainlayout.addWidget(self.wTabOut)
        
        # connect the signals

        



# test bench        
if __name__ == '__main__':
    styleFile = QFile("styleSheet.txt")
    styleFile.open(styleFile.ReadOnly)
    style = str(styleFile.readAll())
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    w = ConnexionWidget()
    w.show()
    sys.exit(app.exec_())

