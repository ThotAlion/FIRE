
# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
from nao_manager import Nao_manager
from interpet import Interpret
from joystick import Joystick
from storytelling import StoryTelling
import time
from numpy import *
import argparse


######################################
#                   TODO
#changer la position de la chute et de l'arabesque
#
#
#
#
#########################################




class main_ui(QtGui.QWidget):

    def __init__(self):
        super(main_ui, self).__init__()
        self.init_ui()

    def init_ui(self):
        QtGui.QMainWindow.__init__(self, None)

        ###Joystick Interpret StoryTelling and Nao_Manager ####
        self.joystick = Joystick(self)
        self.interpret1 = Interpret(1)        
        self.interpret2 = Interpret(2)
        self.story = StoryTelling()
        self.manager = Nao_manager()

        #Timer, updating nao battery level, and connection
        self.timerNao = QtCore.QTimer(self)
        self.connect(self.timerNao, QtCore.SIGNAL("timeout()"), self.manager.nao_getStatus)
        self.timerNao.start(3000)
        self.timerStory = QtCore.QTimer(self)
        self.connect(self.timerStory, QtCore.SIGNAL("timeout()"), self.story.update_clock)
        self.timerStory.start(200)
        
        

        ########### Connect ######
        self.joystick.joy_event1.connect(self.interpret1.translate)
        self.joystick.view_event1.connect(self.interpret1.changeView)
        self.interpret1.interpret_event.connect(self.story.transmit_msg)
        
        self.joystick.joy_event2.connect(self.interpret2.translate)
        self.joystick.view_event2.connect(self.interpret2.changeView)
        self.interpret2.interpret_event.connect(self.story.transmit_msg)
        
        self.story.storytelling_event.connect(self.manager.transmit_msg)
        
        self.joystick.second_joy_detected.connect(self.add_joystick)

        #### GUI######
        self.setWindowTitle("Multiple Nao xbox controller")
        self.layout_main = QtGui.QGridLayout()
        self.group_ManagerStory = QtGui.QGroupBox("Nao Control Joystick")
        self.layout_ManagerStory = QtGui.QVBoxLayout()
        self.layout_ManagerStory.addWidget(self.manager)
        self.layout_ManagerStory.addWidget(self.story)
        self.group_ManagerStory.setLayout(self.layout_ManagerStory)
        
        #set layout QGridBox
        self.layout_main.addWidget(self.group_ManagerStory, 0, 1)
        self.layout_main.addWidget(self.interpret1, 0,0)
        self.setLayout(self.layout_main)
        self.show()

        #### Nao Manager #### LUCY PUIS LUCAS PUIS MAMA
        
        #self.manager.addNao("Baltazar", "10.0.1.13", 9559 )
        
        #self.manager.addNao("Lucy", "10.0.1.13", 9559 )
        self.manager.addNao("Lucas", "10.0.1.3", 9559 )
        #self.manager.addNao("MaMa", "10.0.1.12", 9559 )

        self.manager.init_manager()
    
    ## add a Widget for a second joystick if detected 
    def add_joystick(self,a):
        print "ADD GUI FOR SECOND JOYSTICK"
        self.layout_main.addWidget(self.interpret2, 0,2)
        
        

    
if __name__ == "__main__":
    import sys

    app=QtGui.QApplication(sys.argv) 
    main_application_window=main_ui()
    sys.exit(app.exec_())
