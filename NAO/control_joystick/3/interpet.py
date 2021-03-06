from PyQt4 import QtGui, QtCore
import time


class Interpret(QtGui.QWidget):

    interpret_event = QtCore.pyqtSignal(list)

    def __init__(self):

        super(Interpret, self).__init__()

        self.list_of_dic = []
        self.current_dic = 0
        dic1 = {}
        dic2 = {}

        ##############  GUI ############################
        #TODO change to radio list
        #construct
        self.layoutMain = QtGui.QHBoxLayout()
        layoutGroup = QtGui.QVBoxLayout()
        groupDic = QtGui.QGroupBox("Interpret")
        groupDic.setLayout(layoutGroup)
        self.radio_dic1 = QtGui.QRadioButton("Dic 1")
        self.radio_dic1.setChecked(QtCore.Qt.Checked)
        self.radio_dic2 = QtGui.QRadioButton("Dic 2")
        layoutView = QtGui.QGridLayout()
        groupView = QtGui.QGroupBox("Controller view")
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
        self.imgSit = "images/sit.png"
        self.imgStand = "images/stand.png"
        self.imgStandInit = "images/standInit.png"
        self.imgRest = "images/rest.png"
        self.imgRamasser = "images/ramasser.png"
        self.imgReaction = "images/reaction.png"
        self.imgPieta = "images/pieta.png"
        self.imgMur = "images/mur.png"
        self.imgChoreDuo = "images/choreduo.png"
        self.imgAspirateur = "images/aspirateur.png"
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
        self.layoutMain.addWidget(groupDic)
        self.layoutMain.addWidget(groupView)
        self.setLayout(self.layoutMain)
        


        ############## DICTIONNAIRE 1 ###################

        #### --1-- RB LB ####
        dic1["RB"] = ["SWITCH", 1, 0]
        dic1["LB"] = ["", 1, 0]
        dic1["LB+RB"] = ["UNSELECT_ALL"]
        dic1["LB_X"] = ["SELECT", 0, 0]
        dic1["LB_Y"] = ["SELECT", 1, 0]
        dic1["LB_B"] = ["SELECT", 2, 0]
        dic1["LB_A"] = ["SELECT", 3, 0]

        
        #### --1-- BUTTON ###
        dic1["Y"] = ["ANIM", "TORSION", 0]
        dic1["X"] = ["ANIM", "TRIANGLE", 0]
        dic1["A"] = ["ANIM","CLAVIER", 0]
        dic1["B"] = ["ANIM", "ARABESQUE", 0]

        dic1["RIGHT_Y"] = ["ANIM","COTE", 0]
        dic1["RIGHT_X"] = ["ANIM", "PYRAMIDE", 0]
        dic1["RIGHT_A"] = ["ANIM", "SALUTA", 0]
        dic1["RIGHT_B"] = ["ANIM", "TOUPIE", 0]

        dic1["UP_Y"] = ["AUTONOME", -1, 0]
        dic1["UP_X"] = ["AUTONOME", 0, 0]
        dic1["UP_B"] = ["AUTONOME", 1, 0]
        dic1["UP_A"] = ["AUTONOME", 2, 0]

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
        dic2["LB_X"] = ["SELECT", 0, 0]
        dic2["LB_Y"] = ["SELECT", 1, 0]
        dic2["LB_B"] = ["SELECT", 2, 0]
        dic2["LB_A"] = ["SELECT", 3, 0]

        
        #### --2-- BUTTON ###
        dic2["X"] = ["COMBO", "RAMASSER", 0]
        dic2["Y"] = ["COMBO", "REACTION", 0]
        dic2["B"] = ["COMBO", "PIETA", 0]
        dic2["A"] = ["COMBO","MUR", 0]
        

        dic2["RIGHT_X"] = ["COMBO", "DUO", 0]
        dic2["RIGHT_Y"] = ["COMBO","ASPI", 0]
        dic2["RIGHT_B"] = ["COMBO", "TRIO", 0]
        dic2["RIGHT_A"] = ["COMBO", "", 0]
        

        dic2["UP_Y"] = ["AUTONOME", -1, 0]
        dic2["UP_X"] = ["AUTONOME", 0, 0]
        dic2["UP_B"] = ["AUTONOME", 1, 0]
        dic2["UP_A"] = ["AUTONOME", 2, 0]

        dic2["DOWN_Y"] = ["POSTURE", "Stand", 0]
        dic2["DOWN_X"] = ["POSTURE", "Rest", 0]
        dic2["DOWN_B"] = ["POSTURE", "StandInit", 0]
        dic2["DOWN_A"] = ["POSTURE", "Sit", 0]

        dic2["LEFT_Y"] = ["",0, 0]
        dic2["LEFT_X"] = ["", "RONDE", 0]
        dic2["LEFT_B"] = ["", 0, 0]
        dic2["LEFT_A"] = ["", 0, 0]

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
                    res.append([ translated_word[0], word[1], word[2]])

                # COPY ARGS FROM THE INTERPRET, NAME OF ANIMATION, VALUE OF FPS
                elif len(translated_word) == 3:
                    res.append(translated_word)


        self.interpret_event.emit(res)
    
    def changeView(self, a):
        
        print a
        if self.current_dic == 0:
        
            if a=="none":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgTriangle))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgTorsion))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgArabesque))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgEmpty))
            elif a=="right":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgPyramide))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgCote))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgAnnaToupi))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgSaluta)) 
            elif a=="left":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRonde))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgEmpty))            
            elif a=="up":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgAutoReset))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgAutoStop))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgAutoMinus))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgAutoPlus))
            elif a=="down":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRest))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgStand))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgStandInit))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgSit))
                
        elif self.current_dic == 1:
        
            if a=="none":
        
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRamasser))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgReaction))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgPieta))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgMur))
            elif a=="right":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgChoreDuo))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgAspirateur))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgEmpty))
            elif a=="up":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgAutoReset))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgAutoStop))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgAutoMinus))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgAutoPlus))
            elif a=="down":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRest))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgStand))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgStandInit))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgSit))
            elif a=="left":
                self.buttonLeft.setPixmap(QtGui.QPixmap(self.imgRonde))
                self.buttonTop.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonRight.setPixmap(QtGui.QPixmap(self.imgEmpty))
                self.buttonBottom.setPixmap(QtGui.QPixmap(self.imgEmpty)) 
                
                
                
            
                
        
        
        
        
        
        


        