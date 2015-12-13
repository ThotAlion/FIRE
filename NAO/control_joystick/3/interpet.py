from PyQt4 import QtGui, QtCore
import time


class Interpret(QtGui.QWidget):

    def __init__(self):

        super(Interpret, self).__init__()

        self.list_of_dic = []
        self.current_dic = 0
        dic1 = {}



        ############## DICTIONNAIRE 1 ###################

        #### --1-- RB LB ####
        dic1["RB"] = ["SWITCH", 1, 0]
        dic1["LB"] = ["SWITCH", 0, 0]
        dic1["LB+RB"] = ["SELECT_ALL"]
        dic1["RB_Y"] = ["SELECT", 1, 0]
        dic1["RB_X"] = ["SELECT", 2, 0]
        dic1["RB_B"] = ["SELECT", 3, 0]
        dic1["RB_A"] = ["SELECT", 4, 0]
        dic1["LB_Y"] = ["UNSELECT", 1, 0]
        dic1["LB_X"] = ["UNSELECT", 2, 0]
        dic1["LB_B"] = ["UNSELECT", 3, 0]
        dic1["LB_A"] = ["UNSELECT", 4, 0]

        
        #### --1-- BUTTON ###
        dic1["Y"] = ["ANIM", "TORSION", 0]
        dic1["X"] = ["ANIM", "TRIANGLE", 0]
        dic1["A"] = ["ANIM","CLAVIER", 0]
        dic1["B"] = ["ANIM", "ARABESQUE", 0]

        dic1["RIGHT_Y"] = ["ANIM","COTE", 0]
        dic1["RIGHT_X"] = ["ANIM", "CLAVIER", 0]
        dic1["RIGHT_B"] = ["ANIM", "SALUTA", 0]
        dic1["RIGHT_A"] = ["ANIM", "PYRAMIDE", 0]

        dic1["UP_Y"] = ["PLAY_SOUND", 0, 0]
        dic1["UP_X"] = ["PLAY_SOUND", 1, 0]
        dic1["UP_B"] = ["PLAY_SOUND", 2, 0]
        dic1["UP_A"] = ["PLAY_SOUND", 3, 0]

        dic1["DOWN_Y"] = ["POSTURE", "STAND", 0]
        dic1["DOWN_X"] = ["POSTURE", "REST", 0]
        dic1["DOWN_B"] = ["POSTURE", "STANDINIT", 0]
        dic1["DOWN_A"] = ["POSTURE", "SIT", 0]

        dic1["LEFT_Y"] = ["FPS", 15, 0]
        dic1["LEFT_X"] = ["ANIM", "RONDE", 0]
        dic1["LEFT_B"] = ["FPS", 25, 0]
        dic1["LEFT_A"] = ["FPS", 30, 0]

        ##### --1-- JOYSTICK ####
        dic1["JOY_MAIN"] = ["WALK"]
        dic1["LT"] = ["TURN"]
        dic1["RT"] = ["TURN"]
        dic1["JOY_SEC"] = ["HEAD"]


        self.list_of_dic.append(dic1)





    def changeDict(self, a):
        if(a>(-1) and a<len(self.list_of_dic)):
           self.current_dic = a

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


        return res


