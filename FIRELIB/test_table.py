import Interface
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class totolist(QStandardItemModel):
    
    def __init__(self,parent=None, *args):
        QStandardItemModel.__init__(self,0,2,parent, *args)
        self.setHorizontalHeaderLabels(["name","first letter"])
    
    def data(self,i,role):
        if not i.isValid():
            return QVariant()
        else:
            item = self.item(i.row(),0)
            if role == Qt.DisplayRole:
                if i.column() == 0:
                    return QVariant(item.text())
                elif i.column() == 1:
                    return QVariant(item.text()[0])
                else:
                    return QVariant()
    
    
                
            
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    l = QVBoxLayout(w)
    t = QTableView()
    l.addWidget(t)
    m = totolist()
    m.invisibleRootItem().appendRow([QStandardItem("Thomas PEYRUSE")])
    m.invisibleRootItem().appendRow([QStandardItem("Pauline PEYRUSE")])
    t.setModel(m)

    w.show()
    
    sys.exit(app.exec_())
    
    