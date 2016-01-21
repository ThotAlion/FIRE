from nao import Nao
from PyQt4 import QtGui, QtCore
import copy

class Nao_manager(QtGui.QWidget):

    def __init__(self):

        super(Nao_manager, self).__init__()

        ####### NAO MANAGEMENT #######
        self.list_of_nao = []
        self.selection1 = []
        self.selection2 = []
        self.selectionGlobal = []

        ######## GUI #################

        ####Layout
        self.layoutMain = QtGui.QVBoxLayout()
        self.layoutNao= QtGui.QGridLayout()
        self.layoutNao.setAlignment(QtCore.Qt.AlignHCenter)
        self.layoutNao.setAlignment(QtCore.Qt.AlignTop)
        self.layoutManager = QtGui.QHBoxLayout()

        self.layoutMain.addLayout(self.layoutNao)
        #self.layoutMain.addLayout(self.layoutManager)
        self.setLayout(self.layoutMain)

        ####CheckBox for selection
        self.list_of_selectionCheckBox1 = []
        self.list_of_selectionCheckBox2 = []

        #####Group Selection
        #construct
        groupSelection = QtGui.QGroupBox("selection")
        layoutSelection = QtGui.QVBoxLayout()
        groupSelection.setLayout(layoutSelection)
        self.selectionButton_1all = QtGui.QPushButton("1 - All")
        self.selectionButton_1nall = QtGui.QPushButton("1 - None")
        self.selectionButton_2all = QtGui.QPushButton("2 - All")
        self.selectionButton_2nall = QtGui.QPushButton("2 - None")
        #connect
        self.selectionButton_1all.clicked.connect(lambda: self.selectAll(1,True))
        self.selectionButton_1nall.clicked.connect(lambda: self.selectAll(1,False))
        self.selectionButton_2all.clicked.connect(lambda: self.selectAll(2,True))
        self.selectionButton_2nall.clicked.connect(lambda: self.selectAll(2,False))
        #add to layout
        
        layoutSelection.addWidget(self.selectionButton_1all)
        layoutSelection.addWidget(self.selectionButton_1nall)
        layoutSelection.addWidget(self.selectionButton_2all)
        layoutSelection.addWidget(self.selectionButton_2nall)
        self.layoutManager.addWidget(groupSelection)

        #####GroupWalk : walk
        #construct
        groupWalk = QtGui.QGroupBox("walk")
        groupWalk.setMinimumWidth(100)
        layoutWalk = QtGui.QVBoxLayout()
        groupWalk.setLayout(layoutWalk)
        self.sliderWalk_x = QtGui.QSlider(QtCore.Qt.Vertical)
        self.sliderWalk_x.setRange(-100, 100)
        self.sliderWalk_y = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.sliderWalk_y.setRange(-100, 100)
        self.sliderWalk_y.setTickInterval(100)
        self.sliderWalk_tetha = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.sliderWalk_tetha.setRange(-100, 100)
        self.sliderWalk_tetha.setTickInterval(100)
        #add to layout
        layoutWalk.addWidget(self.sliderWalk_x)
        layoutWalk.addWidget(self.sliderWalk_y)
        layoutWalk.addWidget(self.sliderWalk_tetha)
        self.layoutManager.addWidget(groupWalk)
        
                                          
        #####GroupPosture : posture
        #construct
        groupPosture = QtGui.QGroupBox("Posture")
        layoutPosture = QtGui.QVBoxLayout()
        groupPosture.setLayout(layoutPosture)
        self.postureButton_rest = QtGui.QPushButton("rest")
        self.postureButton_stand = QtGui.QPushButton("stand")
        self.postureButton_standInit = QtGui.QPushButton("stand init")
        self.postureButton_sit = QtGui.QPushButton("sit")
        #connect
        self.postureButton_rest.clicked.connect(lambda: self.nao_go_posture("Rest"))
        self.postureButton_stand.clicked.connect(lambda: self.nao_go_posture("Stand"))
        self.postureButton_standInit.clicked.connect(lambda: self.self.nao_go_posture("StandInit"))
        self.postureButton_sit.clicked.connect(lambda: self.self.nao_go_posture("Sit"))
        #add to layout
        layoutPosture.addWidget(self.postureButton_rest)
        layoutPosture.addWidget(self.postureButton_stand)
        layoutPosture.addWidget(self.postureButton_standInit)
        layoutPosture.addWidget(self.postureButton_sit)
        self.layoutManager.addWidget(groupPosture)

        #####GroupAnimation
        #construct
        groupAnim = QtGui.QGroupBox("Animation Cunningham")
        layoutAnim = QtGui.QGridLayout()
        groupAnim.setLayout(layoutAnim)
        self.list_of_animButton = []
        self.list_of_animButton.append(QtGui.QPushButton("Torsion"))
        self.list_of_animButton.append(QtGui.QPushButton("Triangle"))
        self.list_of_animButton.append(QtGui.QPushButton("Cote"))
        self.list_of_animButton.append(QtGui.QPushButton("Clavier"))
        self.list_of_animButton.append(QtGui.QPushButton("Pyramide"))
        self.list_of_animButton.append(QtGui.QPushButton("Salut A"))
        self.list_of_animButton.append(QtGui.QPushButton("Arabesque"))
        self.list_of_animButton.append(QtGui.QPushButton("Ronde"))
        self.list_of_animButton.append(QtGui.QPushButton("anim9"))
        #connect
        self.list_of_animButton[0].clicked.connect(lambda: self.nao_memoryEvent("anim", "TORSION"))
        self.list_of_animButton[1].clicked.connect(lambda: self.nao_memoryEvent("anim", "TRIANGLE"))
        self.list_of_animButton[2].clicked.connect(lambda: self.nao_memoryEvent("anim", "COTE"))
        self.list_of_animButton[3].clicked.connect(lambda: self.nao_memoryEvent("anim", "CLAVIER"))
        self.list_of_animButton[4].clicked.connect(lambda: self.nao_memoryEvent("anim", "PYRAMIDE"))
        self.list_of_animButton[5].clicked.connect(lambda: self.nao_memoryEvent("anim", "SALUTA"))
        self.list_of_animButton[6].clicked.connect(lambda: self.nao_memoryEvent("anim", "ARABESQUE"))
        self.list_of_animButton[7].clicked.connect(lambda: self.nao_memoryEvent("anim", "RONDE"))
        self.list_of_animButton[8].clicked.connect(lambda: self.nao_memoryEvent("anim", "anim9"))
        #add to layout
        for i in range(3):
            for j in range(3):
                layoutAnim.addWidget(self.list_of_animButton[(i*3) + j ], i, j )
        self.layoutManager.addWidget(groupAnim)

        #####GroupAnimLibrary
        #construct
        groupAnimLib = QtGui.QGroupBox("Animation Librarie")
        layoutAnimLib = QtGui.QGridLayout()
        groupAnimLib.setLayout(layoutAnimLib)
        self.list_of_animLibButton = []
        self.list_of_animLibButton.append(QtGui.QPushButton("1"))
        self.list_of_animLibButton.append(QtGui.QPushButton("2"))
        self.list_of_animLibButton.append(QtGui.QPushButton("3"))
        self.list_of_animLibButton.append(QtGui.QPushButton("4"))
        self.list_of_animLibButton.append(QtGui.QPushButton("5"))
        self.list_of_animLibButton.append(QtGui.QPushButton("6"))
        self.list_of_animLibButton.append(QtGui.QPushButton("7"))
        self.list_of_animLibButton.append(QtGui.QPushButton("8"))
        self.list_of_animLibButton.append(QtGui.QPushButton("9"))
        #connect
        self.list_of_animLibButton[0].clicked.connect(lambda: self.nao_memoryEvent("animLib", "1"))
        self.list_of_animLibButton[1].clicked.connect(lambda: self.nao_memoryEvent("animLib", "2"))
        self.list_of_animLibButton[2].clicked.connect(lambda: self.nao_memoryEvent("animLib", "3"))
        self.list_of_animLibButton[3].clicked.connect(lambda: self.nao_memoryEvent("animLib", "4"))
        self.list_of_animLibButton[4].clicked.connect(lambda: self.nao_memoryEvent("animLib", "5"))
        self.list_of_animLibButton[5].clicked.connect(lambda: self.nao_memoryEvent("animLib", "6"))
        self.list_of_animLibButton[6].clicked.connect(lambda: self.nao_memoryEvent("animLib", "7"))
        self.list_of_animLibButton[7].clicked.connect(lambda: self.nao_memoryEvent("animLib", "8"))
        self.list_of_animLibButton[8].clicked.connect(lambda: self.nao_memoryEvent("animLib", "9"))
        #add to layout
        for i in range(3):
            for j in range(3):
                layoutAnimLib.addWidget(self.list_of_animLibButton[(i*3) + j ], i, j )
        #Anim Group desativated
        #self.layoutManager.addWidget(groupAnimLib)


    def addNao(self, name, adresseIP, port ):
        #nao management
        naoId = len(self.list_of_nao)
        nao = Nao(adresseIP, name, naoId)
        self.list_of_nao.append(nao)
        self.selection1.append(False)
        self.selection2.append(False)
        self.selectionGlobal.append(False)

        #gui management
        self.layoutNao.addWidget(nao, 2, naoId, QtCore.Qt.AlignCenter)
        checkBox1 = QtGui.QCheckBox("1")
        checkBox1.setStyleSheet("background-color:yellow")
        checkBox2 = QtGui.QCheckBox("2")
        checkBox2.setStyleSheet("background-color:white")
        checkBox1.clicked.connect(lambda: self.addselect(1, checkBox1.isChecked(), naoId ))
        checkBox2.clicked.connect(lambda: self.addselect(2, checkBox2.isChecked(), naoId ))
        self.list_of_selectionCheckBox1.append(checkBox1)
        self.list_of_selectionCheckBox2.append(checkBox2)
        self.layoutNao.addWidget( checkBox1, 0, naoId, QtCore.Qt.AlignCenter)
        self.layoutNao.addWidget( checkBox2, 1, naoId, QtCore.Qt.AlignCenter)
        

    def init_nao(self):

        for nao in self.list_of_nao :
            nao.init_pos()

    def init_manager(self):

        if len(self.list_of_nao) != len(self.selection1) :
            print( " probleme nao manager init selection1")
        elif len(self.list_of_nao) != len(self.selection2) :
            print( " probleme nao manager init selection 2")
        elif len(self.list_of_nao) != len(self.selectionGlobal) :
            print( " probleme nao manager init selection Global")
        else :
            self.init_nao()
            self.activateNao()
            return True


    # switching from select all to unselect all
    def selectAll( self, joy_id, is_selecting=True):
        if is_selecting:
             print str(joy_id)+"selecting ALL"
        else :
            print str(joy_id)+"un_selecting all"
            
        selection = []
            
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2

        for i in range(len(selection)):
            selection[i] = is_selecting
            
        self.activateNao()
            

    # select only one nao, switching from one to the other
    def selectSwitch(self, joy_id, isIncreasing ):

        print "manager:selectSwitch"
        #find the last nao activated
        
        last_id = 0
        current_id = 0
        selection = []
        selection_opposed = []
        
        if joy_id == 1 : 
            selection = self.selection1
            selection_opposed = self.selection2
        elif joy_id == 2 : 
            selection = self.selection2
            selection_opposed = self.selection1
            
        for is_selected in self.selectionGlobal:
            if is_selected:
                last_id = current_id
            current_id += 1

        for i in range(len(selection)):
            selection[i] =  ((last_id + 1)%len(selection))==i  

        self.activateNao()
                

    # select or unselect one nao, over the current selection, according to its ID
    def addselect(self, joy_id, isSelecting, nao_id ):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        else :
            print "error joystick"

        if isSelecting :
            print "joystick "+str(joy_id)+" :: nao manager : select , nao_id= "+str(nao_id)
        else :
            print "joystick "+str(joy_id)+" :: nao manager : unselect , nao_id= "+str(nao_id)

        if nao_id>-1 and nao_id< len(self.list_of_nao):
            selection[nao_id] = isSelecting

        self.activateNao()
        
    # select or unselect nao according to a number 1000 choose the first nao for example
    def select(self, joy_id, selectNumber):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        else :
            print "error joystick" 
            
        for i in range(len(selection)):
            selection[i] =  ( int(selectNumber) / pow(10, 3 - i) % 2 ) == 1
            
        self.activateNao()
    


    # activate some or all nao according to selection list
    def activateNao(self):
        print "activateNao - joystick 1 :"
        print self.selection1
        print "activateNao - joystick 2 :"
        print self.selection2
        # calculate the Global selection , according to joystick 1 and 2
        self.calcGlobalSelection()
        
        for a in range(len(self.selectionGlobal)):
            if (self.selectionGlobal[a] and self.selection1[a] and self.selection2[a]):
                self.selection2[a] = False
        
        #Check the checkbox for the first joystick
        for a in range(len(self.list_of_nao)):
            (self.list_of_nao[a]).activate( self.selection1[a], 1 )
            if self.selection1[a] :
                (self.list_of_selectionCheckBox1[a]).setCheckState(QtCore.Qt.Checked)
            else:
                (self.list_of_selectionCheckBox1[a]).setCheckState(QtCore.Qt.Unchecked)
        #Check the checkbox for the 2n joystick
        for a in range(len(self.list_of_nao)):
            (self.list_of_nao[a]).activate( self.selection2[a], 2 )
            if self.selection2[a] :
                (self.list_of_selectionCheckBox2[a]).setCheckState(QtCore.Qt.Checked)
            else:
                (self.list_of_selectionCheckBox2[a]).setCheckState(QtCore.Qt.Unchecked)
   
    # calc a global selection according to the addition of selection1 and selection 2
    def calcGlobalSelection(self):
    
        for a in range( len(self.list_of_nao)):
            self.selectionGlobal[a] = self.selection1[a] or self.selection2[a]

    # call a memory event to all selected nao
    def nao_memoryEvent(self, joy_id, name, arg ):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        #All nao selected from 1 and 2
        elif joy_id == 0:
            selection = self.selectionGlobal 
        
        
        print "Memory Event : "+name+" -- "+str(arg)
        for i in range(len(self.list_of_nao)):
            if selection[i]:
                self.list_of_nao[i].memoryEvent(name, arg)

    # update_walk and turning to all selected nao
    def nao_update_walk(self,joy_id, X, Y, Theta, Speed):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        #All nao selected from 1 and 2
        elif joy_id == 0:
            selection = self.selectionGlobal 

        for i in range(len(self.list_of_nao)):
            if selection[i]:
                self.list_of_nao[i].update_walk( X, Y , Theta, Speed)

        print "marche X="+str(X)+" Y="+str(Y)+" Theta="+str(Theta)+" Speed="+str(Speed)+""
        self.sliderWalk_tetha.setValue(-Theta*100)
        self.sliderWalk_x.setValue(X*100*Speed)
        self.sliderWalk_y.setValue(-Y*100)
    
    def nao_update_walk_to_point(self,joy_id, X, Y, Theta, Speed):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        #All nao selected from 1 and 2
        elif joy_id == 0:
            selection = self.selectionGlobal 

        for i in range(len(self.list_of_nao)):
            if selection[i]:
                self.list_of_nao[i].update_walk_to_point( X, Y , Theta, Speed)

        print "marche to Point X="+str(X)+" Y="+str(Y)+" Theta="+str(Theta)+" Speed="+str(Speed)+""
        self.sliderWalk_tetha.setValue(-Theta*100)
        self.sliderWalk_x.setValue(X*100*Speed)
        self.sliderWalk_y.setValue(-Y*100)


    # update turning head to all selected nao
    def nao_move_head(self,joy_id, yaw,pitch):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        #All nao selected from 1 and 2
        elif joy_id == 0:
            selection = self.selectionGlobal

        for i in range(len(self.list_of_nao)):
            if selection[i]:
                self.list_of_nao[i].move_head(yaw,pitch)

        print "Tete yaw="+str(yaw)+" pitch="+str(pitch)+" "

    # ask a posture to all selected nao
    def nao_go_posture(self, joy_id, posture_name):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        #All nao selected from 1 and 2
        elif joy_id == 0:
            selection = selectionGlobal

        for i in range(len(self.list_of_nao)):
            if selection[i]:
                self.list_of_nao[i].go_posture( posture_name)
                
    def nao_autonomeLevel(self, joy_id, arg):
    
        selection = []
        if joy_id == 1 : 
            selection = self.selection1
        elif joy_id == 2 : 
            selection = self.selection2
        #All nao selected from 1 and 2
        elif joy_id == 0:
            selection = self.selectionGlobal

        isReset = (arg == 0)
        isStop = (arg == -1)
        isIncreasing = (arg == 2)
        
        for i in range(len(self.list_of_nao)):
            if selection[i]:
                self.list_of_nao[i].changeAutonomeLevel(isIncreasing, isReset, isStop)

    def nao_getStatus(self):

        for nao in self.list_of_nao :
            nao.get_status()


    ####################################################################    
    # TRANSMIT message from interpret to itself and all selected nao(s).
    # Contains all dictionnary message and functions calls
    #
    #To avoid repetion of messages, the function call 1 walk and 1 head for 
    #each msgGlobal. We don't need more that 25 walk and head information / sec
    #
    ####################################################################
    def transmit_msg(self, msgGlobal):

        walk_information = False
        head_information = False
        
        for msg in msgGlobal:


            if(len(msg)==4):

                name = msg[0]
                joy_id = msg[1]
                arg1 = msg[2]
                arg2 = msg[3]


                #### SELECTION ####
                if   name == "SWITCH" :
                    self.selectSwitch(joy_id, 1)
                elif name == "SELECT_ALL" :
                    self.selectAll(joy_id)
                elif name == "UNSELECT_ALL" :
                    self.selectAll(joy_id, False)
                elif name == "ADDSELECT":
                    self.addselect(joy_id, True, arg1 )
                elif name == "ADDUNSELECT":
                    self.addselect(joy_id, False, arg1 )
                elif name == "SELECT":
                    self.select(joy_id, arg1)


                ### MOTION  ######
                elif name == "ANIM":
                    self.nao_memoryEvent(joy_id, "anim", arg1 )
                
                elif name == "COMBO":
                    self.nao_memoryEvent(joy_id, "combo", arg1 )
                                       
                elif name == "POSTURE":
                    self.nao_go_posture(joy_id, arg1)

                elif name == "WALK" and not(walk_information): #arg1 left<0 right>0 -- arg2 up>0 down<0
                    if arg1==0.0 and arg2==0.0 :
                        self.nao_update_walk(joy_id, 0,0,0.0,0.0)
                    else :
                        self.nao_update_walk(joy_id, abs(arg2)/(arg2 * 0.99999)*abs(arg2), 0.0, arg1*0.7, abs(arg2))
                    walk_information = True
                
                # Point walk, command when you want to move from A to B in 1 command
                elif name == "PWALK" and not(walk_information):
                    
                    self.nao_update_walk_to_point(joy_id, arg2, 0, arg1, 0.1)
                    walk_information = True
                    

                elif name == "WALKPREC" and not(walk_information): #arg1 left<0 right>0 -- arg2 up>0 down<0
                    if arg1==0.0 and arg2==0.0 :
                        self.nao_update_walk(joy_id,0,0,0.0,0.0)
                    else :
                        self.nao_update_walk(joy_id,  abs(arg2)/(arg2 * 0.99999)*abs(arg2), 0.0, arg1*0.15, abs(arg2))
                    walk_information = True
                    
                elif name == "WALKSIDE" and not(walk_information): #arg1 left<0 right>0 -- arg2 up>0 down<0
                    if arg1==0.0 and arg2==0.0 :
                        self.nao_update_walk(joy_id, 0,0,0.0,0.0)
                    else :
                        self.nao_update_walk(joy_id, abs(arg2)/(arg2 * 0.99999)*abs(arg2),arg1*0.7, 0.0,  abs(arg2))
                    walk_information = True
                    
                elif name == "TURN":

                    if(arg1==0):
                        self.nao_update_walk(joy_id, 0.0,0.0,0.0, 0.0)
                    elif arg1 > 0.0:
                        self.nao_update_walk(joy_id, 0.0,0.0,0.9, arg1)
                    elif arg1 < 0.0:
                        self.nao_update_walk(joy_id, 0.0,0.0,-0.9, abs(arg1))

                    
                elif name == "HEAD" and not(head_information): #arg1 left<0 right>0 --- arg2 up>0, down<0

                    self.nao_move_head(joy_id, -arg1*40.5, -arg2*29.5)
                    head_information = True

                ### OTHERS #######

                elif name == "FPS":
                    self.nao_memoryEvent(joy_id, "SetFps", arg1)
                    
                    
                elif name == "PLAY_SOUND":
                    self.nao_memoryEvent(joy_id, "PlaySound", arg1)

                elif name == "AUTONOME":
                    self.nao_autonomeLevel(joy_id, arg1)          

                
            

            

                        
        
         
