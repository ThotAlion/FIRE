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
        self.label_warning = QtGui.QLabel("Msg sent")
        self.label_warning.setStyleSheet("background-color:red")
        self.button_next = QtGui.QPushButton("Next")
        self.button_prev = QtGui.QPushButton("Prev")
        self.button_call = QtGui.QPushButton("Call")
        self.button_save = QtGui.QPushButton("Save")
        #ListView
        self.listView = QtGui.QListView()
        self.model = QtGui.QStandardItemModel(self.listView)
        ##Add to layout
        self.layoutMenu.addWidget(self.checkBox_realTime)
        self.layoutMenu.addWidget(self.label_warning)
        self.layoutMenu.addWidget(self.button_next)
        self.layoutMenu.addWidget(self.button_prev)
        self.layoutMenu.addWidget(self.button_call)
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
        self.connect(self.listView, QtCore.SIGNAL("activated(QModelIndex)"), self.callSelection  )
        self.button_save.clicked.connect(self.save_file)
        self.button_call.clicked.connect(self.callSelection_button)
        self.button_next.clicked.connect(self.next_index)
        self.button_prev.clicked.connect(self.prev_index)
        
        ## Warning information when message pressed
        self.isMessageSent = False
        self.imgBlank = "images/blank.png"
        self.imgSent = "images/sent.png"
        
        #Select the fist line of QViewList
        first_item = self.model.item(0)
        first_modelIndex = self.model.indexFromItem(first_item)
        self.listView.setCurrentIndex(first_modelIndex)
        
        
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
        
    def warning_message_status(self):
        
        if self.isMessageSent: 
            self.label_warning.setPixmap(QtGui.QPixmap(self.imgSent))
            self.isMessageSent = False
        else :
            self.label_warning.setPixmap(QtGui.QPixmap(self.imgBlank))
        
    def next_index(self):
    
        selection_list = self.listView.selectedIndexes()
        row = 0
        if len(selection_list) == 1:
            indexItem = selection_list[0]
            count = 1
            indexItemNext = indexItem.sibling(indexItem.row() + count, 0)
            #continue next until the selected line is NOT a comment
            while self.is_selectedRow_comment(indexItemNext):
                indexItemNext = indexItem.sibling(indexItem.row() + count, 0)
                count += 1   
            self.listView.setCurrentIndex(indexItemNext)
        else :
            print "erreur : seleciton multiple"

    def prev_index(self):
    
        selection_list = self.listView.selectedIndexes()
        row = 1
        if len(selection_list) == 1:
            indexItem = selection_list[0]
            indexItemNext = indexItem.sibling(indexItem.row() - 1, 0)
            self.listView.setCurrentIndex(indexItemNext)
        else :
            print "erreur : seleciton multiple"
    
    #call a script message from current selection, from ""enter"" key or  ""call" button
    
    def is_selectedRow_comment(self, index):
        line = str(index.data().toString())
        list_of_word = line.split()
        if line[:1] == '*' :
            return True
        else :
            return False
    
    def callSelection(self, index):
        #weed need a QModelIndex
        line = str(index.data().toString())

        list_of_word = line.split()
        res = []
        first = []
        
        #Check if the line is a comment or not
        if line[:1] == '*' :
            print "no comment"
            #select the next line
            self.next_index()
        
        #if not, split the line , convert word to float if needed
        else : 
        
            while len(list_of_word)<3:
                list_of_word.append("0")
            
            for word in list_of_word:
                
                if str(word[:1]).isdigit() or str(word[:1]) == "-":
                    first.append(float(word))
                else:
                    first.append(word)
             
            res.append(first)
            print res
            
            #send to nao_manager
            self.write_msg(res)
            #send warning icon
            self.isMessageSent = True
            #select the next line
            self.next_index()
        
    # connected to "call" button, and resend to self.callSelection function    
    def callSelection_button(self):
    
        #selection_list is a QModelIndexList
        selection_list = self.listView.selectedIndexes()
        row = 0
        if len(selection_list) == 1:
            #indexItem is a QModelIndex
            indexItem = selection_list[0]
            self.callSelection(indexItem)

    def transmit_msg(self,l):
        res = []
        #First, control that transmit message is controlling the storytelling itself ( next, call, prev)
        for msg in l:
            if(len(msg)==4):
                name = msg[0]
                arg1 = msg[2]
                
                if name == "STORY":
                    if arg1 == "CALL":
                        self.callSelection_button()
                    
                    elif arg1 == "NEXT":
                        self.next_index()
                    
                    elif arg1 == "PREV":
                        self.prev_index()
                    
                
        
        #If not, Controlling nao in real time using controller, and passing trough storrytelling object
        if self.checkBox_realTime.isChecked():
            self.storytelling_event.emit(l)
        
    def write_msg(self,l):
    
        self.storytelling_event.emit(l)
    
    
            