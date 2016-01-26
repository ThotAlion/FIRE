from PyQt4 import QtGui, QtCore
import time


class Interpret(QtGui.QWidget):

    interpret_event = QtCore.pyqtSignal(list)

    def __init__(self, joystick_id):

        super(Interpret, self).__init__()

        self.list_of_dic = []
        self.current_dic = 0
        self.joy_id = joystick_id
        dic1 = {}
        dic2 = {}

        ##############  GUI ############################
        #TODO change to radio list
        #construct
        self.layoutMain = QtGui.QVBoxLayout()
        layoutGroup = QtGui.QHBoxLayout()
        groupDic = QtGui.QGroupBox("Interpret")
        groupDic.setLayout(layoutGroup)
        self.radio_dic1 = QtGui.QRadioButton("Dic 1")
        self.radio_dic1.setChecked(QtCore.Qt.Checked)
        self.radio_dic2 = QtGui.QRadioButton("Dic 2")
        layoutView = QtGui.QGridLayout()
        groupView = QtGui.QGroupBox("Controller view "+str(self.joy_id))
        if( self.joy_id == 1):
            groupView.setStyleSheet("background-color:yellow")
        else:
            groupView.setStyleSheet("background-color:white")
        groupView.setLayout(layoutView)
        self.buttonLeft = QtGui.QLabel("X")
        self.buttonTop = QtGui.QLabel("Y")
        self.buttonRight = QtGui.QLabel("B")
        self.buttonBottom = QtGui.QLabel("A")
        #images
        self.imgTorsion = "images/torsion.png"
        self.imgSaluta = "images/saluta.png"
        self.imgPyramide = "images/pyramide.png"
        self.imgTriangle = "images/triangle.png"
        self.imgAnnaToupi = "images/annaToupi.png"
        self.imgArabesque = "images/arabesque.png"
        self.imgCote = "images/cote.png"
        self.imgRonde = "images/ronde.png"
        self.imgEmpty = "images/empty.png"
        self.imgAutoReset = "images/auto-reset.png"
        self.imgAutoStop = "images/auto-stop.png"
        self.imgAutoPlus = "images/auto-plus.png"
        self.imgAutoMinus = "images/auto-minus.png"
        self.imgAutoCunni = "images/auto-cunni.png"
        self.imgAutoFun = "images/auto-fun.png"
        self.imgAutoSoft = "images/auto-soft.png"
        self.imgSit = "images/sit.png"
        self.imgStand = "images/stand.png"
        self.imgStandInit = "images/standInit.png"
        self.imgRest = "images/rest.png"
        self.imgRamasser = "images/ramasser.png"
        self.imgReaction = "images/reaction.png"
        self.imgPieta = "images/pieta.png"
        self.imgMur = "images/mur.png"
        self.imgChoreDuo = "images/duo.png"
        self.imgPieta2 = "images/pieta2.png"
        self.imgCiel = "images/ciel.png"
        self.imgOpera = "images/opera.png"
        self.imgWings = "images/wings.png"
        self.imgLightShine = "images/lightshine.png"
        self.imgCielRevelation = "images/revelation.png"
        self.imgRonde2 = "images/ronde2.png"
        self.imgLucy = "images/lucy.png"
        self.imgMama = "images/mama.png"
        self.imgLucas = "images/lucas.png"
        self.imgStoryNext = "images/next.png"
        self.imgStoryPrev = "images/prev.png"
        self.imgStoryCall = "images/call.png"
        self.imgStoryEmpty = "images/story.png"
        self.imgFalling = "images/falling.png"
        
        #setPixmap
        self.changeView(0)
        #connect
        self.radio_dic1.clicked.connect( lambda: self.changeDict(0))
        self.radio_dic2.clicked.connect( lambda: self.changeDict(1))
        #add to layout
        layoutGroup.addWidget(self.radio_dic1)
        layoutGroup.addWidget(self.radio_dic2)
        layoutView.addWidget(self.buttonLeft, 1, 0)
        layoutView.addWidget(self.buttonTop, 0, 1)
        layoutView.addWidget(self.buttonRight, 1, 2)
        layoutView.addWidget(self.buttonBottom, 2, 1)
        self.layoutMain.addWidget(groupView)
        self.layoutMain.addWidget(groupDic)
        self.setLayout(self.layoutMain)
        


        ############## DICTIONNAIRE 1 ###################

        #### --1-- RB LB ####
        dic1["RB"] = ["SWITCH", 1, 0]
        dic1["LB"] = ["", 1, 0]
        dic1["LB+RB"] = ["UNSELECT_ALL"]
        dic1["LB_X"] = ["ADDSELECT", 0, 0]
        dic1["LB_Y"] = ["ADDSELECT", 3, 0]
        dic1["LB_B"] = ["ADDSELECT", 1, 0]
        dic1["LB_A"] = ["ADDSELECT", 2, 0]

        
        #### --1-- BUTTON ###
        dic1["Y"] = ["ANIM", "TORSION", 0]
        dic1["X"] = ["ANIM", "TRIANGLE", 0]
        dic1["A"] = ["ANIM","FALLING", 0]
        dic1["B"] = ["ANIM", "ARABESQUE", 0]

        dic1["RIGHT_Y"] = ["ANIM","COTE", 0]
        dic1["RIGHT_X"] = ["ANIM", "PYRAMIDE", 0]
        dic1["RIGHT_A"] = ["ANIM", "SALUTA", 0]
        dic1["RIGHT_B"] = ["ANIM", "TOUPIE", 0]

        dic1["UP_Y"] = ["AUTONOMED", 4, 0]
        dic1["UP_X"] = ["AUTONOMED", 3, 0]
        dic1["UP_B"] = ["AUTONOMED", 6, 0]
        dic1["UP_A"] = ["AUTONOMED", 7, 0]

        dic1["DOWN_Y"] = ["POSTURE", "Stand", 0]
        dic1["DOWN_X"] = ["POSTURE", "Rest", 0]
        dic1["DOWN_B"] = ["POSTURE", "StandInit", 0]
        dic1["DOWN_A"] = ["POSTURE", "Sit", 0]

        dic1["LEFT_Y"] = ["FPS", -5, 0]
        dic1["LEFT_X"] = ["ANIM", "RONDE", 0]
        dic1["LEFT_B"] = ["FPS", 5, 0]
        dic1["LEFT_A"] = ["FPS", 10, 0]

        ##### --1-- JOYSTICK ####
        dic1["JOY_MAIN"] = ["WALK"]
        dic1["LEFT_JOY_MAIN"] = ["WALKSIDE"]
        dic1["UP_JOY_MAIN"] = ["WALKPREC"]
        dic1["LT"] = ["TURN"]
        dic1["RT"] = ["TURN"]
        dic1["JOY_SEC"] = ["HEAD"]

        self.list_of_dic.append(dic1)

        ############## DICTIONNAIRE 2 ###################

        #### --2-- RB LB ####
        dic2["RB"] = ["SWITCH", 1, 0]
        dic2["LB"] = ["", 1, 0]
        dic2["LB+RB"] = ["UNSELECT_ALL"]
        dic2["LB_X"] = ["ADDSELECT", 0, 0]
        dic2["LB_Y"] = ["ADDSELECT", 3, 0]
        dic2["LB_B"] = ["ADDSELECT", 1, 0]
        dic2["LB_A"] = ["ADDSELECT", 2, 0]

        
        #### --2-- BUTTON ###
        dic2["X"] = ["STORY", "", 0]
        dic2["Y"] = ["STORY", "PREV", 0]
        dic2["B"] = ["STORY", "CALL", 0]
        dic2["A"] = ["STORY","NEXT", 0]
        

        dic2["RIGHT_X"] = ["ANIM", "LIGHTSHINE", 0]
        dic2["RIGHT_Y"] = ["ANIM","WINGS", 0]
        dic2["RIGHT_B"] = ["ANIM", "DUO", 0]
        dic2["RIGHT_A"] = ["ANIM", "TOUPIE", 0]
        

        dic2["UP_Y"] = ["AUTONOMED", 4, 0]
        dic2["UP_X"] = ["AUTONOMED", 3, 0]
        dic2["UP_B"] = ["AUTONOMED", 6, 0]
        dic2["UP_A"] = ["AUTONOMED", 7, 0]

        dic2["DOWN_Y"] = ["POSTURE", "Stand", 0]
        dic2["DOWN_X"] = ["POSTURE", "Rest", 0]
        dic2["DOWN_B"] = ["POSTURE", "StandInit", 0]
        dic2["DOWN_A"] = ["POSTURE", "Sit", 0]

        dic2["LEFT_Y"] = ["COMBO","RAMASSER", 0]
        dic2["LEFT_X"] = ["ANIM", "RONDE", 0]
        dic2["LEFT_B"] = ["ANIM", "RONDE2", 0]
        dic2["LEFT_A"] = ["ANIM", "CIELREVELATION", 0]

        ##### --2-- JOYSTICK ####
        dic2["JOY_MAIN"] = ["WALK"]
        dic2["LEFT_JOY_MAIN"] = ["WALKSIDE"]
        dic2["UP_JOY_MAIN"] = ["WALKPREC"]
        dic2["LT"] = ["TURN"]
        dic2["RT"] = ["TURN"]
        dic2["JOY_SEC"] = ["HEAD"]

        
        self.list_of_dic.append(dic2)
        
        ##### -init viewer -- ####
        self.changeView("none")





    def changeDict(self, a):
        if(a>(-1) and a<len(self.list_of_dic)):
           self.current_dic = a
           print "---- change of dic : "+str(a)+" ------"
           self.changeView("none")

    def translate( self, a ):

        res = []
        for word in a:
            if len(word) == 3:

                # COPY ARGS FROM THE JOYSTICK, VALUE OF JOYSTICK FOR EXAMPLE
                translated_word = (self.list_of_dic[self.current_dic])[ word[0] ]
                if len(translated_word) == 1:
                    res.append([ translated_word[0],self.joy_id, word[1], word[2]])

                # COPY ARGS FROM THE INTERPRET, NAME OF ANIMATION, VALUE OF FPS
                elif len(translated_word) == 3:
                    res.append([ translated_word[0],self.joy_id, translated_word[1], translated_word[2]])


        self.interpret_event.emit(res)
    
    def changeView(self, a):
        
        print a
        if self.current_dic == 0:
        
            if a=="none":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgTriangle))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgTorsion))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgArabesque))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgFalling))
            elif a=="right":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgPyramide))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgCote))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgAnnaToupi))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgSaluta)) 
            elif a=="left":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRonde))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgOpera))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgEmpty))            
            elif a=="up":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgAutoReset))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgAutoCunni))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgAutoSoft))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgAutoFun))
            elif a=="down":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRest))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgStand))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgStandInit))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgSit))
            elif a=="lb":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgLucy))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgLucas))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgMama))  
              
                
        elif self.current_dic == 1:
        
            if a=="none":
        
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgStoryEmpty))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgStoryPrev))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgStoryCall))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgStoryNext)) 
            elif a=="right":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgLightShine))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgWings))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgChoreDuo))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgAnnaToupi))
            elif a=="up":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgAutoReset))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgAutoCunni))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgAutoSoft))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgAutoFun))
            elif a=="down":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRest))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgStand))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgStandInit))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgSit))
            elif a=="left":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRonde))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgRamasser))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgRonde2))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgCielRevelation)) 
            elif a=="lb":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgLucy))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgLucas))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgMama)) 
                
                
                
            
                
        
        
        
        
        
        


        