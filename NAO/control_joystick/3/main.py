# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
from nao_manager import Nao_manager
from interpet import Interpret
from joystick import Joystick
import time
from numpy import *
import argparse




class main_ui(QtGui.QWidget):

    def __init__(self):
        super(main_ui, self).__init__()
        self.init_ui()

    def init_ui(self):
        QtGui.QMainWindow.__init__(self, None)


        self.interpret = Interpret()
        #self.joystick = Joystick(self)
        self.manager = Nao_manager()

        self.manager.addNao("Lucy", "0.0.1.13", 9559 )
        self.manager.addNao("MaMa", "0.0.1.12", 9559 )
        self.manager.init_manager()

        ########### Connect ######
        #self.joystick.joy_event.connect(self.interpret.translate)
        #self.interpret.interpret_event.connect(self.manager.transmit_msg)

        #### GUI######
        self.setWindowTitle("Multiple Nao xbox controller")
        self.layout_main = QtGui.QGridLayout()
        self.layout_main.addWidget(self.manager, 0, 0)
        self.setLayout(self.layout_main)

        self.show()    
    
if __name__ == "__main__":
    import sys

    app=QtGui.QApplication(sys.argv) 
    main_application_window=main_ui()
    sys.exit(app.exec_())
