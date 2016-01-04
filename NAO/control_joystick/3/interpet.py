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
        #construct
        self.layoutMain = QtGui.QVBoxLayout()
        layoutGroup = QtGui.QVBoxLayout()
        group = QtGui.QGroupBox("Interpret")
        group.setLayout(layoutGroup)
        self.dic1Button = QtGui.QPushButton("Dic1")
        self.dic2Button = QtGui.QPushButton("Dic2")
        #connect
        self.dic1Button.clicked.connect( lambda: self.changeDict(0))
        self.dic2Button.clicked.connect( lambda: self.changeDict(1))
        #add to layout
        layoutGroup.addWidget(self.dic1Button)
        layoutGroup.addWidget(self.dic2Button)
        self.layoutMain.addWidget(group)
        self.setLayout(self.layoutMain)
        


        ############## DICTIONNAIRE 1 ###################

        #### --1-- RB LB ####
        dic1["RB"] = ["SWITCH", 1, 0]
        dic1["LB"] = ["SWITCH", 0, 0]
        dic1["LB+RB"] = ["SELECT_ALL"]
        dic1["RB_Y"] = ["SELECT", 0, 0]
        dic1["RB_X"] = ["SELECT", 1, 0]
        dic1["RB_B"] = ["SELECT", 2, 0]
        dic1["RB_A"] = ["SELECT", 3, 0]
        dic1["LB_Y"] = ["UNSELECT", 0, 0]
        dic1["LB_X"] = ["UNSELECT", 1, 0]
        dic1["LB_B"] = ["UNSELECT", 2, 0]
        dic1["LB_A"] = ["UNSELECT", 3, 0]

        
        #### --1-- BUTTON ###
        dic1["Y"] = ["ANIM", "TORSION", 0]
        dic1["X"] = ["ANIM", "TRIANGLE", 0]
        dic1["A"] = ["ANIM","CLAVIER", 0]
        dic1["B"] = ["ANIM", "ARABESQUE", 0]

        dic1["RIGHT_Y"] = ["ANIM","COTE", 0]
        dic1["RIGHT_X"] = ["ANIM", "PYRAMIDE", 0]
        dic1["RIGHT_A"] = ["ANIM", "SALUTA", 0]
        dic1["RIGHT_B"] = ["ANIM", "TOUPIE", 0]

        dic1["UP_Y"] = ["AUTONOME", 2, 0]
        dic1["UP_X"] = ["AUTONOME", 1, 0]
        dic1["UP_B"] = ["AUTONOME", 3, 0]
        dic1["UP_A"] = ["AUTONOME", 4, 0]

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

        #### --1-- RB LB ####
        dic2["RB"] = ["", 0, 0]
        dic2["LB"] = ["", 0, 0]
        dic2["LB+RB"] = ["SELECT_ALL"]
        dic2["RB_Y"] = ["SELECT", 2, 0]
        dic2["RB_X"] = ["SELECT", 1, 0]
        dic2["RB_B"] = ["SELECT", 3, 0]
        dic2["RB_A"] = ["SELECT", 0, 0]
        dic2["LB_Y"] = ["UNSELECT", 2, 0]
        dic2["LB_X"] = ["UNSELECT", 1, 0]
        dic2["LB_B"] = ["UNSELECT", 3, 0]
        dic2["LB_A"] = ["UNSELECT", 0, 0]

        
        #### --1-- BUTTON ###
        dic2["Y"] = ["ANIMLIB", "", 0]
        dic2["X"] = ["ANIMLIB", "", 0]
        dic2["A"] = ["ANIMLIB","", 0]
        dic2["B"] = ["ANIMLIB", "", 0]

        dic2["RIGHT_Y"] = ["ANIMLIB","", 0]
        dic2["RIGHT_X"] = ["ANIMLIB", "", 0]
        dic2["RIGHT_A"] = ["ANIMLIB", "", 0]
        dic2["RIGHT_B"] = ["ANIMLIB", "", 0]

        dic2["UP_Y"] = ["", 0, 0]
        dic2["UP_X"] = ["", 0, 0]
        dic2["UP_B"] = ["", 0, 0]
        dic2["UP_A"] = ["", 0, 0]

        dic2["DOWN_Y"] = ["POSTURE", "Stand", 0]
        dic2["DOWN_X"] = ["POSTURE", "Rest", 0]
        dic2["DOWN_B"] = ["POSTURE", "StandInit", 0]
        dic2["DOWN_A"] = ["POSTURE", "Sit", 0]

        dic2["LEFT_Y"] = ["",0, 0]
        dic2["LEFT_X"] = ["", "RONDE", 0]
        dic2["LEFT_B"] = ["", 0, 0]
        dic2["LEFT_A"] = ["", 0, 0]

        ##### --1-- JOYSTICK ####
        dic2["JOY_MAIN"] = ["WALK"]
        dic2["LEFT_JOY_MAIN"] = ["WALKSIDE"]
        dic2["UP_JOY_MAIN"] = ["WALKPREC"]
        dic2["LT"] = ["TURN"]
        dic2["RT"] = ["TURN"]
        dic2["JOY_SEC"] = ["HEAD"]

        
        self.list_of_dic.append(dic2)





    def changeDict(self, a):
        if(a>(-1) and a<len(self.list_of_dic)):
           self.current_dic = a
           print "---- change of dic : "+str(a)+" ------"

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


