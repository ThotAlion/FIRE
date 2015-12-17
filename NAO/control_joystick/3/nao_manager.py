from nao import Nao
from PyQt4 import QtGui, QtCore
import copy

class Nao_manager(QtGui.QWidget):

    def __init__(self):

        super(Nao_manager, self).__init__()

        ####### NAO MANAGEMENT #######
        self.list_of_nao = []
        self.selection = []

        ######## GUI #################

        ####Layout
        self.layoutMain = QtGui.QVBoxLayout()
        self.layoutNao= QtGui.QGridLayout()
        self.layoutNao.setAlignment(QtCore.Qt.AlignHCenter)
        self.layoutNao.setAlignment(QtCore.Qt.AlignTop)
        self.layoutManager = QtGui.QHBoxLayout()

        self.layoutMain.addLayout(self.layoutNao)
        self.layoutMain.addLayout(self.layoutManager)
        self.setLayout(self.layoutMain)

        ####CheckBox for selection
        self.list_of_selectionCheckBox = []

        #####Group Selection
        #construct
        groupSelection = QtGui.QGroupBox("selection")
        layoutSelection = QtGui.QVBoxLayout()
        groupSelection.setLayout(layoutSelection)
        self.selectionButton_all = QtGui.QPushButton("All")
        self.selectionButton_nall = QtGui.QPushButton("None")
        #connect
        self.selectionButton_all.clicked.connect(lambda: self.selectAll(True))
        self.selectionButton_nall.clicked.connect(lambda: self.selectAll(False))
        #add to layout
        layoutSelection.addWidget(self.selectionButton_all)
        layoutSelection.addWidget(self.selectionButton_nall)
        self.layoutManager.addWidget(groupSelection)
                                          


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

        self.layoutManager.addWidget(groupAnimLib)
        

        

    def addNao(self, name, adresseIP, port ):
        #nao management
        naoId = len(self.list_of_nao)
        nao = Nao(adresseIP, name, naoId)
        self.list_of_nao.append(nao)
        self.selection.append(False)

        #gui management
        self.layoutNao.addWidget(nao, 1, naoId, QtCore.Qt.AlignCenter)
        checkBox = QtGui.QCheckBox("")
        self.list_of_selectionCheckBox.append(checkBox)
        self.layoutNao.addWidget( checkBox, 0, naoId, QtCore.Qt.AlignCenter)
        

    def init_nao(self):

        for nao in self.list_of_nao :
            nao.init_pos()

    def init_manager(self):

        if len(self.list_of_nao) != len(self.selection) :
            print( " probleme nao manager init ")
        else :
            self.init_nao()
            return True


    # switching from select all to unselect all
    def selectAll(self, is_selecting=True):
        if is_selecting:
             print "selecting ALL"
        else :
            print "un_selecting all"

        for i in range(len(self.selection)):
            self.selection[i] = is_selecting

        self.activateNao()
   

    # select only one nao, switching from one to the other
    def selectSwitch(self, isIncreasing ):

        print "manager:selectSwitch"
        #find the last nao activated
        last_id = 0
        current_id = 0
        for is_selected in self.selection:
            if is_selected:
                last_id = current_id
            current_id += 1

        for i in range(len(self.selection)):
            self.selection[i] = ( ((last_id + 1)%len(self.selection))==i )

        self.activateNao()
                

    # select or unselect one nao, over the current selection, according to its ID
    def select(self, isSelecting, nao_id ):

        if nao_id>-1 and nao_id< len(self.list_of_nao):
            self.selection[nao_id] = isSelecting

        self.activateNao()

        

    # return True if a nao is selected
    def is_selected(self, nao_id):
        if nao_id>-1 and nao_id< len(self.list_of_nao):
            return[nao_id] 

            

    # activate some or all nao according to selection list
    def activateNao(self):
        print "activateNao :"
        print self.selection

        for a in range(len(self.list_of_nao)):
            (self.list_of_nao[a]).activate( self.selection[a] )
            if self.selection[a] :
                print "setCheck : "+str(a)
                (self.list_of_selectionCheckBox[a]).setCheckState(QtCore.Qt.Checked)
            else:
                (self.list_of_selectionCheckBox[a]).setCheckState(QtCore.Qt.Unchecked)

    # call a memory event to all selected nao
    def nao_memoryEvent(self, name, arg ):
        
        print "Memory Event : "+name+" -- "+str(arg)
        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].memoryEvent(name, arg)

    # update_walk and turning to all selected nao
    def nao_update_walk(self, X, Y, Theta, Speed):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].update_walk( X, Y , Theta, Speed)

        print "marche X="+str(X)+" Y="+str(Y)+" Theta="+str(Theta)+" Speed="+str(Speed)+""

    # update turning head to all selected nao
    def nao_move_head(self, yaw,pitch):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].move_head(yaw,pitch)

    # ask a posture to all selected nao
    def nao_go_posture(self, posture_name):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].go_posture( posture_name)

    def nao_getStatus(self):

        for nao in self.list_of_nao :
            nao.get_status()

    def nao_leds(self, leds_posture):

        zone = ""
        value = 0
        if leds_posture == "INIT":
            zone = "eye"
            value = 1
        if leds_posture == "OFF":
            zone = "eye"
            value = 0
            
        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].use_leds( zone, value)
        


    ####################################################################    
    # transmit message from interpret to itself and all selected nao(s).
    # Contains all dictionnary message and functions calls
    ####################################################################
    def transmit_msg(self, msgGlobal):

        
        
        for msg in msgGlobal:


            if(len(msg)==3):

                name = msg[0]
                arg1 = msg[1]
                arg2 = msg[2]


                #### SELECTION ####
                if   name == "SWITCH" :
                    self.selectSwitch(arg1==1)
                elif name == "SELECT_ALL" :
                    self.selectAll()
                elif name == "SELECT":
                    self.select(True, arg1 )
                elif name == "UNSELECT":
                    self.select(False, arg1 )


                ### MOTION  ######
                elif name == "ANIM":
                    self.nao_memoryEvent("anim", arg1 )
                    
                elif name == "POSTURE":
                    self.nao_go_posture(arg1)

                elif name == "WALK": #arg1 left<0 right>0 -- arg2 up>0 down<0
                    if arg1==0.0 and arg2==0.0 :
                        self.nao_update_walk(0,0,0.0,0.0)
                    else :
                        self.nao_update_walk( abs(arg2)/(arg2), 0.0, arg1*abs(arg1)*0.7, abs(arg2))
                    
                elif name == "TURN":

                    if(arg1==0):
                        self.nao_update_walk(0.0,0.0,0.0, 0.0)
                    elif arg1 > 0.0:
                        self.nao_update_walk(0.0,0.0,0.9, arg1)
                    elif arg1 < 0.0:
                        self.nao_update_walk(0.0,0.0,-0.9, abs(arg1))

                    
                elif name == "HEAD": #arg1 left<0 right>0 --- arg2 up>0, down<0

                    self.nao_move_head(-arg1*40.5, arg2*29.5)

                ### OTHERS #######

                elif name == "FPS":
                    self.nao_memoryEvent("SetFps", arg1)
                    
                elif name == "LEDS":
                    self.nao_leds( arg1)
                    
                elif name == "PLAY_SOUND":
                    self.nao_memoryEvent("PlaySound", arg1)

                elif name == "AUTONOME":
                    self.nao_memoryEvent("autonome", arg1)            

                
            

            

                        
        
         
