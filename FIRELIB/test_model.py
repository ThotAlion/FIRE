import Interface
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    l = QVBoxLayout(w)
    t = QTreeView()
    b = QPushButton("remove")
    l.addWidget(b)
    l.addWidget(t)
    m = QStandardItemModel()
    m.setColumnCount(1)
    m.setHorizontalHeaderLabels(["Name"])
    t.setModel(m)
    
    i1 = Interface.Interface(name = "int1")
    i2 = Interface.Interface(name = "int2")
    i3 = Interface.Interface(name = "int3")
    
    r = m.invisibleRootItem()
    r.appendRow(i1)
    i1.appendRow(i2)
    r.appendRow(i3)
    
    w.show()
    
    w.connect(b,SIGNAL("pressed()"),m.removeRow(t.currentIndex().row(),t.currentIndex().parent()))
    
    sys.exit(app.exec_())
    
    