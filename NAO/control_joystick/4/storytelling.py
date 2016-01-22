from PyQt4 import QtGui, QtCore

class StoryTelling(QtGui.QWidget):

    storytelling_event = QtCore.pyqtSignal(list)

    def __init__(self):
        
        super(StoryTelling, self).__init__()
        self.isRealTime = True
        
        ##GUI
        self.layoutMain = QtGui.QHBoxLayout()
        self.groupMenu = QtGui.QGroupBox("StoryTelling")
        self.groupMenu.setStyleSheet("background-color:red")
        self.layoutMenu = QtGui.QVBoxLayout()
        self.checkBox_realTime = QtGui.QCheckBox("realTime")
        self.checkBox_realTime.setChecked(QtCore.Qt.Checked)
        self.button_next = QtGui.QPushButton("Next")
        self.button_open = QtGui.QPushButton("Open")
        self.button_save = QtGui.QPushButton("Save")
        #ListView
        self.listView = QtGui.QListView()
        self.model = QtGui.QStandardItemModel(self.listView)
        ##Add to layout
        self.layoutMenu.addWidget(self.checkBox_realTime)
        self.layoutMenu.addWidget(self.button_next)
        self.layoutMenu.addWidget(self.button_open)
        self.layoutMenu.addWidget(self.button_save)
        self.groupMenu.setLayout(self.layoutMenu)
        self.layoutMain.addWidget(self.groupMenu)
        self.layoutMain.addWidget(self.listView)
        self.setLayout(self.layoutMain)
        
        ### Settings model and list of string
        self.list_string = [
            'Cookie dough', 
            'Hummus', 
            'Spaghetti', 
            'Dal makhani', 
            'Chocolate whipped cream' 
        ]
        self.open_file()
        self.listView.setModel(self.model)
        ## Connect
        self.model.itemChanged.connect(self.line_changed)
        self.connect(self.listView, QtCore.SIGNAL("activated(QModelIndex)"), self.handleSelectionChanged  )
        self.button_save.clicked.connect(self.save_file)
        self.button_open.clicked.connect(self.open_file)
        
        
        
    def fill_model(self):
    
        self.model.beginResetModel()
        
        for line in self.list_string:
            # Create an item with a caption
            item = QtGui.QStandardItem(line)
 
            # Add a checkbox to it
            item.setCheckable(False)
 
            # Add the item to the model
            self.model.appendRow(item)
            
    def save_file(self):
        file = open('file/conduite.txt', 'w')
        print "save file"
        print self.model.rowCount()
        
        for a in range(self.model.rowCount()):
            word = str(self.model.item(a).text())

            file.write(word+"\n")
        
        
        file.close()
        self.open_file()
        
    def open_file(self):
        file = open('file/conduite.txt', 'r')
        self.list_string = []
        self.model.clear()
        for line in file:
            self.list_string.append(line[:len(line)-1])
            
        self.fill_model()
        print self.list_string
        
            
    def line_changed(self,item):
    
        print "line_changed"
        
    def handleSelectionChanged(self, index):
        
        print "hande changed"
        line = str(index.data().toString())
        list_of_word = line.split()
        res = []
        first = []
        
        while len(list_of_word)<3:
            list_of_word.append(0)
        
        for word in list_of_word:
            if str(word[:1]).isdigit() or str(word[:1]) == "-":
                first.append(float(word))
            else :
                first.append(word)
         
        res.append(first)
        print res
        self.transmit_msg(res)
        
        

    def transmit_msg(self,l):
        res = []
        
        #Controlling nao in real time using controller, and passing trough storrytelling object
        if self.checkBox_realTime.isChecked():
            self.storytelling_event.emit(l)
        
    def write_msg(self,l):
    
        self.storytelling_event.emit(l)
    
    
            